from pymongo import MongoClient
import os
from CalculScore import calcul_score

client = MongoClient(os.getenv("MONGO_URL"))
db = client["greenstyle_DB"]
brands = db["brands"]

brand = brands.find_one()

print("📦 Marque brute:")
print(brand)

scores = calcul_score.calculate_scores(brand)

print("\n📊 Scores calculés:")
print(scores)
