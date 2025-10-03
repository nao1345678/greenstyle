#!/usr/bin/env python3
"""
Script pour vérifier et corriger les URLs des logos des marques
"""

import requests
import csv
import re
from urllib.parse import urljoin, urlparse
import time

def find_logo_on_website(website_url, brand_name):
    """
    Tente de trouver le logo sur le site web officiel
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(website_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Recherche de patterns de logos communs
        logo_patterns = [
            r'<img[^>]*src=["\']([^"\']*logo[^"\']*)["\'][^>]*>',
            r'<img[^>]*src=["\']([^"\']*brand[^"\']*)["\'][^>]*>',
            r'<img[^>]*src=["\']([^"\']*header[^"\']*)["\'][^>]*>',
            r'<img[^>]*alt=["\'][^"\']*logo[^"\']*["\'][^>]*src=["\']([^"\']*)["\'][^>]*>',
        ]
        
        content = response.text.lower()
        
        for pattern in logo_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Convertir en URL absolue
                logo_url = urljoin(website_url, match)
                # Vérifier que c'est une image
                if any(ext in logo_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']):
                    return logo_url
        
        # Recherche dans les CSS pour les logos en background
        css_pattern = r'background-image:\s*url\(["\']?([^"\']*logo[^"\']*)["\']?\)'
        css_matches = re.findall(css_pattern, content, re.IGNORECASE)
        for match in css_matches:
            logo_url = urljoin(website_url, match)
            if any(ext in logo_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']):
                return logo_url
                
    except Exception as e:
        print(f"Erreur lors de la recherche sur {website_url}: {e}")
    
    return None

def verify_logo_url(logo_url):
    """
    Vérifie si une URL de logo est accessible
    """
    if not logo_url or logo_url == '':
        return False, "URL vide"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.head(logo_url, headers=headers, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            if 'image' in content_type:
                return True, "OK"
            else:
                return False, f"Mauvais type de contenu: {content_type}"
        else:
            return False, f"Code HTTP: {response.status_code}"
            
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def process_brands_csv(csv_file):
    """
    Traite le fichier CSV des marques
    """
    updated_brands = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        brands = list(reader)
    
    for i, brand in enumerate(brands):
        brand_name = brand['brand']
        website = brand.get('website', '')
        current_logo = brand.get('logo', '')
        
        print(f"\n[{i+1}/{len(brands)}] Traitement de {brand_name}")
        
        # Vérifier l'URL actuelle du logo
        if current_logo:
            is_valid, message = verify_logo_url(current_logo)
            print(f"  Logo actuel: {is_valid} - {message}")
            
            if is_valid:
                updated_brands.append(brand)
                continue
        
        # Essayer de trouver un nouveau logo
        if website:
            print(f"  Recherche du logo sur {website}")
            new_logo = find_logo_on_website(website, brand_name)
            
            if new_logo:
                is_valid, message = verify_logo_url(new_logo)
                print(f"  Nouveau logo trouvé: {new_logo} - {is_valid} - {message}")
                
                if is_valid:
                    brand['logo'] = new_logo
                else:
                    brand['logo'] = ''  # Vider si invalide
            else:
                print(f"  Aucun logo trouvé sur le site")
                brand['logo'] = ''  # Vider si non trouvé
        else:
            print(f"  Pas de site web, logo vidé")
            brand['logo'] = ''
        
        updated_brands.append(brand)
        
        # Pause pour éviter de surcharger les serveurs
        time.sleep(1)
    
    return updated_brands

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
    output_file = "brands_database_fixed_verified.csv"
    
    print("=== Vérification des URLs des logos ===")
    print(f"Fichier d'entrée: {input_file}")
    print(f"Fichier de sortie: {output_file}")
    
    try:
        updated_brands = process_brands_csv(input_file)
        save_updated_csv(updated_brands, output_file)
        
        print(f"\n=== Résumé ===")
        print(f"Total des marques traitées: {len(updated_brands)}")
        
        # Statistiques
        with_logo = sum(1 for brand in updated_brands if brand.get('logo', '').strip())
        without_logo = len(updated_brands) - with_logo
        
        print(f"Marques avec logo: {with_logo}")
        print(f"Marques sans logo: {without_logo}")
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
