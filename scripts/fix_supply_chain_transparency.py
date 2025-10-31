import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from models.brand import Brand

load_dotenv()

def to_float_or_none(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None
    return None

async def main():
    mongo_url = os.getenv("MONGO_URL")
    mongo_db = os.getenv("MONGO_DB")
    if not mongo_url:
        raise RuntimeError("MONGO_URL manquant")
    client = AsyncIOMotorClient(mongo_url)
    db = client.get_database(mongo_db) if mongo_db else client.get_default_database()
    await init_beanie(database=db, document_models=[Brand])

    raw_coll = db["brands"]
    cursor = raw_coll.find({"supply_chain_transparency": {"$type": "string"}})

    fixed = 0
    skipped = 0
    async for doc in cursor:
        val = doc.get("supply_chain_transparency")
        new_val = to_float_or_none(val)
        if new_val is None:
            await raw_coll.update_one({"_id": doc["_id"]}, {"$unset": {"supply_chain_transparency": ""}})
            fixed += 1
        else:
            await raw_coll.update_one({"_id": doc["_id"]}, {"$set": {"supply_chain_transparency": new_val}})
            fixed += 1

    print(f"Nettoyage terminé. Docs modifiés: {fixed}, ignorés: {skipped}")

if __name__ == "__main__":
    asyncio.run(main())
