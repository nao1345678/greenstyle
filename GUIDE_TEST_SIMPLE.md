# 🧪 Guide de Test Simple - Extension GreenStyle

## ✅ Vérifications préalables

Avant de tester, assurez-vous que :
- ✅ MongoDB est démarré
- ✅ Le backend FastAPI est actif (port 8000)
- ✅ L'API répond correctement

---

## 📋 Étapes pour Tester

### 1. Charger l'extension dans Chrome

1. **Ouvrez Chrome** et allez sur : `chrome://extensions/`
2. **Activez le "Mode développeur"** (toggle en haut à droite)
3. Cliquez sur **"Charger l'extension non empaquetée"** (ou "Load unpacked")
4. **Sélectionnez le dossier** : `/Users/jm/Desktop/ETH.IA/extensions`
5. L'extension "GreenStyle - Détection de durabilité" devrait apparaître dans la liste
6. **Épinglez l'extension** à la barre d'outils :
   - Cliquez sur l'icône en forme de pièce de puzzle (🧩) dans la barre d'outils
   - Trouvez "GreenStyle" dans la liste
   - Cliquez sur l'épingle (📌) à côté

### 2. Tester avec la page de test

1. **Ouvrez le fichier de test** :
   - Dans Chrome : `Fichier` → `Ouvrir un fichier...`
   - Ou glissez-déposez `test_extension.html` dans Chrome
   - Le chemin devrait être : `file:///Users/jm/Desktop/ETH.IA/test_extension.html`

2. **Attendez 2-3 secondes** pour que le script de détection s'exécute

3. **Cliquez sur l'icône de l'extension** (icône GreenStyle dans la barre d'outils)

4. **Résultat attendu** :
   - Le popup s'ouvre
   - Affiche les marques détectées : Nike, Adidas, Patagonia, Zara, H&M, etc.
   - Pour chaque marque :
     - Score de durabilité (ex: 3.5/10 ou 6.8/10)
     - Jauges "work" et "planet" (barres colorées)
     - Matières durables (%)
     - Certifications
     - Badges planète/travail si applicable

### 3. Tester avec un site réel (optionnel)

1. Visitez un site e-commerce réel :
   - `https://www.nike.com`
   - `https://www.zara.com`
   - `https://www.patagonia.com`

2. Attendez que la page charge complètement

3. Cliquez sur l'icône de l'extension

4. Vous devriez voir les marques détectées avec leurs scores

---

## 🔍 Comment vérifier que ça fonctionne ?

### Indicateurs visuels :

✅ **Popup s'ouvre** → Extension chargée  
✅ **Marques affichées** → Détection fonctionne  
✅ **Scores affichés** → API fonctionne  
✅ **Jauges animées** → Interface fonctionne  

### Indicateurs techniques :

1. **Console du navigateur** (F12) :
   - Onglet "Console"
   - Devrait voir des messages `[GreenStyle]`
   - Pas d'erreurs rouges

2. **Console du service worker** :
   - `chrome://extensions/`
   - Trouvez "GreenStyle"
   - Cliquez sur "Examiner les vues" → "service worker"
   - Devrait voir des logs `[GreenStyle Background]`

3. **Logs du backend** :
   - Dans le terminal : `tail -f /tmp/uvicorn.log`
   - Devrait voir des requêtes `/brands/name/...`
   - Devrait voir "Marque sauvegardée dans MongoDB" pour les nouvelles marques

---

## 🐛 Dépannage rapide

### Le popup ne s'ouvre pas
- Vérifiez que l'extension est bien chargée dans `chrome://extensions/`
- Rechargez l'extension (icône ⟳)
- Vérifiez qu'il n'y a pas d'erreurs (icône rouge)

### Aucune marque détectée
- Vérifiez la console (F12) pour les erreurs
- Attendez quelques secondes après le chargement de la page
- Rechargez la page et réessayez

### Les scores sont "N/A" ou vides
- Vérifiez que le backend est démarré : `curl http://localhost:8000/health`
- Vérifiez que MongoDB est démarré : `ps aux | grep mongod`
- Regardez les logs du backend pour voir les erreurs

### Erreur CORS ou réseau
- Vérifiez que le backend écoute sur `http://localhost:8000`
- Vérifiez les permissions dans `manifest.json`
- Vérifiez la console du service worker pour les détails

---

## 📊 Test complet du flux

1. **Première visite** (marque non dans MongoDB) :
   - Détecte la marque
   - Scrape les données
   - Calcule les scores
   - Sauvegarde dans MongoDB
   - Affiche les résultats

2. **Visite suivante** (marque dans MongoDB) :
   - Détecte la marque
   - Récupère depuis MongoDB (pas de scraping)
   - Affiche les résultats (plus rapide)

---

## ✨ Fonctionnalités à tester

- [ ] Détection automatique des marques
- [ ] Affichage des scores de durabilité
- [ ] Jauges visuelles (work/planet)
- [ ] Matières durables (%)
- [ ] Certifications
- [ ] Badges planète/travail
- [ ] Animations dans le popup
- [ ] Scraping automatique des nouvelles marques
- [ ] Mise en cache (marques déjà scrapées)

---

**Bon test ! 🚀**

