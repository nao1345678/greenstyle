"""
Service de scraping automatique pour les marques
Utilise les scrapers existants pour collecter les données de durabilité
"""
import sys
import os
from typing import Dict, Optional

# Ajouter le répertoire parent au path pour importer les scrapers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
            data['certifications'] = ', '.join(cert_result['certifications'])
            print(f"  ✅ Certifications: {data['certifications']}")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping certifications: {e}")
    
    # 3. Gestion des invendus
    try:
        unsold_result = analyze_unsold_management(brand_name, website or '')
        if unsold_result and unsold_result.get('policy'):
            data['unsold_management'] = unsold_result['policy']
            print(f"  ✅ Gestion invendus: trouvée")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping invendus: {e}")
    
    # 4. Pays de production
    try:
        countries = get_production_countries_from_database(brand_name)
        if countries:
            data['country_production'] = countries
            print(f"  ✅ Pays de production: {countries}")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping pays: {e}")
    
    return data

