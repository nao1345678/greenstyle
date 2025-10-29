import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
if not env_path:
    env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL manquant : vérifie ton .env (emplacement/nom de variable)")
