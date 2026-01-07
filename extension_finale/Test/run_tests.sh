#!/bin/bash
# Script pour exécuter les tests

set -e

echo "🧪 Exécution des tests GreenStyle"
echo ""

# Vérifier que pytest est installé
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest n'est pas installé"
    echo "📦 Installation des dépendances..."
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    pip install -r "$SCRIPT_DIR/requirements_test.txt"
fi

# Options par défaut
TEST_TYPE="${1:-all}"
COVERAGE="${2:-false}"

# Se placer dans le répertoire parent pour exécuter les tests
cd "$(dirname "$0")/.." || exit

case $TEST_TYPE in
    unit)
        echo "📝 Exécution des tests unitaires..."
        if [ "$COVERAGE" = "true" ]; then
            pytest Test/tests/unit/ --cov=src --cov-report=term-missing
        else
            pytest Test/tests/unit/ -v
        fi
        ;;
    functional)
        echo "🔧 Exécution des tests fonctionnels..."
        if [ "$COVERAGE" = "true" ]; then
            pytest Test/tests/functional/ --cov=src --cov-report=term-missing
        else
            pytest Test/tests/functional/ -v
        fi
        ;;
    integration)
        echo "🔗 Exécution des tests d'intégration..."
        if [ "$COVERAGE" = "true" ]; then
            pytest Test/tests/integration/ --cov=src --cov-report=term-missing
        else
            pytest Test/tests/integration/ -v
        fi
        ;;
    all|*)
        echo "🚀 Exécution de tous les tests..."
        if [ "$COVERAGE" = "true" ]; then
            pytest Test/tests/ --cov=src --cov-report=html --cov-report=term-missing
            echo ""
            echo "📊 Rapport de couverture généré dans htmlcov/index.html"
        else
            pytest Test/tests/ -v
        fi
        ;;
esac

echo ""
echo "✅ Tests terminés"

