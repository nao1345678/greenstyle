from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
client.admin.command("ping")

print("✅ Connexion MongoDB OK")

db = client["greenstyle_DB"]
collections = db.list_collection_names()
print("📂 Collections :", collections)