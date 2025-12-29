import math
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP

# Barèmes des certifications (affiné avec plus de certifications)
CERTIFICATION_SCORES = {
    # Certifications majeures (15-20 pts)
    "gots": 20,  # Global Organic Textile Standard - très strict
    "fair trade certified": 18,  # Commerce équitable
    "b corp": 18,  # B-Corporation - impact social et environnemental
    "cradle to cradle": 20,  # Design circulaire complet
    
    # Certifications importantes (10-15 pts)
    "bluesign": 15,  # Production textile durable
    "oeko-tex standard 100": 12,  # Textiles sans substances nocives
    "oeko-tex made in green": 15,  # Oeko-Tex + responsabilité sociale
    "organic cotton": 12,  # Coton biologique
    "organic": 12,
    "grs": 12,  # Global Recycled Standard
    "rws": 12,  # Responsible Wool Standard
    
    # Certifications moyennes (6-10 pts)
    "recycled claim standard": 8,
    "rcs": 8,  # Recycled Claim Standard
    "better cotton initiative": 8,
    "bci": 8,
    "fsc": 8,  # Forest Stewardship Council
    "carbon neutral": 10,
    "climate neutral": 10,
    
    # Certifications basiques (3-6 pts)
    "peta approved": 5,
    "vegan": 5,
    "cruelty free": 5,
    "leather working group": 6,
    "lwg": 6,
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

    # 1. Pays de Production (max 25 pts) - Affiné avec plus de nuances pour plus de précision
    # Pays avec réglementations strictes et proximité (meilleur score)
    if "france" in location_info or "local" in location_info or "made in france" in location_info:
        env_score_base += 25
    # Pays européens avec excellentes réglementations environnementales
    elif any(country in location_info for country in ["denmark", "sweden", "norway", "finland"]):
        env_score_base += 22
    # Autres pays européens avec bonnes réglementations
    elif any(country in location_info for country in ["germany", "netherlands", "austria", "switzerland"]):
        env_score_base += 20
    # Autres pays européens
    elif any(country in location_info for country in EUROPEAN_COUNTRIES):
        env_score_base += 18
    # Pays développés hors Europe avec bonnes pratiques (USA, Canada, Japon, etc.)
    elif any(country in location_info for country in ["usa", "united states", "canada", "japan", "australia", "new zealand"]):
        env_score_base += 14
    # Pays en développement avec certaines garanties et certifications
    elif any(country in location_info for country in ["brazil", "india", "mexico", "turkey", "south korea"]):
        env_score_base += 10
    # Pays à risque modéré (Thaïlande, Philippines, etc.)
    elif any(country in location_info for country in ["thailand", "philippines", "sri lanka"]):
        env_score_base += 6
    # Pays à risque élevé (Chine, Bangladesh, Vietnam sans garanties)
    elif any(country in location_info for country in ["china", "bangladesh", "vietnam", "cambodia", "indonesia", "myanmar"]):
        env_score_base += 3
    elif location_info.strip():  # Si on a une info de pays mais non reconnu
        env_score_base += 7  # Score moyen pour pays non catégorisé
    else:
        env_score_base += 5   # Score par défaut réaliste (pas d'info = score neutre)

    # 2. Matières Responsables (max 25 pts) - Affiné avec plus de paliers pour plus de précision
    if materials_percent >= 90:
        env_score_base += 25  # Excellent (90-100%)
    elif materials_percent >= 80:
        env_score_base += 23  # Très excellent (80-90%)
    elif materials_percent >= 70:
        env_score_base += 21  # Excellent (70-80%)
    elif materials_percent >= 60:
        env_score_base += 19  # Très bon (60-70%)
    elif materials_percent >= 50:
        env_score_base += 17  # Bon (50-60%)
    elif materials_percent >= 40:
        env_score_base += 15  # Moyen-élevé (40-50%)
    elif materials_percent >= 30:
        env_score_base += 13  # Moyen (30-40%)
    elif materials_percent >= 25:
        env_score_base += 11  # Moyen-faible (25-30%)
    elif materials_percent >= 15:
        env_score_base += 9   # Faible mais effort (15-25%)
    elif materials_percent >= 10:
        env_score_base += 7   # Très faible effort (10-15%)
    elif materials_percent > 0:
        env_score_base += 5   # Effort minimal (0-10%)
    else:
        env_score_base += 3   # Aucun effort (score par défaut réaliste)

    # 3. Certifications (max 25 pts) - Affiné avec bonus pour multiples certifications
    cert_points = 0
    certs_found = []
    for cert in certs_list:
        score = CERTIFICATION_SCORES.get(cert, 2)  # 2 pts par défaut si inconnue
        cert_points += score
        certs_found.append(cert)
    
    # Bonus si plusieurs certifications importantes (synergie)
    if len(certs_found) >= 3:
        cert_points += 3  # Bonus pour diversité des certifications
    elif len(certs_found) >= 2:
        cert_points += 1
    
    env_score_base += min(cert_points, 25)

    # 4. Gestion des Invendus (max 20 pts) - Affiné avec plus de pratiques pour plus de précision
    # Pratiques circulaires avancées (meilleur score)
    if any(k in unsold_info for k in ["circular", "upcycling", "cradle to cradle"]):
        env_score_base += 20
    # Réparation et réutilisation (excellent)
    elif any(k in unsold_info for k in ["réparation", "repair", "réutilisation", "reuse", "refurbish"]):
        env_score_base += 18
    # Recyclage actif avec programmes dédiés
    elif any(k in unsold_info for k in ["recyclage", "recycling", "recycled", "recycling program"]):
        env_score_base += 15
    # Donation/charité (bonne pratique)
    elif any(k in unsold_info for k in ["don", "charity", "caritatif", "donation", "give"]):
        env_score_base += 12
    # Réduction/limitation (effort modéré)
    elif any(k in unsold_info for k in ["réduction", "reduction", "limitation", "limit", "minimize"]):
        env_score_base += 9
    # Pratiques partielles ou limitées
    elif any(k in unsold_info for k in ["partiel", "partial", "some", "limited"]):
        env_score_base += 6
    # Aucune info ou pratique limitée
    else:
        env_score_base += 4  # Score par défaut réaliste (pas d'info = score faible)

    # 5. Transparence (max 20 pts) - Affiné avec plus de nuances pour plus de précision
    if any(k in transparency_info for k in ["totale", "total", "full", "complète", "complete", "très élevée", "very high", "complete transparency"]):
        env_score_base += 20
    elif any(k in transparency_info for k in ["élevée", "high", "good", "bonne", "strong", "excellent"]):
        env_score_base += 17
    elif any(k in transparency_info for k in ["bonne", "good", "satisfaisante", "satisfactory"]):
        env_score_base += 14
    elif any(k in transparency_info for k in ["partielle", "partial", "moderate", "modérée", "moderate transparency"]):
        env_score_base += 11
    elif any(k in transparency_info for k in ["moyenne", "average", "acceptable"]):
        env_score_base += 8
    elif any(k in transparency_info for k in ["médiocre", "mediocre", "poor", "limited", "faible", "low", "weak"]):
        env_score_base += 5
    elif transparency_info.strip():  # Si on a une info (même vague)
        env_score_base += 6   # Score moyen si info présente mais vague
    else:
        env_score_base += 4   # Score par défaut réaliste (pas d'info = score faible)

    # 6. BONUS: Initiatives supplémentaires (max 10 pts) - Affiné pour plus de précision
    # Détection de pratiques supplémentaires mentionnées dans la description
    description = str(brand_data.get('description', '') or '').lower()
    all_text = f"{description} {unsold_info} {transparency_info}".lower()
    
    bonus_points = 0
    
    # Initiatives climatiques (max 4 pts)
    if any(k in all_text for k in ["carbon neutral", "net zero", "zéro émission", "climate positive", "carbon negative"]):
        bonus_points += 4
    elif any(k in all_text for k in ["carbon offset", "compensation carbone", "renewable energy"]):
        bonus_points += 2
    
    # Gestion de l'eau (max 2 pts)
    if any(k in all_text for k in ["water saving", "économie d'eau", "water efficient", "water conservation"]):
        bonus_points += 2
    elif any(k in all_text for k in ["water", "eau"]):
        bonus_points += 1
    
    # Durabilité des produits (max 2 pts)
    if any(k in all_text for k in ["durable", "long lasting", "quality", "réparable", "repairable"]):
        bonus_points += 2
    
    # Économie circulaire (max 2 pts)
    if any(k in all_text for k in ["circular economy", "économie circulaire", "closed loop", "zero waste"]):
        bonus_points += 2
    
    env_score_base += min(bonus_points, 10)
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
    
    # Si on n'a pas de score numérique, essayer de déduire du texte avec plus de précision
    if labor_score is None:
        if any(k in labor_info for k in ["excellent", "a", "outstanding", "exceptional"]): 
            labor_score = 95
        elif any(k in labor_info for k in ["très bon", "very good", "a-", "b+"]): 
            labor_score = 85
        elif any(k in labor_info for k in ["bon", "good", "b", "satisfaisant"]): 
            labor_score = 75
        elif any(k in labor_info for k in ["assez bon", "fairly good", "b-", "c+"]): 
            labor_score = 65
        elif any(k in labor_info for k in ["moyen", "average", "moderate", "c", "acceptable"]): 
            labor_score = 55
        elif any(k in labor_info for k in ["médiocre", "mediocre", "c-", "d+", "below average"]): 
            labor_score = 45
        elif any(k in labor_info for k in ["mauvais", "poor", "bad", "d", "unsatisfactory"]): 
            labor_score = 35
        elif any(k in labor_info for k in ["très mauvais", "very poor", "d-", "f", "unacceptable"]): 
            labor_score = 25
        else: 
            labor_score = 55  # Score par défaut réaliste (moyen)
    
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
