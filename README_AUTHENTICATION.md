# Système d'authentification et gestion des comptes utilisateur

Ce document décrit le système complet de gestion des comptes utilisateur intégré avec l'IA de recommandation.

## Vue d'ensemble

Le système permet aux utilisateurs de:
- Créer un compte sécurisé avec email et mot de passe
- Se connecter et gérer leur session
- Avoir leurs préférences IA automatiquement liées à leur compte
- Conserver leurs données de façon persistante

## Architecture

### Composants

```
user_account_model.py
  └─ Modèle de compte utilisateur avec hachage de mot de passe
  
authentication_service.py
  └─ Service d'inscription, connexion et gestion de sessions
  
integrated_fashion_system.py
  └─ Système intégré combinant auth + IA
  
example_with_authentication.py
  └─ Exemple complet d'utilisation
```

## Sécurité

### Hachage des mots de passe

Les mots de passe ne sont JAMAIS stockés en clair:
- Génération d'un salt unique par utilisateur
- Hachage SHA-256 avec 10000 itérations
- Comparaison sécurisée avec `secrets.compare_digest`

### Validation des mots de passe

Exigences minimales:
- Au moins 8 caractères
- Une lettre majuscule
- Une lettre minuscule
- Un chiffre

### Sessions

- Tokens générés avec `secrets.token_urlsafe`
- Expiration automatique après 24h
- Stockage en mémoire (Redis recommandé en production)

## Utilisation

### Inscription d'un nouvel utilisateur

```python
from integrated_fashion_system import IntegratedFashionSystem

system = IntegratedFashionSystem(
    brands_csv_path='brands_database_with_recycled_materials.csv'
)

result = system.register(
    email="alice@example.com",
    password="SecurePass123",
    username="alice_eco",
    first_name="Alice",
    age=28,
    country="France",
    data_sharing_consent=True
)

if result['success']:
    session_token = result['session_token']
    user_id = result['user']['user_id']
    print(f"Bienvenue {result['user']['username']}!")
```

### Connexion

```python
login_result = system.login(
    email="alice@example.com",
    password="SecurePass123"
)

if login_result['success']:
    session_token = login_result['session_token']
    ai_profile = login_result['ai_profile']
    print(f"Profil: {ai_profile['profile_type']}")
```

### Utilisation avec authentification

Toutes les opérations nécessitent un token de session valide:

```python
# Enregistrer une interaction
system.record_brand_interaction(
    session_token=session_token,
    brand_name="Patagonia",
    interaction_type="like"
)

# Obtenir des recommandations
recommendations = system.get_personalized_recommendations(
    session_token=session_token,
    n_recommendations=10
)

# Obtenir le profil complet
profile = system.get_complete_profile(session_token)
```

### Déconnexion

```python
system.logout(session_token)
```

## Modèle de données

### UserAccount

Attributs du compte:
- `user_id`: Identifiant unique généré automatiquement
- `email`: Email (unique, utilisé pour la connexion)
- `username`: Nom d'affichage
- `password_hash` et `salt`: Mot de passe haché
- `created_at`: Date de création
- `last_login`: Dernière connexion

Informations de profil optionnelles:
- `first_name`, `last_name`
- `age`, `gender`, `country`
- `data_sharing_consent`, `marketing_consent`

États:
- `is_active`: Compte actif ou désactivé
- `is_verified`: Email vérifié

### Liaison avec les préférences IA

Chaque compte (`user_id`) est automatiquement lié à:
- Un profil de préférences IA (`UserPreferences`)
- Un historique d'interactions
- Des recommandations personnalisées

## Stockage des données

### Structure des répertoires

```
user_accounts/
  ├── _email_index.json          # Index email → user_id
  ├── user_abc123.json            # Compte utilisateur 1
  └── user_xyz789.json            # Compte utilisateur 2

user_data/
  ├── user_abc123.json            # Préférences IA utilisateur 1
  └── user_xyz789.json            # Préférences IA utilisateur 2
```

### Protection des données

Les répertoires `user_accounts/` et `user_data/` sont dans `.gitignore`:
- Données personnelles non versionnées
- Conformité RGPD
- Sécurité des comptes

## Gestion du profil

### Mise à jour du profil

```python
system.update_profile(
    session_token=session_token,
    first_name="Alice",
    country="France",
    data_sharing_consent=True
)
```

### Changement de mot de passe

```python
from authentication_service import AuthenticationService

auth = AuthenticationService()
auth.change_password(
    user_id=user_id,
    old_password="OldPass123",
    new_password="NewPass456"
)
```

### Suppression de compte

Supprime le compte ET toutes les données IA:

```python
result = system.delete_user_account(
    session_token=session_token,
    password="SecurePass123"
)
```

## Flux d'utilisation typique

### 1. Nouvelle utilisatrice (Marie)

```python
# Inscription
result = system.register(
    email="marie@example.com",
    password="SecurePass123",
    username="marie_eco"
)
token = result['session_token']

# Interactions
system.record_brand_interaction(token, "Patagonia", "like")
system.record_brand_interaction(token, "Veja", "save")

# Recommandations personnalisées
recs = system.get_personalized_recommendations(token)

# Déconnexion
system.logout(token)
```

### 2. Utilisatrice récurrente

```python
# Connexion
result = system.login("marie@example.com", "SecurePass123")
token = result['session_token']

# Les préférences sont automatiquement chargées
print(result['ai_profile']['profile_type'])  # "Eco-conscient"
print(result['ai_profile']['total_interactions'])  # 2

# Continue à interagir
system.record_brand_interaction(token, "Reformation", "like")

# Nouvelles recommandations basées sur l'historique complet
recs = system.get_personalized_recommendations(token)
```

## API complète

### Authentification

- `register()`: Inscription d'un nouvel utilisateur
- `login()`: Connexion
- `logout()`: Déconnexion
- `verify_and_get_user()`: Vérification du token

### Profil

- `get_complete_profile()`: Profil complet (compte + IA)
- `update_profile()`: Mise à jour du profil

### Interactions et apprentissage

- `record_brand_interaction()`: Enregistre une interaction
- `record_brand_comparison()`: Enregistre une comparaison

### Recommandations

- `get_personalized_recommendations()`: Recommandations personnalisées
- `get_similar_brands()`: Marques similaires
- `explain_brand_recommendation()`: Explication détaillée

### Recherche

- `search_brands()`: Recherche de marques (sans auth)
- `get_categories()`: Liste des catégories

### Administration

- `get_system_statistics()`: Statistiques complètes
- `delete_user_account()`: Suppression complète

## Exemple complet

Lancez la démonstration complète:

```bash
python3 example_with_authentication.py
```

Cette démonstration montre:
- Inscription de deux utilisateurs avec des goûts différents
- Connexion et authentification
- Interactions et apprentissage
- Recommandations personnalisées
- Comparaison des profils
- Déconnexion et reconnexion
- Persistance des données

## Production

### Recommandations pour la production

1. **Stockage des sessions**
   - Utiliser Redis au lieu de la mémoire
   - Gestion distribuée des sessions

2. **Base de données**
   - Migrer vers PostgreSQL ou MongoDB
   - Index sur email pour performance

3. **Sécurité additionnelle**
   - Rate limiting sur login
   - Détection de bots
   - 2FA (authentification à deux facteurs)
   - Validation d'email

4. **RGPD**
   - Export des données utilisateur
   - Droit à l'oubli (anonymisation)
   - Consentements granulaires

5. **Monitoring**
   - Logs d'authentification
   - Alertes sur tentatives suspectes
   - Métriques d'utilisation

## Support

Pour plus d'informations:
- Voir `README_AI.md` pour le système d'IA
- Voir `example_with_authentication.py` pour des exemples complets
- Consulter le code source pour l'API détaillée

