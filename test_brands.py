#!/usr/bin/env python3
"""
Script de test pour démontrer l'utilisation du Brand Scraper
"""

from brand_scraper import BrandScraper
import json

def test_basic_functionality():
    """Test basique du scraper."""
    print("🧪 Test basique du scraper de marques")
    print("="*40)
    
    scraper = BrandScraper()
    
    # Test avec une page simple
    test_url = "https://httpbin.org/html"
    print(f"Test URL: {test_url}")
    
    results = scraper.analyze_page(test_url, delay=0.5)
    
    if "error" not in results:
        print(f"✅ Test réussi! Marques trouvées: {results['total_brands_found']}")
        if results['brands']:
            print(f"Marques: {', '.join(results['brands'])}")
    else:
        print(f"❌ Test échoué: {results['error']}")

def test_custom_brands():
    """Test avec des marques personnalisées."""
    print("\n🧪 Test avec marques personnalisées")
    print("="*40)
    
    class CustomScraper(BrandScraper):
        def _load_brands(self):
            return {
                'test_brand_1', 'test_brand_2', 'example_brand',
                'demo_brand', 'sample_brand', 'head'  # head existe dans httpbin
            }
    
    scraper = CustomScraper()
    
    # Test avec la même URL
    test_url = "https://httpbin.org/html"
    results = scraper.analyze_page(test_url, delay=0.5)
    
    if "error" not in results:
        print(f"✅ Test personnalisé réussi! Marques trouvées: {results['total_brands_found']}")
        if results['brands']:
            print(f"Marques: {', '.join(results['brands'])}")
    else:
        print(f"❌ Test échoué: {results['error']}")

def test_error_handling():
    """Test de gestion d'erreurs."""
    print("\n🧪 Test de gestion d'erreurs")
    print("="*40)
    
    scraper = BrandScraper()
    
    # Test avec une URL invalide
    invalid_url = "https://invalid-domain-that-does-not-exist-12345.com"
    print(f"Test URL invalide: {invalid_url}")
    
    results = scraper.analyze_page(invalid_url, delay=0.1)
    
    if "error" in results:
        print(f"✅ Gestion d'erreur correcte: {results['error']}")
    else:
        print("❌ Erreur: L'erreur n'a pas été détectée")

def test_verbose_mode():
    """Test du mode verbeux."""
    print("\n🧪 Test du mode verbeux")
    print("="*40)
    
    scraper = BrandScraper()
    
    # Créer une page HTML de test avec des marques
    test_html = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Test de marques</h1>
        <p>Cette page contient des références à Nike et Adidas.</p>
        <a href="/nike-shoes">Nike Shoes</a>
        <img alt="Adidas logo" src="/adidas.jpg">
        <div data-brand="apple">Apple Products</div>
    </body>
    </html>
    """
    
    # Simuler une réponse
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(test_html, 'html.parser')
    
    # Extraire le texte
    text_content = scraper.extract_text_content(soup)
    
    # Analyser
    brands_in_text = scraper.find_brands_in_text(text_content)
    brands_in_links = scraper.extract_brands_from_links(soup)
    brands_in_images = scraper.extract_brands_from_images(soup)
    
    print(f"📝 Texte extrait: {len(text_content)} caractères")
    print(f"🏷️  Marques dans le texte: {brands_in_text}")
    print(f"🔗 Marques dans les liens: {brands_in_links}")
    print(f"🖼️  Marques dans les images: {brands_in_images}")
    
    all_brands = brands_in_text | brands_in_links | brands_in_images
    print(f"📊 Total marques trouvées: {len(all_brands)}")
    print(f"📋 Toutes les marques: {all_brands}")

def main():
    """Exécute tous les tests."""
    print("🚀 Démarrage des tests du Brand Scraper")
    print("="*50)
    
    # Test 1: Fonctionnalité basique
    test_basic_functionality()
    
    # Test 2: Marques personnalisées
    test_custom_brands()
    
    # Test 3: Gestion d'erreurs
    test_error_handling()
    
    # Test 4: Mode verbeux
    test_verbose_mode()
    
    print("\n✅ Tous les tests terminés!")

if __name__ == "__main__":
    main() 