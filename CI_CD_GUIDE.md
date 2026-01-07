# Guide CI/CD - Extension GreenStyle

## Qu'est-ce que CI/CD ?

**CI/CD** signifie **Continuous Integration / Continuous Deployment** (Intégration Continue / Déploiement Continu).

### CI - Continuous Integration (Intégration Continue)
- **Objectif** : Automatiser l'exécution des tests à chaque modification du code
- **Quand** : À chaque push ou pull request
- **Avantages** :
  - Détection rapide des bugs
  - Assurance de la qualité du code
  - Confiance dans les modifications

### CD - Continuous Deployment (Déploiement Continu)
- **Objectif** : Déployer automatiquement le code si les tests passent
- **Quand** : Après que tous les tests CI ont réussi
- **Avantages** :
  - Déploiement automatique
  - Réduction des erreurs manuelles
  - Livraison plus rapide

## Configuration CI/CD pour ce projet

### Fichiers créés

1. **`.github/workflows/simple-tests.yml`** : Workflow simple pour les tests
2. **`.github/workflows/tests.yml`** : Workflow avancé avec linting et couverture
3. **`.github/workflows/README.md`** : Documentation des workflows

### Comment ça fonctionne ?

```
┌─────────────────┐
│  Push sur GitHub│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │
│  déclenche le   │
│    workflow     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Installation    │
│  Python + Deps  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Exécution des    │
│     tests        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  ✅ Pass   ❌ Fail
    │         │
    │         └─> Notification d'erreur
    │
    └─> (Optionnel) Déploiement automatique
```

## Activation du CI/CD

### Étape 1 : Créer un dépôt GitHub

```bash
# Si vous n'avez pas encore de dépôt GitHub
git init
git add .
git commit -m "Initial commit avec CI/CD"
git remote add origin https://github.com/votre-username/votre-repo.git
git push -u origin main
```

### Étape 2 : Vérifier les workflows

1. Aller sur votre dépôt GitHub
2. Cliquer sur l'onglet **"Actions"**
3. Vous devriez voir les workflows disponibles

### Étape 3 : Tester

Faire un push pour déclencher les tests :

```bash
git add .
git commit -m "Test CI/CD"
git push
```

Les tests s'exécuteront automatiquement !

## Workflows disponibles

### Workflow Simple (`simple-tests.yml`)

**Recommandé pour commencer**

- ✅ Tests unitaires
- ✅ Tests de scraping
- ✅ Rapide et simple
- ❌ Pas de linting
- ❌ Pas de couverture

**Utilisation :**
```bash
# Les tests s'exécutent automatiquement à chaque push
```

### Workflow Avancé (`tests.yml`)

**Pour une qualité de code maximale**

- ✅ Tests unitaires
- ✅ Tests fonctionnels
- ✅ Tests sur plusieurs versions Python (3.9, 3.10, 3.11)
- ✅ Linting (Black, Flake8)
- ✅ Couverture de code
- ✅ Upload vers Codecov

**Utilisation :**
```bash
# Les tests s'exécutent automatiquement à chaque push
# Plus de vérifications = plus de temps d'exécution
```

## Résultats des tests

### Voir les résultats

1. Aller sur GitHub → Votre dépôt
2. Onglet **"Actions"**
3. Cliquer sur le workflow en cours/complété
4. Voir les détails de chaque étape

### Badge de statut

Ajoutez un badge dans votre README.md :

```markdown
![Tests](https://github.com/votre-username/votre-repo/workflows/Tests%20Simples/badge.svg)
```

## Personnalisation

### Ajouter MongoDB pour les tests complets

Éditez `.github/workflows/simple-tests.yml` :

```yaml
- name: Démarrer MongoDB
  uses: supercharge/mongodb-github-action@1.8.0
  with:
    mongodb-version: '6.0'

- name: Exécution de tous les tests
  run: |
    cd extension_finale
    pytest Test/tests/ -v
```

### Ajouter des notifications

```yaml
- name: Notification Slack (si échec)
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Les tests ont échoué !'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Ajouter un déploiement automatique

```yaml
deploy:
  needs: test
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - name: Déployer
      run: |
        echo "Déploiement automatique..."
        # Vos commandes de déploiement
```

## Commandes utiles

### Tester localement (simuler GitHub Actions)

```bash
# Installer act (simulateur GitHub Actions)
brew install act  # macOS
# ou
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Exécuter le workflow
act -j test
```

### Voir les logs détaillés

Dans GitHub Actions, cliquez sur chaque étape pour voir les logs complets.

## Dépannage

### Les tests échouent

1. Vérifier les logs dans GitHub Actions
2. Tester localement : `pytest Test/tests/ -v`
3. Vérifier que toutes les dépendances sont dans `requirements_test.txt`

### Le workflow ne se déclenche pas

1. Vérifier que les fichiers sont dans `.github/workflows/`
2. Vérifier la syntaxe YAML (pas d'erreurs)
3. Vérifier que vous poussez sur la bonne branche

### MongoDB non disponible

C'est normal ! Les tests qui nécessitent MongoDB seront ignorés. Pour les activer, ajoutez l'action MongoDB dans le workflow.

## Avantages du CI/CD

✅ **Détection précoce des bugs** : Les erreurs sont détectées immédiatement  
✅ **Confiance** : Vous savez que le code fonctionne avant de merger  
✅ **Documentation vivante** : Les tests servent de documentation  
✅ **Qualité** : Le code est vérifié automatiquement  
✅ **Rapidité** : Pas besoin d'exécuter les tests manuellement  

## Prochaines étapes

1. ✅ CI/CD de base configuré
2. 🔄 Ajouter MongoDB pour les tests complets
3. 🔄 Ajouter le déploiement automatique
4. 🔄 Ajouter des notifications
5. 🔄 Ajouter des tests de performance

---

**Note** : Le CI/CD est maintenant configuré ! À chaque push, les tests s'exécuteront automatiquement.


