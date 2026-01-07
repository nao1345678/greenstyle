# Guide des Tests - Extension GreenStyle

Ce répertoire contient tous les tests pour l'extension GreenStyle.

## Structure

```
Test/
├── tests/
│   ├── unit/              # Tests unitaires
│   │   ├── test_score_color.py
│   │   ├── test_brand_data_fallback.py
│   │   └── test_calcul_score.py
│   ├── functional/        # Tests fonctionnels
│   │   ├── test_brand_routes.py
│   │   └── test_scraper_service.py
│   ├── integration/       # Tests d'intégration
│   │   └── test_api_integration.py
│   ├── extension/         # Tests pour l'extension Chrome
│   │   └── test_brand_detection.js
│   ├── conftest.py        # Configuration pytest
│   └── README.md
├── pytest.ini
├── requirements_test.txt
├── Makefile
└── run_tests.sh
```

## Installation

Installer les dépendances de test :

```bash
cd extension_finale
pip install -r Test/requirements_test.txt
```

## Exécution des tests

### Méthode 1 : Avec Makefile (recommandé)

```bash
cd extension_finale/Test

# Installer les dépendances
make install-test

# Exécuter tous les tests
make test

# Tests unitaires uniquement
make test-unit

# Tests fonctionnels uniquement
make test-functional

# Tests d'intégration uniquement
make test-integration

# Tests avec couverture de code
make test-coverage

# Tests rapides (uniquement unitaires)
make test-quick

# Nettoyer les fichiers de test
make clean
```

### Méthode 2 : Avec le script shell

```bash
cd extension_finale/Test

# Tous les tests
./run_tests.sh

# Tests unitaires
./run_tests.sh unit

# Tests fonctionnels
./run_tests.sh functional

# Tests d'intégration
./run_tests.sh integration

# Avec couverture
./run_tests.sh all true
```

### Méthode 3 : Directement avec pytest

```bash
# Tous les tests
pytest

# Tests unitaires uniquement
pytest tests/unit/

# Tests fonctionnels uniquement
pytest tests/functional/

# Tests d'intégration uniquement
pytest tests/integration/

# Tests avec couverture de code
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/unit/test_score_color.py
pytest tests/functional/test_brand_routes.py::TestBrandRoutes::test_create_brand
```

## Types de tests

### Tests unitaires

Testent les fonctions individuelles en isolation :
- `test_score_color.py` : Tests pour les fonctions de couleur et label de score
- `test_brand_data_fallback.py` : Tests pour la base de données de fallback
- `test_calcul_score.py` : Tests pour le calcul des scores de durabilité

### Tests fonctionnels

Testent les fonctionnalités complètes :
- `test_brand_routes.py` : Tests pour toutes les routes API de marques
- `test_scraper_service.py` : Tests pour le service de scraping

### Tests d'intégration

Testent le flux complet de bout en bout :
- `test_api_integration.py` : Tests du workflow complet de l'API

### Tests d'extension

Tests pour l'extension Chrome (JavaScript) :
- `test_brand_detection.js` : Tests pour la détection de marques

## Configuration MongoDB

Les tests peuvent fonctionner avec ou sans MongoDB. Si MongoDB n'est pas disponible, certains tests seront ignorés.

Pour utiliser MongoDB dans les tests :

```bash
export MONGO_TEST_URL="mongodb://localhost:27017"
```

## Marqueurs pytest

- `@pytest.mark.unit` : Tests unitaires
- `@pytest.mark.functional` : Tests fonctionnels
- `@pytest.mark.integration` : Tests d'intégration
- `@pytest.mark.slow` : Tests lents
- `@pytest.mark.requires_mongo` : Tests nécessitant MongoDB

Exemple :

```bash
# Exécuter uniquement les tests unitaires
pytest -m unit

# Exclure les tests lents
pytest -m "not slow"
```

## Fixtures disponibles

- `client` : Client HTTP AsyncClient pour les tests d'API
- `test_db` : Base de données MongoDB de test
- `sample_brand_data` : Données de test pour une marque générique
- `sample_brand_data_veja` : Données de test pour Veja

## Exemples d'utilisation

### Test unitaire simple

```python
def test_get_score_color():
    from utils.score_color import get_score_color
    assert get_score_color(8.0) == "green"
```

### Test fonctionnel

```python
@pytest.mark.asyncio
async def test_create_brand(client, sample_brand_data):
    response = await client.post("/brands/", json=sample_brand_data)
    assert response.status_code == 200
```

## Tests JavaScript (Extension Chrome)

Pour tester l'extension Chrome, installer Jest :

```bash
cd extension_finale/Test/tests
npm install
npm test
```

Ou avec couverture :

```bash
npm run test:coverage
```

## Notes importantes

1. Les tests d'API utilisent `httpx.AsyncClient` pour tester FastAPI
2. Les tests peuvent fonctionner sans MongoDB (certains seront ignorés)
3. Les tests de scraping peuvent être lents (utiliser `@pytest.mark.slow`)
4. Les tests d'extension JavaScript nécessitent Jest ou un environnement Node.js
5. Le Makefile et le script `run_tests.sh` facilitent l'exécution des tests
6. La couverture de code est générée dans `htmlcov/index.html` après `make test-coverage`

