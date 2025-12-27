import math
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP

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
        env_score_base += 15  # Augmenté de 10 à 15
    elif location_info.strip():  # Si on a une info de pays
        env_score_base += 8   # Augmenté de 5 à 8
    else:
        env_score_base += 5   # Pas d'info = score minimal

    # 2. Matières Responsables (max 20 pts) 
    if materials_percent >= 50:
        env_score_base += 20
    elif materials_percent >= 25:
        env_score_base += 15  # Entre 25-50% = score moyen-élevé
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
        env_score_base += 8   # Augmenté de 7 à 8
    elif transparency_info.strip():  # Si on a une info (même vague)
        env_score_base += 6   # Score moyen si info présente
    else:
        env_score_base += 4   # Augmenté de 3 à 4 (score minimal plus généreux)

    env_score_base = min(env_score_base, 100)

    # ----------------------------------------------------
    # CALCUL ÉTHIQUE DU TRAVAIL (max 100)
    # ----------------------------------------------------
    # Vérifier si labor_ethics est déjà dans les données (depuis fallback)
    labor_val_raw = brand_data.get('labor_ethics')
    labor_score = None
    
    # Si labor_ethics est déjà un nombre (depuis fallback ou scraping), le traiter
    if labor_val_raw is not None:
        try:
            labor_val = float(labor_val_raw)
            if labor_val > 0:
                # Si valeur <= 10, c'est probablement déjà sur 10, convertir en score sur 100
                if labor_val <= 10:
                    labor_score = round(labor_val * 10)  # 8.5/10 → 85/100
                # Si valeur > 10 et <= 100, c'est déjà sur 100
                elif labor_val <= 100:
                    labor_score = round(labor_val)
                # Sinon (valeur > 100), c'est probablement sur 5, multiplier par 20
                else:
                    labor_score = round(labor_val * 20)
        except (ValueError, TypeError):
            pass
    
    # Si on n'a pas de score numérique, essayer de déduire du texte
    if labor_score is None:
        if any(k in labor_info for k in ["excellent", "a"]): labor_score = 100
        elif any(k in labor_info for k in ["bon", "good", "b"]): labor_score = 80
        elif any(k in labor_info for k in ["moyen", "average", "moderate", "c"]): labor_score = 60
        elif any(k in labor_info for k in ["mauvais", "poor", "bad", "d"]): labor_score = 40
        else: labor_score = 50  # Score par défaut plus réaliste
    
    labor_score = min(max(labor_score, 0), 100)  # S'assurer que c'est entre 0 et 100

    # --- CALCUL FINAL SUR 10 (au lieu de 5) ---
    def to_10(val):
        return float((Decimal(val) / Decimal('10')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    env_final = to_10(env_score_base)
    labor_final = to_10(labor_score)
    score_final = float((Decimal(env_final + labor_final) / Decimal('2')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    return {
        "global_env_impact": env_final,
        "labor_ethics": labor_final,
        "final_score": score_final
    }
