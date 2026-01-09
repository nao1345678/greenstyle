# Explication du Système de Scraping Automatique

## 📊 État Actuel de la Base de Données

D'après les tests effectués, la base de données contient actuellement **282 marques** pré-chargées avec leurs scores de durabilité.

## 🔄 Fonctionnement du Scraping Automatique

### Quand une marque n'est PAS dans la base de données :

1. **Recherche dans MongoDB** : Le système cherche d'abord la marque dans la base de données MongoDB
2. **Si non trouvée** : Le scraping automatique est lancé (si `auto_scrape=True`, ce qui est le cas par défaut)
3. **Scraping des données** : Le système utilise plusieurs sources :
   - Base de données de fallback (marques connues)
   - Scrapers spécialisés (matières recyclées, certifications, etc.)
   - Analyse du site web de la marque
   - APIs externes (si disponibles)
4. **Calcul des scores** : Les scores sont calculés automatiquement :
   - Impact environnemental (sur 10)
   - Éthique du travail (sur 10)
   - Score final (moyenne des deux)
5. **Sauvegarde dans MongoDB** : La marque est **automatiquement ajoutée** à la base de données avec toutes ses données et scores

### Code concerné :

```python
# Dans extension_finale/src/routes/brand_routes.py

@router.get("/name/{brand_name}", response_model=BrandOut)
async def get_brand_by_name(brand_name: str, auto_scrape: bool = True):
    # 1. Chercher dans MongoDB
    existing_brand = await Brand.find_one(...)
    
    if existing_brand:
        return to_out(existing_brand)  # Retourner la marque existante
    
    # 2. Si non trouvée, scraper automatiquement
    if not existing_brand and auto_scrape:
        scraped_data = await scrape_brand_data(brand_name)
        scores = calculate_scores(scraped_data)
        scraped_data.update(scores)
        
        # 3. Sauvegarder dans MongoDB
        if mongo_available:
            brand = Brand(**scraped_data)
            await brand.insert()  # ✅ AJOUTÉ À LA BASE DE DONNÉES
            print(f"✅ Marque '{brand_name}' sauvegardée dans MongoDB")
        
        return BrandOut(**scraped_data)
```

## ✅ Réponses à vos Questions

### 1. Est-ce que toutes les marques sont dans la base de données ?

**Non**, pas toutes les marques du monde. La base contient actuellement **282 marques** pré-chargées. Mais le système peut gérer n'importe quelle marque grâce au scraping automatique.

### 2. Si une marque n'est pas dans la base, un scraping est lancé ?

**Oui, exactement !** Voici le processus :

1. L'utilisateur cherche une marque (via l'extension ou le site web)
2. Le système cherche dans MongoDB
3. Si **non trouvée** → Scraping automatique lancé
4. Les données sont collectées (certifications, matières, pays de production, etc.)
5. Les scores sont calculés automatiquement
6. La marque est **ajoutée à MongoDB** pour les prochaines fois

### 3. La marque scrapée est-elle ajoutée à la base de données ?

**Oui, absolument !** Ligne 254-256 du code :
```python
brand = Brand(**scraped_data)
await brand.insert()  # ✅ Sauvegarde dans MongoDB
```

Cela signifie que :
- La première fois qu'une marque est recherchée, elle est scrapée et sauvegardée
- Les fois suivantes, elle est récupérée directement depuis MongoDB (plus rapide)

## 🎯 Exemple Concret

**Scénario** : Un utilisateur cherche la marque "Nike" qui n'est pas dans la base

1. **Requête** : `GET /brands/name/nike?auto_scrape=true`
2. **Recherche MongoDB** : Non trouvée
3. **Scraping lancé** :
   - Recherche des certifications (B-Corp, etc.)
   - Analyse des matières durables
   - Recherche du pays de production
   - Analyse de la gestion des invendus
4. **Calcul des scores** :
   - Impact environnemental : 6.5/10
   - Éthique du travail : 7.0/10
   - Score final : 6.75/10
5. **Sauvegarde** : Nike est ajoutée à MongoDB avec tous ses scores
6. **Prochaine fois** : Nike sera récupérée directement depuis MongoDB (instantané)

## ⚙️ Configuration

Le scraping automatique est activé par défaut (`auto_scrape=True`). Pour le désactiver :

```bash
# Avec scraping automatique (défaut)
GET /brands/name/nike?auto_scrape=true

# Sans scraping automatique
GET /brands/name/nike?auto_scrape=false
```

## 📝 Notes Importantes

- Le scraping peut prendre quelques secondes (5-10 secondes)
- Si MongoDB n'est pas disponible, les données sont scrapées mais **non sauvegardées**
- Les marques scrapées sont disponibles immédiatement pour l'utilisateur qui les a demandées
- Les autres utilisateurs bénéficient ensuite de ces marques déjà scrapées dans la base

