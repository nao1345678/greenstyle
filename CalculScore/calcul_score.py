import math
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP
from pymongo import MongoClient
# Barèmes des certifications 
CERTIFICATION_SCORES = {
    "gots": 15,
    "fair trade certified": 10,
    "b corp": 10,
    "oeko-tex standard 100": 6,
    "bluesign": 6,
    "recycled claim standard": 3,
    "rcs": 3,
}

# Liste étendue pour la détection européenne 
EUROPEAN_COUNTRIES = [
    "europe", "france", "germany", "netherlands", "italy", "spain", 
    "portugal", "belgium", "sweden", "denmark", "uk", "united kingdom"
]

def calculate_scores(brand_data: Dict[str, Any]) -> Dict[str, float]:
    env_score_base = 0
    
    # --- PRÉPARATION DES DONNÉES ---
    # On regarde la production en priorité, sinon l'origine 
    production = str(brand_data.get('country_production', '') or '').lower()
    origin = str(brand_data.get('country_origin', '') or '').lower()
    location_info = f"{production} {origin}"

    # Matériaux durables
    try:
        materials_percent = float(brand_data.get('sustainable_materials', 0) or 0)
    except:
        materials_percent = 0.0

    # Certifications (peuvent être une liste ou une chaîne séparée par des virgules) 
    certs_raw = brand_data.get('certifications')
    if isinstance(certs_raw, list):
        certs_list = [c.strip().lower() for c in certs_raw if c]
    else:
        certs_list = [c.strip() for c in str(certs_raw or '').lower().split(',') if c.strip()]

    unsold_info = str(brand_data.get('unsold_management', '') or '').lower()
    transparency_info = str(brand_data.get('supply_chain_transparency', '') or '').lower()
    labor_info = str(brand_data.get('labor_ethics', '') or '').lower()

    # ----------------------------------------------------
    # CALCUL DU SCORE ENVIRONNEMENTAL 
    # ----------------------------------------------------

    # 1. Pays de Production (max 20 pts) 
    if "france" in location_info or "local" in location_info:
        env_score_base += 20
    elif any(country in location_info for country in EUROPEAN_COUNTRIES):
        env_score_base += 10
    else:
        env_score_base += 5

    # 2. Matières Responsables (max 20 pts) 
    if materials_percent >= 50:
        env_score_base += 20
    elif materials_percent > 0:
        env_score_base += 10
    else:
        env_score_base += 5

    # 3. Certifications (max 20 pts) 
    cert_points = 0
    for cert in certs_list:
        score = CERTIFICATION_SCORES.get(cert, 3) # 3 pts par défaut si inconnue 
        cert_points += score
    env_score_base += min(cert_points, 20)

    # 4. Gestion des Invendus (max 20 pts)
    # Ajout de "recycling", "donation", "program"
    if any(k in unsold_info for k in ["recyclage", "recycling", "circular", "upcycling"]):
        env_score_base += 20
    elif any(k in unsold_info for k in ["don", "charity", "caritatif"]):
        env_score_base += 10
    else:
        env_score_base += 5

    # 5. Transparence (max 20 pts) 
    # Ajout de "good" et "moderate" 
    if any(k in transparency_info for k in ["totale", "total", "full"]):
        env_score_base += 20
    elif any(k in transparency_info for k in ["partielle", "partial", "moderate", "good"]):
        env_score_base += 15
    elif any(k in transparency_info for k in ["médiocre", "mediocre", "poor", "limited"]):
        env_score_base += 7
    else:
        env_score_base += 3

    env_score_base = min(env_score_base, 100)

    # ----------------------------------------------------
    # CALCUL ÉTHIQUE DU TRAVAIL (max 100)
    # ----------------------------------------------------
    try:
        labor_val = float(brand_data.get('labor_ethics', 0))
        labor_score = round(labor_val * 20) if labor_val <= 5 else round(labor_val)
    except:
        if any(k in labor_info for k in ["excellent", "a"]): labor_score = 100
        elif any(k in labor_info for k in ["bon", "good", "b"]): labor_score = 80
        elif any(k in labor_info for k in ["moyen", "average", "moderate", "c"]): labor_score = 60
        elif any(k in labor_info for k in ["mauvais", "poor", "bad", "d"]): labor_score = 40
        else: labor_score = 20
    
    labor_score = min(labor_score, 100)

    # --- CALCUL FINAL SUR 5 ---
    def to_5(val):
        return float((Decimal(val) / Decimal('20')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    env_final = to_5(env_score_base)
    labor_final = to_5(labor_score)
    score_final = float((Decimal(env_final + labor_final) / Decimal('2')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    return {
        "global_env_impact": env_final,
        "labor_ethics": labor_final,
        "final_score": score_final
    }

def test_brand_from_db(brand):
    # 1. Connexion à MongoDB
    # Remplace par ta chaîne de connexion (ex: mongodb://localhost:27017/)
    client = MongoClient("mongodb://localhost:27017/") 
    db = client["greenstyle_"]
    collection = db["brands"]

    # 2. Récupération des données
    brand_data = collection.find_one({"brand": brand})

    if brand_data:
        print(f"--- Données récupérées pour {brand} ---")
        # 3. Calcul du score
        results = calculate_scores(brand_data)
        
        print("\n--- RÉSULTATS DU CALCUL ---")
        print(f"Impact Environnemental : {results['global_env_impact']}/5")
        print(f"Éthique du Travail     : {results['labor_ethics']}/5")
        print(f"SCORE FINAL            : {results['final_score']}/5")
    else:
        print(f"Erreur : La marque '{brand}' est introuvable dans la base.")

# Lancer le test
if __name__ == "__main__":
    # TEST MANUEL RAPIDE
    test_data = {
        "brand": "TestBrand",
        "country_production": "France",
        "sustainable_materials": 60,
        "certifications": "gots, b corp",
        "unsold_management": "recycling",
        "supply_chain_transparency": "total",
        "labor_ethics": "4"
    }
    print("--- Test Manuel ---")
    print(calculate_scores(test_data))
    
    # ENSUITE LANCER LE TEST DB
    print("\n--- Test Database ---")
    test_brand_from_db("EcoWave")