# 🧪 Guide de Test Rapide - Extension GreenStyle

## ✅ Vérifications préalables

- ✅ Backend API actif sur http://localhost:8000
- ✅ Extension dans `extension_finale/extensions/`
- 
---

## 📋 Étapes pour Tester

### 1. Charger l'extension dans Chrome

1. **Ouvrez Chrome** et allez sur : `chrome://extensions/`
2. **Activez le "Mode développeur"** (toggle en haut à droite)
3. Cliquez sur **"Charger l'extension non empaquetée"** (ou "Load unpacked")
4. **Sélectionnez le dossier** : 
   ```
   /Users/jm/Desktop/ETH.IA/extension_finale/extensions
   ```
5. L'extension "GreenStyle - Détection de durabilité" devrait apparaître
6. **Épinglez l'extension** à la barre d'outils (icône 🧩 → trouver GreenStyle → 📌)

### 2. Tester sur un site e-commerce réel

#### Option A : Galeries Lafayette (test avec UGG)
1. Visitez : `https://www.galerieslafayette.com/p/bottines+neumel+en+cuir-ugg/2013117726471/320`
2. **Attendez 2-3 secondes** pour que la détection s'exécute
3. **Cliquez sur l'icône GreenStyle** dans la barre d'outils
4. **Résultat attendu** :
   - La marque "UGG" devrait être détectée
   - Score de durabilité affiché
   - Jauges "work" et "planet"

#### Option B : Site Nike
1. Visitez : `https://www.nike.com`
2. Naviguez sur une page produit
3. Cliquez sur l'icône de l'extension
4. Vérifiez que "Nike" est détecté avec son score

#### Option C : Site Patagonia (marque engagée)
1. Visitez : `https://www.patagonia.com`
2. Cliquez sur l'icône de l'extension
3. **Résultat attendu** :
   - Score élevé (8-9/10)
   - Badges "Planet" et "Labor" si applicable
   - Certifications affichées

### 3. Vérifier les fonctionnalités

#### ✅ Détection de marques
- Les marques présentes sur la page sont détectées automatiquement
- Les marques apparaissent dans le popup

#### ✅ Affichage des scores
- Score final (ex: 8.7/10)
- Jauge "Planet" (impact environnemental)
- Jauge "Work" (éthique du travail)
- Couleur du score (vert = excellent, orange = moyen, rouge = faible)

#### ✅ Informations détaillées
- Matières durables (%)
- Certifications (Fair Trade, B-Corp, etc.)
- Pays de production
- Gestion des invendus

#### ✅ Données de fallback
- Les marques engagées (Veja, Patagonia, etc.) ont des données précises même sans scraping
- Les scores sont corrects pour ces marques

---

## 🔍 Debugging

### Console Chrome DevTools

1. **Ouvrez les DevTools** : `F12` ou `Cmd+Option+I`
2. **Onglet Console** pour voir les logs :
   - `[GreenStyle Background]` - Logs du service worker
   - `[GreenStyle Popup]` - Logs du popup
   - `[GreenStyle Content]` - Logs du content script

### Vérifier l'API

Testez directement l'API :
```bash
# Test Veja (marque engagée avec fallback)
curl http://localhost:8000/brands/name/veja

# Test Nike
curl http://localhost:8000/brands/name/nike

# Test UGG
curl http://localhost:8000/brands/name/ugg
```

### Problèmes courants

#### ❌ Extension ne détecte pas de marques
- Vérifiez que le content script s'exécute (Console DevTools)
- Vérifiez que l'extension a les permissions nécessaires
- Rechargez la page après avoir chargé l'extension

#### ❌ Scores ne s'affichent pas
- Vérifiez que l'API backend est accessible : `http://localhost:8000`
- Vérifiez les logs dans la console du service worker
- Testez l'API directement avec curl

#### ❌ Erreur 503 (MongoDB non disponible)
- C'est normal si MongoDB n'est pas démarré
- L'extension utilise le mode démo ou le scraping direct
- Les marques avec fallback (Veja, Patagonia) fonctionnent toujours

---

## 📊 Marques de test recommandées

### Marques avec données de fallback (scores précis)
- **Veja** : Score ~8.7/10 (Excellent)
- **Patagonia** : Score ~9.0/10 (Excellent)
- **Reformation** : Score ~8.5/10 (Excellent)
- **Everlane** : Score ~8.0/10 (Très bon)
- **Allbirds** : Score ~8.2/10 (Très bon)

### Marques à tester (scraping)
- **Nike** : Score variable selon scraping
- **Adidas** : Score variable selon scraping
- **Zara** : Score généralement faible (fast fashion)
- **H&M** : Score généralement faible (fast fashion)
- **UGG** : Score variable selon scraping

---

## ✅ Checklist de test

- [ ] Extension chargée dans Chrome
- [ ] Extension épinglée à la barre d'outils
- [ ] Backend API accessible (http://localhost:8000)
- [ ] Détection de marques fonctionne
- [ ] Scores s'affichent correctement
- [ ] Jauges "Planet" et "Work" visibles
- [ ] Certifications affichées
- [ ] Marques engagées (Veja, Patagonia) ont de bons scores
- [ ] Console DevTools sans erreurs critiques

---

**Bon test ! 🚀**


