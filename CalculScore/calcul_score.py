# Fichier : CalculScore/calcul_score.py (Corrigé avec Decimal)

import math
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP # 💡 Importation nécessaire

def calculate_scores(brand_data: Dict[str, Any]) -> Dict[str, float]:
    
    env_score_base = 0
    labor_score_base = 0 
    
    country_origin = str(brand_data.get('country_origin', '')).lower()
    responsible_materials_percent = float(brand_data.get('sustainable_materials', 0) or 0)
    certifications_str = str(brand_data.get('certifications', '') or '')
    unsold_management_info = str(brand_data.get('unsold_management', '')).lower()
    transparency_info = str(brand_data.get('supply_chain_transparency', '')).lower()


    # ----------------------------------------------------
    # CALCUL DU SCORE D'IMPACT ENVIRONNEMENTAL (max 100 points)
    # ----------------------------------------------------
    
    # Pays d'origine (max 20 points)
    if "local" in country_origin or "france" in country_origin:
        env_score_base += 20
    elif "europe" in country_origin:
        env_score_base += 10
    else:
        env_score_base += 5
        
    # Materiels Responsable (max 20 points)
    if responsible_materials_percent >= 50:
        env_score_base += 20
    elif responsible_materials_percent > 0:
        env_score_base += 10
    else:
        env_score_base += 5
        
    # Certifications (max 40 points)
    certifications_list = [c.strip() for c in certifications_str.split(',') if c.strip()]
    env_score_base += min(len(certifications_list) * 10, 40)

    # Invendu (max 10 points)
    if "recyclage" in unsold_management_info or "don" in unsold_management_info:
        env_score_base += 10
    else:
        env_score_base += 5
        
    # Transparence info (max 10 points)
    if "totale" in transparency_info:
        env_score_base += 10
    elif "partielle" in transparency_info:
        env_score_base += 7
    elif "médiocre" in transparency_info:
        env_score_base += 3

    # On s'assure que le score ne depasse pas 100
    env_score_base = min(env_score_base, 100)

    # ------------------------------------------------------------ 
    # --- CALCUL DU SCORE D'ÉTHIQUE DU TRAVAIL (max 100 points) ---
    # Le score est basé sur une note de 0 à 1 (ou A à D), mise à l'échelle sur 100.
    # ------------------------------------------------------------ 
    
    # On récupère la donnée brute (peut être un nombre décimal, un entier, ou un mot)
    labor_ethics_data = brand_data.get('labor_ethics', 0)
    labor_score_base = 0
    float_score = None

    # Tente d'abord de convertir en float (pour gérer 0.8, 1.0, 60.0, etc.)
    try:
        # S'assure que la conversion est possible
        float_score = float(labor_ethics_data)
    except (ValueError, TypeError):
        # Si ce n'est pas un nombre, float_score reste None
        pass 


    if float_score is not None:
        if 0.0 <= float_score <= 1.0:
            # C'est la nouvelle note de 0 à 1, on la met à l'échelle sur 100.
            labor_score_base = round(float_score * 100)
        elif 1.0 < float_score <= 100:
            # C'est une ancienne note sur 100, on la garde.
            labor_score_base = round(float_score)
        else:
             # Si le float est < 0 ou > 100, on le met à 0
            labor_score_base = 0 
    else:
        # Si ce n'est pas un nombre, on utilise les mots-clés ou les lettres (A, B, C, D).
        ethique_travail_info = str(labor_ethics_data).lower().strip()

        if ethique_travail_info == "a" or "excellent" in ethique_travail_info:
            labor_score_base = 100
        elif ethique_travail_info == "b" or "bonne" in ethique_travail_info:
            labor_score_base = 80
        elif ethique_travail_info == "c" or "moyenne" in ethique_travail_info:
            labor_score_base = 60
        elif ethique_travail_info == "d" or "médiocre" in ethique_travail_info or "mauvaises conditions" in ethique_travail_info:
            # Correspond à 40 points, le bas de l'échelle des notes.
            labor_score_base = 40
        elif "aucune" in ethique_travail_info:
            # 20 points pour "aucune" car c'est le minimum non nul.
            labor_score_base = 20
        # Sinon labor_score_base reste à 0 (valeur initiale).


    # On s'assure que le score ne dépasse pas 100
    labor_score_base = min(labor_score_base, 100)


    # --- CONVERSION ET CALCUL DU SCORE FINAL (sur 5) ---
    
    # NOTE: Le bloc ci-dessous utilise la méthode Decimal pour assurer une précision
    # dans l'arrondi (ROUND_HALF_UP) et évite d'utiliser la fonction custom_round redondante.

    # 1. Calcul de l'Impact Environnemental sur 5 (env_score_base / 20)
    # On utilise Decimal pour les calculs d'arrondi précis
    intermediate_env = Decimal(env_score_base) / Decimal('20')
    
    # Arrondir à 1 décimale avec ROUND_HALF_UP et convertir en float pour le retour
    global_env_impact_decimal = intermediate_env.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    global_env_impact = float(global_env_impact_decimal)

    # 2. Calcul de l'Éthique du Travail sur 5 (labor_score_base / 20)
    intermediate_labor = Decimal(labor_score_base) / Decimal('20')
    labor_ethics_decimal = intermediate_labor.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    labor_ethics = float(labor_ethics_decimal)
    
    # 3. Calcul de la Moyenne Finale
    # Utiliser les valeurs Decimal pour la moyenne précise
    final_score_decimal = (global_env_impact_decimal + labor_ethics_decimal) / Decimal('2')
    
    # Arrondir le score final et le convertir en float pour le retour
    final_score = float(final_score_decimal.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    return {
        "global_env_impact": global_env_impact,
        "labor_ethics": labor_ethics,
        "final_score": final_score,
    }