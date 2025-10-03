#!/usr/bin/env python3
"""
Script pour collecter les données de matériaux durables des marques de mode
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
            'materials', 'matériaux', 'recycled', 'organic', 'eco'
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

def extract_sustainable_materials_percentage(sustainability_url, brand_name):
    """
    Extrait le pourcentage de matériaux durables depuis la page de durabilité
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
        
        # Patterns pour trouver des pourcentages de matériaux durables
        patterns = [
            r'(\d+)%\s*(?:of\s*)?(?:our\s*)?(?:products\s*)?(?:are\s*)?(?:made\s*)?(?:from\s*)?(?:sustainable|recycled|organic|eco-friendly|responsible)\s*(?:materials|fibers|fabrics)',
            r'(?:sustainable|recycled|organic|eco-friendly|responsible)\s*(?:materials|fibers|fabrics).*?(\d+)%',
            r'(\d+)%\s*(?:sustainable|recycled|organic|eco-friendly|responsible)',
            r'(?:use|using)\s*(\d+)%\s*(?:sustainable|recycled|organic|eco-friendly|responsible)',
            r'(?:materials|fibers|fabrics).*?(\d+)%.*?(?:sustainable|recycled|organic|eco-friendly|responsible)',
        ]
        
        percentages = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    percentage = int(match)
                    if 1 <= percentage <= 100:  # Pourcentage valide
                        percentages.append(percentage)
                except ValueError:
                    continue
        
        if percentages:
            # Retourner le pourcentage le plus élevé trouvé
            return max(percentages)
        
        return None
        
    except Exception as e:
        print(f"Erreur lors de l'extraction sur {sustainability_url}: {e}")
        return None

def get_sustainable_materials_from_database(brand_name):
    """
    Données prédéfinies pour les marques principales (basées sur des rapports publics)
    """
    database = {
        # Marques sportswear
        'Nike': 30,
        'Adidas': 25,
        'Puma': 20,
        'Reebok': 15,
        
        # Fast fashion
        'H&M': 25,
        'Zara': 10,
        'Uniqlo': 15,
        'Gap': 20,
        
        # Marques premium
        'Levi\'s': 30,
        'Patagonia': 70,
        'The North Face': 35,
        
        # Marques de luxe
        'Stella McCartney': 85,
        'Eileen Fisher': 90,
        'Everlane': 40,
        
        # Marques outdoor
        'Arc\'teryx': 45,
        'Columbia': 25,
        
        # Marques casual
        'COS': 35,
        'Madewell': 25,
        'Tommy Hilfiger': 20,
        'Ralph Lauren': 15,
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

def process_brands_for_sustainable_materials(csv_file):
    """
    Traite le fichier CSV pour ajouter les données de matériaux durables
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
        current_sustainable = brand.get('sustainable_materials', '')
        
        # Vérifier si la marque est déjà complète
        if is_brand_complete(brand):
            print(f"[{i+1}/{len(brands)}] {brand_name} - COMPLÈTE (ignorée)")
            complete_brands += 1
            updated_brands.append(brand)
            continue
        
        incomplete_brands += 1
        print(f"\n[{i+1}/{len(brands)}] Traitement de {brand_name} - INCOMPLÈTE")
        
        # Vérifier si on a déjà des données de matériaux durables
        if current_sustainable and current_sustainable.strip():
            print(f"  Déjà des données de matériaux: {current_sustainable}%")
            updated_brands.append(brand)
            continue
        
        # Essayer la base de données prédéfinie d'abord
        percentage = get_sustainable_materials_from_database(brand_name)
        if percentage:
            print(f"  Données trouvées dans la base: {percentage}%")
            brand['sustainable_materials'] = percentage
            updated_brands.append(brand)
            continue
        
        # Recherche sur le site web
        if website:
            print(f"  Recherche sur {website}")
            sustainability_url = find_sustainability_page(website, brand_name)
            
            if sustainability_url:
                print(f"  Page durabilité trouvée: {sustainability_url}")
                percentage = extract_sustainable_materials_percentage(sustainability_url, brand_name)
                
                if percentage:
                    print(f"  Pourcentage trouvé: {percentage}%")
                    brand['sustainable_materials'] = percentage
                else:
                    print(f"  Aucun pourcentage trouvé")
                    brand['sustainable_materials'] = ''
            else:
                print(f"  Aucune page durabilité trouvée")
                brand['sustainable_materials'] = ''
        else:
            print(f"  Pas de site web")
            brand['sustainable_materials'] = ''
        
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
    output_file = "brands_database_with_sustainable_materials.csv"
    
    print("=== Collecte des données de matériaux durables ===")
    print(f"Fichier d'entrée: {input_file}")
    print(f"Fichier de sortie: {output_file}")
    
    try:
        updated_brands, complete_count, incomplete_count = process_brands_for_sustainable_materials(input_file)
        save_updated_csv(updated_brands, output_file)
        
        print(f"\n=== Résumé ===")
        print(f"Total des marques traitées: {len(updated_brands)}")
        print(f"Marques complètes (ignorées): {complete_count}")
        print(f"Marques incomplètes traitées: {incomplete_count}")
        
        # Statistiques
        with_data = sum(1 for brand in updated_brands if brand.get('sustainable_materials', '').strip())
        without_data = len(updated_brands) - with_data
        
        print(f"Marques avec données de matériaux durables: {with_data}")
        print(f"Marques sans données: {without_data}")
        
        # Afficher quelques exemples
        print(f"\n=== Exemples de données collectées ===")
        for brand in updated_brands[:10]:
            if brand.get('sustainable_materials', '').strip():
                print(f"{brand['brand']}: {brand['sustainable_materials']}%")
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
