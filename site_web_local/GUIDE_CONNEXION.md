# Guide de Connexion - Site Web ↔ Backend ↔ Base de données ↔ Extension

## Problèmes identifiés

### ❌ Le site n'est pas connecté au backend

**Problème :** 
- Le site utilise un proxy Vite qui fonctionne uniquement en développement
- Pas de configuration pour la production
- Pas de variable d'environnement pour l'URL du backend

**Solution appliquée :**
- ✅ Ajout de la variable d'environnement `VITE_API_URL`
- ✅ Modification de `http.ts` pour utiliser cette variable
- ✅ Configuration Nginx pour proxy en production

### ❌ Le site n'est pas connecté à la base de données

**Problème :**
- Le site ne se connecte pas directement à MongoDB (normal)
- Le site doit passer par le backend API

**Solution :**
- ✅ Le backend est connecté à MongoDB
- ✅ Le site se connecte au backend via `/api/brands/`

### ❌ L'extension n'est pas connectée au backend

**Problème :**
- L'extension utilise `http://localhost:8000` (correct)
- Mais le backend doit être démarré

**Solution :**
- ✅ Vérifier que le backend est démarré sur port 8000

## Configuration corrigée

### 1. Site Web (frontend/site-vue)

**Fichier modifié :** `src/api/http.ts`

**Avant :**
```typescript
baseURL: '/api',  // Fonctionne uniquement en développement
```

**Après :**
```typescript
// Utilise VITE_API_URL si définie, sinon proxy en dev, sinon localhost:8000
const getBaseURL = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  if (import.meta.env.DEV) {
    return '/api'  // Proxy Vite
  }
  return 'http://localhost:8000'
}
```

### 2. Nginx (production)

**Fichier modifié :** `nginx/default.conf`

**Ajouté :** Configuration proxy pour `/api` et `/brands`

### 3. Extension Chrome

**Fichier :** `extension_finale/extensions/background.js`

**Configuration :** ✅ Déjà correcte
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Pour connecter le site

### Étape 1 : Démarrer le backend

```bash
cd extension_finale/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Vérifier : `curl http://localhost:8000/health`

### Étape 2 : Configurer le site web

**Option A : Développement (recommandé)**

```bash
cd site_web_local/frontend/site-vue
npm install
npm run dev
```

Le proxy Vite redirige automatiquement `/api` → `http://localhost:8000`

**Option B : Production avec variable d'environnement**

```bash
cd site_web_local/frontend/site-vue
# Créer .env
echo "VITE_API_URL=http://localhost:8000" > .env
npm install
npm run build
npm run preview
```

### Étape 3 : Tester la connexion

**Dans le navigateur (F12 console) :**
```javascript
// Test API directement
fetch('http://localhost:8000/brands/')
  .then(r => r.json())
  .then(console.log)

// Test via le site
fetch('/api/brands/')
  .then(r => r.json())
  .then(console.log)
```

## Architecture de connexion

```
Extension Chrome
    │
    └─► http://localhost:8000/brands/name/{brand}
           │
           ▼
      Backend FastAPI (:8000)
           │
           ├─► MongoDB (greenstyle_DB)
           │
           └─► Réponse JSON
                    │
                    ▼
           Site Web (Vue.js)
           └─► fetch('/api/brands/')  → Proxy Vite → http://localhost:8000/brands/
```

## Checklist de vérification

- [ ] Backend démarré sur port 8000
- [ ] MongoDB démarré et accessible
- [ ] Base de données `greenstyle_DB` créée
- [ ] Site web configuré avec `.env` (ou proxy Vite en dev)
- [ ] Extension chargée dans Chrome
- [ ] Test de connexion réussi

## Résolution des problèmes

### Le site ne peut pas se connecter au backend

**Erreur :** `Network Error` ou `CORS Error`

**Solutions :**
1. Vérifier que le backend est démarré : `curl http://localhost:8000/health`
2. Vérifier CORS dans le backend (déjà configuré : `allow_origins=["*"]`)
3. Vérifier la variable d'environnement `VITE_API_URL`
4. Vérifier que le proxy Vite fonctionne en développement

### L'extension ne trouve pas les marques

**Erreur :** `404 Not Found` ou `Network Error`

**Solutions :**
1. Vérifier que le backend est démarré
2. Vérifier l'URL dans `background.js` : `http://localhost:8000`
3. Vérifier les logs dans Chrome DevTools (F12)

### MongoDB n'est pas connecté

**Erreur :** `503 Service Unavailable` ou erreur de connexion MongoDB

**Solutions :**
1. Démarrer MongoDB : `mongod` ou `brew services start mongodb-community`
2. Vérifier la connexion : `mongosh --eval "db.adminCommand('ping')"`
3. Vérifier les variables d'environnement : `MONGO_URL`, `MONGO_DB`

## Exemple de configuration complète

### Terminal 1 : MongoDB
```bash
mongod
```

### Terminal 2 : Backend
```bash
cd extension_finale/src
MONGO_URL=mongodb://localhost:27017/greenstyle
MONGO_DB=greenstyle_DB
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3 : Site Web
```bash
cd site_web_local/frontend/site-vue
npm run dev
```

### Chrome : Extension
1. Charger l'extension depuis `extension_finale/extensions`
2. Aller sur un site e-commerce
3. Vérifier que les marques sont détectées

## Résumé des modifications

1. ✅ `frontend/site-vue/src/api/http.ts` - Ajout de la configuration dynamique
2. ✅ `site-vue/src/api/http.ts` - Même modification
3. ✅ `frontend/nginx/default.conf` - Ajout du proxy pour `/api`
4. ✅ Documentation complète dans `CONFIGURATION_CONNEXION.md`

Maintenant le site peut se connecter au backend en développement ET en production !


