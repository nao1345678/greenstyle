"""
Script d'import des données de marques dans MongoDB
Utilise les données JSON et CSV disponibles dans le projet
"""
import asyncio
import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Importer les modèles
try:
    from src.models.brand import Brand
except ImportError:
    from models.brand import Brand

load_dotenv()

# Chemins des données
ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIRS = [
    ROOT / "scrapping" / "scrapping_v4" / "data",
    ROOT / "scrapping" / "data",
    ROOT / "data",
]


def load_json_data(file_path: Path) -> List[Dict[str, Any]]:
    """Charge les données depuis un fichier JSON"""
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                if "items" in data:
                    return data["items"]
                return [data]
            return []
    except Exception as e:
        print(f"⚠️  Erreur lors du chargement de {file_path}: {e}")
        return []


def load_csv_data(file_path: Path) -> List[Dict[str, Any]]:
    """Charge les données depuis un fichier CSV"""
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"⚠️  Erreur lors du chargement de {file_path}: {e}")
        return []


def normalize_brand_name(name: str) -> str:
    """Normalise le nom de la marque"""
    if not name:
        return ""
    return name.strip().lower()


async def import_living_wage_data(data_dir: Path) -> int:
    """Importe les données de living wage"""
    files = [
        data_dir / "living_wage.json",
        data_dir / "living_wage_complete_391_items.json",
    ]
    
    count = 0
    for file_path in files:
        if not file_path.exists():
            continue
        
        print(f"📊 Import des données living wage depuis {file_path.name}...")
        records = load_json_data(file_path)
        
        for record in records:
            brand_name = record.get("company") or record.get("brand") or record.get("name")
            if not brand_name:
                continue
            
            brand_name = normalize_brand_name(brand_name)
            value = record.get("value", "").strip().lower()
            
            # Mapper yes/partial/no vers des scores
            if value == "yes":
                labor_score = 85.0
            elif value == "partial":
                labor_score = 50.0
            elif value == "no":
                labor_score = 25.0
            else:
                continue
            
            # Chercher ou créer la marque
            brand = await Brand.find_one(Brand.brand_name == brand_name)
            if not brand:
                brand = Brand(brand_name=brand_name)
            
            brand.labor_ethics = labor_score
            await brand.save()
            count += 1
        
        print(f"  ✅ {count} marques mises à jour depuis {file_path.name}")
    
    return count


async def import_transparency_data(data_dir: Path) -> int:
    """Importe les données de transparence"""
    files = [
        data_dir / "supply_chain_transparency_data.json",
        data_dir / "transparency_scores_simple.json",
    ]
    
    count = 0
    for file_path in files:
        if not file_path.exists():
            continue
        
        print(f"📊 Import des données de transparence depuis {file_path.name}...")
        records = load_json_data(file_path)
        
        for record in records:
            brand_name = record.get("company") or record.get("brand") or record.get("name")
            if not brand_name:
                continue
            
            brand_name = normalize_brand_name(brand_name)
            
            # Récupérer le score de transparence
            transparency_value = record.get("value") or record.get("score") or record.get("transparency")
            
            if transparency_value is None:
                continue
            
            try:
                transparency_score = float(str(transparency_value).replace(",", "."))
            except:
                continue
            
            # Mapper vers un niveau de transparence textuel
            if transparency_score >= 8:
                transparency_level = "Totale"
            elif transparency_score >= 6:
                transparency_level = "Élevée"
            elif transparency_score >= 4:
                transparency_level = "Modérée"
            else:
                transparency_level = "Faible"
            
            # Chercher ou créer la marque
            brand = await Brand.find_one(Brand.brand_name == brand_name)
            if not brand:
                brand = Brand(brand_name=brand_name)
            
            brand.supply_chain_transparency = transparency_level
            await brand.save()
            count += 1
        
        print(f"  ✅ {count} marques mises à jour depuis {file_path.name}")
    
    return count


async def import_csv_brands(csv_path: Path) -> int:
    """Importe les marques depuis un fichier CSV"""
    if not csv_path.exists():
        return 0
    
    print(f"📊 Import des marques depuis {csv_path.name}...")
    records = load_csv_data(csv_path)
    
    count = 0
    for record in records:
        brand_name = record.get("brand") or record.get("nom_marque") or record.get("brand_name")
        if not brand_name:
            continue
        
        brand_name = normalize_brand_name(brand_name)
        
        # Chercher ou créer la marque
        brand = await Brand.find_one(Brand.brand_name == brand_name)
        if not brand:
            brand = Brand(brand_name=brand_name)
        
        # Mapper les champs CSV vers le modèle Brand
        if record.get("sustainable_materials"):
            try:
                brand.sustainable_materials = float(record["sustainable_materials"])
            except:
                pass
        
        if record.get("certifications"):
            brand.certifications = str(record["certifications"]).strip()
        
        if record.get("country_origin"):
            brand.country_origin = str(record["country_origin"]).strip()
        
        if record.get("country_production"):
            brand.country_production = str(record["country_production"]).strip()
        
        if record.get("unsold_management"):
            brand.unsold_management = str(record["unsold_management"]).strip()
        
        if record.get("supply_chain_transparency"):
            brand.supply_chain_transparency = str(record["supply_chain_transparency"]).strip()
        
        if record.get("global_env_impact"):
            try:
                brand.global_env_impact = float(record["global_env_impact"])
            except:
                pass
        
        if record.get("labor_ethics"):
            try:
                brand.labor_ethics = float(record["labor_ethics"])
            except:
                pass
        
        if record.get("final_score"):
            try:
                brand.final_score = float(record["final_score"])
            except:
                pass
        
        if record.get("description"):
            brand.description = str(record["description"]).strip()
        
        if record.get("logo"):
            brand.logo = str(record["logo"]).strip()
        
        if record.get("website"):
            brand.website = str(record["website"]).strip()
        
        await brand.save()
        count += 1
    
    print(f"  ✅ {count} marques importées depuis {csv_path.name}")
    return count


async def init_database():
    """Initialise la connexion MongoDB"""
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/greenstyle")
    db_name = os.getenv("MONGO_DB", "greenstyle_DB")
    
    print(f"🔌 Connexion à MongoDB: {mongo_url}")
    print(f"📦 Base de données: {db_name}")
    
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=10000)
    try:
        await client.admin.command('ping')
        db = client.get_database(db_name)
        await init_beanie(database=db, document_models=[Brand])
        print("✅ MongoDB connecté et Beanie initialisé")
        return client, db
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB: {e}")
        raise


async def main():
    """Fonction principale d'import"""
    print("🚀 Démarrage de l'import des données de marques")
    print("=" * 60)
    
    # Initialiser la base de données
    client, db = await init_database()
    
    try:
        # Trouver le dossier de données
        data_dir = None
        for dir_path in DATA_DIRS:
            if dir_path.exists():
                data_dir = dir_path
                break
        
        if not data_dir:
            print("⚠️  Aucun dossier de données trouvé")
            print(f"   Recherché dans: {DATA_DIRS}")
            return
        
        print(f"📁 Dossier de données: {data_dir}")
        print()
        
        # Importer les données JSON
        living_wage_count = await import_living_wage_data(data_dir)
        transparency_count = await import_transparency_data(data_dir)
        
        # Importer les données CSV
        csv_files = [
            ROOT / "brands_database_with_recycled_materials.csv",
            ROOT / "brands_database_with_sustainable_materials.csv",
            ROOT / "brands_database_with_production_countries.csv",
            ROOT / "brands_database_fixed.csv",
            ROOT / "brands_database.csv",
        ]
        
        csv_count = 0
        for csv_file in csv_files:
            if csv_file.exists():
                count = await import_csv_brands(csv_file)
                csv_count += count
        
        # Résumé
        print()
        print("=" * 60)
        print("📊 Résumé de l'import")
        print("=" * 60)
        print(f"✅ Living wage: {living_wage_count} marques")
        print(f"✅ Transparence: {transparency_count} marques")
        print(f"✅ CSV: {csv_count} marques")
        print(f"📦 Total: {living_wage_count + transparency_count + csv_count} opérations")
        print()
        print("✅ Import terminé avec succès !")
        
    finally:
        client.close()
        print("🔌 Connexion MongoDB fermée")


if __name__ == "__main__":
    asyncio.run(main())

