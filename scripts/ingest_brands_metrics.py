from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.brand import Brand
from models.category import Category

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

VALUE_MAP = {
    "yes": 1.0,
    "partial": 0.5,
    "no": 0.0,
    "": None,
    None: None,
}

def to_float(x) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(str(x).replace(",", "."))
    except Exception:
        return None


def json_records_from_path(path: Path) -> List[Dict[str, Any]]:
    """
    Normalise un fichier en liste de dicts.
    Gère :
      - JSON liste: [{...}, {...}]
      - JSON enveloppe: {"items":[...]}
      - NDJSON: une ligne = un JSON
      - dict nom->valeur: {"Veja": 85} -> [{"company":"Veja","value":85}]
    Ignore les lignes/objets invalides.
    """
    raw = path.read_text(encoding="utf-8").strip()

    if "\n" in raw and raw.count("{") > 1 and not raw.lstrip().startswith("{"):
        out: List[Dict[str, Any]] = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                out.append(obj)
        return out

    parsed = json.loads(raw)

    if isinstance(parsed, list):
        return [x for x in parsed if isinstance(x, dict)]

    if isinstance(parsed, dict):
        if "items" in parsed and isinstance(parsed["items"], list):
            return [x for x in parsed["items"] if isinstance(x, dict)]

        scalar_types = (int, float, str, bool, type(None))
        if parsed and all(isinstance(k, str) for k in parsed.keys()) and all(isinstance(v, scalar_types) for v in parsed.values()):
            return [{"company": k, "value": v} for k, v in parsed.items()]

    return []


async def init_db():
    mongo_url = os.getenv("MONGO_URL")
    mongo_db = os.getenv("MONGO_DB")
    if not mongo_url:
        raise RuntimeError("Variable d'environnement MONGO_URL manquante dans .env")

    client = AsyncIOMotorClient(mongo_url)
    if mongo_db:
        db = client.get_database(mongo_db)
    else:
        try:
            db = client.get_default_database()
        except Exception:
            # Utiliser greenstyle_DB par défaut (cohérent avec setup_database.js)
            db = client.get_database("greenstyle_DB")

    await init_beanie(database=db, document_models=[Brand, Category])
    print("Connexion MongoDB réussie !")


class Counters:
    created: int = 0
    updated: int = 0
    skipped: int = 0

COUNTERS = Counters()

async def upsert_brand_metric(brand_name: str, field: str, value: Optional[float]):
    if not brand_name or value is None:
        COUNTERS.skipped += 1
        return
    brand = await Brand.find_one({"brand_name": brand_name})
    created = False
    if not brand:
        brand = Brand(brand_name=brand_name)
        created = True

    old = getattr(brand, field, None)
    setattr(brand, field, value)
    await brand.save()

    if created:
        COUNTERS.created += 1
        print(f"Nouvelle marque créée : {brand_name}")
        print(f"   → {field} = {value}")
    else:
        if old != value:
            COUNTERS.updated += 1
            print(f" {brand_name} → {field}: {old} -> {value}")


async def process_living_wage(paths: List[Path]):
    total = 0
    for path in paths:
        print(f"Traitement {path.name} ...")
        records = json_records_from_path(path)
        count = 0
        for it in records:
            if not isinstance(it, dict):
                continue
            company = it.get("company") or it.get("brand") or it.get("name")
            if not company:
                continue
            val = str(it.get("value", "")).strip().lower() if it.get("value") is not None else ""
            score = VALUE_MAP.get(val)
            await upsert_brand_metric(company, "labor_ethics", score)
            count += 1
        total += count
        print(f"{count} lignes traitées dans {path.name}")
    return total


async def process_transparency(paths: List[Path]):
    total = 0
    for path in paths:
        print(f"Traitement {path.name} ...")
        records = json_records_from_path(path)
        count = 0
        for it in records:
            if not isinstance(it, dict):
                continue
            company = it.get("company") or it.get("brand") or it.get("name")
            if not company:
                continue
            value = it.get("value", it.get("score", it.get("transparency")))
            score = to_float(value)
            await upsert_brand_metric(company, "supply_chain_transparency", score)
            count += 1
        total += count
        print(f"{count} lignes traitées dans {path.name}")
    return total


async def process_transparency_simple(paths: List[Path]):
    total = 0
    for path in paths:
        print(f"Traitement {path.name} ...")
        records = json_records_from_path(path)
        count = 0
        for it in records:
            if not isinstance(it, dict):
                continue
            company = it.get("company") or it.get("brand") or it.get("name")
            if not company:
                continue
            score = to_float(it.get("value"))
            await upsert_brand_metric(company, "final_score", score)
            count += 1
        total += count
        print(f"{count} lignes traitées dans {path.name}")
    return total


def collect_paths(data_dir: Path) -> Dict[str, List[Path]]:
    """
    Récupère les fichiers à traiter dans data_dir.
    """
    living = list(data_dir.glob("living_wage*.json"))
    if (data_dir / "living_wage.json").exists() and (data_dir / "living_wage.json") not in living:
        living.append(data_dir / "living_wage.json")

    transparency = []
    if (data_dir / "supply_chain_transparency_data.json").exists():
        transparency.append(data_dir / "supply_chain_transparency_data.json")

    transparency_simple = []
    if (data_dir / "transparency_scores_simple.json").exists():
        transparency_simple.append(data_dir / "transparency_scores_simple.json")

    return {
        "living": living,
        "transparency": transparency,
        "transparency_simple": transparency_simple,
    }


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default=None,
        help="Chemin du dossier de données (ex: scrapping/scrapping_v4/data). "
             "Par défaut, essaie ./data puis ./scrapping/scrapping_v4/data",
    )
    args = parser.parse_args()

    if args.data:
        data_dir = (Path(args.data) if Path(args.data).is_absolute()
                    else (ROOT / args.data)).resolve()
    else:
        candidates = [
            ROOT / "data",
            ROOT / "scrapping" / "scrapping_v4" / "data",
            ROOT / "scrapping" / "data",
        ]
        data_dir = next((p for p in candidates if p.exists()), candidates[0])

    print("DATA_DIR =", data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Le dossier de données n'existe pas: {data_dir}")

    await init_db()

    paths = collect_paths(data_dir)

    total_lw = await process_living_wage(paths["living"]) if paths["living"] else (print("Aucun living_wage*.json trouvé"), 0)[1]
    total_tr = await process_transparency(paths["transparency"]) if paths["transparency"] else (print("supply_chain_transparency_data.json introuvable"), 0)[1]
    total_ts = await process_transparency_simple(paths["transparency_simple"]) if paths["transparency_simple"] else (print("transparency_scores_simple.json introuvable"), 0)[1]

    print("\n──────── Résumé ────────")
    print(f"Living wage traités        : {total_lw}")
    print(f"Transparency (détaillé)    : {total_tr}")
    print(f"Transparency (simple)      : {total_ts}")
    print(f"Marques créées             : {COUNTERS.created}")
    print(f"Mises à jour               : {COUNTERS.updated}")
    print(f"Ignorées (valeur vide)     : {COUNTERS.skipped}")
    print("Insertion / mise à jour terminée !")


if __name__ == "__main__":
    asyncio.run(main())
