import math
from typing import Dict, Any

def calculate_scores(brand_data: Dict[str, Any]) -> Dict[str, float]:
    
    # Initialisation des scores (base 100 points)
    env_score_base = 0
    labor_score_base = 0
    
    # --- CALCUL DU SCORE D'IMPACT ENVIRONNEMENTAL (max 100 points) ---
    
    # 1. Country of Origin (max 20 points)
    country_of_origin = str(brand_data.get('country_of_origin', '')).lower()
    if "local" in country_of_origin or "france" in country_of_origin:
        env_score_base += 20
    elif "europe" in country_of_origin:
        env_score_base += 10
    else:
        env_score_base += 5
        
    # 2. Responsible Materials (max 20 points)
    # Champ MongoDB: responsible_materials (int)
    responsible_materials_percent = int(brand_data.get('responsible_materials', 0)) 
    if responsible_materials_percent >= 50:
        env_score_base += 20
    elif responsible_materials_percent > 0:
        env_score_base += 10
    else:
        env_score_base += 5
        
    # 3. Certifications (max 40 points)
    # Champ MongoDB: certifications (array)
    certifications_list = brand_data.get('certifications', [])
    env_score_base += min(len(certifications_list) * 10, 40)

    # 4. Unsold Management (Gestion des invendus) (max 10 points)
    # Champ MongoDB: unsold_management (string)
    unsold_management_info = str(brand_data.get('unsold_management', '')).lower()
    if "recyclage" in unsold_management_info or "don" in unsold_management_info:
        env_score_base += 10
    else:
        env_score_base += 5
        
    # 5. Supply Chain Transparency (Transparence de la chaîne) (max 10 points)
    # Champ MongoDB: supply_chain_transparency (string)
    transparency_info = str(brand_data.get('supply_chain_transparency', '')).lower()
    if "totale" in transparency_info:
        env_score_base += 10
    elif "partielle" in transparency_info:
        env_score_base += 7
    elif "médiocre" in transparency_info:
        env_score_base += 3
