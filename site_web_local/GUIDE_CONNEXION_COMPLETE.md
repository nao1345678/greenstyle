# Guide de Connexion Complète - Tous les Composants

## ✅ Corrections Appliquées

J'ai identifié et corrigé les problèmes de connexion entre :
- **Site Web** ↔ Backend
- **Backend** ↔ Base de données MongoDB
- **Extension** ↔ Backend

## 🔧 Modifications Effectuées

### 1. Site Web - Configuration API (`frontend/site-vue/src/api/http.ts`)

**Problème :** Utilisait uniquement un proxy Vite qui fonctionne uniquement en développement.

**Solution :** Configuration dynamique qui utilise :
- Variable d'environnement `VITE_API_URL` si définie
- Proxy Vite (`/api`) en développement
- URL directe (`http://localhost:8000`) par défaut

### 2. Nginx - Configuration Proxy (`frontend/nginx/default.conf`)

**Problème :** Nginx ne proxyait pas les requêtes API vers le backend.

**Solution :** Ajout de la configuration proxy pour `/api` et `/brands` vers le backend.

### 3. Extension Chrome (`extension_finale/extensions/background.js`)

**Status :** ✅ Déjà correctement configurée avec `http://localhost:8000`

## 📋 Instructions de Connexion

### Option 1 : Développement Local (Recommandé)

#### Étape 1 : Démarrer MongoDB
```bash
# Option A : Si installé localement
mongod

# Option B : Avec Docker
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

#### Étape 2 : Initialiser la base de données
```bash
cd GreenstyleDataBaseCreate
mongosh < setup_database.js
```

#### Étape 3 : Importer les données
```bash
cd extension_finale
python3 scripts/import_brands_data.py
```

#### Étape 4 : Démarrer le Backend
```bash
cd extension_finale/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Vérifier : `curl http://localhost:8000/health`

#### Étape 5 : Démarrer le Site Web
```bash
cd site_web_local/frontend/site-vue
npm install
npm run dev
```

Le site sera accessible sur : `http://localhost:5173` (ou autre port Vite)

#### Étape 6 : Charger l'Extension Chrome
1. Ouvrir Chrome : `chrome://extensions/`
2. Activer "Mode développeur"
3. Cliquer "Charger l'extension non empaquetée"
4. Sélectionner : `extension_finale/extensions`

### Option 2 : Avec Docker Compose (Tout automatisé)

#### Utiliser le docker-compose créé
```bash
cd site_web_local
docker-compose up -d
```

Cela démarre automatiquement :
- MongoDB sur port 27017
- Backend sur port 8000
- Frontend sur port 80

## 🧪 Tests de Connexion

### Test 1 : Backend ↔ MongoDB
```bash
curl http://localhost:8000/health
# Réponse attendue : {"status": "healthy"}
```

### Test 2 : Backend ↔ API Brands
```bash
# Lister toutes les marques
curl http://localhost:8000/brands/

# Récupérer une marque spécifique
curl http://localhost:8000/brands/name/veja
```

### Test 3 : Site Web ↔ Backend
Ouvrir la console du navigateur (F12) :
```javascript
// Test direct
fetch('http://localhost:8000/brands/')
  .then(r => r.json())
  .then(console.log)

// Test via proxy (en développement)
fetch('/api/brands/')
  .then(r => r.json())
  .then(console.log)
```

### Test 4 : Extension ↔ Backend
1. Charger l'extension
2. Aller sur un site e-commerce (ex: Galeries Lafayette)
3. Ouvrir la console Chrome (F12)
4. Vérifier les logs : `[GreenStyle Background]`

## 🔍 Architecture de Connexion

```
┌─────────────────────────────────────────────────────────────┐
│  Extension Chrome                                           │
│  extension_finale/extensions/background.js                  │
│  API_BASE_URL = 'http://localhost:8000'                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTP GET /brands/name/{brand}
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Site Web (Vue.js)                                          │
│  site_web_local/frontend/site-vue/                          │
│  fetch('/api/brands/') → Proxy Vite → http://localhost:8000│
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTP GET /brands/
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend API (FastAPI)                                      │
│  extension_finale/src/main.py                               │
│  Port : 8000                                                │
│  CORS : allow_origins=["*"]                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ MongoDB Client
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  MongoDB                                                     │
│  Base de données : greenstyle_DB                            │
│  Collection : brands                                         │
│  Port : 27017                                               │
└─────────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration des Variables d'Environnement

### Backend (`extension_finale/src/.env`)
```env
MONGO_URL=mongodb://localhost:27017/greenstyle
MONGO_DB=greenstyle_DB
```

### Frontend (`site_web_local/frontend/site-vue/.env`)
```env
VITE_API_URL=http://localhost:8000
```

**Note :** En développement, cette variable n'est pas nécessaire car le proxy Vite gère automatiquement.

## 🚨 Problèmes Courants et Solutions

### Problème : "Network Error" dans le site web

**Cause :** Le backend n'est pas démarré ou n'est pas accessible.

**Solution :**
1. Vérifier que le backend est démarré : `curl http://localhost:8000/health`
2. Vérifier les logs du backend
3. Vérifier la variable `VITE_API_URL` dans `.env`

### Problème : "CORS Error"

**Cause :** Le backend bloque les requêtes cross-origin.

**Solution :**
Le backend est déjà configuré avec `allow_origins=["*"]`. Si problème persiste :
- Vérifier que le backend est sur le port 8000
- Vérifier que CORS est bien activé dans `src/main.py`

### Problème : Extension ne trouve pas les marques

**Cause :** Le backend n'est pas accessible ou MongoDB n'est pas connecté.

**Solution :**
1. Vérifier que le backend est démarré
2. Vérifier les logs dans Chrome DevTools (F12)
3. Vérifier l'URL dans `background.js` : `http://localhost:8000`

### Problème : MongoDB non connecté

**Cause :** MongoDB n'est pas démarré ou les variables d'environnement sont incorrectes.

**Solution :**
1. Démarrer MongoDB : `mongod` ou `brew services start mongodb-community`
2. Vérifier la connexion : `mongosh --eval "db.adminCommand('ping')"`
3. Vérifier les variables d'environnement : `MONGO_URL`, `MONGO_DB`

## ✅ Checklist de Connexion

Avant de démarrer, vérifier :

- [ ] MongoDB est démarré et accessible
- [ ] Base de données `greenstyle_DB` existe
- [ ] Collection `brands` existe
- [ ] Données sont importées (via `scripts/import_brands_data.py`)
- [ ] Backend est démarré sur port 8000
- [ ] Backend peut se connecter à MongoDB
- [ ] Site web a accès au backend (test avec curl)
- [ ] Extension peut accéder au backend
- [ ] CORS est configuré dans le backend

## 📝 Résumé des Fichiers Modifiés

1. ✅ `site_web_local/frontend/site-vue/src/api/http.ts` - Configuration dynamique de l'URL
2. ✅ `site_web_local/site-vue/src/api/http.ts` - Même modification
3. ✅ `site_web_local/frontend/nginx/default.conf` - Configuration proxy Nginx
4. ✅ `extension_finale/Dockerfile` - Dockerfile pour le backend
5. ✅ `site_web_local/docker-compose.yml` - Configuration Docker Compose complète

## 🎯 Test Rapide

Pour tester rapidement que tout est connecté :

```bash
# Terminal 1 : MongoDB
mongod

# Terminal 2 : Backend
cd extension_finale/src && uvicorn main:app --reload --port 8000

# Terminal 3 : Site Web
cd site_web_local/frontend/site-vue && npm run dev

# Navigateur : Tester
# 1. Ouvrir http://localhost:5173 (ou le port affiché par Vite)
# 2. Ouvrir la console (F12)
# 3. Exécuter : fetch('/api/brands/').then(r => r.json()).then(console.log)
# 4. Vérifier que les marques sont retournées
```

Tous les composants sont maintenant correctement configurés pour se connecter !


