# Guide de démarrage rapide

## Installation

Installez d'abord les dépendances Python:

```bash
pip3 install -r requirements.txt
```

## Test du système

### Option 1: Lancer les tests unitaires

```bash
python3 test_fashion_ai.py
```

Cela validera que tous les composants fonctionnent correctement.

### Option 2: Démonstration avec authentification (RECOMMANDÉ)

```bash
python3 example_with_authentication.py
```

Cette démonstration montre le système complet:
- Inscription et connexion d'utilisateurs
- Authentification sécurisée
- Interactions avec les marques
- Recommandations personnalisées
- Persistance des données

### Option 3: Démonstration IA simple (sans authentification)

```bash
python3 example_usage.py
```

Version simplifiée focalisée uniquement sur l'IA d'apprentissage.

## Utilisation dans votre code

### Avec authentification (système complet)

```python
from integrated_fashion_system import IntegratedFashionSystem

# Initialise le système complet
system = IntegratedFashionSystem(
    brands_csv_path='brands_database_with_recycled_materials.csv'
)

# Inscription d'un utilisateur
result = system.register(
    email="alice@example.com",
    password="SecurePass123",
    username="alice_eco"
)

if result['success']:
    token = result['session_token']
    
    # Interactions
    system.record_brand_interaction(token, "Patagonia", "like")
    system.record_brand_interaction(token, "Supreme", "dislike")
    
    # Recommandations personnalisées
    recs = system.get_personalized_recommendations(token)
    for rec in recs['recommendations']:
        print(f"{rec['brand_name']}: {rec['score']:.3f}")
    
    # Déconnexion
    system.logout(token)
```

### Sans authentification (IA uniquement)

```python
from fashion_ai_api import FashionAI

# Initialise
ai = FashionAI(brands_csv_path='brands_database_with_recycled_materials.csv')

# Crée un utilisateur
user_id = "alice"
ai.create_user(user_id)

# Enregistre des interactions
ai.record_interaction(user_id, "Patagonia", "like")
ai.record_interaction(user_id, "Supreme", "dislike")

# Obtient des recommandations
recs = ai.get_recommendations(user_id, n_recommendations=10)
for rec in recs:
    print(f"{rec['brand_name']}: {rec['score']:.3f}")
```

## Structure des fichiers

```
user_preference_model.py       - Modèle de données utilisateur
preference_learning_engine.py  - Algorithme d'apprentissage
recommendation_engine.py        - Moteur de recommandation
fashion_ai_api.py              - API principale
example_usage.py               - Exemple complet
test_fashion_ai.py            - Tests unitaires
```

## Données utilisateur

Les préférences sont automatiquement sauvegardées dans `user_data/` au format JSON.
Ce répertoire est ignoré par git pour protéger les données personnelles.

## Support

Consultez README_AI.md pour la documentation complète.

