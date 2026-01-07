.PHONY: test test-unit test-functional test-integration test-coverage install-test clean

# Installation des dépendances de test
install-test:
	pip install -r Test/requirements_test.txt

# Exécuter tous les tests
test:
	cd .. && pytest Test/tests/ -v

# Tests unitaires uniquement
test-unit:
	cd .. && pytest Test/tests/unit/ -v -m unit

# Tests fonctionnels uniquement
test-functional:
	cd .. && pytest Test/tests/functional/ -v -m functional

# Tests d'intégration uniquement
test-integration:
	cd .. && pytest Test/tests/integration/ -v -m integration

# Tests avec couverture de code
test-coverage:
	cd .. && pytest Test/tests/ --cov=src --cov-report=html --cov-report=term-missing
	@echo "📊 Rapport de couverture généré dans htmlcov/index.html"

# Nettoyer les fichiers de test
clean:
	find .. -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find .. -type f -name "*.pyc" -delete
	find .. -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf ../htmlcov ../.coverage ../.pytest_cache

# Tests rapides (uniquement unitaires)
test-quick:
	cd .. && pytest Test/tests/unit/ -v --tb=short

# Tests lents (intégration + scraping)
test-slow:
	cd .. && pytest Test/tests/integration/ -v -m integration

