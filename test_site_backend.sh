#!/bin/bash
# Script pour tester la connexion Site Web ↔ Backend ↔ Base de données

echo "🧪 Test de Connexion - Site Web ↔ Backend ↔ Base de données"
echo "=" | head -c 60; echo

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1 : Backend est-il démarré ?
echo -e "\n📡 Test 1 : Backend est-il démarré ?"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend accessible sur http://localhost:8000${NC}"
    HEALTH=$(curl -s http://localhost:8000/health | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)
    echo "   Status : $HEALTH"
else
    echo -e "${RED}❌ Backend non accessible${NC}"
    echo "   Démarrer avec : cd extension_finale/src && uvicorn main:app --reload --port 8000"
    exit 1
fi

# Test 2 : Endpoint racine
echo -e "\n📡 Test 2 : Endpoint racine"
ROOT=$(curl -s http://localhost:8000/ 2>&1)
if echo "$ROOT" | grep -q "GreenStyle"; then
    echo -e "${GREEN}✅ Endpoint racine OK${NC}"
    echo "$ROOT" | python3 -m json.tool 2>/dev/null | head -5
else
    echo -e "${RED}❌ Endpoint racine ne fonctionne pas${NC}"
fi

# Test 3 : Liste des marques
echo -e "\n📊 Test 3 : Liste des marques"
BRANDS=$(curl -s http://localhost:8000/brands/ 2>&1)
BRAND_COUNT=$(echo "$BRANDS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ ! -z "$BRAND_COUNT" ] && [ "$BRAND_COUNT" -gt "0" ]; then
    echo -e "${GREEN}✅ ${BRAND_COUNT} marque(s) trouvée(s) dans la base${NC}"
    echo "$BRANDS" | python3 -m json.tool 2>/dev/null | grep -E "brand_name" | head -5
else
    echo -e "${YELLOW}⚠️  Aucune marque dans la base (normal si pas importée)${NC}"
fi

# Test 4 : Marque scrappée (Veja)
echo -e "\n🔍 Test 4 : Marque scrappée - Veja"
VEJA=$(curl -s "http://localhost:8000/brands/name/veja?auto_scrape=true" 2>&1)
if echo "$VEJA" | grep -q "brand_name"; then
    BRAND_NAME=$(echo "$VEJA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('brand_name', 'N/A'))" 2>/dev/null)
    FINAL_SCORE=$(echo "$VEJA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('final_score', 'N/A'))" 2>/dev/null)
    SUSTAINABLE=$(echo "$VEJA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('sustainable_materials', 'N/A'))" 2>/dev/null)
    CERTIFICATIONS=$(echo "$VEJA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('certifications', 'N/A'))" 2>/dev/null)
    
    echo -e "${GREEN}✅ Veja trouvée :${NC}"
    echo "   Nom : $BRAND_NAME"
    echo "   Score final : $FINAL_SCORE"
    echo "   Matières durables : $SUSTAINABLE%"
    echo "   Certifications : $CERTIFICATIONS"
    
    if [ "$SUSTAINABLE" != "None" ] && [ "$SUSTAINABLE" != "null" ] && [ ! -z "$SUSTAINABLE" ]; then
        echo -e "${GREEN}   ✅ Données scrappées complètes${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Données scrappées incomplètes (fallback utilisé)${NC}"
    fi
else
    echo -e "${RED}❌ Veja non trouvée${NC}"
fi

# Test 5 : Marque scrappée (Patagonia)
echo -e "\n🔍 Test 5 : Marque scrappée - Patagonia"
PATAGONIA=$(curl -s "http://localhost:8000/brands/name/patagonia?auto_scrape=true" 2>&1)
if echo "$PATAGONIA" | grep -q "brand_name"; then
    BRAND_NAME=$(echo "$PATAGONIA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('brand_name', 'N/A'))" 2>/dev/null)
    FINAL_SCORE=$(echo "$PATAGONIA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('final_score', 'N/A'))" 2>/dev/null)
    SUSTAINABLE=$(echo "$PATAGONIA" | python3 -c "import sys, json; print(json.load(sys.stdin).get('sustainable_materials', 'N/A'))" 2>/dev/null)
    
    echo -e "${GREEN}✅ Patagonia trouvée :${NC}"
    echo "   Nom : $BRAND_NAME"
    echo "   Score final : $FINAL_SCORE"
    echo "   Matières durables : $SUSTAINABLE%"
    
    if [ "$SUSTAINABLE" != "None" ] && [ "$SUSTAINABLE" != "null" ] && [ ! -z "$SUSTAINABLE" ]; then
        echo -e "${GREEN}   ✅ Données scrappées complètes${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Données scrappées incomplètes${NC}"
    fi
else
    echo -e "${RED}❌ Patagonia non trouvée${NC}"
fi

# Test 6 : Site web est-il démarré ?
echo -e "\n🌐 Test 6 : Site web est-il démarré ?"
VITE_PORT=$(lsof -ti:5173 2>/dev/null || lsof -ti:3000 2>/dev/null || echo "")
if [ ! -z "$VITE_PORT" ]; then
    PORT=$(lsof -ti:5173 2>/dev/null && echo "5173" || echo "3000")
    echo -e "${GREEN}✅ Site web accessible sur http://localhost:${PORT}${NC}"
    
    # Test proxy
    echo -e "\n🔗 Test 7 : Proxy Vite (/api → backend)"
    PROXY_TEST=$(curl -s "http://localhost:${PORT}/api/brands/" 2>&1 | head -5)
    if echo "$PROXY_TEST" | grep -q "brand_name\|\[\]"; then
        echo -e "${GREEN}✅ Proxy fonctionne${NC}"
        echo "   Réponse : $(echo "$PROXY_TEST" | head -2)"
    else
        echo -e "${YELLOW}⚠️  Proxy ne fonctionne pas ou aucune marque${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Site web non démarré${NC}"
    echo "   Démarrer avec : cd site_web_local/frontend/site-vue && npm run dev"
fi

# Test 7 : Extension Chrome
echo -e "\n🧩 Test 8 : Extension Chrome"
EXTENSION_DIR="../extension_finale/extensions"
if [ -f "$EXTENSION_DIR/background.js" ]; then
    echo -e "${GREEN}✅ Extension trouvée dans $EXTENSION_DIR${NC}"
    
    # Vérifier la configuration API
    API_URL=$(grep -o "API_BASE_URL.*=.*['\"].*['\"]" "$EXTENSION_DIR/background.js" | head -1)
    if echo "$API_URL" | grep -q "localhost:8000"; then
        echo -e "${GREEN}   ✅ URL backend configurée : $API_URL${NC}"
    else
        echo -e "${YELLOW}   ⚠️  URL backend : $API_URL${NC}"
    fi
else
    echo -e "${RED}❌ Extension non trouvée${NC}"
fi

echo -e "\n" 
echo "=" | head -c 60; echo
echo "📊 Résumé des Tests"
echo "=" | head -c 60; echo


