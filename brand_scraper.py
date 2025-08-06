#!/usr/bin/env python3
"""
Script CLI pour scraper les marques présentes sur un site marchand.
Usage: python brand_scraper.py <URL> [options]
"""

import requests
import argparse
import sys
import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Set, Dict, Optional
import time
import random

class BrandScraper:
    def __init__(self, user_agent: str = None):
        """Initialise le scraper avec un user-agent personnalisé."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Liste de marques connues (peut être étendue)
        self.brands = self._load_brands()
    
    def _load_brands(self) -> Set[str]:
        """Charge la liste des marques connues."""
        # Liste basique de marques populaires (à étendre selon vos besoins)
        brands = {
            # Mode
            'nike', 'adidas', 'puma', 'reebok', 'converse', 'vans', 'timberland',
            'levis', 'zara', 'h&m', 'uniqlo', 'gap', 'tommy hilfiger', 'calvin klein',
            'ralph lauren', 'lacoste', 'polo', 'guess', 'diesel', 'benetton',
            
            # Électronique
            'apple', 'samsung', 'sony', 'lg', 'panasonic', 'philips', 'sharp',
            'canon', 'nikon', 'fujifilm', 'gopro', 'dji', 'microsoft', 'dell',
            'hp', 'lenovo', 'asus', 'acer', 'toshiba', 'intel', 'amd', 'nvidia',
            
            # Automobile
            'bmw', 'mercedes', 'audi', 'volkswagen', 'porsche', 'ferrari', 'lamborghini',
            'toyota', 'honda', 'nissan', 'mazda', 'subaru', 'ford', 'chevrolet',
            'cadillac', 'buick', 'chrysler', 'dodge', 'jeep', 'fiat', 'alfa romeo',
            
            # Cosmétiques
            'loreal', 'maybelline', 'revlon', 'mac', 'clinique', 'estee lauder',
            'chanel', 'dior', 'ysl', 'guerlain', 'lancome', 'clarins', 'biotherm',
            
            # Alimentation
            'coca-cola', 'pepsi', 'nestle', 'danone', 'kellogg', 'kraft', 'heinz',
            'unilever', 'p&g', 'colgate', 'oral-b', 'gillette', 'pampers',
            
            # Sport
            'wilson', 'head', 'babolat', 'yonex', 'prince', 'dunlop', 'slazenger',
            
            # Luxe
            'louis vuitton', 'gucci', 'prada', 'hermes', 'cartier', 'rolex', 'omega',
            'swatch', 'casio', 'seiko', 'citizen', 'timex', 'fossil'
        }
        return brands
    
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
    
    def find_brands_in_text(self, text: str) -> Set[str]:
        """Trouve les marques présentes dans le texte."""
        found_brands = set()
        
        for brand in self.brands:
            # Recherche insensible à la casse
            if brand.lower() in text:
                found_brands.add(brand)
        
        return found_brands
    
    def extract_brands_from_links(self, soup: BeautifulSoup) -> Set[str]:
        """Extrait les marques depuis les liens et attributs."""
        found_brands = set()
        
        # Chercher dans les liens
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            for brand in self.brands:
                if brand in href or brand in text:
                    found_brands.add(brand)
        
        # Chercher dans les attributs data-*
        for element in soup.find_all(attrs={"data-brand": True}):
            brand_attr = element.get('data-brand', '').lower()
            for brand in self.brands:
                if brand in brand_attr:
                    found_brands.add(brand)
        
        return found_brands
    
    def extract_brands_from_images(self, soup: BeautifulSoup) -> Set[str]:
        """Extrait les marques depuis les attributs alt des images."""
        found_brands = set()
        
        for img in soup.find_all('img'):
            alt_text = img.get('alt', '').lower()
            title_text = img.get('title', '').lower()
            
            for brand in self.brands:
                if brand in alt_text or brand in title_text:
                    found_brands.add(brand)
        
        return found_brands
    
    def analyze_page(self, url: str, delay: float = 1.0) -> Dict:
        """Analyse complète d'une page pour trouver les marques."""
        soup = self.scrape_page(url, delay)
        if not soup:
            return {"error": "Impossible de charger la page"}
        
        # Extraire le texte
        text_content = self.extract_text_content(soup)
        
        # Chercher les marques dans différents endroits
        brands_in_text = self.find_brands_in_text(text_content)
        brands_in_links = self.extract_brands_from_links(soup)
        brands_in_images = self.extract_brands_from_images(soup)
        
        # Combiner tous les résultats
        all_brands = brands_in_text | brands_in_links | brands_in_images
        
        return {
            "url": url,
            "total_brands_found": len(all_brands),
            "brands": sorted(list(all_brands)),
            "brands_in_text": sorted(list(brands_in_text)),
            "brands_in_links": sorted(list(brands_in_links)),
            "brands_in_images": sorted(list(brands_in_images)),
            "text_length": len(text_content)
        }

def main():
    parser = argparse.ArgumentParser(
        description="Scraper pour identifier les marques présentes sur un site marchand",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python brand_scraper.py https://example.com
  python brand_scraper.py https://example.com --delay 2.0
  python brand_scraper.py https://example.com --output results.json
        """
    )
    
    parser.add_argument('url', help='URL du site à analyser')
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
    
    print("🚀 Démarrage du scraper de marques...")
    print(f"📊 URL cible: {args.url}")
    print(f"⏱️  Délai: {args.delay}s")
    
    # Créer le scraper
    scraper = BrandScraper(user_agent=args.user_agent)
    
    # Analyser la page
    results = scraper.analyze_page(args.url, args.delay)
    
    if "error" in results:
        print(f"❌ {results['error']}")
        sys.exit(1)
    
    # Afficher les résultats
    print("\n" + "="*50)
    print("📈 RÉSULTATS DE L'ANALYSE")
    print("="*50)
    print(f"🌐 URL analysée: {results['url']}")
    print(f"📊 Nombre total de marques trouvées: {results['total_brands_found']}")
    print(f"📝 Taille du texte analysé: {results['text_length']:,} caractères")
    
    if results['brands']:
        print(f"\n🏷️  Marques identifiées ({len(results['brands'])}):")
        for i, brand in enumerate(results['brands'], 1):
            print(f"  {i:2d}. {brand}")
        
        if args.verbose:
            print(f"\n📋 Détail par source:")
            print(f"  Texte: {len(results['brands_in_text'])} marques")
            print(f"  Liens: {len(results['brands_in_links'])} marques")
            print(f"  Images: {len(results['brands_in_images'])} marques")
    else:
        print("\n❌ Aucune marque identifiée sur cette page.")
        print("💡 Suggestions:")
        print("  - Vérifiez que l'URL est correcte")
        print("  - Essayez une page produit ou catégorie")
        print("  - La liste des marques peut être étendue")
    
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