#!/usr/bin/env python3
"""
Version avancée du Brand Scraper avec support CSV et alias
"""

import requests
import argparse
import sys
import json
import pandas as pd
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Set, Dict, Optional
import time
import random

class AdvancedBrandScraper:
    def __init__(self, brands_file: str = None, user_agent: str = None):
        """Initialise le scraper avec support CSV et alias."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Charger les marques depuis le fichier CSV ou utiliser la liste par défaut
        self.brands_data = self._load_brands_from_csv(brands_file) if brands_file else self._load_default_brands()
        self.brands = self._extract_all_brands()
    
    def _load_brands_from_csv(self, filename: str) -> Dict:
        """Charge les marques depuis un fichier CSV."""
        try:
            df = pd.read_csv(filename)
            brands_data = {}
            
            for _, row in df.iterrows():
                category = row['category']
                brand = row['brand']
                aliases = row['aliases'].split(',') if pd.notna(row['aliases']) else []
                
                if category not in brands_data:
                    brands_data[category] = {}
                
                brands_data[category][brand] = [alias.strip() for alias in aliases]
            
            print(f"✅ Chargé {len(df)} marques depuis {filename}")
            return brands_data
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement du CSV: {e}")
            print("🔄 Utilisation de la liste par défaut...")
            return self._load_default_brands()
    
    def _load_default_brands(self) -> Dict:
        """Charge la liste par défaut des marques."""
        return {
            'Mode': {
                'nike': ['nike air', 'air jordan'],
                'adidas': ['adidas originals', 'adidas performance'],
                'puma': ['puma sport'],
                'reebok': ['reebok classic'],
                'converse': ['converse all star'],
                'vans': ['vans old skool'],
                'timberland': ['timberland boots'],
                'levis': ['levi\'s', 'levis'],
                'zara': ['zara home'],
                'h&m': ['h&m home'],
                'uniqlo': ['uniqlo japan'],
                'gap': ['gap kids'],
                'tommy hilfiger': ['tommy'],
                'calvin klein': ['ck', 'calvin klein underwear'],
                'ralph lauren': ['polo ralph lauren'],
                'lacoste': ['lacoste sport'],
                'polo': ['polo ralph lauren'],
                'guess': ['guess jeans'],
                'diesel': ['diesel jeans'],
                'benetton': ['benetton group']
            },
            'Électronique': {
                'apple': ['apple inc', 'iphone', 'macbook', 'ipad'],
                'samsung': ['samsung electronics', 'galaxy'],
                'sony': ['sony corporation'],
                'lg': ['lg electronics'],
                'panasonic': ['panasonic corporation'],
                'philips': ['philips lighting'],
                'sharp': ['sharp corporation'],
                'canon': ['canon inc'],
                'nikon': ['nikon corporation'],
                'fujifilm': ['fuji film'],
                'gopro': ['gopro hero'],
                'dji': ['dji drones'],
                'microsoft': ['ms', 'msft'],
                'dell': ['dell technologies'],
                'hp': ['hewlett packard'],
                'lenovo': ['lenovo group'],
                'asus': ['asus computer'],
                'acer': ['acer inc'],
                'toshiba': ['toshiba corporation'],
                'intel': ['intel corporation'],
                'amd': ['advanced micro devices'],
                'nvidia': ['nvidia corporation']
            },
            'Automobile': {
                'bmw': ['bayerische motoren werke'],
                'mercedes': ['mercedes-benz', 'benz'],
                'audi': ['audi ag'],
                'volkswagen': ['vw', 'volkswagen group'],
                'porsche': ['porsche ag'],
                'ferrari': ['ferrari nv'],
                'lamborghini': ['lamborghini automobili'],
                'toyota': ['toyota motor'],
                'honda': ['honda motor'],
                'nissan': ['nissan motor'],
                'mazda': ['mazda motor'],
                'subaru': ['subaru corporation'],
                'ford': ['ford motor'],
                'chevrolet': ['chevrolet motors'],
                'cadillac': ['cadillac motor'],
                'buick': ['buick motor'],
                'chrysler': ['chrysler group'],
                'dodge': ['dodge motor'],
                'jeep': ['jeep brand'],
                'fiat': ['fiat chrysler'],
                'alfa romeo': ['alfa romeo automobiles']
            }
        }
    
    def _extract_all_brands(self) -> Set[str]:
        """Extrait toutes les marques et alias en un seul set."""
        all_brands = set()
        
        for category, brands in self.brands_data.items():
            for brand, aliases in brands.items():
                all_brands.add(brand.lower())
                all_brands.update([alias.lower() for alias in aliases])
        
        return all_brands
    
    def scrape_page(self, url: str, delay: float = 1.0) -> Optional[BeautifulSoup]:
        """Scrape une page web et retourne l'objet BeautifulSoup."""
        try:
            print(f"🔍 Scraping de l'URL: {url}")
            
            # Délai pour être respectueux
            if delay > 0:
                time.sleep(delay + random.uniform(0, 0.5))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"✅ Page chargée avec succès ({len(response.content)} bytes)")
            return soup
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors du scraping: {e}")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return None
    
    def extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extrait tout le texte visible de la page."""
        # Supprimer les scripts et styles
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Extraire le texte
        text = soup.get_text()
        
        # Nettoyer le texte
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text.lower()
    
    def find_brands_in_text(self, text: str) -> Dict[str, List[str]]:
        """Trouve les marques présentes dans le texte avec catégorisation."""
        found_brands = {}
        
        for category, brands in self.brands_data.items():
            category_brands = []
            for brand, aliases in brands.items():
                # Recherche insensible à la casse
                if brand.lower() in text or any(alias.lower() in text for alias in aliases):
                    category_brands.append(brand)
            
            if category_brands:
                found_brands[category] = category_brands
        
        return found_brands
    
    def extract_brands_from_links(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extrait les marques depuis les liens et attributs avec catégorisation."""
        found_brands = {}
        
        # Chercher dans les liens
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            for category, brands in self.brands_data.items():
                for brand, aliases in brands.items():
                    if (brand.lower() in href or brand.lower() in text or 
                        any(alias.lower() in href or alias.lower() in text for alias in aliases)):
                        
                        if category not in found_brands:
                            found_brands[category] = []
                        if brand not in found_brands[category]:
                            found_brands[category].append(brand)
        
        # Chercher dans les attributs data-*
        for element in soup.find_all(attrs={"data-brand": True}):
            brand_attr = element.get('data-brand', '').lower()
            
            for category, brands in self.brands_data.items():
                for brand, aliases in brands.items():
                    if (brand.lower() in brand_attr or 
                        any(alias.lower() in brand_attr for alias in aliases)):
                        
                        if category not in found_brands:
                            found_brands[category] = []
                        if brand not in found_brands[category]:
                            found_brands[category].append(brand)
        
        return found_brands
    
    def extract_brands_from_images(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extrait les marques depuis les attributs alt des images avec catégorisation."""
        found_brands = {}
        
        for img in soup.find_all('img'):
            alt_text = img.get('alt', '').lower()
            title_text = img.get('title', '').lower()
            
            for category, brands in self.brands_data.items():
                for brand, aliases in brands.items():
                    if (brand.lower() in alt_text or brand.lower() in title_text or
                        any(alias.lower() in alt_text or alias.lower() in title_text for alias in aliases)):
                        
                        if category not in found_brands:
                            found_brands[category] = []
                        if brand not in found_brands[category]:
                            found_brands[category].append(brand)
        
        return found_brands
    
    def analyze_page(self, url: str, delay: float = 1.0) -> Dict:
        """Analyse complète d'une page pour trouver les marques avec catégorisation."""
        soup = self.scrape_page(url, delay)
        if not soup:
            return {"error": "Impossible de charger la page"}
        
        # Extraire le texte
        text_content = self.extract_text_content(soup)
        
        # Chercher les marques dans différents endroits
        brands_in_text = self.find_brands_in_text(text_content)
        brands_in_links = self.extract_brands_from_links(soup)
        brands_in_images = self.extract_brands_from_images(soup)
        
        # Combiner tous les résultats par catégorie
        all_brands_by_category = {}
        all_brands_flat = set()
        
        for category_brands in [brands_in_text, brands_in_links, brands_in_images]:
            for category, brands in category_brands.items():
                if category not in all_brands_by_category:
                    all_brands_by_category[category] = []
                
                for brand in brands:
                    if brand not in all_brands_by_category[category]:
                        all_brands_by_category[category].append(brand)
                    all_brands_flat.add(brand)
        
        return {
            "url": url,
            "total_brands_found": len(all_brands_flat),
            "brands_by_category": all_brands_by_category,
            "all_brands": sorted(list(all_brands_flat)),
            "brands_in_text": brands_in_text,
            "brands_in_links": brands_in_links,
            "brands_in_images": brands_in_images,
            "text_length": len(text_content),
            "total_categories": len(all_brands_by_category)
        }

def main():
    parser = argparse.ArgumentParser(
        description="Scraper avancé pour identifier les marques présentes sur un site marchand",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python advanced_brand_scraper.py https://example.com
  python advanced_brand_scraper.py https://example.com --brands brands_database.csv
  python advanced_brand_scraper.py https://example.com --output results.json --verbose
        """
    )
    
    parser.add_argument('url', help='URL du site à analyser')
    parser.add_argument('--brands', help='Fichier CSV contenant la base de données des marques')
    parser.add_argument('--delay', type=float, default=1.0, 
                       help='Délai entre les requêtes (défaut: 1.0s)')
    parser.add_argument('--output', help='Fichier de sortie pour les résultats JSON')
    parser.add_argument('--user-agent', help='User-Agent personnalisé')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Mode verbeux')
    
    args = parser.parse_args()
    
    # Validation de l'URL
    if not args.url.startswith(('http://', 'https://')):
        print("❌ Erreur: L'URL doit commencer par http:// ou https://")
        sys.exit(1)
    
    print("🚀 Démarrage du scraper avancé de marques...")
    print(f"📊 URL cible: {args.url}")
    print(f"⏱️  Délai: {args.delay}s")
    if args.brands:
        print(f"📋 Base de données: {args.brands}")
    
    # Créer le scraper
    scraper = AdvancedBrandScraper(brands_file=args.brands, user_agent=args.user_agent)
    
    # Analyser la page
    results = scraper.analyze_page(args.url, args.delay)
    
    if "error" in results:
        print(f"❌ {results['error']}")
        sys.exit(1)
    
    # Afficher les résultats
    print("\n" + "="*60)
    print("📈 RÉSULTATS DE L'ANALYSE AVANCÉE")
    print("="*60)
    print(f"🌐 URL analysée: {results['url']}")
    print(f"📊 Nombre total de marques trouvées: {results['total_brands_found']}")
    print(f"📁 Nombre de catégories: {results['total_categories']}")
    print(f"📝 Taille du texte analysé: {results['text_length']:,} caractères")
    
    if results['brands_by_category']:
        print(f"\n🏷️  Marques par catégorie:")
        for category, brands in results['brands_by_category'].items():
            print(f"  📂 {category} ({len(brands)} marques):")
            for brand in brands:
                print(f"    • {brand}")
        
        if args.verbose:
            print(f"\n📋 Détail par source:")
            for source_name, source_data in [
                ("Texte", results['brands_in_text']),
                ("Liens", results['brands_in_links']),
                ("Images", results['brands_in_images'])
            ]:
                if source_data:
                    print(f"  {source_name}:")
                    for category, brands in source_data.items():
                        print(f"    {category}: {', '.join(brands)}")
    else:
        print("\n❌ Aucune marque identifiée sur cette page.")
        print("💡 Suggestions:")
        print("  - Vérifiez que l'URL est correcte")
        print("  - Essayez une page produit ou catégorie")
        print("  - La base de données des marques peut être étendue")
    
    # Sauvegarder les résultats si demandé
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Résultats sauvegardés dans: {args.output}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    print("\n✅ Analyse terminée!")

if __name__ == "__main__":
    main() 