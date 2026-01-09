#!/bin/bash

# Script de démarrage pour la démonstration GreenStyle
# Ce script démarre MongoDB, le backend et le frontend

set -e

echo "🚀 Démarrage de GreenStyle pour la démonstration..."
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour vérifier si un port est utilisé
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# 1. Vérifier MongoDB
echo "📦 Étape 1/3 : Vérification de MongoDB..."
if check_port 27017; then
    echo -e "${GREEN}✅ MongoDB est déjà démarré sur le port 27017${NC}"
    MONGO_RUNNING=true
else
    echo -e "${YELLOW}⚠️  MongoDB n'est pas démarré${NC}"
    echo "   Options :"
    echo "   1. Installer MongoDB : brew install mongodb-community"
    echo "   2. Démarrer : brew services start mongodb-community"
    echo "   3. Ou utiliser Docker : docker run -d -p 27017:27017 mongo:6.0"
    echo ""
    read -p "Voulez-vous continuer sans MongoDB ? (le backend fonctionnera en mode dégradé) [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Arrêt du script. Veuillez démarrer MongoDB d'abord."
        exit 1
    fi
    MONGO_RUNNING=false
fi

# 2. Démarrer le Backend
echo ""
echo "🔧 Étape 2/3 : Démarrage du Backend FastAPI..."
cd extension_finale/src

# Vérifier les dépendances
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installation des dépendances Python...${NC}"
    pip3 install -r ../requirements.txt
fi

# Vérifier si le port 8000 est libre
if check_port 8000; then
    echo -e "${RED}❌ Le port 8000 est déjà utilisé${NC}"
    echo "   Arrêtez le processus qui utilise ce port ou changez le port dans le script"
    exit 1
fi

echo -e "${GREEN}✅ Démarrage du backend sur http://localhost:8000${NC}"
echo "   Documentation API : http://localhost:8000/docs"
echo "   Health check : http://localhost:8000/health"
echo ""

# Démarrer le backend en arrière-plan
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /tmp/greenstyle_backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend démarré (PID: $BACKEND_PID)"
echo "   Logs : tail -f /tmp/greenstyle_backend.log"

# Attendre que le backend soit prêt
echo "   Attente du démarrage du backend..."
sleep 3

# Vérifier que le backend répond
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend opérationnel${NC}"
else
    echo -e "${RED}❌ Le backend ne répond pas${NC}"
    echo "   Vérifiez les logs : tail -f /tmp/greenstyle_backend.log"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# 3. Démarrer le Frontend
echo ""
echo "🎨 Étape 3/3 : Démarrage du Frontend Vue.js..."
cd ../../site_web_local/frontend/site-vue

# Vérifier node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  Installation des dépendances npm...${NC}"
    npm install
fi

# Vérifier si le port 5173 est libre (ou autre port Vite)
FRONTEND_PORT=5173
if check_port $FRONTEND_PORT; then
    echo -e "${YELLOW}⚠️  Le port $FRONTEND_PORT est utilisé, Vite choisira un autre port${NC}"
fi

echo -e "${GREEN}✅ Démarrage du frontend${NC}"
echo "   Le site sera accessible sur http://localhost:5173 (ou le port affiché)"
echo ""

# Démarrer le frontend en arrière-plan
npm run dev > /tmp/greenstyle_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend démarré (PID: $FRONTEND_PID)"
echo "   Logs : tail -f /tmp/greenstyle_frontend.log"

# Attendre un peu
sleep 5

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Tout est démarré !${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 URLs importantes :"
echo "   • Site Web : http://localhost:5173"
echo "   • API Backend : http://localhost:8000"
echo "   • Documentation API : http://localhost:8000/docs"
echo "   • Health Check : http://localhost:8000/health"
echo ""
echo "📋 Commandes utiles :"
echo "   • Voir les logs backend : tail -f /tmp/greenstyle_backend.log"
echo "   • Voir les logs frontend : tail -f /tmp/greenstyle_frontend.log"
echo "   • Arrêter tout : kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "🎯 Pour la démonstration :"
echo "   1. Ouvrez http://localhost:5173 dans votre navigateur"
echo "   2. Testez la connexion/inscription"
echo "   3. Explorez les marques et leurs scores"
echo "   4. Testez l'extension Chrome (charger extension_finale/extensions/)"
echo ""
echo "⚠️  Pour arrêter les services, appuyez sur Ctrl+C ou exécutez :"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Attendre que l'utilisateur appuie sur Ctrl+C
trap "echo ''; echo '🛑 Arrêt des services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Garder le script actif
wait

