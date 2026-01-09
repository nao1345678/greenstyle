#!/usr/bin/env python3
"""
Script de test pour vérifier les connexions entre tous les composants
"""
import asyncio
import sys
import os
from pathlib import Path

# Ajouter le chemin du backend
sys.path.insert(0, str(Path(__file__).parent / "extension_finale" / "src"))

async def test_backend_mongodb():
    """Test la connexion Backend ↔ MongoDB"""
    print("🔍 Test 1 : Connexion Backend ↔ MongoDB")
    print("-" * 60)
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from beanie import init_beanie
        from models.brand import Brand
        
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/greenstyle")
        db_name = os.getenv("MONGO_DB", "greenstyle_DB")
        
        print(f"   📡 Connexion à MongoDB : {mongo_url}")
        print(f"   📦 Base de données : {db_name}")
        
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("   ✅ MongoDB est accessible")
        
        db = client.get_database(db_name)
        await init_beanie(database=db, document_models=[Brand])
        print("   ✅ Beanie initialisé")
        
        # Compter les marques dans la base
        count = await Brand.find_all().count()
        print(f"   📊 Nombre de marques dans la base : {count}")
        
        # Tester une marque scrappée (Veja)
        veja = await Brand.find_one(Brand.brand_name == "veja")
        if veja:
            print(f"   ✅ Marque scrappée trouvée : Veja (score: {veja.final_score})")
        else:
            print("   ⚠️  Veja non trouvée dans la base (normal si pas importée)")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        return False


async def test_api_endpoints():
    """Test les endpoints de l'API"""
    print("\n🔍 Test 2 : Endpoints API")
    print("-" * 60)
    
    try:
        from httpx import AsyncClient, ASGITransport
        from main import app
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Test endpoint racine
            response = await client.get("/")
            print(f"   GET / : {response.status_code}")
            if response.status_code == 200:
                print(f"      ✅ {response.json()}")
            
            # Test endpoint health
            response = await client.get("/health")
            print(f"   GET /health : {response.status_code}")
            if response.status_code == 200:
                print(f"      ✅ {response.json()}")
            
            # Test endpoint brands
            response = await client.get("/brands/")
            print(f"   GET /brands/ : {response.status_code}")
            if response.status_code == 200:
                brands = response.json()
                print(f"      ✅ {len(brands)} marques retournées")
                if brands:
                    print(f"      📋 Première marque : {brands[0].get('brand_name', 'N/A')}")
            
            # Test endpoint brand by name (Veja)
            response = await client.get("/brands/name/veja?auto_scrape=true")
            print(f"   GET /brands/name/veja : {response.status_code}")
            if response.status_code == 200:
                brand = response.json()
                print(f"      ✅ Veja trouvée : score {brand.get('final_score', 'N/A')}")
                print(f"         Matières durables : {brand.get('sustainable_materials', 'N/A')}%")
                print(f"         Impact environnemental : {brand.get('global_env_impact', 'N/A')}")
                print(f"         Éthique du travail : {brand.get('labor_ethics', 'N/A')}")
            elif response.status_code == 404:
                print(f"      ⚠️  Veja non trouvée (scraping automatique activé)")
            
            # Test endpoint brand by name (Nike)
            response = await client.get("/brands/name/nike?auto_scrape=true")
            print(f"   GET /brands/name/nike : {response.status_code}")
            if response.status_code == 200:
                brand = response.json()
                print(f"      ✅ Nike trouvée : score {brand.get('final_score', 'N/A')}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_scraping():
    """Test le scraping de marques"""
    print("\n🔍 Test 3 : Scraping de marques")
    print("-" * 60)
    
    try:
        from services.scraper_service import scrape_brand_data
        
        # Test Veja (marque avec fallback)
        print("   📊 Scraping Veja (marque engagée)...")
        veja_data = await scrape_brand_data("veja")
        if veja_data:
            print(f"      ✅ Veja scrapée : {veja_data.get('brand_name')}")
            print(f"         Matières : {veja_data.get('sustainable_materials', 'N/A')}%")
            print(f"         Certifications : {veja_data.get('certifications', 'N/A')}")
        
        # Test Nike (marque fast fashion)
        print("\n   📊 Scraping Nike (fast fashion)...")
        nike_data = await scrape_brand_data("nike")
        if nike_data:
            print(f"      ✅ Nike scrapée : {nike_data.get('brand_name')}")
            print(f"         Matières : {nike_data.get('sustainable_materials', 'N/A')}%")
        
        # Test marque inconnue
        print("\n   📊 Scraping marque inconnue...")
        unknown_data = await scrape_brand_data("marque_inexistante_xyz")
        if unknown_data:
            print(f"      ✅ Structure de données OK : {unknown_data.get('brand_name')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Fonction principale de test"""
    print("🧪 Tests de Connexion - Site ↔ Backend ↔ MongoDB ↔ Extension")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1 : Backend ↔ MongoDB
    result1 = await test_backend_mongodb()
    results.append(("Backend ↔ MongoDB", result1))
    
    # Test 2 : Endpoints API
    result2 = await test_api_endpoints()
    results.append(("Endpoints API", result2))
    
    # Test 3 : Scraping
    result3 = await test_scraping()
    results.append(("Scraping de marques", result3))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé des Tests")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\n📈 Score : {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Les connexions fonctionnent.")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")


if __name__ == "__main__":
    asyncio.run(main())

