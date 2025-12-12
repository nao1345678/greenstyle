from __future__ import annotations
import os, time, re
from typing import Dict, Any, List, Optional, Tuple
import requests
from requests.adapters import HTTPAdapter, Retry

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")
SERP_ENDPOINT = "https://serpapi.com/search.json"
HEADERS = {"User-Agent": "GreenStyleBot/1.0", "Accept": "application/json"}

if not SERP_API_KEY:
    raise RuntimeError("SERPAPI_API_KEY manquant dans .env")

COUNTRY_RE = re.compile(
    r"\b(USA|United States|United Kingdom|UK|France|Germany|Italy|Spain|Portugal|China|Vietnam|Bangladesh|India|Turkey|Cambodia|Tunisia|Morocco|Netherlands|Sweden|Norway|Denmark|Canada|Australia|New Zealand)\b",
    re.I,
)

def _session(retries: int = 3, backoff: float = 0.5) -> requests.Session:
    r = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    ad = HTTPAdapter(max_retries=r, pool_maxsize=8)
    s = requests.Session()
    s.headers.update(HEADERS)
    s.mount("https://", ad)
    s.mount("http://", ad)
    return s

def serp_search(q: str, params: Optional[Dict[str, Any]] = None, timeout: Tuple[float, float] = (8, 20)) -> Dict[str, Any]:
    base = {"engine": "google", "q": q, "api_key": SERP_API_KEY, "hl": "en", "gl": "us"}
    if params:
        base.update(params)
    resp = _session().get(SERP_ENDPOINT, params=base, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def parse_knowledge_graph(j: Dict[str, Any]) -> Dict[str, Any]:
    kg = j.get("knowledge_graph") or {}
    cats = kg.get("type")
    categories = cats if isinstance(cats, list) else [cats] if cats else []
    return {
        "brand_name": kg.get("title"),
        "logo": kg.get("image") or kg.get("logo"),
        "website": kg.get("website"),
        "categories": categories,
    }

def parse_organic_links(j: Dict[str, Any], domains: Optional[List[str]] = None, limit: int = 5) -> List[str]:
    out: List[str] = []
    for it in j.get("organic_results", []):
        link = it.get("link")
        if not link:
            continue
        if domains:
            if any(d in link for d in domains):
                out.append(link)
        else:
            out.append(link)
        if len(out) >= limit:
            break
    return out

def extract_country(j: Dict[str, Any]) -> Optional[str]:
    for k in ("answer_box", "knowledge_graph"):
        block = j.get(k)
        if isinstance(block, dict):
            text = " ".join(str(v) for v in block.values() if isinstance(v, (str, list, dict)))
            m = COUNTRY_RE.search(text)
            if m:
                return m.group(0)
    for it in j.get("organic_results", []):
        txt = it.get("snippet") or ""
        m = COUNTRY_RE.search(txt)
        if m:
            return m.group(0)
    return None

def extract_price_hint(j: Dict[str, Any]) -> Optional[str]:
    blobs: List[str] = []
    for k in ("answer_box", "knowledge_graph"):
        block = j.get(k)
        if isinstance(block, dict):
            blobs.append(" ".join(str(v) for v in block.values() if isinstance(v, (str, list, dict))))
    for it in j.get("organic_results", []):
        for k in ("title", "snippet"):
            if it.get(k):
                blobs.append(it[k])
    big = " \n".join(blobs)
    if "€€€" in big or "$$$" in big: return "$$$"
    if "€€" in big or "$$" in big:   return "$$"
    if "€" in big or "$" in big or "£" in big: return "$"
    return None

def normalize_price_to_number(hint: Optional[str]) -> Optional[float]:
    if hint == "$": return 1.0
    if hint == "$$": return 2.0
    if hint == "$$$": return 3.0
    return None

def fetch_brand_overview(brand: str) -> Dict[str, Any]:
    out = {"brand": brand, "brand_name": None, "logo": None, "website": None, "categories": []}
    try:
        j = serp_search(brand)
        out.update({k: v for k, v in parse_knowledge_graph(j).items() if v})
    except Exception as e:
        out["error_overview"] = str(e)
    return out

def fetch_brand_extras(brand: str) -> Dict[str, Any]:
    extras: Dict[str, Any] = {"price_range_hint": None, "price_range": None, "country_origin": None, "country_production": None, "ngo_links": []}
    try:
        jp = serp_search(f"{brand} price range")
        hint = extract_price_hint(jp)
        extras["price_range_hint"] = hint
        extras["price_range"] = normalize_price_to_number(hint)
        time.sleep(0.5)
    except Exception as e:
        extras["error_price"] = str(e)

    try:
        jo = serp_search(f"{brand} country of origin")
        extras["country_origin"] = extract_country(jo)
        time.sleep(0.5)
    except Exception as e:
        extras["error_origin"] = str(e)

    try:
        jp = serp_search(f"Where are {brand} products made")
        extras["country_production"] = extract_country(jp)
        time.sleep(0.5)
    except Exception as e:
        extras["error_production"] = str(e)

    try:
        domains = ["goodonyou.eco", "fairwear.org", "bcorporation.net", "cleanclothes.org"]
        jn = serp_search(f'{brand} site:goodonyou.eco OR site:fairwear.org OR site:bcorporation.net OR site:cleanclothes.org')
        extras["ngo_links"] = parse_organic_links(jn, domains, limit=10)
    except Exception as e:
        extras["error_ngo"] = str(e)

    return extras

def scrape_brand(brand: str) -> Dict[str, Any]:
    base = fetch_brand_overview(brand)
    ext = fetch_brand_extras(brand)
    base.update(ext)
    return base
