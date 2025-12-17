# Soutenance - Projet GreenStyle : Plateforme de Recommandation de Mode Durable

## Table des matières
1. [Vue d'ensemble du projet](#vue-densemble)
2. [Architecture générale](#architecture-générale)
3. [Composants principaux](#composants-principaux)
4. [Fonctionnement du système](#fonctionnement)
5. [Technologies utilisées](#technologies)
6. [Flux de données](#flux-de-données)
7. [Points techniques à expliquer](#points-techniques)

---

## Vue d'ensemble du projet {#vue-densemble}

### Objectif
Créer une plateforme qui aide les utilisateurs à découvrir des marques de mode durables en fonction de leurs préférences personnelles. Le système apprend de leurs interactions et améliore ses recommandations au fil du temps.

### Problématique résolue
- Les consommateurs veulent acheter de manière plus responsable
- Difficile de trouver des marques qui correspondent à leurs valeurs
- Besoin de personnalisation selon les critères de durabilité

---

## Architecture générale {#architecture-générale}

Le projet est organisé en **4 grandes parties** :

### 1. **Collecte de données (Backend Python)**
- Scrapers qui collectent des informations sur les marques
- Base de données CSV enrichie avec des données de durabilité
- Orchestrateur IA qui coordonne tous les scrapers

### 2. **API Backend (FastAPI + MongoDB)**
- API REST pour exposer les données
- Gestion des utilisateurs et authentification
- Stockage des marques dans MongoDB

### 3. **Système d'IA et Recommandation**
- Moteur d'apprentissage des préférences
- Moteur de recommandation personnalisé
- Scoring de durabilité avec Machine Learning

### 4. **Extension Chrome (Frontend JavaScript/TypeScript)**
- Détection automatique des marques sur les pages web
- Affichage des informations de durabilité
- Enregistrement des interactions utilisateur

---

## Composants principaux {#composants-principaux}

### 1. Collecte de données - Les Scrapers

#### `ai_master_orchestrator.py`
**Rôle** : C'est le "chef d'orchestre" qui coordonne tous les scrapers.

**Fonctionnement** :
- Prend une liste de marques en CSV
- Pour chaque marque, décide intelligemment quelle source utiliser
- Apprend des tentatives précédentes pour optimiser les prochaines fois
- Scrape : matières recyclées, certifications, gestion des invendus

**Points clés à expliquer** :
```
"L'IA apprend quelle source est la plus fiable pour chaque type d'information.
Par exemple, si pour les certifications, B-Corp est plus fiable que les sites web,
l'IA va prioriser B-Corp pour les prochaines marques."
```

#### Autres scrapers spécialisés :
- `recycled_materials_scraper.py` : Trouve les pourcentages de matières recyclées
- `certifications_scraper.py` : Recherche les certifications (B-Corp, Fair Trade, etc.)
- `unsold_management_scraper.py` : Analyse la politique de gestion des invendus
- `country_production_scraper.py` : Trouve les pays de production

### 2. Base de données - MongoDB

#### Structure des collections
- **Brands** : Informations sur les marques (durabilité, certifications, etc.)
- **Users** : Comptes utilisateurs
- **Categories** : Catégories de mode (streetwear, luxe, etc.)
- **Favorites** : Marques favorites des utilisateurs
- **Alternatives** : Suggestions de marques alternatives

#### Fichiers de création
Dans `GreenstyleDataBaseCreate/` :
- Scripts Node.js pour créer les collections MongoDB
- Structure de la base de données

### 3. API Backend - FastAPI

#### `src/main.py`
**Point d'entrée** de l'API :
- Initialise FastAPI
- Connecte MongoDB avec Beanie (ORM pour MongoDB)
- Enregistre les routes (brands, users)

**Routes disponibles** :
- `GET /brands` : Liste toutes les marques
- `POST /brands` : Crée une nouvelle marque
- `GET /brands/{id}` : Détails d'une marque
- `PUT /brands/{id}` : Met à jour une marque
- `DELETE /brands/{id}` : Supprime une marque

#### `src/models/brand.py`
**Définit la structure d'une marque** :
- Schémas Pydantic pour la validation
- Modèle Beanie pour MongoDB
- Champs : nom, logo, site web, scores de durabilité, badges, etc.

### 4. Système d'IA - Apprentissage et Recommandation

#### `fashion_ai_api.py`
**API principale pour l'IA** :
- Gère les utilisateurs et leurs préférences
- Enregistre les interactions (like, dislike, click, etc.)
- Génère des recommandations personnalisées

**Méthodes principales** :
- `record_interaction()` : Enregistre une interaction et apprend
- `get_recommendations()` : Obtient des recommandations personnalisées
- `get_user_profile()` : Profil utilisateur avec ses préférences apprises

#### `preference_learning_engine.py`
**Moteur d'apprentissage** :
- Analyse les interactions utilisateur
- Déduit quels critères sont importants pour l'utilisateur
- Met à jour les "poids" (weights) de chaque critère

**Exemple d'apprentissage** :
```
Si l'utilisateur "like" une marque avec beaucoup de matières recyclées,
le système augmente le poids du critère "sustainable_materials" pour cet utilisateur.
```

**Algorithme** :
- Utilise un "learning rate" (vitesse d'apprentissage)
- Ajuste les poids selon les interactions positives/négatives
- Plus d'interactions = plus de confiance dans les préférences

#### `recommendation_engine.py`
**Moteur de recommandation** :
- Calcule un score de pertinence pour chaque marque
- Compare les caractéristiques de la marque avec les préférences utilisateur
- Génère des explications ("match_reasons")

**Calcul du score** :
```
Pour chaque marque :
  score = Σ (poids_utilisateur[critère] × valeur_marque[critère])
  
Plus le score est élevé, plus la marque correspond à l'utilisateur.
```

#### `ml_sustainability_scorer.py`
**Machine Learning pour scorer la durabilité** :
- Entraîne un modèle RandomForest sur les données existantes
- Prédit les scores de durabilité pour les nouvelles marques
- Utilise les critères collectés pour prédire le `final_score`

### 5. Authentification

#### `authentication_service.py`
**Gestion des utilisateurs** :
- Inscription/connexion
- Hashage des mots de passe (bcrypt)
- Gestion des sessions avec tokens
- Sécurité : validation email, mots de passe forts

### 6. Extension Chrome - Détection de marques

#### `brand_detection_engine.js`
**Détection sur les pages web** :
- Analyse le DOM de la page
- Cherche des mentions de marques dans le texte
- Utilise une base de données de marques connues
- Détecte aussi les alias (ex: "Nike Air" = Nike)

**Sources de détection** :
- Texte visible de la page
- Liens et URLs
- Attributs alt des images
- Métadonnées HTML
- Attributs data-* (data-brand, etc.)

#### `learning_brand_detector.js`
**Version auto-apprenante** :
- Découvre de nouvelles marques automatiquement
- Valide les candidats avec un score de confiance
- Sauvegarde les nouvelles marques dans localStorage
- S'améliore avec le temps

---

## Fonctionnement du système {#fonctionnement}

### Flux complet : De la collecte à la recommandation

#### Étape 1 : Collecte initiale
```
1. Lancer ai_master_orchestrator.py avec un CSV de marques
2. Pour chaque marque :
   - L'IA choisit la meilleure source (selon l'apprentissage)
   - Scrape les données (matières recyclées, certifications, etc.)
   - Enregistre les résultats dans le CSV
3. Entraîne le modèle ML pour prédire les scores
4. Sauvegarde tout dans brands_database_with_recycled_materials.csv
```

#### Étape 2 : Import dans MongoDB
```
1. Les scripts Node.js créent les collections MongoDB
2. Import du CSV dans la collection "brands"
3. Les données sont maintenant accessibles via l'API
```

#### Étape 3 : Utilisation par l'utilisateur
```
1. L'utilisateur installe l'extension Chrome
2. En naviguant sur un site e-commerce, l'extension détecte les marques
3. Affiche les informations de durabilité
4. L'utilisateur interagit (like, dislike, clique, etc.)
```

#### Étape 4 : Apprentissage
```
1. Chaque interaction est envoyée à l'API (record_interaction)
2. Le moteur d'apprentissage analyse :
   - Quelle marque ?
   - Quel type d'interaction ?
   - Quelles caractéristiques de la marque ?
3. Met à jour les préférences de l'utilisateur
4. Ajuste les poids des critères
```

#### Étape 5 : Recommandation
```
1. L'utilisateur demande des recommandations
2. Le moteur de recommandation :
   - Récupère les préférences apprises
   - Calcule un score pour chaque marque
   - Trie par score décroissant
   - Retourne les meilleures correspondances avec explications
```

---

## Technologies utilisées {#technologies}

### Backend Python
- **FastAPI** : Framework web moderne et rapide pour l'API
- **Pandas** : Manipulation des données CSV
- **Beanie** : ORM pour MongoDB (async)
- **scikit-learn** : Machine Learning (RandomForest)
- **Motor** : Driver MongoDB asynchrone

### Base de données
- **MongoDB** : Base de données NoSQL pour stocker les marques
- **CSV** : Format intermédiaire pour les données scrapées

### Frontend
- **JavaScript/TypeScript** : Code de l'extension Chrome
- **HTML/CSS** : Interface utilisateur

### Scraping
- **Requests** : Requêtes HTTP
- **BeautifulSoup** : Parsing HTML
- **Selenium** (possiblement) : Pour les sites dynamiques

---

## Flux de données {#flux-de-données}

### Schéma simplifié

```
┌─────────────────┐
│   CSV Sources   │  (brands_database.csv)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Scrapers IA   │  (ai_master_orchestrator.py)
│   - Recycled    │
│   - Certifs     │
│   - Unsold      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CSV Enrichi    │  (brands_database_with_recycled_materials.csv)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    MongoDB      │  (Base de données)
│  - brands       │
│  - users        │
│  - favorites    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │  (src/main.py)
│   - Routes      │
│   - Validation  │
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌──────────────┐  ┌──────────────┐
│  Fashion AI  │  │  Extension   │
│  API         │  │  Chrome      │
│  (Learning)  │  │  (Detection) │
└──────────────┘  └──────────────┘
```

---

## Points techniques à expliquer {#points-techniques}

### 1. Comment l'IA apprend les préférences ?

**Réponse simple** :
"L'utilisateur interagit avec des marques (like, dislike, etc.). 
Le système analyse quelles caractéristiques ont les marques qu'il aime.
Si l'utilisateur aime souvent des marques avec beaucoup de matières recyclées,
le système comprend que ce critère est important pour lui.
Il augmente le 'poids' de ce critère dans son profil."

**Exemple concret** :
```
Utilisateur "like" 3 marques :
- Marque A : 80% matières recyclées, score environnement 9/10
- Marque B : 75% matières recyclées, score environnement 8/10  
- Marque C : 70% matières recyclées, score environnement 7/10

Le système déduit : "Cet utilisateur valorise les matières recyclées"
→ Augmente le poids de "sustainable_materials" de 0.1 à 0.3
```

### 2. Comment fonctionne le scoring de recommandation ?

**Réponse simple** :
"Pour chaque marque, on multiplie chaque caractéristique par l'importance 
que l'utilisateur accorde à ce critère, puis on additionne tout."

**Formule** :
```
Score = (matières_recyclées × poids_utilisateur_matières) +
        (certifications × poids_utilisateur_certifs) +
        (transparence × poids_utilisateur_transparence) +
        ...
```

**Exemple** :
```
Marque X :
- 70% matières recyclées (valeur: 0.7)
- 3 certifications (valeur: 0.6)
- Transparence moyenne (valeur: 0.5)

Utilisateur avec poids :
- Matières : 0.4 (très important)
- Certifications : 0.2 (moyen)
- Transparence : 0.1 (peu important)

Score = (0.7 × 0.4) + (0.6 × 0.2) + (0.5 × 0.1)
      = 0.28 + 0.12 + 0.05
      = 0.45
```

### 3. Comment l'orchestrateur IA optimise les scrapers ?

**Réponse simple** :
"L'IA mémorise quelles sources ont fonctionné dans le passé.
Par exemple, si pour les certifications, B-Corp a réussi 9 fois sur 10,
alors pour la prochaine marque, l'IA va essayer B-Corp en premier."

**Mécanisme** :
1. Essaie chaque source dans l'ordre
2. Enregistre : succès/échec + temps pris
3. Calcule un taux de succès pour chaque source
4. Pour les prochaines marques, trie les sources par taux de succès

### 4. Comment fonctionne la détection dans l'extension ?

**Réponse simple** :
"L'extension analyse tous les textes de la page et cherche des noms de marques.
Elle a une base de données de marques connues et leurs alias.
Quand elle trouve une correspondance, elle affiche l'info de durabilité."

**Processus** :
1. Récupère tout le texte de la page
2. Cherche dans la base de données de marques
3. Vérifie aussi les alias (ex: "Nike Air" = Nike)
4. Affiche les résultats dans un popup/badge

### 5. Pourquoi MongoDB plutôt qu'une base SQL ?

**Réponse simple** :
"MongoDB est plus flexible. Les marques peuvent avoir des champs différents
selon les données collectées. C'est plus facile d'ajouter de nouveaux champs
sans modifier toute la structure de la base."

**Avantages** :
- Schéma flexible (pas besoin de définir toutes les colonnes à l'avance)
- Stockage JSON naturel
- Bon pour des données semi-structurées

---

## Structure des fichiers importants

### Backend Python
```
├── ai_master_orchestrator.py    # Orchestrateur principal
├── fashion_ai_api.py            # API IA principale
├── preference_learning_engine.py # Moteur d'apprentissage
├── recommendation_engine.py     # Moteur de recommandation
├── ml_sustainability_scorer.py  # ML pour scoring
├── authentication_service.py    # Authentification
├── recycled_materials_scraper.py # Scraper matières
├── certifications_scraper.py     # Scraper certifications
└── unsold_management_scraper.py  # Scraper invendus
```

### API FastAPI
```
src/
├── main.py              # Point d'entrée API
├── config.py            # Configuration (MongoDB URL)
├── models/
│   ├── brand.py         # Modèle Brand
│   ├── user.py          # Modèle User
│   └── ...
└── routes/
    ├── brand_routes.py  # Routes pour les marques
    └── user_routes.py   # Routes pour les users
```

### Extension Chrome
```
├── brand_detection_engine.js      # Détection basique
├── learning_brand_detector.js     # Détection auto-apprenante
├── brand_detector_extension.ts    # Version TypeScript
└── ai_brand_detector_demo.html    # Demo HTML
```

### Base de données
```
GreenstyleDataBaseCreate/
├── CreateDB_brands.js      # Création collection brands
├── CreateDB_users.js       # Création collection users
├── CreateDB_categories.js  # Création collection categories
└── setup_database.js       # Script de setup complet
```

---

## Questions possibles et réponses

### Q: Comment garantissez-vous la qualité des données scrapées ?

**R:** 
- L'IA apprend des sources les plus fiables
- Validation croisée entre plusieurs sources
- Scores de confiance pour chaque donnée
- Possibilité de révision manuelle

### Q: Que se passe-t-il si un utilisateur n'a pas encore d'interactions ?

**R:**
- Le système utilise des poids par défaut (tous égaux)
- Les recommandations sont basées sur les scores moyens de durabilité
- Au fur et à mesure des interactions, le profil se personnalise

### Q: Comment gérez-vous la performance avec beaucoup d'utilisateurs ?

**R:**
- MongoDB est scalable horizontalement
- Les préférences utilisateur sont en cache en mémoire
- Calculs de recommandation optimisés avec NumPy
- Possibilité d'ajouter Redis pour le cache

### Q: Comment l'extension fonctionne-t-elle sur différents sites web ?

**R:**
- Analyse générique du DOM (texte, liens, métadonnées)
- Détection multi-sources (pas dépendant d'une structure spécifique)
- Base de données de marques avec alias pour couvrir les variations
- Mode auto-apprenant pour découvrir de nouvelles marques

### Q: Quelles sont les limitations actuelles ?

**R:**
- Scraping limité par les politiques des sites (rate limiting)
- Détection de marques peut avoir des faux positifs
- Apprentissage nécessite plusieurs interactions pour être efficace
- Certaines données peuvent être manquantes pour certaines marques

---

## Démonstration suggérée

### 1. Montrer la collecte de données
```bash
# Lancer l'orchestrateur
python3 ai_master_orchestrator.py --test
```
**Expliquer** : "Voici comment on collecte les données de durabilité pour les marques"

### 2. Montrer l'API
```bash
# Démarrer FastAPI
uvicorn src.main:app --reload
```
**Expliquer** : "L'API expose les données via des endpoints REST"

### 3. Montrer l'apprentissage
```python
# Exemple avec fashion_ai_api.py
from fashion_ai_api import FashionAI

ai = FashionAI('brands_database_with_recycled_materials.csv')

# Utilisateur like une marque
ai.record_interaction('user123', 'Patagonia', 'like')

# Obtenir recommandations
recos = ai.get_recommendations('user123', n_recommendations=5)
```
**Expliquer** : "Le système apprend des préférences et recommande"

### 4. Montrer l'extension
**Expliquer** : "L'extension détecte les marques sur les pages web et affiche les infos"

---

## Points forts à mettre en avant

1. **Système auto-apprenant** : S'améliore avec l'usage
2. **Personnalisation** : Adapte les recommandations à chaque utilisateur
3. **IA orchestratrice** : Optimise automatiquement la collecte de données
4. **Approche complète** : De la collecte à la recommandation
5. **Technologies modernes** : FastAPI, MongoDB, Machine Learning

---

## Conclusion

Le projet combine :
- **Collecte intelligente** de données de durabilité
- **Apprentissage automatique** des préférences utilisateur
- **Recommandation personnalisée** basée sur les valeurs de chacun
- **Interface utilisateur** (extension Chrome) pour une expérience fluide

Le système devient **plus intelligent** au fur et à mesure que les utilisateurs interagissent avec lui, créant une expérience personnalisée pour découvrir des marques de mode durables.




