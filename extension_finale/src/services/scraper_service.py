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
    Utilise plusieurs sources pour obtenir des données complètes
    
    Sources de scraping:
    1. Base de données de fallback (marques connues)
    2. Scrapers spécialisés (matières, certifications, etc.)
    3. APIs externes (si disponibles)
    4. Analyse du site web de la marque
    
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
        data = fallback_data.copy()
        # Enrichir avec le scraping si possible (sans écraser les données de fallback)
        # On continue le scraping pour potentiellement enrichir les données
    else:
        data = {
            'brand_name': brand_name,
            'sustainable_materials': None,
            'certifications': None,
            'unsold_management': None,
            'country_production': None,
            'country_origin': None,
            'supply_chain_transparency': None,
        }
    
    # 1. Matières recyclées/durables (Source: scraper spécialisé)
    try:
        recycled_result = analyze_brand_for_recycled_materials(brand_name, website or '')
        if recycled_result and recycled_result.get('percentage'):
            # Ne pas écraser si on a déjà une valeur de fallback
            if data.get('sustainable_materials') is None:
                data['sustainable_materials'] = float(recycled_result['percentage'])
                print(f"  ✅ Matières durables (scraper): {data['sustainable_materials']}%")
            else:
                print(f"  ℹ️  Matières durables déjà définies (fallback): {data.get('sustainable_materials')}%")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping matières: {e}")
    
    # 1b. Recherche alternative: analyser le site web pour des mentions de matières durables
    if data.get('sustainable_materials') is None and website:
        try:
            # Cette fonction pourrait être implémentée pour scraper directement le site
            # Pour l'instant, on laisse les scrapers spécialisés gérer
            pass
        except Exception as e:
            print(f"  ⚠️  Erreur analyse site web: {e}")
    
    # 2. Certifications (Source: scraper spécialisé + base de données)
    try:
        cert_result = find_certifications_for_brand(brand_name, website or '')
        if cert_result and cert_result.get('certifications'):
            certs = cert_result['certifications']
            
            # Fusionner avec les certifications existantes (fallback)
            existing_certs = data.get('certifications', '')
            if isinstance(existing_certs, str) and existing_certs:
                existing_list = [c.strip() for c in existing_certs.split(',') if c.strip()]
            else:
                existing_list = []
            
            # Traiter les nouvelles certifications
            if isinstance(certs, list):
                certs_list = []
                for c in certs:
                    c_str = str(c).strip()
                    # Ignorer les URLs
                    if c_str and not c_str.startswith('http://') and not c_str.startswith('https://'):
                        certs_list.append(c_str)
            elif isinstance(certs, str):
                certs_list = [c.strip() for c in certs.split(',') if c.strip()]
            else:
                certs_list = []
            
            # Fusionner et dédupliquer
            all_certs = list(set(existing_list + certs_list))
            data['certifications'] = ', '.join(all_certs) if all_certs else None
            
            if data['certifications']:
                print(f"  ✅ Certifications (scraper): {data['certifications']}")
    except Exception as e:
        print(f"  ⚠️  Erreur scraping certifications: {e}")
        if data.get('certifications') is None:
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
    
    # 8. Enrichissement avec des données supplémentaires si disponibles
    # (Peut être étendu avec des APIs externes comme Good On You, Fashion Revolution, etc.)
    
    # 9. Calcul de la transparence si non défini
    if data.get('supply_chain_transparency') is None:
        # Déduire de la présence de données
        data_filled = sum(1 for k in ['sustainable_materials', 'certifications', 'unsold_management', 'country_production'] 
                         if data.get(k) is not None)
        if data_filled >= 3:
            data['supply_chain_transparency'] = 'Modérée'
        elif data_filled >= 1:
            data['supply_chain_transparency'] = 'Faible'
        else:
            data['supply_chain_transparency'] = 'Très faible'
    
    print(f"✅ Scraping terminé pour: {brand_name}")
    data_filled_count = sum(1 for v in data.values() if v is not None)
    print(f"📊 Données collectées: {data_filled_count}/{len(data)} champs remplis")
    
    # Log des sources utilisées
    if fallback_data:
        print(f"📚 Source principale: Base de données de fallback (marque connue)")
    else:
        print(f"📚 Source principale: Scrapers automatiques")
    
    return data

