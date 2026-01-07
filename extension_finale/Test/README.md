# Dossier Test - Extension GreenStyle

Ce dossier contient tous les fichiers de tests pour l'extension GreenStyle.

## Structure

```
Test/
├── tests/                    # Répertoire principal des tests
│   ├── unit/                 # Tests unitaires
│   ├── functional/           # Tests fonctionnels
│   ├── integration/          # Tests d'intégration
│   ├── extension/            # Tests pour l'extension Chrome
│   └── conftest.py           # Configuration pytest
├── pytest.ini                # Configuration pytest
├── requirements_test.txt      # Dépendances Python pour les tests
├── Makefile                  # Commandes Make pour les tests
├── run_tests.sh              # Script shell pour exécuter les tests
└── README.md                 # Ce fichier
```

## Installation

Depuis le répertoire `extension_finale/` :

```bash
pip install -r Test/requirements_test.txt
```

## Exécution des tests

### Depuis extension_finale/Test/

```bash
cd extension_finale/Test

# Avec Makefile
make install-test
make test
make test-coverage

# Avec le script shell
./run_tests.sh
./run_tests.sh unit
./run_tests.sh all true
```

### Depuis extension_finale/

```bash
cd extension_finale

# Avec pytest directement
pytest Test/tests/ -v
pytest Test/tests/unit/ -v
pytest Test/tests/ --cov=src --cov-report=html
```

## Documentation détaillée

Consultez `Test/tests/README.md` pour une documentation complète sur les tests.



