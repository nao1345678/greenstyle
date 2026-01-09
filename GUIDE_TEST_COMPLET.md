# Guide de Test Complet - Extension et Site Web

## 🚀 Démarrage Rapide

### 1. Démarrer le Backend

```bash
cd extension_finale/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Vérifier que le backend fonctionne :
```bash
curl http://localhost:8000/health
# Devrait retourner : {"status":"healthy"}
```

### 2. Démarrer le Site Web

```bash
cd site_web_local/frontend/site-vue
npm install  # Si pas encore fait
npm run dev
```

Le site sera accessible sur : `http://localhost:5173`

### 3. Charger l'Extension Chrome

1. Ouvrir Chrome : `chrome://extensions/`
2. Activer "Mode développeur" (en haut à droite)
3. Cliquer sur "Charger l'extension non empaquetée"
4. Sélectionner le dossier : `extension_finale/extensions/`

## ✅ Tests à Effectuer

### Test 1 : Site Web - Connexion et Inscription

1. **Aller sur** `http://localhost:5173`
2. **Cliquer sur "Connexion"** dans la navbar
3. **Créer un compte** :
   - Prénom : Test
   - Nom d'utilisateur : testuser
   - Email : test@example.com
   - Mot de passe : test123
4. **Vérifier** : Vous êtes redirigé vers la page d'accueil
5. **Vérifier** : Le menu affiche "Mes favoris" au lieu de "Connexion"

### Test 2 : Site Web - Affichage des Marques

1. **Sur la page d'accueil**, vérifier que des marques s'affichent
2. **Cliquer sur une marque** pour voir la page de détail
3. **Vérifier** :
   - Le score est affiché
   - La section "Pourquoi cette note ?" est visible
   - Les critères détaillés sont affichés
   - Le bouton "Ajouter aux favoris" est visible

### Test 3 : Site Web - Ajout aux Favoris

1. **Sur la page de détail d'une marque**, cliquer sur "Ajouter aux favoris"
2. **Vérifier** : Le bouton change en "★ Retirer des favoris"
3. **Aller dans "Mes favoris"** (navbar)
4. **Vérifier** : La marque apparaît dans la liste des favoris

### Test 4 : Extension - Détection de Marques

1. **Ouvrir un site e-commerce** (ex: Zalando, ASOS, etc.)
2. **Cliquer sur l'icône de l'extension** dans la barre d'outils Chrome
3. **Vérifier** :
   - Les marques détectées s'affichent dans le popup
   - Les scores sont affichés
   - Les jauges "work" et "planet" sont visibles

### Test 5 : Extension - Ajout aux Favoris (Sans Connexion)

1. **Dans le popup de l'extension**, trouver une marque
2. **Cliquer sur le bouton favoris**
3. **Vérifier** : Un message indique qu'il faut se connecter
4. **Vérifier** : Le bouton affiche "🔒 Se connecter pour ajouter aux favoris"

### Test 6 : Extension - Ajout aux Favoris (Avec Connexion)

**Note** : Pour que l'extension utilise votre session du site web, vous devez :
- Soit synchroniser manuellement (à implémenter)
- Soit vous connecter via l'API directement depuis l'extension

**Pour l'instant**, l'extension stocke la session localement. Pour tester :

1. **Se connecter sur le site web** (`http://localhost:5173`)
2. **Ouvrir la console du navigateur** (F12)
3. **Exécuter** :
```javascript
// Récupérer les infos de l'utilisateur connecté depuis le store
// (Cette fonctionnalité nécessite une synchronisation entre le site et l'extension)
```

**Alternative** : Tester directement l'API :

```bash
# Créer un utilisateur
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "firstname": "Test",
    "email": "test@example.com",
    "password": "test123"
  }'

# Se connecter
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
# Notez l'ID de l'utilisateur retourné

# Ajouter une marque aux favoris (remplacer USER_ID et BRAND_ID)
curl -X POST "http://localhost:8000/favorites/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER_ID",
    "brand_id": "BRAND_ID"
  }'
```

### Test 7 : Page À Propos

1. **Aller sur** `http://localhost:5173/a-propos`
2. **Vérifier** :
   - Les marges gauche/droite sont à 15%
   - Le texte et les images sont alignés
   - La police "Jersey 10" est utilisée pour les titres

### Test 8 : Page de Connexion/Inscription

1. **Aller sur** `http://localhost:5173/login`
2. **Vérifier** :
   - La police "Jersey 10" est utilisée pour le titre
   - Le formulaire fonctionne correctement
   - Le basculement entre connexion et inscription fonctionne

## 🔍 Vérifications Techniques

### Backend

```bash
# Vérifier que toutes les routes sont disponibles
curl http://localhost:8000/docs  # Documentation Swagger

# Vérifier la route d'authentification
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'

# Vérifier la route des favoris
curl "http://localhost:8000/favorites/?user_id=USER_ID"
```

### Base de Données

Les favoris sont stockés dans MongoDB dans la collection `favorites` avec :
- `user` : Référence à l'utilisateur
- `brand` : Référence à la marque

## ⚠️ Problèmes Connus

1. **Synchronisation Site ↔ Extension** : 
   - L'extension ne synchronise pas automatiquement la session avec le site web
   - Solution temporaire : Se connecter via l'API directement

2. **ID de marque dans l'extension** :
   - L'extension doit recevoir l'ID de la marque depuis l'API
   - Vérifier que `brandData.id` est bien présent dans les données

## 📝 Notes

- Le backend doit être démarré avant le site web
- MongoDB doit être accessible pour les favoris
- L'extension nécessite Chrome avec le mode développeur activé

