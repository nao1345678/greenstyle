import math
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP

# Barèmes des certifications pour le calcul ENVIRONNEMENTAL (max 20 points) [cite: 92]
CERTIFICATION_SCORES = {
    "gots": 15,
    "fair trade certified": 10,
    "b corp": 10,
    "oeko-tex standard 100": 6,
    "bluesign": 6,
    "recycled claim standard": 3,
    "rcs": 3,
}

def calculate_scores(brand_data: Dict[str, Any]) -> Dict[str, float]:
    env_score_base = 0
    labor_score_base = 0

    # --- PRÉPARATION DES DONNÉES ---
    # Normalisation des chaînes pour la comparaison
    country_origin = str(brand_data.get('country_origin', '') or '').lower()
    
    # Pourcentage ou niveau de matières responsables (pour l'étape 2)
    responsible_materials_data = brand_data.get('sustainable_materials', 0)
    try:
        responsible_materials_percent = float(responsible_materials_data)
    except (ValueError, TypeError):
        # Si ce n'est pas un nombre, on le traite comme une chaîne pour la logique
        responsible_materials_percent = 0.0

    certifications_data = brand_data.get('certifications')
    if isinstance(certifications_data, list):
        certifications_list = [c.strip().lower() for c in certifications_data if c and c.strip()]
    else:
        certifications_str = str(certifications_data or '').lower()
        # Supprime les caractères non alphabétiques pour la recherche simple
        certifications_list = [c.strip() for c in certifications_str.split(',') if c.strip()]

    unsold_management_info = str(brand_data.get('unsold_management', '') or '').lower()
    transparency_info = str(brand_data.get('supply_chain_transparency', '') or '').lower()
    
    # ----------------------------------------------------
    # CALCUL DU SCORE D'IMPACT ENVIRONNEMENTAL
    # ----------------------------------------------------

    # 1. Pays d'origine (max 20 points) 
    # 'country_origin' comme source d'info principale pour la production
    if "local" in country_origin or "france" in country_origin:
        env_score_base += 20  # Production locale = 20 points
    elif "europe" in country_origin:
        env_score_base += 10  # Production européenne = 10 points
    else:
        env_score_base += 5   # Production Asie ou autre = 5 points

    # 2. Materiels Responsables (max 20 points) 
    # On utilise le pourcentage stocké dans 'sustainable_materials' pour déduire le niveau.
    if responsible_materials_percent >= 50:
        env_score_base += 20  # Majorité > 50% = 20 points
    elif responsible_materials_percent > 0:
        env_score_base += 10  # Partiel (une seule ligne, ou > 0%) = 10 points
    else:
        env_score_base += 5   # Faible / aucune info = 5 points

    # 3. Certifications (max 20 points) 
    certif_total_points = 0
    for cert in certifications_list:
        found_score = CERTIFICATION_SCORES.get(cert)
        if found_score is not None:
            certif_total_points += found_score
        elif cert:
            # Autres certif inconnues = 3 points
            certif_total_points += 3
    
    # Le score est plafonné à 20 points même si la somme est supérieure 
    env_score_base += min(certif_total_points, 20)
    
    # 4. Gestion des Invendus (max 20 points) 
    if "circularité" in unsold_management_info or "recyclage" in unsold_management_info or "upcycling" in unsold_management_info:
        env_score_base += 20  # Politique claire (circularité, recyclage, etc.) = 20 points
    elif "dons" in unsold_management_info or "caritatifs" in unsold_management_info:
        env_score_base += 10  # Dons à des associations = 10 points
    else:
        env_score_base += 5   # Aucune politique claire = 5 points
        
    # 5. Transparence de la chaîne (max 20 points) 
    if "totale" in transparency_info or "publie publiquement" in transparency_info:
        env_score_base += 20  # Transparence Totale (rang 1, 2, sources) = 20 points
    elif "partielle" in transparency_info or ("rang 1" in transparency_info and "rang 2" in transparency_info):
        env_score_base += 15  # Transparence Partielle (rang 1 et 2) = 15 points
    elif "médiocre" in transparency_info or "rang 1" in transparency_info:
        env_score_base += 7   # Transparence Médiocre (rang 1) = 7 points
    else:
        env_score_base += 3   # Aucune transparence / infos vagues = 3 points
        
    # S'assurer que le score ENVIRONNEMENTAL ne dépasse pas 100
    env_score_base = min(env_score_base, 100)

    # ------------------------------------------------------------
    # --- CALCUL DU SCORE D'ÉTHIQUE DU TRAVAIL ---
    # -----------------------------------------------------------
    
    labor_ethics_data = brand_data.get('labor_ethics', 0)
    float_score = None

    try:
        # Tente de lire directement un score sur 100 ou sur 1.0 (ex: 0.8)
        float_score = float(labor_ethics_data)
    except (ValueError, TypeError):
        pass

    if float_score is not None:
        if 0.0 <= float_score <= 1.0:
            labor_score_base = round(float_score * 100)
        elif 1.0 < float_score <= 100:
            labor_score_base = round(float_score)
        else:
            labor_score_base = 0
    else:
        # Utilise les catégories documentées si aucune note n'est fournie
        ethique_travail_info = str(labor_ethics_data or '').lower().strip()
        
        if ethique_travail_info == "excellent" or ethique_travail_info == "a" or "excellentes pratiques" in ethique_travail_info:
            labor_score_base = 100
        elif ethique_travail_info == "bonnes pratiques" or ethique_travail_info == "b":
            labor_score_base = 80
        elif ethique_travail_info == "pratiques moyennes" or ethique_travail_info == "c":
            labor_score_base = 60
        elif ethique_travail_info == "pratiques médiocres" or ethique_travail_info == "d" or "mauvaises" in ethique_travail_info:
            labor_score_base = 40
        elif "aucune" in ethique_travail_info:
            labor_score_base = 20
            
    labor_score_base = min(labor_score_base, 100)
    
    # --- CONVERSION ET CALCUL DU SCORE FINAL (sur 5) 
    
    # 1. Calcul de l'Impact Environnemental sur 5 (env_score_base / 20)
    intermediate_env = Decimal(env_score_base) / Decimal('20')
    global_env_impact_decimal = intermediate_env.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    global_env_impact = float(global_env_impact_decimal)

    # 2. Calcul de l'Éthique du Travail sur 5 (labor_score_base / 20)
    intermediate_labor = Decimal(labor_score_base) / Decimal('20')
    labor_ethics_decimal = intermediate_labor.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    labor_ethics = float(labor_ethics_decimal)

    # 3. Calcul de la Moyenne Finale
    final_score_decimal = (global_env_impact_decimal + labor_ethics_decimal) / Decimal('2')
    final_score = float(final_score_decimal.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    return {
        "global_env_impact": global_env_impact,
        "labor_ethics": labor_ethics,
        "final_score": final_score,
    }