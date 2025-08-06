#!/usr/bin/env python3
"""
Utilitaires pour le projet de détection de marques
"""

import re
import json
import csv
import logging
from pathlib import Path
from typing import Set, List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import hashlib
import time
from datetime import datetime

def setup_logging(name: str = "brand_detector", level: str = "INFO") -> logging.Logger:
    """Configure le logging pour le projet."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Éviter les doublons
        logger.setLevel(getattr(logging, level.upper()))
        
        # Handler pour la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

def clean_text(text: str) -> str:
    """Nettoie le texte en supprimant les caractères spéciaux et normalisant l'espacement."""
    if not text:
        return ""
    
    # Supprimer les caractères spéciaux et normaliser
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def extract_domain(url: str) -> str:
    """Extrait le domaine d'une URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ""

def is_valid_url(url: str) -> bool:
    """Vérifie si une URL est valide."""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

def normalize_brand_name(brand: str) -> str:
    """Normalise le nom d'une marque pour la comparaison."""
    if not brand:
        return ""
    
    # Nettoyer et normaliser
    brand = clean_text(brand)
    
    # Supprimer les mots communs
    common_words = {'the', 'and', 'or', 'of', 'for', 'with', 'by', 'in', 'on', 'at', 'to'}
    words = brand.split()
    words = [w for w in words if w not in common_words and len(w) > 1]
    
    return ' '.join(words)

def calculate_similarity(str1: str, str2: str) -> float:
    """Calcule la similarité entre deux chaînes (algorithme de Levenshtein simplifié)."""
    if not str1 or not str2:
        return 0.0
    
    str1, str2 = str1.lower(), str2.lower()
    
    # Calcul simple basé sur la longueur de la plus longue sous-chaîne commune
    def longest_common_substring(s1, s2):
        m = [[0] * (1 + len(s2)) for _ in range(1 + len(s1))]
        longest = 0
        for x in range(len(s1)):
            for y in range(len(s2)):
                if s1[x] == s2[y]:
                    m[x + 1][y + 1] = m[x][y] + 1
                    longest = max(longest, m[x + 1][y + 1])
        return longest
    
    lcs = longest_common_substring(str1, str2)
    max_len = max(len(str1), len(str2))
    
    return lcs / max_len if max_len > 0 else 0.0

def load_brands_from_csv(file_path: str) -> Set[str]:
    """Charge les marques depuis un fichier CSV."""
    brands = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Chercher une colonne 'brand' ou 'name' ou la première colonne
                brand = row.get('brand') or row.get('name') or list(row.values())[0]
                if brand and len(brand.strip()) > 1:
                    brands.add(brand.strip().lower())
    except Exception as e:
        print(f"Erreur lors du chargement du CSV: {e}")
    
    return brands

def save_results_to_json(results: Dict[str, Any], file_path: str) -> bool:
    """Sauvegarde les résultats au format JSON."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde JSON: {e}")
        return False

def save_results_to_csv(results: Dict[str, Any], file_path: str) -> bool:
    """Sauvegarde les résultats au format CSV."""
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # En-têtes
            writer.writerow(['URL', 'Total_Brands', 'Brands_Found', 'Timestamp'])
            
            # Données
            brands_str = ', '.join(results.get('brands', []))
            writer.writerow([
                results.get('url', ''),
                results.get('total_brands_found', 0),
                brands_str,
                datetime.now().isoformat()
            ])
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde CSV: {e}")
        return False

def generate_cache_key(url: str, brands: Set[str]) -> str:
    """Génère une clé de cache unique pour une URL et un ensemble de marques."""
    content = f"{url}:{sorted(brands)}"
    return hashlib.md5(content.encode()).hexdigest()

def create_cache_directory() -> Path:
    """Crée le répertoire de cache s'il n'existe pas."""
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def get_file_extension(file_path: str) -> str:
    """Récupère l'extension d'un fichier."""
    return Path(file_path).suffix.lower()

def is_image_url(url: str) -> bool:
    """Vérifie si une URL pointe vers une image."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    return any(path.endswith(ext) for ext in image_extensions)

def extract_meta_info(soup) -> Dict[str, str]:
    """Extrait les informations meta d'une page."""
    meta_info = {}
    
    # Meta tags
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        name = tag.get('name', tag.get('property', ''))
        content = tag.get('content', '')
        if name and content:
            meta_info[name] = content
    
    # Title
    title_tag = soup.find('title')
    if title_tag:
        meta_info['title'] = title_tag.get_text(strip=True)
    
    # Description
    if 'description' not in meta_info:
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            meta_info['description'] = desc_tag.get('content', '')
    
    return meta_info

def format_duration(seconds: float) -> str:
    """Formate une durée en secondes en format lisible."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def print_progress(current: int, total: int, prefix: str = "Progression") -> None:
    """Affiche une barre de progression."""
    percentage = (current / total) * 100 if total > 0 else 0
    bar_length = 30
    filled_length = int(bar_length * current // total)
    
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r{prefix}: |{bar}| {percentage:.1f}% ({current}/{total})', end='')
    
    if current == total:
        print()  # Nouvelle ligne à la fin

def validate_brand_name(brand: str, min_length: int = 2) -> bool:
    """Valide un nom de marque."""
    if not brand or len(brand.strip()) < min_length:
        return False
    
    # Vérifier qu'il ne contient pas que des chiffres
    if brand.isdigit():
        return False
    
    # Vérifier qu'il contient au moins une lettre
    if not any(c.isalpha() for c in brand):
        return False
    
    return True

def merge_brand_sets(*brand_sets: Set[str]) -> Set[str]:
    """Fusionne plusieurs ensembles de marques en supprimant les doublons."""
    merged = set()
    for brand_set in brand_sets:
        merged.update(brand_set)
    return merged

if __name__ == "__main__":
    # Tests des utilitaires
    print("🧪 Tests des utilitaires...")
    
    # Test de nettoyage de texte
    test_text = "Nike® & Adidas™ - Test!@#$%"
    cleaned = clean_text(test_text)
    print(f"Texte original: {test_text}")
    print(f"Texte nettoyé: {cleaned}")
    
    # Test de validation d'URL
    test_urls = [
        "https://example.com",
        "http://invalid",
        "not-a-url"
    ]
    
    for url in test_urls:
        print(f"URL '{url}' valide: {is_valid_url(url)}")
    
    # Test de similarité
    brand1, brand2 = "Nike", "Nikee"
    similarity = calculate_similarity(brand1, brand2)
    print(f"Similarité entre '{brand1}' et '{brand2}': {similarity:.2f}")
    
    print("✅ Tests terminés!")
