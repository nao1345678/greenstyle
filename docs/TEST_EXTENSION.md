# Guide de Test de l'Extension Chrome

## Prérequis

1. **Python 3.9+** installé
2. **MongoDB** installé et démarré (optionnel - l'API fonctionne sans)
3. **Chrome/Chromium** avec accès aux extensions développeur

## Étape 1 : Installer les dépendances du backend

```bash
pip3 install -r requirements_backend.txt
```

## Étape 2 : Démarrer le serveur FastAPI

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : `http://localhost:8000`

### Vérifier que l'API fonctionne

Ouvrez dans votre navigateur : `http://localhost:8000/docs`

Vous devriez voir la documentation interactive de l'API Swagger.

## Étape 3 : Charger l'extension dans Chrome

1. Ouvrez Chrome
2. Allez dans `chrome://extensions/`
3. Activez le **Mode développeur** (toggle en haut à droite)
4. Cliquez sur **Charger l'extension non empaquetée**
5. Sélectionnez le dossier `/Users/jm/Desktop/ETH.IA/extensions`
6. L'extension devrait apparaître dans la barre d'outils

## Étape 4 : Tester la détection de marques

### Test 1 : Page avec marques connues

1. Visitez un site e-commerce avec des marques (ex: Zalando, ASOS, etc.)
2. Ouvrez la console développeur (F12) pour voir les logs
3. L'extension devrait détecter automatiquement les marques présentes
4. Cliquez sur l'icône de l'extension pour voir le popup
5. Vous devriez voir les marques détectées avec leurs scores

### Test 2 : Page de test HTML

Créez un fichier HTML simple avec des marques :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test GreenStyle</title>
</head>
<body>
    <h1>Boutique de Mode</h1>
    <div>
        <h2>Nike Air Max</h2>
        <p>Chaussures de sport Nike</p>
    </div>
    <div>
        <h2>Adidas Originals</h2>
        <p>Collection Adidas</p>
    </div>
    <div>
        <h2>Zara</h2>
        <p>Mode Zara</p>
    </div>
</body>
</html>
```

Ouvrez ce fichier dans Chrome et testez l'extension.

## Étape 5 : Vérifier les données dans l'API

### Tester l'endpoint de recherche de marque

```bash
# Rechercher une marque par nom
curl http://localhost:8000/brands/name/nike

# Lister toutes les marques
curl http://localhost:8000/brands
```

## Dépannage

### L'extension ne détecte pas les marques

- Vérifiez que le serveur FastAPI est bien démarré sur le port 8000
- Ouvrez la console développeur (F12) et regardez les erreurs
- Vérifiez que l'API répond : `curl http://localhost:8000/`

### Erreur CORS

- L'API a CORS activé pour toutes les origines en développement
- Vérifiez que `allow_origins=["*"]` est bien dans `src/main.py`

### MongoDB non connecté

- L'API fonctionne sans MongoDB mais ne retournera pas de données
- Pour avoir des données, importez-les via les scripts dans `GreenstyleDataBaseCreate/`

### Le popup est vide

- Vérifiez que des marques sont bien présentes sur la page
- Vérifiez la console pour voir les marques détectées
- Vérifiez que l'API retourne bien des données pour ces marques

## Marques de test disponibles

L'extension détecte ces marques par défaut :
- Nike, Adidas, Puma, Reebok, Converse, Vans
- Zara, H&M, Uniqlo, Gap
- Patagonia, Veja, Reformation, Everlane
- Et plus...

Pour ajouter des marques, modifiez le tableau `KNOWN_BRANDS` dans `extensions/content_brand_detection.js`



