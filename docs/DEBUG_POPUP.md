# Débogage du Popup - Extension GreenStyle

## Vérifications à faire

### 1. L'icône de l'extension est-elle visible ?

- Allez sur `chrome://extensions/`
- Vérifiez que l'extension "GreenStyle - Détection de durabilité" est activée
- L'icône devrait apparaître dans la barre d'outils Chrome (à côté de l'adresse)

### 2. Le popup s'ouvre-t-il mais est vide ?

1. Cliquez sur l'icône de l'extension
2. Si une fenêtre popup s'ouvre mais est vide/blanche :
   - Clic droit sur l'icône → "Inspecter le popup"
   - Regardez la console pour les erreurs

### 3. Le popup ne s'ouvre pas du tout ?

**Vérifications :**

1. **Rechargez l'extension** :
   - `chrome://extensions/` → Trouvez GreenStyle → Cliquez sur "Recharger"

2. **Vérifiez les erreurs dans la console du popup** :
   - Clic droit sur l'icône de l'extension → "Inspecter le popup"
   - Regardez s'il y a des erreurs JavaScript

3. **Vérifiez que popup.html existe** :
   ```bash
   ls -la /Users/jm/Desktop/ETH.IA/extensions/popup.html
   ```

4. **Vérifiez le manifest.json** :
   - Le champ `"default_popup": "popup.html"` doit être présent

### 4. Erreurs courantes

**Erreur : "popup.html not found"**
- Vérifiez que le fichier existe dans le dossier `extensions/`
- Rechargez l'extension

**Erreur : "Cannot read property of undefined"**
- Le popup essaie d'accéder à des éléments avant qu'ils ne soient chargés
- Vérifiez la console du popup

**Le popup est vide**
- Ouvrez la console du popup (clic droit → Inspecter)
- Vérifiez les erreurs JavaScript
- Vérifiez que `chrome.storage` fonctionne

### 5. Test manuel du popup

1. Ouvrez `chrome://extensions/`
2. Trouvez l'extension GreenStyle
3. Cliquez sur "Détails"
4. Vérifiez que "Autoriser l'accès aux URL de fichiers" est activé (si vous testez sur file://)
5. Rechargez l'extension

### 6. Console du popup

Pour voir les erreurs du popup :
1. Clic droit sur l'icône de l'extension
2. Sélectionnez "Inspecter le popup"
3. Une fenêtre DevTools s'ouvre avec la console
4. Regardez les erreurs

### 7. Test simple

Créez un popup minimal pour tester :

```html
<!doctype html>
<html>
<head>
  <title>Test</title>
</head>
<body>
  <h1>Popup fonctionne !</h1>
</body>
</html>
```

Si ce popup minimal fonctionne, le problème vient du JavaScript du popup.



