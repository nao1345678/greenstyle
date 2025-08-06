# Brand Scraper - IA pour identifier les marques sur les sites marchands

Un script Python CLI intelligent pour scraper les sites marchands et identifier automatiquement les marques présentes sur une page web.

## 🚀 Fonctionnalités

- **Scraping intelligent** : Analyse le contenu textuel, les liens et les images
- **Base de données de marques** : Plus de 100 marques populaires prédéfinies
- **Respect des sites** : Délais configurables pour éviter la surcharge
- **Export JSON** : Sauvegarde des résultats pour analyse ultérieure
- **Mode verbeux** : Détails sur les sources de détection

## 📦 Installation

1. **Cloner ou télécharger le projet**
```bash
git clone <repository-url>
cd brand-scraper
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

### Utilisation basique
```bash
python brand_scraper.py https://example.com
```

### Options disponibles
```bash
python brand_scraper.py https://example.com --delay 2.0 --output results.json --verbose
```

### Paramètres
- `url` : URL du site à analyser (obligatoire)
- `--delay` : Délai entre les requêtes en secondes (défaut: 1.0)
- `--output` : Fichier de sortie pour les résultats JSON
- `--user-agent` : User-Agent personnalisé
- `--verbose` : Mode détaillé avec statistiques par source

## 📊 Exemples d'utilisation

### Analyser un site e-commerce
```bash
python brand_scraper.py https://www.fnac.com/telephonie/telephones-portables
```

### Analyser avec délai plus long
```bash
python brand_scraper.py https://www.amazon.fr --delay 3.0
```

### Sauvegarder les résultats
```bash
python brand_scraper.py https://www.darty.com --output darty_brands.json
```

### Mode détaillé
```bash
python brand_scraper.py https://www.cdiscount.com --verbose
```

## 🔍 Comment ça fonctionne

Le script analyse la page web de plusieurs façons :

1. **Analyse textuelle** : Recherche les marques dans le contenu visible
2. **Analyse des liens** : Détecte les marques dans les URLs et textes des liens
3. **Analyse des images** : Identifie les marques dans les attributs alt/title des images
4. **Attributs data** : Recherche dans les attributs data-brand et similaires

## 📋 Marques supportées

Le script inclut une base de données de plus de 100 marques populaires :

- **Mode** : Nike, Adidas, Zara, H&M, Levi's, etc.
- **Électronique** : Apple, Samsung, Sony, Microsoft, etc.
- **Automobile** : BMW, Mercedes, Toyota, Ford, etc.
- **Cosmétiques** : L'Oréal, Chanel, Dior, etc.
- **Luxe** : Louis Vuitton, Gucci, Rolex, etc.

## ⚠️ Avertissements

- **Respectez les robots.txt** des sites que vous analysez
- **Utilisez des délais appropriés** pour éviter de surcharger les serveurs
- **Vérifiez les conditions d'utilisation** des sites avant scraping
- **Ce script est à des fins éducatives** et d'analyse

## 🔧 Personnalisation

### Ajouter de nouvelles marques

Modifiez la méthode `_load_brands()` dans `brand_scraper.py` :

```python
def _load_brands(self) -> Set[str]:
    brands = {
        # Vos marques existantes...
        'nouvelle_marque_1', 'nouvelle_marque_2',
    }
    return brands
```

### Charger depuis un fichier

Vous pouvez modifier le script pour charger les marques depuis un fichier CSV :

```python
import pandas as pd

def _load_brands_from_file(self, filename: str) -> Set[str]:
    df = pd.read_csv(filename)
    return set(df['brand'].str.lower().tolist())
```

## 📈 Format de sortie

Les résultats sont affichés dans la console et peuvent être exportés en JSON :

```json
{
  "url": "https://example.com",
  "total_brands_found": 5,
  "brands": ["nike", "adidas", "apple", "samsung", "sony"],
  "brands_in_text": ["nike", "adidas"],
  "brands_in_links": ["apple", "samsung"],
  "brands_in_images": ["sony"],
  "text_length": 15420
}
```

## 🐛 Dépannage

### Erreur de connexion
- Vérifiez votre connexion internet
- Essayez avec un délai plus long
- Vérifiez que l'URL est accessible

### Aucune marque trouvée
- Vérifiez que l'URL est correcte
- Essayez une page produit ou catégorie
- La liste des marques peut être étendue

### Erreur de module
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`

## 📝 Licence

Ce projet est fourni à des fins éducatives. Utilisez-le de manière responsable et respectez les conditions d'utilisation des sites web. 