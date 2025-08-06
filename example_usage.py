#!/usr/bin/env python3
"""
Exemple d'utilisation programmatique du BrandScraper
"""

from brand_scraper import BrandScraper
import json

def example_usage():
    """Exemple d'utilisation du scraper de marques."""
    
    # Créer une instance du scraper
    scraper = BrandScraper()
    
    # Liste d'URLs à analyser
    urls_to_analyze = [
        "https://www.fnac.com/telephonie/telephones-portables",
        "https://www.darty.com/nav/achat/informatique/ordinateur-portable/",
        "https://www.cdiscount.com/telephonie/telephones-portables.html"
    ]
    
    print("🚀 Démarrage de l'analyse de plusieurs sites...")
    print("="*60)
    
    all_results = []
    
    for i, url in enumerate(urls_to_analyze, 1):
        print(f"\n📊 Analyse {i}/{len(urls_to_analyze)}: {url}")
        print("-" * 50)
        
        # Analyser la page
        results = scraper.analyze_page(url, delay=2.0)
        
        if "error" in results:
            print(f"❌ Erreur: {results['error']}")
            continue
        
        # Afficher les résultats
        print(f"✅ Marques trouvées: {results['total_brands_found']}")
        if results['brands']:
            print("🏷️  Marques identifiées:")
            for brand in results['brands']:
                print(f"  • {brand}")
        else:
            print("❌ Aucune marque trouvée")
        
        all_results.append(results)
    
    # Sauvegarder tous les résultats
    with open('multi_site_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Résultats sauvegardés dans: multi_site_analysis.json")
    
    # Statistiques globales
    total_brands = set()
    for result in all_results:
        if 'brands' in result:
            total_brands.update(result['brands'])
    
    print(f"\n📈 STATISTIQUES GLOBALES")
    print(f"🌐 Sites analysés: {len(all_results)}")
    print(f"🏷️  Marques uniques trouvées: {len(total_brands)}")
    print(f"📋 Marques: {', '.join(sorted(total_brands))}")

def custom_brand_analysis():
    """Exemple avec une liste de marques personnalisée."""
    
    # Créer un scraper avec des marques personnalisées
    class CustomBrandScraper(BrandScraper):
        def _load_brands(self):
            # Liste personnalisée de marques françaises
            return {
                'carrefour', 'auchan', 'leclerc', 'intermarché', 'casino',
                'monoprix', 'franprix', 'simply market', 'géant', 'cora',
                'orange', 'sfr', 'bouygues', 'free', 'sosh', 'red by sfr',
                'peugeot', 'renault', 'citroën', 'dacia', 'opel',
                'lacoste', 'petit bateau', 'kiabi', 'promod', 'jennyfer',
                'saint james', 'le coq sportif', 'aigle', 'paris texas'
            }
    
    scraper = CustomBrandScraper()
    
    print("🇫🇷 Analyse avec marques françaises personnalisées")
    print("="*50)
    
    # Analyser un site français
    results = scraper.analyze_page("https://www.fnac.com", delay=1.0)
    
    if "error" not in results:
        print(f"✅ Marques françaises trouvées: {results['total_brands_found']}")
        if results['brands']:
            for brand in results['brands']:
                print(f"  • {brand}")
    else:
        print(f"❌ Erreur: {results['error']}")

if __name__ == "__main__":
    print("🎯 Exemples d'utilisation du Brand Scraper")
    print("="*50)
    
    # Exemple 1: Analyse de plusieurs sites
    example_usage()
    
    print("\n" + "="*50)
    
    # Exemple 2: Analyse avec marques personnalisées
    custom_brand_analysis() 