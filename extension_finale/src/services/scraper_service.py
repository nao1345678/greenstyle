"""
Service de scraping automatique pour les marques
Utilise les scrapers existants pour collecter les données de durabilité
"""
import sys
import os
from typing import Dict, Optional

# Ajouter le répertoire parent au path pour importer les scrapers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importer la base de données de fallback pour les marques engagées
try:
    from services.brand_data_fallback import get_fallback_brand_data
except ImportError:
    # Si le module n'est pas trouvé, créer une fonction vide
    def get_fallback_brand_data(brand_name: str):
        return None

try:
    from recycled_materials_scraper import analyze_brand_for_recycled_materials
    from certifications_scraper import find_certifications_for_brand
    from unsold_management_scraper import analyze_unsold_management
    from country_production_scraper import get_production_countries_from_database
except ImportError as e:
    print(f"⚠️  Warning: Impossible d'importer les scrapers: {e}")
    # Fonctions de fallback
    def analyze_brand_for_recycled_materials(*args, **kwargs):
        return {'percentage': None, 'confidence': 'low'}
    def find_certifications_for_brand(*args, **kwargs):
        return {'certifications': [], 'confidence': 'low'}
    def analyze_unsold_management(*args, **kwargs):
        return {'policy': None, 'practices': []}
    def get_production_countries_from_database(*args, **kwargs):
        return None


async def scrape_brand_data(brand_name: str, website: Optional[str] = None) -> Dict:
    """
    Scrape les données de durabilité pour une marque
    
    Args:
        brand_name: Nom de la marque
        website: URL du site web de la marque (optionnel)
    
    Returns:
        Dictionnaire avec les données scrapées
    """
    print(f"🔍 Scraping automatique pour: {brand_name}")
    
    # Vérifier d'abord si on a des données de fallback pour cette marque engagée
    fallback_data = get_fallback_brand_data(brand_name)
    if fallback_data:
        print(f"  ✅ Données de fallback trouvées pour {brand_name} (marque engagée connue)")
        return fallback_data.copy()
    
    data = {
        'brand_name': brand_name,
        'sustainable_materials': None,
        'certifications': None,
        'unsold_management': None,
        'country_production': None,
    }
    
    # 1. Matières recyclées/durables
    try:
        recycled_result = analyze_brand_for_recycled_materials(brand_name, website or '')
        if recycled_result and recycled_result.get('percentage'):
            data['sustainable_materials'] = float(recycled_result['percentage'])
            print(f"  ✅ Matières durables: {data['sustainable_materials']}%")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping matières: {e}")
    
    # 2. Certifications
    try:
        cert_result = find_certifications_for_brand(brand_name, website or '')
        if cert_result and cert_result.get('certifications'):
            certs = cert_result['certifications']
            # S'assurer que c'est toujours une string
            if isinstance(certs, list):
                # Filtrer les valeurs vides et convertir en string
                # Si ce sont des URLs, on les ignore et on retourne None
                # Sinon, on les joint avec des virgules
                certs_list = []
                for c in certs:
                    c_str = str(c).strip()
                    # Ignorer les URLs (commencent par http:// ou https://)
                    if c_str and not c_str.startswith('http://') and not c_str.startswith('https://'):
                        certs_list.append(c_str)
                data['certifications'] = ', '.join(certs_list) if certs_list else None
            elif isinstance(certs, str):
                # Si c'est une string qui contient une URL, on la retourne telle quelle
                # (peut-être que c'est un nom de certification avec une URL dans le texte)
                data['certifications'] = certs.strip() if certs.strip() else None
            else:
                data['certifications'] = str(certs).strip() if certs else None
            
            # Protection finale : s'assurer que c'est bien une string ou None
            if data['certifications'] is not None and not isinstance(data['certifications'], str):
                data['certifications'] = str(data['certifications']).strip() or None
            
            print(f"  ✅ Certifications: {data['certifications']}")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping certifications: {e}")
        data['certifications'] = None
    
    # 3. Gestion des invendus
    try:
        unsold_result = analyze_unsold_management(brand_name, website or '')
        if unsold_result and unsold_result.get('policy'):
            data['unsold_management'] = unsold_result['policy']
            print(f"  ✅ Gestion invendus: {data['unsold_management']}")
        elif unsold_result and unsold_result.get('practices'):
            # Si on a des pratiques mais pas de policy, utiliser les pratiques
            practices = unsold_result['practices']
            if isinstance(practices, list) and practices:
                data['unsold_management'] = ', '.join(str(p) for p in practices if p)
            elif isinstance(practices, str):
                data['unsold_management'] = practices
            if data.get('unsold_management'):
                print(f"  ✅ Gestion invendus: {data['unsold_management']}")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping invendus: {e}")
    
    # 4. Pays de production
    try:
        countries = get_production_countries_from_database(brand_name, website or '')
        if countries:
            # S'assurer que c'est une string
            if isinstance(countries, list):
                data['country_production'] = ', '.join(str(c) for c in countries if c)
            elif isinstance(countries, str):
                data['country_production'] = countries.strip()
            else:
                data['country_production'] = str(countries).strip() if countries else None
            
            if data.get('country_production'):
                print(f"  ✅ Pays de production: {data['country_production']}")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping pays: {e}")
    
    # 5. Pays d'origine (si différent du pays de production)
    if not data.get('country_origin') and data.get('country_production'):
        # Par défaut, utiliser le pays de production comme origine si non spécifié
        data['country_origin'] = data['country_production']
    
    # 6. Website si fourni
    if website:
        data['website'] = website
    
    # 7. Logo - essayer de deviner depuis le website
    if website and not data.get('logo'):
        try:
            from urllib.parse import urlparse
            domain = urlparse(website).netloc.replace('www.', '')
            # Générer une URL de logo probable (peut être amélioré avec une vraie recherche)
            data['logo'] = f"https://logo.clearbit.com/{domain}"
        except:
            pass
    
    print(f"✅ Scraping terminé pour: {brand_name}")
    print(f"📊 Données collectées: {sum(1 for v in data.values() if v is not None)}/{len(data)} champs remplis")
    return data

