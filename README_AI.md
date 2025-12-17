# Système d'IA d'apprentissage des préférences utilisateur pour recommandations de mode

Ce système d'intelligence artificielle apprend automatiquement les goûts et préférences de chaque utilisateur pour lui proposer des recommandations personnalisées de marques de mode basées sur des critères de durabilité, d'éthique et de qualité.

## Comment ça fonctionne

Le système analyse les interactions de l'utilisateur avec différentes marques pour identifier quels critères sont les plus importants pour lui:

- Matériaux durables et recyclés
- Pays de production et d'origine
- Transparence de la chaîne d'approvisionnement
- Impact environnemental global
- Éthique du travail
- Certifications
- Gestion des invendus
- Fourchette de prix

### Apprentissage adaptatif

Plus l'utilisateur interagit avec le système, plus les recommandations deviennent précises. Le système:

1. Enregistre chaque interaction (like, dislike, clic, sauvegarde, achat)
2. Analyse les caractéristiques des marques aimées vs rejetées
3. Ajuste automatiquement les poids des critères
4. Personnalise les recommandations en temps réel

### Types d'interaction

Le système comprend différents types d'interactions avec une force de signal variable:

- **Purchase** (signal fort): Achat d'un produit
- **Save** (signal fort): Sauvegarde de la marque
- **Like** (signal moyen): L'utilisateur aime la marque
- **Click** (signal faible): Simple clic pour voir plus
- **Dislike** (signal moyen négatif): L'utilisateur rejette la marque
- **Comparison** (signal très fort): Choix entre deux marques

## Architecture

### Composants principaux

```
user_preference_model.py
  └─ Modèle de données pour stocker les préférences utilisateur
  
preference_learning_engine.py
  └─ Moteur d'apprentissage qui analyse les interactions
  
recommendation_engine.py
  └─ Moteur de recommandation personnalisé
  
fashion_ai_api.py
  └─ API principale pour interagir avec le système
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Exemple basique

```python
from fashion_ai_api import FashionAI

# Initialise le système
ai = FashionAI(
    brands_csv_path='brands_database_with_recycled_materials.csv',
    learning_rate=0.15
)

# Crée un utilisateur
user_id = "alice"
ai.create_user(user_id)

# Enregistre des interactions
ai.record_interaction(
    user_id=user_id,
    brand_name="Patagonia",
    interaction_type="like"
)

ai.record_interaction(
    user_id=user_id,
    brand_name="Supreme",
    interaction_type="dislike"
)

# Obtient des recommandations personnalisées
recommendations = ai.get_recommendations(
    user_id=user_id,
    n_recommendations=10
)

for rec in recommendations:
    print(f"{rec['brand_name']}: {rec['score']:.3f}")
```

### Profil utilisateur

```python
# Analyse le profil appris
profile = ai.get_user_profile(user_id)

print(f"Type de profil: {profile['profile_type']}")
print(f"Confiance: {profile['learning_confidence']:.1%}")

# Top critères importants pour cet utilisateur
for criterion in profile['top_criteria']:
    print(f"{criterion['criterion']}: {criterion['weight']:.3f}")
```

### Comparaison de marques

```python
# L'apprentissage le plus efficace: comparaison directe
ai.record_comparison(
    user_id=user_id,
    chosen_brand="Patagonia",
    rejected_brand="Nike"
)
```

### Marques similaires

```python
# Trouve des marques similaires à une marque aimée
similar = ai.get_similar_brands(
    user_id=user_id,
    brand_name="Patagonia",
    n_recommendations=5
)
```

### Explication des recommandations

```python
# Comprendre pourquoi une marque est recommandée
explanation = ai.explain_recommendation(
    user_id=user_id,
    brand_name="Veja"
)

print(f"Score: {explanation['overall_score']:.3f}")
print(f"Raisons: {explanation['match_reasons']}")
```

## Démonstration complète

Lancez le script d'exemple pour voir une démonstration complète:

```bash
python example_usage.py
```

Ce script montre:
- Création de deux utilisateurs avec des goûts différents
- Apprentissage progressif des préférences
- Évolution du profil utilisateur
- Recommandations personnalisées
- Comparaison entre profils utilisateurs

## Profils types identifiés

Le système catégorise automatiquement les utilisateurs en profils:

- **Eco-conscient**: Privilégie les matériaux durables et l'impact environnemental
- **Ethique**: Valorise les conditions de travail et la transparence
- **Local**: Préfère les marques produites localement
- **Prix**: Sensible à la fourchette de prix
- **Equilibré**: Pas de préférence marquée

## Persistance des données

Les préférences utilisateur sont automatiquement sauvegardées dans `user_data/` au format JSON et peuvent être rechargées à tout moment:

```python
# Charge un utilisateur existant
user = ai.load_user("alice")

# Sauvegarde manuelle
ai.save_user("alice")
```

## Paramètres d'apprentissage

### Learning Rate

Le `learning_rate` (0.0 - 1.0) contrôle la vitesse d'adaptation:
- **Faible (0.05-0.10)**: Apprentissage lent, plus stable
- **Moyen (0.10-0.20)**: Équilibre entre stabilité et réactivité
- **Élevé (0.20-0.30)**: Adaptation rapide aux nouvelles préférences

### Confiance d'apprentissage

La confiance augmente logarithmiquement avec le nombre d'interactions:
- 0-20% : Très peu de données, recommandations génériques
- 20-50% : Début de personnalisation
- 50-80% : Profil bien défini
- 80-100% : Profil très précis, nombreuses interactions

## Évolution future

Possibilités d'amélioration:
- Apprentissage par renforcement pour optimiser les suggestions
- Détection de tendances temporelles dans les préférences
- Clustering d'utilisateurs similaires pour cold start
- Intégration de données comportementales additionnelles
- A/B testing pour optimiser l'algorithme d'apprentissage

## Performance

Le système est optimisé pour:
- Traiter des milliers de marques en quelques millisecondes
- Gérer des centaines d'utilisateurs simultanés
- Mise à jour en temps réel des préférences
- Sauvegarde asynchrone des données






