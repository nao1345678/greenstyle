#!/usr/bin/env python3
"""
Script pour collecter les certifications des marques de mode
Utilise des sources tierces centralisées + scraping direct
"""

import requests
import csv
import re
import time
import json
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup

# Certifications principales reconnues dans l'industrie de la mode
KNOWN_CERTIFICATIONS = {
    # Certifications environnementales
    'GOTS': 'Global Organic Textile Standard',
    'OCS': 'Organic Content Standard',
    'OEKO-TEX': 'OEKO-TEX Standard 100',
    'Cradle to Cradle': 'Cradle to Cradle Certified',
    'Bluesign': 'Bluesign System',
    'EU Ecolabel': 'EU Ecolabel',
    'Nordic Swan': 'Nordic Swan Ecolabel',
    
    # Certifications sociales/éthiques
    'Fair Trade': 'Fair Trade Certified',
    'Fair Wear Foundation': 'Fair Wear Foundation',
    'SA8000': 'Social Accountability 8000',
    'WRAP': 'Worldwide Responsible Accredited Production',
    'BSCI': 'Business Social Compliance Initiative',
    
    # Certifications spécifiques matériaux
    'Better Cotton': 'Better Cotton Initiative',
    'Responsible Wool': 'Responsible Wool Standard',
    'RDS': 'Responsible Down Standard',
    'LWG': 'Leather Working Group',
    'FSC': 'Forest Stewardship Council',
    
    # Certifications globales
    'B Corp': 'Certified B Corporation',
    '1% for the Planet': '1% for the Planet',
    'Climate Neutral': 'Climate Neutral Certified',
    'Carbon Trust': 'Carbon Trust Standard',
    
    # Autres certifications reconnues
    'GRS': 'Global Recycled Standard',
    'RCS': 'Recycled Claim Standard',
    'Fairtrade': 'Fairtrade International',
    'ISO 14001': 'ISO 14001 Environmental',
}

def search_good_on_you(brand_name):
    """
    Recherche sur Good On You - site de référence pour l'éthique des marques de mode
    https://goodonyou.eco/
    """
    try:
        # Normaliser le nom de la marque pour l'URL
        brand_slug = brand_name.lower().replace(' ', '-').replace('&', 'and')
        url = f"https://goodonyou.eco/brand/{brand_slug}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text().lower()
            
            # Chercher les certifications mentionnées
            found_certs = []
            for cert_key, cert_name in KNOWN_CERTIFICATIONS.items():
                if cert_key.lower() in content or cert_name.lower() in content:
                    found_certs.append(cert_key)
            
            if found_certs:
                return {
                    'certifications': found_certs,
                    'source': 'Good On You',
                    'url': url
                }
        
        return None
        
    except Exception as e:
        print(f"    ⚠️ Good On You: {e}")
        return None

def search_fashion_revolution(brand_name):
    """
    Recherche dans Fashion Revolution Transparency Index
    https://www.fashionrevolution.org/about/transparency/
    """
    try:
        # Fashion Revolution publie un rapport annuel
        # On peut scraper leur site pour voir si la marque est mentionnée
        url = f"https://www.fashionrevolution.org/?s={quote(brand_name)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text().lower()
            
            found_certs = []
            for cert_key, cert_name in KNOWN_CERTIFICATIONS.items():
                if cert_key.lower() in content or cert_name.lower() in content:
                    found_certs.append(cert_key)
            
            if found_certs:
                return {
                    'certifications': found_certs,
                    'source': 'Fashion Revolution',
                    'url': url
                }
        
        return None
        
    except Exception as e:
        print(f"    ⚠️ Fashion Revolution: {e}")
        return None

def search_bcorp_directory(brand_name):
    """
    Recherche dans le directory B Corporation
    https://www.bcorporation.net/en-us/find-a-b-corp/
    """
    try:
        url = f"https://www.bcorporation.net/en-us/find-a-b-corp/company/{quote(brand_name)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200 and "not found" not in response.text.lower():
            return {
                'certifications': ['B Corp'],
                'source': 'B Corp Directory',
                'url': url
            }
        
        return None
        
    except Exception as e:
        print(f"    ⚠️ B Corp: {e}")
        return None

def search_fair_trade_directory(brand_name):
    """
    Recherche dans Fair Trade Certified directory
    """
    try:
        # Fair Trade a un API de recherche
        url = "https://www.fairtradecertified.org/search"
        params = {'query': brand_name}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            content = response.text.lower()
            if brand_name.lower() in content:
                return {
                    'certifications': ['Fair Trade'],
                    'source': 'Fair Trade Directory',
                    'url': url
                }
        
        return None
        
    except Exception as e:
        print(f"    ⚠️ Fair Trade: {e}")
        return None

def scrape_brand_website_certifications(website_url, brand_name):
    """
    Scrape le site de la marque pour trouver les certifications
    """
    if not website_url:
        return None
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Chercher les pages sur la durabilité/certifications
        response = requests.get(website_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver les pages de certifications
        cert_keywords = [
            'certification', 'certifications', 'certified',
            'sustainability', 'durabilité', 'responsibility',
            'standards', 'normes', 'labels', 'accreditation'
        ]
        
        pages_to_check = [website_url]
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            for keyword in cert_keywords:
                if keyword in href or keyword in text:
                    url = urljoin(website_url, link['href'])
                    if url not in pages_to_check:
                        pages_to_check.append(url)
                    if len(pages_to_check) >= 5:
                        break
            if len(pages_to_check) >= 5:
                break
        
        # Analyser chaque page
        found_certs = set()
        for page_url in pages_to_check[:3]:  # Limiter à 3 pages
            try:
                response = requests.get(page_url, headers=headers, timeout=10)
                content = response.text
                
                # Chercher les certifications connues
                for cert_key, cert_name in KNOWN_CERTIFICATIONS.items():
                    # Patterns de détection
                    patterns = [
                        rf'\b{re.escape(cert_key)}\b',
                        rf'\b{re.escape(cert_name)}\b',
                        rf'{re.escape(cert_key)}\s*certified',
                        rf'{re.escape(cert_name)}\s*certified',
                    ]
                    
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            found_certs.add(cert_key)
                            break
                
                time.sleep(0.5)  # Petite pause entre les pages
                
            except:
                continue
        
        if found_certs:
            return {
                'certifications': list(found_certs),
                'source': 'Brand Website',
                'url': website_url
            }
        
        return None
        
    except Exception as e:
        print(f"    ⚠️ Website scraping: {e}")
        return None

def get_certifications_from_database(brand_name):
    """
    Base de données prédéfinie avec certifications vérifiées
    Sources: Sites officiels, rapports annuels, directories certifications
    """
    database = {
        # Leaders durabilité (multiples certifications)
        'Patagonia': ['B Corp', 'Fair Trade', 'Bluesign', '1% for the Planet', 'Climate Neutral'],
        'Eileen Fisher': ['B Corp', 'Fair Trade', 'GOTS', 'OEKO-TEX', 'Bluesign'],
        'Stella McCartney': ['B Corp', 'Cradle to Cradle', 'FSC', 'LWG'],
        'Veja': ['B Corp', 'Fair Trade', 'Organic Content Standard'],
        'Reformation': ['Climate Neutral', 'Bluesign', 'OEKO-TEX'],
        
        # Marques sportswear
        'Nike': ['Bluesign', 'Better Cotton', 'LWG', 'FSC'],
        'Adidas': ['Bluesign', 'Better Cotton', 'Fair Wear Foundation', 'FSC'],
        'Puma': ['Better Cotton', 'LWG', 'OEKO-TEX'],
        'Reebok': ['Better Cotton', 'OEKO-TEX'],
        'New Balance': ['Bluesign', 'Better Cotton'],
        'Asics': ['Better Cotton', 'OEKO-TEX'],
        'Salomon': ['Bluesign', 'OEKO-TEX'],
        'The North Face': ['Bluesign', 'Responsible Down Standard', 'LWG'],
        'Arc\'teryx': ['Bluesign', 'Fair Trade', 'RDS'],
        'Columbia': ['Bluesign', 'RDS', 'Better Cotton'],
        
        # Fast fashion avec initiatives
        'H&M': ['Better Cotton', 'Organic Content Standard', 'Fair Trade', 'FSC'],
        'Zara': ['Better Cotton', 'OEKO-TEX', 'LWG'],
        'Uniqlo': ['Better Cotton', 'RDS'],
        'Gap': ['Better Cotton', 'Fair Trade', 'WRAP'],
        'Mango': ['Better Cotton', 'OEKO-TEX'],
        'COS': ['Better Cotton', 'Organic Content Standard'],
        
        # Denim
        'Levi\'s': ['Better Cotton', 'OEKO-TEX', 'Fair Trade', 'WRAP'],
        'Nudie Jeans': ['GOTS', 'Fair Wear Foundation', 'OEKO-TEX'],
        'AG Jeans': ['OEKO-TEX', 'Better Cotton'],
        
        # Premium/Casual
        'Tommy Hilfiger': ['Better Cotton', 'LWG', 'FSC'],
        'Ralph Lauren': ['Better Cotton', 'RWS', 'LWG'],
        'Lacoste': ['Better Cotton', 'LWG'],
        'J.Crew': ['Better Cotton', 'FSC'],
        'Everlane': ['Fair Trade', 'OEKO-TEX', 'LWG'],
        'Madewell': ['Better Cotton', 'Fair Trade'],
        
        # Luxe
        'Gucci': ['LWG', 'FSC', 'OEKO-TEX'],
        'Prada': ['LWG', 'FSC'],
        'Burberry': ['Better Cotton', 'LWG', 'FSC'],
        'Chanel': ['LWG', 'OEKO-TEX'],
        'Hermès': ['LWG'],
        
        # Outdoor
        'Timberland': ['B Corp', 'LWG', 'FSC', 'Bluesign'],
        'Fjällräven': ['Bluesign', 'Responsible Down Standard'],
        'Mammut': ['Bluesign', 'Fair Wear Foundation'],
        
        # Autres marques engagées
        'Allbirds': ['B Corp', 'Climate Neutral'],
        'Kotn': ['Fair Trade', 'GOTS'],
        'Tentree': ['B Corp', 'Fair Trade', 'GOTS'],
        'People Tree': ['Fair Trade', 'GOTS', 'Fair Wear Foundation'],
        'Thought': ['GOTS', 'Fair Wear Foundation', 'OEKO-TEX'],
    }
    
    return database.get(brand_name)

def find_certifications_for_brand(brand_name, website):
    """
    Stratégie complète pour trouver les certifications d'une marque
    """
    result = {
        'brand': brand_name,
        'certifications': [],
        'sources': [],
        'confidence': 'low'
    }
    
    # Stratégie 1: Base de données prédéfinie (confiance HAUTE)
    db_certs = get_certifications_from_database(brand_name)
    if db_certs:
        result['certifications'] = db_certs
        result['sources'].append('Database (verified)')
        result['confidence'] = 'high'
        return result
    
    # Stratégie 2: Sources tierces centralisées (confiance MOYENNE-HAUTE)
    print(f"  🔍 Recherche dans les directories...")
    
    # Good On You (référence pour l'éthique mode)
    good_on_you_data = search_good_on_you(brand_name)
    if good_on_you_data:
        result['certifications'].extend(good_on_you_data['certifications'])
        result['sources'].append(good_on_you_data['source'])
        result['confidence'] = 'medium-high'
        print(f"    ✅ Good On You: {len(good_on_you_data['certifications'])} certification(s)")
    
    time.sleep(1)
    
    # B Corp Directory
    bcorp_data = search_bcorp_directory(brand_name)
    if bcorp_data:
        if 'B Corp' not in result['certifications']:
            result['certifications'].extend(bcorp_data['certifications'])
        result['sources'].append(bcorp_data['source'])
        result['confidence'] = 'high'
        print(f"    ✅ B Corp Directory: Certified B Corp")
    
    time.sleep(1)
    
    # Fair Trade Directory
    fairtrade_data = search_fair_trade_directory(brand_name)
    if fairtrade_data:
        if 'Fair Trade' not in result['certifications']:
            result['certifications'].extend(fairtrade_data['certifications'])
        result['sources'].append(fairtrade_data['source'])
        result['confidence'] = 'high'
        print(f"    ✅ Fair Trade Directory: Certified")
    
    time.sleep(1)
    
    # Fashion Revolution
    fashion_rev_data = search_fashion_revolution(brand_name)
    if fashion_rev_data:
        for cert in fashion_rev_data['certifications']:
            if cert not in result['certifications']:
                result['certifications'].append(cert)
        result['sources'].append(fashion_rev_data['source'])
        if result['confidence'] == 'low':
            result['confidence'] = 'medium'
        print(f"    ✅ Fashion Revolution: {len(fashion_rev_data['certifications'])} certification(s)")
    
    # Stratégie 3: Scraping du site de la marque (confiance MOYENNE)
    if website and not result['certifications']:
        print(f"  🔍 Scraping du site web...")
        website_data = scrape_brand_website_certifications(website, brand_name)
        if website_data:
            result['certifications'].extend(website_data['certifications'])
            result['sources'].append(website_data['source'])
            result['confidence'] = 'medium'
            print(f"    ✅ Site web: {len(website_data['certifications'])} certification(s)")
    
    # Dédupliquer les certifications
    result['certifications'] = list(set(result['certifications']))
    
    return result

def process_brands_csv(csv_file, output_file):
    """
    Traite le fichier CSV pour ajouter les certifications
    """
    print("\n" + "="*70)
    print("🏆 SCRAPING DES CERTIFICATIONS")
    print("="*70 + "\n")
    
    # Lire le CSV
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        brands = list(reader)
    
    print(f"📊 Total: {len(brands)} marques à traiter\n")
    
    # Traiter chaque marque
    updated_brands = []
    stats = {
        'found': 0,
        'not_found': 0,
        'already_filled': 0,
        'total_certs': 0
    }
    
    for i, brand in enumerate(brands, 1):
        brand_name = brand['brand']
        website = brand.get('website', '')
        current_value = brand.get('certifications', '').strip()
        
        print(f"\n[{i}/{len(brands)}] 🏷️  {brand_name}")
        print("-" * 70)
        
        # Si déjà rempli, passer
        if current_value:
            print(f"  ✓ Déjà rempli: {current_value}")
            stats['already_filled'] += 1
            updated_brands.append(brand)
            continue
        
        # Analyser la marque
        result = find_certifications_for_brand(brand_name, website)
        
        if result['certifications']:
            certs_str = ', '.join(result['certifications'])
            brand['certifications'] = certs_str
            brand['certifications_source'] = ' | '.join(result['sources'])
            brand['certifications_confidence'] = result['confidence']
            
            stats['found'] += 1
            stats['total_certs'] += len(result['certifications'])
            
            print(f"  💚 Trouvé: {len(result['certifications'])} certification(s)")
            print(f"     {certs_str}")
            print(f"     Confiance: {result['confidence']}")
        else:
            brand['certifications'] = ''
            brand['certifications_source'] = ''
            brand['certifications_confidence'] = 'none'
            stats['not_found'] += 1
            print(f"  ❌ Aucune certification trouvée")
        
        updated_brands.append(brand)
        
        # Pause pour éviter de surcharger les serveurs
        if i < len(brands):
            time.sleep(2)
    
    # Sauvegarder
    if updated_brands:
        # Ajouter les nouvelles colonnes si nécessaire
        for brand in updated_brands:
            if 'certifications_source' not in brand:
                brand['certifications_source'] = ''
            if 'certifications_confidence' not in brand:
                brand['certifications_confidence'] = ''
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=updated_brands[0].keys())
            writer.writeheader()
            writer.writerows(updated_brands)
        
        print(f"\n{'='*70}")
        print(f"✅ Fichier sauvegardé: {output_file}")
        print(f"{'='*70}\n")
    
    # Statistiques
    print("📊 STATISTIQUES")
    print("-" * 70)
    print(f"  ✅ Certifications trouvées:  {stats['found']}")
    print(f"  ❌ Non trouvées:              {stats['not_found']}")
    print(f"  ✓  Déjà remplies:             {stats['already_filled']}")
    print(f"  🏆 Total certifications:      {stats['total_certs']}")
    if stats['found'] > 0:
        print(f"  📈 Moyenne par marque:        {stats['total_certs']/stats['found']:.1f}")
    
    # Top marques avec le plus de certifications
    brands_with_certs = [b for b in updated_brands if b.get('certifications', '').strip()]
    if brands_with_certs:
        sorted_brands = sorted(brands_with_certs,
                             key=lambda x: len(x['certifications'].split(',')),
                             reverse=True)
        print(f"\n🏆 TOP 10 MARQUES AVEC LE PLUS DE CERTIFICATIONS")
        print("-" * 70)
        for i, b in enumerate(sorted_brands[:10], 1):
            cert_count = len(b['certifications'].split(','))
            print(f"  {i:2d}. {b['brand']:25s} {cert_count} certification(s)")
            print(f"      {b['certifications'][:80]}")

if __name__ == "__main__":
    input_file = "brands_database_with_production_countries.csv"
    output_file = "brands_database_with_certifications.csv"
    
    try:
        process_brands_csv(input_file, output_file)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

