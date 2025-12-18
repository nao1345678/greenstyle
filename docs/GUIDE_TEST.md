# Guide de Test - Extension GreenStyle

## Étape 1 : Démarrer le serveur backend

Ouvrez un terminal et lancez :

```bash
cd /Users/jm/Desktop/ETH.IA/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Vous devriez voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ MongoDB connecté
```

**Vérification** : Ouvrez `http://localhost:8000/docs` dans votre navigateur pour voir la documentation de l'API.

---

## Étape 2 : Charger l'extension dans Chrome

1. **Ouvrez Chrome**
2. **Allez sur** `chrome://extensions/`
3. **Activez le "Mode développeur"** (toggle en haut à droite)
4. **Cliquez sur "Charger l'extension non empaquetée"**
5. **Sélectionnez le dossier** : `/Users/jm/Desktop/ETH.IA/extensions`
6. **L'extension apparaît** dans la barre d'outils avec l'icône 🌱

---

## Étape 3 : Tester sur une vraie page web

### Option A : Site e-commerce réel

1. **Visitez un site e-commerce** avec des marques de mode :
   - Zalando : https://www.zalando.fr/
   - ASOS : https://www.asos.com/
   - Amazon Fashion : https://www.amazon.fr/fashion
   - Vinted : https://www.vinted.fr/

2. **Ouvrez la console développeur** (F12) pour voir les logs :
   - Vous devriez voir : `[GreenStyle] Marques détectées: nike, adidas, ...`

3. **Cliquez sur l'icône de l'extension** dans la barre d'outils

4. **Le popup s'ouvre** et affiche :
   - La page analysée
   - Les marques détectées avec leurs scores de durabilité

### Option B : Page de test locale

1. **Ouvrez le fichier** `/Users/jm/Desktop/ETH.IA/test_page.html` dans Chrome
   - Fichier → Ouvrir un fichier → Sélectionnez `test_page.html`

2. **L'extension détecte automatiquement** les marques sur la page

3. **Cliquez sur l'icône de l'extension** pour voir les résultats

---

## Étape 4 : Vérifier que tout fonctionne

### ✅ Checklist

- [ ] Le serveur FastAPI est lancé et répond sur `http://localhost:8000`
- [ ] L'extension est chargée dans Chrome (visible dans `chrome://extensions/`)
- [ ] L'icône de l'extension apparaît dans la barre d'outils
- [ ] Sur une page avec des marques, la console affiche les marques détectées
- [ ] Le popup affiche les marques avec leurs scores

### 🔍 Dépannage

**Le popup est vide ?**
- Vérifiez que le serveur backend est bien lancé
- Ouvrez la console (F12) et regardez les erreurs
- Vérifiez que l'API répond : `curl http://localhost:8000/`

**Aucune marque détectée ?**
- Vérifiez que la page contient bien des marques connues (Nike, Adidas, Zara, etc.)
- Ouvrez la console pour voir les logs `[GreenStyle]`
- Les marques doivent être dans la liste `KNOWN_BRANDS` du code

**Erreur CORS ?**
- L'API a CORS activé pour toutes les origines en développement
- Vérifiez que `allow_origins=["*"]` est dans `src/main.py`

**MongoDB non connecté ?**
- L'API fonctionne sans MongoDB mais retournera 404 pour les marques
- Pour avoir des données, importez-les via les scripts dans `GreenstyleDataBaseCreate/`

---

## Test rapide

1. **Lancez le serveur** : `cd src && uvicorn main:app --reload`
2. **Chargez l'extension** dans Chrome
3. **Visitez** : https://www.zalando.fr/
4. **Cliquez sur l'icône** de l'extension
5. **Vous devriez voir** les marques détectées !

---

## Commandes utiles

```bash
# Vérifier que le serveur répond
curl http://localhost:8000/

# Tester une marque dans l'API
curl http://localhost:8000/brands/name/nike

# Voir les logs du serveur
# (dans le terminal où uvicorn est lancé)
```



