# Options de Base de Données Physique

## 📊 État Actuel

Actuellement, le projet utilise **MongoDB** qui :
- ✅ Stocke les données **physiquement sur le disque**
- ❌ Nécessite un **serveur MongoDB en cours d'exécution**
- 📍 Emplacement : `/usr/local/var/mongodb/` (si installé localement)

## 🔄 Options Disponibles

### Option 1 : MongoDB (Actuel) - Serveur + Fichiers Physiques

**Comment ça marche :**
- Serveur MongoDB qui tourne en arrière-plan
- Données stockées dans des fichiers sur le disque
- Accès via le port 27017

**Avantages :**
- ✅ Déjà configuré dans le projet
- ✅ Base NoSQL flexible
- ✅ Bon pour les données complexes
- ✅ Supporte les relations (Beanie)

**Inconvénients :**
- ❌ Nécessite d'installer/démarrer MongoDB
- ❌ Prend de la mémoire (serveur qui tourne)
- ❌ Plus complexe à déployer

**Emplacement physique :**
```
/usr/local/var/mongodb/  (macOS avec Homebrew)
/data/db/                (Docker)
```

---

### Option 2 : SQLite - Fichier Unique (Recommandé pour simplicité)

**Comment ça marche :**
- Un seul fichier `.db` contient toute la base
- Pas besoin de serveur
- Fichier dans le projet

**Avantages :**
- ✅ **Pas de serveur à démarrer**
- ✅ **Fichier unique facile à gérer**
- ✅ **Portable** (copier le fichier = copier la base)
- ✅ **Simple à déployer**
- ✅ **Parfait pour le développement**

**Inconvénients :**
- ❌ Moins performant pour très gros volumes
- ❌ Pas de connexions simultanées multiples (limité)
- ❌ Nécessite de migrer le code (MongoDB → SQLite)

**Emplacement physique :**
```
/Users/jm/Desktop/ETH.IA/extension_finale/data/greenstyle.db
```

---

### Option 3 : PostgreSQL/MySQL - Serveur + Fichiers Physiques

**Comment ça marche :**
- Serveur SQL traditionnel
- Données dans des fichiers sur le disque
- Accès via port (5432 pour PostgreSQL, 3306 pour MySQL)

**Avantages :**
- ✅ Base SQL relationnelle puissante
- ✅ Très performant
- ✅ Standard de l'industrie

**Inconvénients :**
- ❌ Nécessite d'installer un serveur
- ❌ Plus complexe que SQLite
- ❌ Nécessite migration complète du code

---

## 💡 Recommandation : SQLite pour Simplicité

Pour avoir une **vraie base de données physique** (fichier) sans serveur, **SQLite est la meilleure option**.

### Migration vers SQLite

**Ce qu'il faudrait faire :**

1. **Installer SQLAlchemy** (ORM pour SQLite)
2. **Créer les modèles SQL** (au lieu de Beanie/MongoDB)
3. **Adapter les routes** pour utiliser SQLAlchemy
4. **Créer le fichier de base** : `greenstyle.db`

**Exemple de structure :**

```python
# Au lieu de Beanie (MongoDB)
from beanie import Document

# Utiliser SQLAlchemy (SQLite)
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(String, primary_key=True)
    brand_name = Column(String)
    final_score = Column(Float)
    # ...
```

**Fichier physique :**
```
extension_finale/data/greenstyle.db  (un seul fichier !)
```

---

## 🎯 Comparaison Rapide

| Critère | MongoDB | SQLite | PostgreSQL |
|---------|---------|--------|------------|
| **Serveur requis** | ✅ Oui | ❌ Non | ✅ Oui |
| **Fichier physique** | ✅ Oui | ✅ Oui (1 fichier) | ✅ Oui |
| **Facilité** | ⚠️ Moyen | ✅ Très facile | ⚠️ Complexe |
| **Déjà configuré** | ✅ Oui | ❌ Non | ❌ Non |
| **Performance** | ✅ Bonne | ⚠️ Moyenne | ✅ Excellente |
| **Portable** | ⚠️ Non | ✅ Oui | ⚠️ Non |

---

## 🚀 Voulez-vous migrer vers SQLite ?

Si vous voulez une **base de données physique simple** (fichier unique, pas de serveur), je peux :

1. ✅ Créer les modèles SQLAlchemy
2. ✅ Adapter le code pour SQLite
3. ✅ Créer le fichier `greenstyle.db`
4. ✅ Migrer les données existantes

**Avantages immédiats :**
- Pas besoin d'installer MongoDB
- Fichier dans le projet (facile à versionner/backup)
- Démarrage instantané (pas de serveur)

**Dites-moi si vous voulez que je fasse cette migration !**

