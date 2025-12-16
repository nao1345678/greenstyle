# 🚀 Démonstration du Brand Scraper

## 📋 Vue d'ensemble

Ce projet contient une IA pour scraper les sites marchands et identifier automatiquement les marques présentes sur une page web.

## 🛠️ Fichiers du projet

- `brand_scraper.py` - Script principal CLI
- `advanced_brand_scraper.py` - Version avancée avec support CSV et catégorisation
- `brands_database_fixed.csv` - Base de données de marques avec alias
- `test_brands.py` - Script de test et démonstration
- `example_usage.py` - Exemples d'utilisation programmatique
- `requirements.txt` - Dépendances Python

## 🎯 Utilisation rapide

### Installation
```bash
pip3 install -r requirements.txt
```

### Utilisation basique
```bash
python3 brand_scraper.py https://example.com
```

### Utilisation avancée avec base de données CSV
```bash
python3 advanced_brand_scraper.py https://example.com --brands brands_database_fixed.csv --verbose
```

## 📊 Exemples de résultats

### Test sur httpbin.org
```bash
python3 advanced_brand_scraper.py https://httpbin.org/html --brands brands_database_fixed.csv
```

**Résultats:**
- 4 marques trouvées
- Catégories: Mode, Électronique, Sport, Luxe
- Marques: calvin klein, microsoft, head, louis vuitton

### Test avec sauvegarde JSON
```bash
python3 brand_scraper.py https://example.com --output results.json --verbose
```

## 🔧 Fonctionnalités

### Version basique (`brand_scraper.py`)
- ✅ Scraping de pages web
- ✅ Détection de marques dans le texte
- ✅ Analyse des liens et images
- ✅ Export JSON
- ✅ Mode verbeux
- ✅ Délais configurables

### Version avancée (`advanced_brand_scraper.py`)
- ✅ Tout de la version basique
- ✅ Support CSV pour la base de données
- ✅ Catégorisation des marques
- ✅ Gestion des alias
- ✅ Analyse par source (texte, liens, images)

## 📈 Base de données de marques

Le fichier `brands_database_fixed.csv` contient 109 marques réparties en 7 catégories:

- **Mode** (20 marques): Nike, Adidas, Zara, H&M, etc.
- **Électronique** (22 marques): Apple, Samsung, Sony, Microsoft, etc.
- **Automobile** (21 marques): BMW, Mercedes, Toyota, Ford, etc.
- **Cosmétiques** (13 marques): L'Oréal, Chanel, Dior, etc.
- **Alimentation** (13 marques): Coca-Cola, Nestlé, Danone, etc.
- **Sport** (7 marques): Wilson, Head, Babolat, etc.
- **Luxe** (13 marques): Louis Vuitton, Gucci, Rolex, etc.

## 🧪 Tests

### Lancer les tests
```bash
python3 test_brands.py
```

### Tests inclus
- ✅ Fonctionnalité basique
- ✅ Marques personnalisées
- ✅ Gestion d'erreurs
- ✅ Mode verbeux

## 💡 Exemples d'utilisation

### 1. Analyse simple
```bash
python3 brand_scraper.py https://www.fnac.com/telephonie/telephones-portables
```

### 2. Analyse avec délai
```bash
python3 brand_scraper.py https://www.amazon.fr --delay 3.0
```

### 3. Analyse avancée avec catégorisation
```bash
python3 advanced_brand_scraper.py https://www.darty.com --brands brands_database_fixed.csv --verbose
```

### 4. Sauvegarde des résultats
```bash
python3 brand_scraper.py https://www.cdiscount.com --output cdiscount_brands.json
```

## 🔍 Comment ça fonctionne

1. **Scraping** : Le script télécharge la page web
2. **Extraction** : Analyse le contenu HTML (texte, liens, images)
3. **Recherche** : Compare avec la base de données de marques
4. **Catégorisation** : Organise les résultats par catégorie
5. **Rapport** : Affiche et sauvegarde les résultats

## ⚠️ Bonnes pratiques

- ✅ Respectez les robots.txt
- ✅ Utilisez des délais appropriés (1-3 secondes)
- ✅ Vérifiez les conditions d'utilisation des sites
- ✅ Testez sur des sites de démonstration d'abord

## 🚀 Prochaines étapes

- [ ] Ajouter plus de marques à la base de données
- [ ] Implémenter la détection de logos par IA
- [ ] Ajouter le support multilingue
- [ ] Créer une interface web
- [ ] Ajouter des métriques de confiance

---

**Note** : Ce projet est à des fins éducatives. Utilisez-le de manière responsable et respectez les conditions d'utilisation des sites web. 