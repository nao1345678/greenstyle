#!/usr/bin/env python3
"""
Script pour collecter les données de pays de production des marques de mode
"""

import requests
import csv
import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def find_sustainability_page(website_url, brand_name):
    """
    Trouve la page de durabilité sur le site officiel
    """
    if not website_url:
        return None
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(website_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Recherche de liens vers les pages de durabilité
        sustainability_keywords = [
            'sustainability', 'sustainable', 'responsibility', 'environmental',
            'durabilité', 'responsabilité', 'environnement', 'impact',
            'supply-chain', 'suppliers', 'manufacturing', 'production',
            'chaîne', 'fournisseurs', 'fabrication', 'production'
        ]
        
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            for keyword in sustainability_keywords:
                if keyword in href or keyword in text:
                    # Convertir en URL absolue
                    sustainability_url = urljoin(website_url, link['href'])
                    return sustainability_url
        
        return None
        
    except Exception as e:
        print(f"Erreur lors de la recherche de page durabilité sur {website_url}: {e}")
        return None

def extract_production_countries(sustainability_url, brand_name):
    """
    Extrait les pays de production depuis la page de durabilité
    """
    if not sustainability_url:
        return None
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(sustainability_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        content = response.text.lower()
        
        # Liste des pays de production courants dans la mode
        common_countries = [
            'china', 'bangladesh', 'vietnam', 'india', 'turkey', 'indonesia',
            'cambodia', 'myanmar', 'pakistan', 'sri lanka', 'thailand',
            'philippines', 'mexico', 'guatemala', 'honduras', 'el salvador',
            'morocco', 'tunisia', 'ethiopia', 'madagascar', 'lesotho',
            'italy', 'portugal', 'spain', 'france', 'germany', 'poland',
            'romania', 'bulgaria', 'ukraine', 'usa', 'canada', 'peru',
            'brazil', 'argentina', 'colombia', 'japan', 'south korea',
            'taiwan', 'hong kong', 'singapore', 'malaysia'
        ]
        
        found_countries = []
        
        # Recherche de patterns mentionnant les pays de production
        patterns = [
            r'(?:manufactured|produced|made|sourced)\s*(?:in|from)\s*([^,\.]+)',
            r'(?:production|manufacturing)\s*(?:in|at|located in)\s*([^,\.]+)',
            r'(?:suppliers|factories|facilities)\s*(?:in|located in)\s*([^,\.]+)',
            r'(?:we work with|we partner with|our partners in)\s*([^,\.]+)',
            r'(?:countries|regions)\s*(?:include|are|:)\s*([^,\.]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Nettoyer le match
                country_text = match.strip()
                
                # Vérifier si c'est un pays connu
                for country in common_countries:
                    if country in country_text.lower():
                        if country not in found_countries:
                            found_countries.append(country.title())
        
        # Recherche directe des noms de pays dans le contenu
        for country in common_countries:
            if country in content:
                if country.title() not in found_countries:
                    found_countries.append(country.title())
        
        if found_countries:
            return ', '.join(found_countries[:5])  # Limiter à 5 pays max
        
        return None
        
    except Exception as e:
        print(f"Erreur lors de l'extraction sur {sustainability_url}: {e}")
        return None

def get_production_countries_from_database(brand_name):
    """
    Données prédéfinies pour les marques principales (basées sur des rapports publics)
    """
    database = {
        # Marques sportswear
        'Nike': 'China,Vietnam,Indonesia',
        'Adidas': 'China,Vietnam,Indonesia,India',
        'Puma': 'China,Vietnam,Bangladesh',
        'Reebok': 'China,Vietnam,India',
        
        # Fast fashion
        'H&M': 'Bangladesh,China,Vietnam',
        'Zara': 'Spain,Portugal,Morocco,Turkey',
        'Uniqlo': 'China,Vietnam,Bangladesh',
        'Gap': 'China,Vietnam,Bangladesh',
        
        # Marques premium
        'Levi\'s': 'USA,Mexico,Bangladesh',
        'Patagonia': 'USA,Vietnam,Bangladesh',
        'The North Face': 'China,Vietnam,Bangladesh',
        
        # Marques de luxe
        'Stella McCartney': 'Italy,Portugal,Spain',
        'Eileen Fisher': 'USA,Peru,India',
        'Everlane': 'USA,Italy,Japan',
        
        # Marques outdoor
        'Arc\'teryx': 'China,Vietnam,Bangladesh',
        'Columbia': 'China,Vietnam,Bangladesh',
        
        # Marques casual
        'COS': 'Europe,Turkey',
        'Madewell': 'USA,China,Vietnam',
        'Tommy Hilfiger': 'China,Vietnam,Bangladesh',
        'Ralph Lauren': 'USA,Italy,China',
        'Lacoste': 'France,Portugal,Morocco',
        'J.Crew': 'China,Vietnam,Peru',
        'Gant': 'Europe,Turkey',
        'Abercrombie & Fitch': 'China,Vietnam,Bangladesh',
        'Benetton': 'Italy,Turkey,Bangladesh',
        'Scotch & Soda': 'Turkey,China,Vietnam',
    }
    
    return database.get(brand_name)

def is_brand_complete(brand):
    """
    Vérifie si une marque a déjà tous ses critères remplis
    """
    required_fields = [
        'sustainable_materials', 'certifications', 'country_origin', 
        'country_production', 'global_env_impact', 'labor_ethics', 
        'final_score', 'short_description', 'description'
    ]
    
    for field in required_fields:
        value = brand.get(field, '')
        if isinstance(value, (int, float)):
            continue  # Les valeurs numériques sont considérées comme complètes
        if not value or str(value).strip() == '':
            return False
    
    return True

def process_brands_for_production_countries(csv_file):
    """
    Traite le fichier CSV pour ajouter les données de pays de production
    """
    updated_brands = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        brands = list(reader)
    
    # Compter les marques complètes vs incomplètes
    complete_brands = 0
    incomplete_brands = 0
    
    for i, brand in enumerate(brands):
        brand_name = brand['brand']
        website = brand.get('website', '')
        current_production = brand.get('country_production', '')
        
        # Vérifier si la marque est déjà complète
        if is_brand_complete(brand):
            print(f"[{i+1}/{len(brands)}] {brand_name} - COMPLÈTE (ignorée)")
            complete_brands += 1
            updated_brands.append(brand)
            continue
        
        incomplete_brands += 1
        print(f"\n[{i+1}/{len(brands)}] Traitement de {brand_name} - INCOMPLÈTE")
        
        # Vérifier si on a déjà des données de pays de production
        if current_production and current_production.strip():
            print(f"  Déjà des données de production: {current_production}")
            updated_brands.append(brand)
            continue
        
        # Essayer la base de données prédéfinie d'abord
        countries = get_production_countries_from_database(brand_name)
        if countries:
            print(f"  Données trouvées dans la base: {countries}")
            brand['country_production'] = countries
            updated_brands.append(brand)
            continue
        
        # Recherche sur le site web
        if website:
            print(f"  Recherche sur {website}")
            sustainability_url = find_sustainability_page(website, brand_name)
            
            if sustainability_url:
                print(f"  Page durabilité trouvée: {sustainability_url}")
                countries = extract_production_countries(sustainability_url, brand_name)
                
                if countries:
                    print(f"  Pays de production trouvés: {countries}")
                    brand['country_production'] = countries
                else:
                    print(f"  Aucun pays de production trouvé")
                    brand['country_production'] = ''
            else:
                print(f"  Aucune page durabilité trouvée")
                brand['country_production'] = ''
        else:
            print(f"  Pas de site web")
            brand['country_production'] = ''
        
        updated_brands.append(brand)
        
        # Pause pour éviter de surcharger les serveurs
        time.sleep(2)
    
    return updated_brands, complete_brands, incomplete_brands

def save_updated_csv(brands, output_file):
    """
    Sauvegarde le CSV mis à jour
    """
    if not brands:
        print("Aucune marque à sauvegarder")
        return
    
    fieldnames = brands[0].keys()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(brands)
    
    print(f"\nFichier sauvegardé: {output_file}")

if __name__ == "__main__":
    input_file = "brands_database_fixed.csv"
    output_file = "brands_database_with_production_countries.csv"
    
    print("=== Collecte des données de pays de production ===")
    print(f"Fichier d'entrée: {input_file}")
    print(f"Fichier de sortie: {output_file}")
    
    try:
        updated_brands, complete_count, incomplete_count = process_brands_for_production_countries(input_file)
        save_updated_csv(updated_brands, output_file)
        
        print(f"\n=== Résumé ===")
        print(f"Total des marques traitées: {len(updated_brands)}")
        print(f"Marques complètes (ignorées): {complete_count}")
        print(f"Marques incomplètes traitées: {incomplete_count}")
        
        # Statistiques
        with_data = sum(1 for brand in updated_brands if brand.get('country_production', '').strip())
        without_data = len(updated_brands) - with_data
        
        print(f"Marques avec données de pays de production: {with_data}")
        print(f"Marques sans données: {without_data}")
        
        # Afficher quelques exemples
        print(f"\n=== Exemples de données collectées ===")
        for brand in updated_brands[:10]:
            if brand.get('country_production', '').strip():
                print(f"{brand['brand']}: {brand['country_production']}")
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
