import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import requests
from requests.adapters import HTTPAdapter, Retry

WIKIRATE_API = "https://wikirate.org/Answers.json"
WIKIRATE_API_KEY = os.getenv("WIKIRATE_API_KEY")
HEADERS = {
    "User-Agent": "GreenStyleBot/1.0",
    "Accept": "application/json",
}

ROOT = Path(__file__).resolve().parents[2]
SCRAPES_DIR = ROOT / "data" / "scrapes"
SCRAPES_DIR.mkdir(parents=True, exist_ok=True)


def _build_session(total_retries: int = 3, backoff: float = 0.5) -> requests.Session:
    """Session requests avec retries sur erreurs réseau et 429/5xx."""
    retry = Retry(
        total=total_retries,
        backoff_factor=backoff,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_maxsize=8)
    s = requests.Session()
    s.headers.update(HEADERS)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def fetch_answers(
    metric_id: int,
    company: Optional[str] = None,
    limit: int = 100,
    timeout: Tuple[float, float] = (10.0, 20.0),
    max_pages: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Paginer /Answers.json pour un metric_id.
    - Si company est fourni → filtrage souple côté client.
    - Retries automatiques + timeouts + pagination limitée.
    - Retourne toujours une liste de dicts.
    """
    session = _build_session()
    results: List[Dict[str, Any]] = []
    offset = 0
    page_count = 0
    company_norm = company.strip().lower() if company else None

    while True:
        params = {"metric_id": metric_id, "limit": limit, "offset": offset}
        if WIKIRATE_API_KEY:
            params["api_key"] = WIKIRATE_API_KEY

        try:
            resp = session.get(WIKIRATE_API, params=params, timeout=timeout)
            resp.raise_for_status()
            batch = resp.json()
        except requests.exceptions.ReadTimeout:
            print(f" Timeout WikiRate (page offset={offset}) — arrêt de la pagination.")
            break
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"WikiRate request failed: {e}") from e

        if isinstance(batch, dict) and "items" in batch and isinstance(batch["items"], list):
            batch = batch["items"]
        if not isinstance(batch, list):
            break

        original_len = len(batch)
        batch = [x for x in batch if isinstance(x, dict)]

        page_count += 1

        if company_norm:
            batch = [
                x for x in batch
                if company_norm in str(x.get("company", "")).strip().lower()
            ]

        results.extend(batch)

        if original_len < limit:
            break
        if max_pages is not None and page_count >= max_pages:
            break

        offset += limit

    ts = int(time.time())
    fname = f"answers_{metric_id}_{(company or 'all').replace(' ', '_')}_{ts}.json"
    dump_path = SCRAPES_DIR / fname
    try:
        dump_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

    return results


VALUE_MAP = {"yes": 1.0, "partial": 0.5, "no": 0.0}


LETTER_MAP = {"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25, "E": 0.0}


def living_wage_score(value: Any) -> Optional[float]:
    """Ancien mapping yes/partial/no."""
    if value is None:
        return None
    v = str(value).strip().lower()
    return VALUE_MAP.get(v)


def living_wage_letter_score(value: Any) -> Optional[float]:
    """Nouveau mapping A–E (Clean Clothes Campaign metric 5990097)."""
    if value is None:
        return None
    v = str(value).strip().upper()
    return LETTER_MAP.get(v)


def to_float(value: Any) -> Optional[float]:
    """Convertit une valeur textuelle ou numérique en float."""
    if value is None:
        return None
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return None
