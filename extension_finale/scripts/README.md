# Scripts d'import de données

Ce dossier contient les scripts pour importer des données dans MongoDB.

## Scripts disponibles

### `import_brands_data.py`

Script principal pour importer les données de marques depuis les fichiers JSON et CSV du projet.

**Sources de données :**
- `scrapping/scrapping_v4/data/living_wage.json` - Données sur les salaires décents
- `scrapping/scrapping_v4/data/supply_chain_transparency_data.json` - Données de transparence
- `scrapping/scrapping_v4/data/transparency_scores_simple.json` - Scores de transparence simplifiés
- `brands_database_with_recycled_materials.csv` - Base de données CSV avec matières recyclées
- `brands_database_with_sustainable_materials.csv` - Base de données CSV avec matières durables
- `brands_database_with_production_countries.csv` - Base de données CSV avec pays de production
- `brands_database_fixed.csv` - Base de données CSV corrigée
- `brands_database.csv` - Base de données CSV principale

## Utilisation

### Prérequis

1. MongoDB doit être démarré et accessible
2. Les variables d'environnement doivent être configurées :
   ```bash
   MONGO_URL=mongodb://localhost:27017/greenstyle
   MONGO_DB=greenstyle_DB
   ```

### Exécution

```bash
cd extension_finale
python3 scripts/import_brands_data.py
```

### Ce que fait le script

1. **Connexion à MongoDB** : Se connecte à la base de données `greenstyle_DB`
2. **Import des données JSON** :
   - Living wage : Met à jour le champ `labor_ethics` des marques
   - Transparence : Met à jour le champ `supply_chain_transparency` des marques
3. **Import des données CSV** :
   - Importe toutes les marques depuis les fichiers CSV disponibles
   - Met à jour les champs existants ou crée de nouvelles marques
4. **Résumé** : Affiche un résumé des opérations effectuées

## Structure des données

### Format JSON (living_wage)

```json
{
  "company": "Nike",
  "value": "yes"
}
```

Valeurs possibles :
- `"yes"` → `labor_ethics = 85.0`
- `"partial"` → `labor_ethics = 50.0`
- `"no"` → `labor_ethics = 25.0`

### Format JSON (transparence)

```json
{
  "company": "Patagonia",
  "value": 8.5
}
```

Mapping vers niveaux textuels :
- `>= 8` → "Totale"
- `>= 6` → "Élevée"
- `>= 4` → "Modérée"
- `< 4` → "Faible"

### Format CSV

Le script lit les colonnes suivantes du CSV :
- `brand` / `nom_marque` / `brand_name` : Nom de la marque (requis)
- `sustainable_materials` : Pourcentage de matières durables
- `certifications` : Certifications (texte libre)
- `country_origin` : Pays d'origine
- `country_production` : Pays de production
- `unsold_management` : Gestion des invendus
- `supply_chain_transparency` : Niveau de transparence
- `global_env_impact` : Score d'impact environnemental
- `labor_ethics` : Score d'éthique du travail
- `final_score` : Score final
- `description` : Description de la marque
- `logo` : URL du logo
- `website` : URL du site web

## Notes importantes

- Le script **met à jour** les marques existantes ou **crée** de nouvelles marques
- Les noms de marques sont normalisés (minuscules, trim)
- Les erreurs sont affichées mais n'arrêtent pas l'import
- Le script est idempotent : peut être exécuté plusieurs fois sans problème

## Dépannage

### Erreur de connexion MongoDB

Vérifiez que MongoDB est démarré :
```bash
mongosh --eval "db.adminCommand('ping')"
```

### Aucune donnée importée

Vérifiez que les fichiers de données existent dans les dossiers recherchés :
- `scrapping/scrapping_v4/data/`
- `scrapping/data/`
- `data/`

### Erreurs d'import

Les erreurs sont affichées dans la console mais n'arrêtent pas le processus. Vérifiez les logs pour identifier les problèmes.

