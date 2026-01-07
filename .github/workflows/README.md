# CI/CD - GitHub Actions

Ce dossier contient les workflows GitHub Actions pour l'intégration continue et le déploiement continu.

## Workflows disponibles

### 1. `simple-tests.yml` (Recommandé pour commencer)

Workflow simple qui exécute les tests unitaires et fonctionnels à chaque push.

**Déclencheurs :**
- Push sur les branches `main`, `master`, `develop`
- Pull requests vers ces branches
- Déclenchement manuel (workflow_dispatch)

**Actions :**
- Installation de Python 3.10
- Installation des dépendances de test
- Exécution des tests unitaires
- Exécution des tests de scraping

### 2. `tests.yml` (Avancé)

Workflow complet avec :
- Tests sur plusieurs versions de Python (3.9, 3.10, 3.11)
- Tests de linting (Black, Flake8)
- Rapport de couverture de code
- Upload vers Codecov

## Utilisation

### Pour activer le CI/CD :

1. **Créer un dépôt GitHub** (si ce n'est pas déjà fait)
2. **Pousser le code** sur GitHub
3. **Les tests s'exécuteront automatiquement** à chaque push

### Pour tester localement :

```bash
# Simuler le workflow GitHub Actions
act -j test

# Ou installer act (si disponible)
# brew install act  # Sur macOS
```

### Pour voir les résultats :

1. Aller sur votre dépôt GitHub
2. Cliquer sur l'onglet "Actions"
3. Voir les workflows en cours et les résultats

## Personnalisation

### Modifier les branches déclenchées :

Éditez le fichier `.github/workflows/simple-tests.yml` :

```yaml
on:
  push:
    branches: [ main, votre-branche ]
```

### Ajouter des tests supplémentaires :

Ajoutez des étapes dans la section `steps` :

```yaml
- name: Votre test personnalisé
  run: |
    cd extension_finale
    pytest Test/tests/votre_test.py -v
```

### Ajouter MongoDB pour les tests complets :

```yaml
- name: Démarrer MongoDB
  uses: supercharge/mongodb-github-action@1.8.0
  with:
    mongodb-version: '6.0'
```

## Statut des tests

Les badges de statut peuvent être ajoutés dans votre README :

```markdown
![Tests](https://github.com/votre-username/votre-repo/workflows/Tests%20Simples/badge.svg)
```

## Notes

- Les tests qui nécessitent MongoDB seront ignorés si MongoDB n'est pas disponible
- Le workflow simple est recommandé pour commencer
- Le workflow avancé nécessite plus de configuration mais offre plus de fonctionnalités


