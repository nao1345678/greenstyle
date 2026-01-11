# Guide de Connexion - Backend ↔ Frontend

Ce guide explique comment connecter tous les modules du projet : scraping → MongoDB → FastAPI → Extension Chrome

## Architecture complète

```
┌─────────────────┐
│   Scrapers      │ → Collectent les données de durabilité
│  (Selenium/BS)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CSV/MongoDB    │ → Stocke les marques avec scores
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │ → API REST avec routes /brands
│   (Backend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extension      │ → Détecte marques et affiche scores
│  Chrome         │
└─────────────────┘
```

## Étapes de connexion

### 1. Préparer les données (Scraping → MongoDB)

#### Option A : Via CSV puis import MongoDB
```bash
# 1. Lancer les scrapers pour enrichir le CSV
python3 ai_master_orchestrator.py --test  # Mode test avec 5 marques

# 2. Calculer les scores
python3 score_brands_from_csv.py brands_database_with_recycled_materials.csv

# 3. Importer dans MongoDB (via script Node.js)
cd GreenstyleDataBaseCreate
node setup_database.js
```

#### Option B : Directement via FastAPI
```bash
# Lancer FastAPI et utiliser les endpoints POST /brands
# Les scrapers peuvent appeler directement l'API
```

### 2. Démarrer le Backend FastAPI

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer MongoDB dans src/config.py
# MONGO_URL = "mongodb://localhost:27017/greenstyle"

# Démarrer l'API
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : `http://localhost:8000`

**Endpoints disponibles :**
- `GET /brands` - Liste toutes les marques
- `GET /brands/{brand_id}` - Détails d'une marque par ID
- `GET /brands/name/{brand_name}` - Recherche par nom (pour l'extension)
- `GET /brands/search/{query}` - Recherche partielle
- `POST /brands` - Créer une marque
- `PUT /brands/{brand_id}` - Mettre à jour
- `DELETE /brands/{brand_id}` - Supprimer

**Documentation Swagger :** `http://localhost:8000/docs`

### 3. Installer et configurer l'Extension Chrome

1. **Ouvrir Chrome** → `chrome://extensions/`
2. **Activer le mode développeur** (en haut à droite)
3. **Cliquer sur "Charger l'extension non empaquetée"**
4. **Sélectionner le dossier** `extensions/`

#### Configuration de l'API

Modifier `extensions/content_brand_detection.js` :
```javascript
const API_BASE_URL = 'http://localhost:8000'; // Adapter selon votre config
```

Si l'API est sur un autre serveur :
```javascript
const API_BASE_URL = 'http://votre-serveur:8000';
```

### 4. Tester la connexion complète

1. **Démarrer FastAPI** (étape 2)
2. **Charger l'extension** (étape 3)
3. **Visiter un site e-commerce** (ex: Zalando, ASOS, etc.)
4. **L'extension devrait** :
   - Détecter les marques présentes sur la page
   - Appeler l'API pour récupérer les scores
   - Afficher des badges colorés sur les éléments contenant les marques

**Couleurs des badges :**
- 🟢 **Vert** (#22c55e) : Score 7-10 (Excellent)
- 🟠 **Orange** (#f59e0b) : Score 4-6.9 (Moyen)
- 🔴 **Rouge** (#ef4444) : Score 0-3.9 (Faible)
- ⚪ **Gris** (#808080) : Pas de score disponible

## Structure des données

### Format de réponse API (BrandOut)

```json
{
  "id": "507f1f77bcf86cd799439011",
  "brand_name": "Patagonia",
  "final_score": 8.5,
  "score_color": "#22c55e",
  "score_label": "Excellent",
  "sustainable_materials": 87,
  "certifications": "B Corp, Fair Trade",
  "planet_badge": true,
  "labor_badge": true,
  ...
}
```

## Dépannage

### L'extension ne détecte pas les marques
- Vérifier que `content_brand_detection.js` est bien chargé (onglet Console)
- Vérifier que les marques sont dans `KNOWN_BRANDS`
- Vérifier les permissions dans `manifest.json`

### L'API ne répond pas
- Vérifier que FastAPI est démarré : `curl http://localhost:8000/brands`
- Vérifier la connexion MongoDB dans `src/config.py`
- Vérifier les logs FastAPI pour les erreurs

### CORS errors
- Ajouter CORS dans `src/main.py` :
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En dev seulement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Les badges ne s'affichent pas
- Ouvrir la Console Chrome (F12) pour voir les erreurs
- Vérifier que l'API retourne bien `score_color`
- Vérifier que les éléments HTML sont bien détectés

## Prochaines étapes

- [ ] Ajouter authentification (clé API pour l'extension)
- [ ] Améliorer la détection de marques (utiliser brand_detection_engine.js complet)
- [ ] Ajouter un popup avec détails complets de la marque
- [ ] Cache local pour éviter trop d'appels API
- [ ] Support des sites e-commerce spécifiques (Zalando, ASOS, etc.)

