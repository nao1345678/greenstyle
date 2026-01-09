# Configuration de la connexion Site Web ↔ Backend ↔ Base de données ↔ Extension

Ce document explique comment connecter tous les composants du projet.

## Architecture complète

```
┌─────────────────┐
│  Extension      │ ──► http://localhost:8000/brands/name/{brand}
│  Chrome         │
└─────────────────┘

┌─────────────────┐
│  Site Web       │ ──► http://localhost:8000/brands/  (via proxy /api)
│  (Vue.js)       │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Backend API    │ ──► MongoDB greenstyle_DB
│  (FastAPI)      │
│  :8000          │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  MongoDB        │
│  greenstyle_DB  │
└─────────────────┘
```

## Problèmes identifiés et solutions

### ❌ Problème 1 : Site web utilise uniquement un proxy en développement

**Symptôme :** Le site fonctionne avec `npm run dev` mais pas en production.

**Solution :** Configuration avec variable d'environnement `VITE_API_URL`

### ❌ Problème 2 : Nginx n'est pas configuré pour proxy les API

**Symptôme :** En production avec Docker, les requêtes `/api` ne sont pas redirigées.

**Solution :** Configuration Nginx mise à jour pour proxy vers le backend

### ❌ Problème 3 : Pas de variable d'environnement pour la configuration

**Symptôme :** L'URL du backend est codée en dur.

**Solution :** Utilisation de `VITE_API_URL` pour la configuration

## Configuration

### 1. Site Web (frontend/site-vue)

#### Développement

1. **Créer un fichier `.env`** :
```bash
cd site_web_local/frontend/site-vue
cp .env.example .env
```

2. **Configurer `.env`** :
```env
VITE_API_URL=http://localhost:8000
```

3. **Lancer en développement** :
```bash
npm install
npm run dev
```

Le proxy Vite redirige automatiquement `/api` vers `http://localhost:8000`.

#### Production

1. **Construire le site** :
```bash
npm run build
```

2. **Configurer la variable d'environnement** :
```env
VITE_API_URL=http://backend:8000
```

Ou pour un serveur externe :
```env
VITE_API_URL=http://votre-backend.com:8000
```

3. **Déployer avec Docker** :
```bash
cd site_web_local/frontend
docker build -t greenstyle-frontend .
docker run -p 80:80 greenstyle-frontend
```

### 2. Backend API

#### Vérifier la configuration

Le backend (`extension_finale/src/main.py`) est déjà configuré avec :
- ✅ CORS activé (accepte toutes les origines)
- ✅ Routes `/brands/` disponibles
- ✅ Connexion MongoDB configurable via variables d'environnement

#### Démarrer le backend

```bash
cd extension_finale/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Ou avec variables d'environnement :
```bash
MONGO_URL=mongodb://localhost:27017/greenstyle
MONGO_DB=greenstyle_DB
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Base de données MongoDB

#### Vérifier que MongoDB est démarré

```bash
# Vérifier que MongoDB tourne
mongosh --eval "db.adminCommand('ping')"
```

#### Initialiser la base de données

```bash
cd GreenstyleDataBaseCreate
mongosh < setup_database.js
```

#### Importer les données

```bash
cd extension_finale
python3 scripts/import_brands_data.py
```

### 4. Extension Chrome

L'extension est déjà configurée pour utiliser `http://localhost:8000` :

```javascript
// extension_finale/extensions/background.js
const API_BASE_URL = 'http://localhost:8000';
```

**Pas besoin de modification** si le backend est sur `localhost:8000`.

## Docker Compose (Recommandé)

Pour connecter tous les composants automatiquement, créez un `docker-compose.yml` :

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: greenstyle_DB

  backend:
    build: ./extension_finale
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      MONGO_URL: mongodb://mongodb:27017/greenstyle
      MONGO_DB: greenstyle_DB

  frontend:
    build: ./site_web_local/frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      VITE_API_URL: http://backend:8000
```

Lancer avec :
```bash
docker-compose up -d
```

## Tests de connexion

### Test 1 : Backend ↔ MongoDB

```bash
curl http://localhost:8000/health
```

Réponse attendue : `{"status": "healthy"}`

### Test 2 : Site Web ↔ Backend

Dans la console du navigateur (F12) :
```javascript
fetch('http://localhost:8000/brands/')
  .then(r => r.json())
  .then(console.log)
```

### Test 3 : Extension ↔ Backend

1. Charger l'extension dans Chrome
2. Aller sur un site e-commerce
3. Ouvrir la console (F12)
4. Vérifier les logs : `[GreenStyle Background]`

### Test 4 : Endpoint complet

```bash
# Récupérer une marque
curl http://localhost:8000/brands/name/veja

# Lister toutes les marques
curl http://localhost:8000/brands/
```

## Résolution des problèmes

### Le site ne peut pas se connecter au backend

1. **Vérifier que le backend est démarré** :
   ```bash
   curl http://localhost:8000/health
   ```

2. **Vérifier CORS** :
   - Le backend accepte toutes les origines (`allow_origins=["*"]`)
   - Si problème, vérifier les logs du backend

3. **Vérifier la variable d'environnement** :
   - En développement : utiliser le proxy Vite (`/api`)
   - En production : définir `VITE_API_URL`

### L'extension ne trouve pas les marques

1. **Vérifier l'URL du backend** dans `background.js`
2. **Vérifier que le backend est accessible** depuis le navigateur
3. **Vérifier les logs** dans la console Chrome (F12)

### MongoDB n'est pas connecté

1. **Vérifier que MongoDB est démarré** :
   ```bash
   mongosh --eval "db.adminCommand('ping')"
   ```

2. **Vérifier les variables d'environnement** :
   ```bash
   echo $MONGO_URL
   echo $MONGO_DB
   ```

3. **Vérifier les logs du backend** au démarrage

## Checklist de connexion

- [ ] MongoDB démarré et accessible
- [ ] Base de données `greenstyle_DB` créée
- [ ] Données importées dans MongoDB
- [ ] Backend FastAPI démarré sur port 8000
- [ ] CORS configuré dans le backend
- [ ] Site web configuré avec `VITE_API_URL`
- [ ] Extension configurée avec la bonne URL
- [ ] Nginx configuré pour proxy (production)
- [ ] Tous les tests de connexion passent

## Support

En cas de problème, vérifier :
1. Les logs du backend (`extension_finale/src`)
2. Les logs du frontend (console navigateur)
3. Les logs de l'extension (Chrome DevTools)
4. Les logs MongoDB


