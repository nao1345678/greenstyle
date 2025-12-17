# Importe la librairie pour se connecter a Mongo DB 
from pymongo import MongoClient
# Pouvoir interagir avec l'os pour lire les variable d'env
import os

import sys

# --- CHARGEMENT  DE .ENV  ---

def load_env_manual(env_path="../.env"):

    # Ajoute le répertoire parent au chemin d'importation (pour l'import de calcul_score si nécessaire)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    try:
        # Tente d'ouvrir le fichier .env qui se trouve à la racine'
        with open(env_path, 'r') as f:
            for line in f:
                # Ignore les les lignes vides ou les commentaires
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    value = value.strip().strip('\'"')
                    # Definit la variables dans l'environnement
                    os.environ[key.strip()] = value
    except FileNotFoundError:
        print(f"Attention : Le fichier {env_path} est introuvable. Assurez-vous qu'il est à la racine de votre projet.")

# Lance le chargement des variables d'env
load_env_manual() 

# Importation de la fonction
from calcul_score import calculate_scores 

# Configuration de la bases
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", 'greenstyle_DB') 
BRAND_COLLECTION = 'brands'

# Initialisation de bases de données
def get_mongo_collection(collection_name: str):
    """Initialise la connexion à MongoDB et retourne une collection spécifique."""
    
    if not MONGO_URL:
        print("Erreur: MONGO_URL n'est pas définie dans votre .env.")
        exit()

    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping') 
        print(f"Connexion à MongoDB réussie au cluster.")
    except Exception as e:
        print(f" Erreur de connexion MongoDB. Vérifiez votre URL: {e}")
        raise
        
    db = client[DB_NAME]
    return db[collection_name]


# Calcul et Modifie la brands
def calculate_and_update_all_brands():
    """
    Récupère les marques sans score final, calcule le score, et met à jour.
    """
    brands_collection = get_mongo_collection(BRAND_COLLECTION)

    query = {
        "$or": [
            {"final_score": {"$exists": False}}, 
            {"final_score": None}
        ]
    }
    
    brands_to_update_cursor = brands_collection.find(query)
    count = brands_collection.count_documents(query)

    if count == 0:
        print("Aucune marque à calculer/mettre à jour trouvée. Terminé.")
        return

    print(f" Début du traitement de {count} marque(s) sans score...")

    updated_count = 0
    for brand in brands_to_update_cursor:
        try:
            calculated_scores = calculate_scores(brand)
            
            update_result = brands_collection.update_one(
                {'_id': brand['_id']}, 
                {'$set': calculated_scores} 
            )
            
            if update_result.modified_count > 0:
                brand_name = brand.get('brand_name', 'Marque Inconnue')
                print(f" [OK] Marque '{brand_name}' mise à jour. Score Final: {calculated_scores['final_score']}")
                updated_count += 1

        except Exception as e:
            print(f" [ERREUR] Impossible de traiter la marque avec _id {brand.get('_id')}: {e}")
            
    print(f"--- Processus de scoring automatique terminé. {updated_count} marque(s) mises à jour. ---")


if __name__ == '__main__':
    calculate_and_update_all_brands()