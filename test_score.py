from CalculScore import calcul_score
import json

# 1. Définition des cas de test
test_cases = [
    {
        "name": "Marque Éco-Responsable (Local & Certifiée)",
        "data": {
            "country_production": "France",
            "sustainable_materials": 80,
            "certifications": ["GOTS", "B Corp"],
            "unsold_management": "Recyclage et Upcycling",
            "supply_chain_transparency": "Totale",
            "labor_ethics": "Excellent"
        }
    },
    {
        "name": "Marque Fast Fashion (Données Anglais & Production Asie)",
        "data": {
            "country_production": "Vietnam",
            "country_origin": "USA",
            "sustainable_materials": 10,
            "certifications": [],
            "unsold_management": "None",
            "supply_chain_transparency": "Limited",
            "labor_ethics": "Poor"
        }
    },
    {
        "name": "Marque Moyenne (Europe & Transparence Partielle)",
        "data": {
            "country_production": "Portugal",
            "sustainable_materials": 30,
            "certifications": ["Oeko-Tex"],
            "unsold_management": "Donation to charity",
            "supply_chain_transparency": "Moderate",
            "labor_ethics": "B"
        }
    }
]

def run_tests():
    print("=== TEST DU CALCULATEUR GREENSTYLE (Pondération 20x5) ===\n")
    
    for case in test_cases:
        name = case["name"]
        data = case["data"]
        
        result = calcul_score.calculate_scores(data)
        
        print(f"--- {name} ---")
        print(f" Impact Environnemental : {result['global_env_impact']}/5")
        print(f"  Éthique du Travail     : {result['labor_ethics']}/5")
        print(f" SCORE FINAL            : {result['final_score']}/5")
        
        # Petit diagnostic pour expliquer le score env
        print("Détails du calcul (estimation des points) :")
        # On peut rajouter des prints dans la fonction calcul_score pour débugger
        print("-" * 30 + "\n")

if __name__ == "__main__":
    run_tests()