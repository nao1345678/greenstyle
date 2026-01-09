# Où se trouve la Base de Données ?

## 📍 Localisation de la Base de Données

### Configuration Actuelle

La base de données MongoDB est configurée pour se connecter à :
- **URL** : `mongodb://localhost:27017/greenstyle`
- **Nom de la base** : `greenstyle_DB`
- **Port** : `27017` (port par défaut de MongoDB)

### Fichiers de Configuration

1. **Backend** : `extension_finale/src/main.py`
   ```python
   mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/greenstyle")
   db_name = os.getenv("MONGO_DB", "greenstyle_DB")
   ```

2. **Scripts d'initialisation** : `GreenstyleDataBaseCreate/setup_database.js`
   - Crée les collections : `users`, `brands`, `favorites`, `categories`, `alternatives`, `sites`

3. **Docker Compose** : `site_web_local/docker-compose.yml`
   - Configure MongoDB dans un conteneur Docker

## 🚀 Comment Démarrer la Base de Données

### Option 1 : MongoDB Local (Installation manuelle)

**Si MongoDB n'est pas installé :**

```bash
# Sur macOS avec Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Vérifier que MongoDB tourne
mongosh --eval "db.adminCommand('ping')"
```

**Si MongoDB est déjà installé :**

```bash
# Démarrer MongoDB
mongod

# Ou avec Homebrew
brew services start mongodb-community
```

### Option 2 : MongoDB avec Docker (Recommandé)

```bash
# Démarrer MongoDB dans un conteneur Docker
docker run -d \
  --name greenstyle_mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:6.0

# Vérifier que le conteneur tourne
docker ps | grep mongodb
```

### Option 3 : Docker Compose (Tout en un)

```bash
cd site_web_local
docker-compose up -d mongodb
```

## 📦 Initialiser la Base de Données

Une fois MongoDB démarré :

### 1. Créer les Collections

```bash
cd GreenstyleDataBaseCreate
mongosh < setup_database.js
```

Cela crée :
- Collection `brands` (marques)
- Collection `users` (utilisateurs)
- Collection `favorites` (favoris)
- Collection `categories` (catégories)
- Collection `alternatives` (alternatives)
- Collection `sites` (sites web)

### 2. Importer les Marques (282 marques)

```bash
cd extension_finale
python3 scripts/import_brands_data.py
```

## 🔍 Vérifier que la Base de Données Fonctionne

### Vérifier la Connexion

```bash
# Avec mongosh
mongosh
use greenstyle_DB
db.brands.countDocuments()
# Devrait retourner le nombre de marques (282 si importées)

# Ou avec Python
python3 test_mongo.py
```

### Vérifier les Collections

```bash
mongosh greenstyle_DB
show collections
# Devrait afficher : brands, users, favorites, etc.
```

### Compter les Marques

```bash
mongosh greenstyle_DB
db.brands.countDocuments()
# Devrait retourner 282 (ou plus si des marques ont été scrapées)
```

## 📂 Où sont Stockées les Données ?

### Si MongoDB est Local

- **macOS** : `/usr/local/var/mongodb/` (par défaut)
- **Linux** : `/var/lib/mongodb/`
- **Windows** : `C:\data\db\`

### Si MongoDB est dans Docker

Les données sont dans un volume Docker :
```bash
docker volume inspect mongodb_data
```

## ⚙️ Configuration via Variables d'Environnement

Vous pouvez créer un fichier `.env` dans `extension_finale/src/` :

```env
MONGO_URL=mongodb://localhost:27017/greenstyle
MONGO_DB=greenstyle_DB
```

## 🐛 Problèmes Courants

### MongoDB n'est pas démarré

**Symptôme** : Le backend affiche "⚠️ MongoDB non disponible"

**Solution** :
```bash
# Vérifier si MongoDB tourne
ps aux | grep mongod

# Démarrer MongoDB
mongod
# Ou
brew services start mongodb-community
# Ou
docker start greenstyle_mongodb
```

### Port 27017 déjà utilisé

**Symptôme** : Erreur "Address already in use"

**Solution** :
```bash
# Trouver le processus qui utilise le port
lsof -i :27017

# Tuer le processus ou utiliser un autre port
```

### Base de données vide

**Symptôme** : `db.brands.countDocuments()` retourne 0

**Solution** :
```bash
# Réimporter les données
cd extension_finale
python3 scripts/import_brands_data.py
```

## 📊 État Actuel

D'après les tests :
- ✅ **282 marques** sont dans la base de données
- ✅ Les collections sont créées
- ✅ Le scraping automatique ajoute de nouvelles marques à la base

## 🔗 Liens Utiles

- **Documentation MongoDB** : https://docs.mongodb.com/
- **MongoDB Compass** (GUI) : https://www.mongodb.com/products/compass
- **Scripts d'initialisation** : `GreenstyleDataBaseCreate/`

