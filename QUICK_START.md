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

### Option 2: Lancer la démonstration complète

```bash
python3 example_usage.py
```

Cette démonstration crée deux utilisateurs avec des profils différents et montre:
- Comment le système apprend des préférences
- Comment les recommandations s'adaptent à chaque utilisateur
- Comment comparer les profils

## Utilisation dans votre code

### Exemple minimal

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

