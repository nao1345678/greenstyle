from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import os
import sys
import subprocess
import datetime
import requests
from models.brand import Brand
from services.wikirate import fetch_answers, living_wage_score, to_float
from services.wikirate import living_wage_letter_score

router = APIRouter(prefix="/admin", tags=["Admin"])

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "ingest_brands_metrics.py"
DATA_DIR = ROOT / "scrapping" / "scrapping_v4" / "data"
LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True, parents=True)

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


def _start_ingest_subprocess(logfile: Path):
    """
    Lance le script d'ingestion dans un sous-processus avec le python du venv,
    redirige stdout/stderr vers un fichier de log.
    """
    LOGS_DIR.mkdir(exist_ok=True, parents=True)
    cmd = [sys.executable, str(SCRIPT), "--data", str(DATA_DIR)]
    with logfile.open("w", encoding="utf-8") as f:
        subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=str(ROOT))


@router.post("/ingest")
def trigger_ingest(background_tasks: BackgroundTasks, x_admin_token: str | None = Header(default=None)):
    if ADMIN_TOKEN and x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not SCRIPT.exists():
        raise HTTPException(status_code=500, detail=f"Script introuvable: {SCRIPT}")
    if not DATA_DIR.exists():
        raise HTTPException(status_code=500, detail=f"Dossier data introuvable: {DATA_DIR}")

    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    logfile = LOGS_DIR / f"ingest-{ts}.log"
    background_tasks.add_task(_start_ingest_subprocess, logfile=logfile)

    return {
        "status": "started",
        "script": str(SCRIPT),
        "data_dir": str(DATA_DIR),
        "logfile": str(logfile),
        "hint": "Consulte le logfile pour suivre la progression."
    }


@router.get("/ingest/logs")
def list_ingest_logs():
    logs = sorted([p.name for p in LOGS_DIR.glob("ingest-*.log")], reverse=True)
    return {"logs": logs}


@router.get("/ingest/logs/{logname}")
def read_ingest_log(logname: str):
    logpath = LOGS_DIR / logname
    if not logpath.exists():
        raise HTTPException(status_code=404, detail="Log introuvable")
    return {"name": logname, "content": logpath.read_text(encoding="utf-8")}


class ScrapeRequest(BaseModel):
    brand_name: Optional[str] = None
    metric_ids: List[int]
    update_brand_fields: bool = True
    limit: Optional[int] = None
    max_pages: Optional[int] = None
    connect_timeout: Optional[float] = None
    read_timeout: Optional[float] = None


def map_metric_to_field(metric_title: str, metric_id: int) -> Optional[str]:
    title = (metric_title or "").lower()

    if any(k in title for k in ["living wage", "freedom of association", "collective bargaining", "social compliance", "supplier list", "audits"]):
        return "labor_ethics"

    if "transparency" in title and "supply" in title:
        return "supply_chain_transparency"

    if "transparency" in title and "index" in title:
        return "final_score"

    return None


async def upsert_brand_field(brand_name: str, field: str, value):
    if brand_name is None:
        return None
    b = await Brand.find_one({"brand_name": brand_name})
    created = False
    if not b:
        b = Brand(brand_name=brand_name)
        created = True
    old = getattr(b, field, None)
    setattr(b, field, value)
    await b.save()
    return {"brand": brand_name, "field": field, "old": old, "new": value, "created": created}


@router.post("/scrape/wikirate")
async def scrape_wikirate(payload: ScrapeRequest, x_admin_token: str | None = Header(default=None)) -> Dict[str, Any]:
    if ADMIN_TOKEN and x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not payload.metric_ids:
        raise HTTPException(status_code=400, detail="metric_ids requis")

    limit = payload.limit if payload.limit is not None else (50 if payload.brand_name else 100)
    max_pages = payload.max_pages if payload.max_pages is not None else (None if payload.brand_name else 5)
    cto = payload.connect_timeout if payload.connect_timeout is not None else 8.0
    rto = payload.read_timeout if payload.read_timeout is not None else 15.0

    agg: Dict[str, Dict[str, Any]] = {}
    total_answers = 0

    for mid in payload.metric_ids:
        try:
            answers = fetch_answers(
                mid,
                company=payload.brand_name,
                limit=limit,
                timeout=(cto, rto),
                max_pages=max_pages,
            )
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e))
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Requests error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scrape error: {e}")

        total_answers += len(answers)

        for ans in answers:
            if not isinstance(ans, dict):
                continue

            brand = ans.get("company")
            metric_title = ans.get("metric_title") or ans.get("metric", "")
            field = map_metric_to_field(metric_title, mid)
            if field is None or brand is None:
                continue

            val = ans.get("value")
            if field == "labor_ethics":
                norm = living_wage_letter_score(val)
            else:
                norm = to_float(val)
            if norm is None:
                continue

            agg.setdefault(brand, {})
            try:
                agg[brand][field] = max(float(agg[brand].get(field, -1)), float(norm))
            except Exception:
                agg[brand][field] = norm

    if not payload.update_brand_fields:
        return {
            "answers_count": total_answers,
            "brands_detected": list(agg.keys()),
            "preview": agg,
            "pagination": {"limit": limit, "max_pages": max_pages, "timeouts": {"connect": cto, "read": rto}},
        }

    changes = []
    for brand, fields in agg.items():
        for field, value in fields.items():
            chg = await upsert_brand_field(brand, field, value)
            if chg:
                changes.append(chg)

    return {
        "status": "ok",
        "answers_count": total_answers,
        "brands_updated": len(agg),
        "changes": changes[:100],
        "pagination": {"limit": limit, "max_pages": max_pages, "timeouts": {"connect": cto, "read": rto}},
    }
