# Guide de Présentation - Version Apprenti Développeur

## Structure recommandée pour votre présentation (10-15 minutes)

### 1. Introduction (2 min)
- **Problématique** : "Les consommateurs veulent acheter de manière responsable, mais c'est difficile de trouver des marques qui correspondent à leurs valeurs"
- **Solution** : "J'ai créé une plateforme qui apprend les préférences de chaque utilisateur et recommande des marques durables personnalisées"

### 2. Architecture globale (3 min)
- **4 grandes parties** :
  1. Collecte de données (scrapers Python)
  2. API Backend (FastAPI + MongoDB)
  3. Système d'IA (apprentissage + recommandation)
  4. Extension Chrome (détection de marques)

### 3. Démos et explications techniques (8 min)

#### A. Collecte de données (2 min)
**Ce que vous montrez** :
- Le fichier CSV avec les marques
- Lancer un scraper (ou montrer les résultats)
- Expliquer : "L'IA collecte automatiquement les données de durabilité"

**Ce que vous dites** :
> "Pour chaque marque, j'ai créé des scrapers qui vont chercher automatiquement les informations de durabilité : les matières recyclées, les certifications, la gestion des invendus. L'orchestrateur IA apprend quelle source est la plus fiable et optimise les prochaines collectes."

#### B. API et Base de données (2 min)
**Ce que vous montrez** :
- L'API FastAPI en cours d'exécution
- Une requête GET /brands dans le navigateur
- La structure MongoDB

**Ce que vous dites** :
> "J'ai créé une API REST avec FastAPI qui expose toutes les données. Les marques sont stockées dans MongoDB. J'utilise MongoDB parce que les données peuvent être différentes selon les marques, et c'est plus flexible qu'une base SQL classique."

#### C. Système d'IA d'apprentissage (3 min)
**Ce que vous montrez** :
- Code du `preference_learning_engine.py` (juste la partie clé)
- Exemple d'interaction utilisateur
- Résultat de recommandation

**Ce que vous dites** :
> "Le système apprend des préférences de chaque utilisateur. Quand un utilisateur 'like' une marque, le système analyse : quelles caractéristiques a cette marque ? Si l'utilisateur aime souvent des marques avec beaucoup de matières recyclées, le système comprend que c'est important pour lui et augmente le poids de ce critère dans son profil."

**Exemple concret** :
> "Par exemple, si un utilisateur like 3 marques qui ont toutes 80% de matières recyclées, le système va augmenter l'importance du critère 'matières recyclées' pour cet utilisateur. Les prochaines recommandations privilégieront les marques avec beaucoup de matières recyclées."

#### D. Extension Chrome (1 min)
**Ce que vous montrez** :
- L'extension installée
- Une page web avec des marques détectées
- L'affichage des informations de durabilité

**Ce que vous dites** :
> "L'extension Chrome détecte automatiquement les marques présentes sur les pages web. Elle analyse le texte de la page, les liens, les métadonnées. Quand elle trouve une marque, elle affiche les informations de durabilité directement sur la page."

### 4. Points techniques clés (2 min)
- **Apprentissage** : "Le système s'améliore avec chaque interaction"
- **Personnalisation** : "Chaque utilisateur a son propre profil de préférences"
- **Optimisation** : "L'IA apprend quelle source de données est la plus fiable"

### 5. Conclusion (1 min)
- **Résultat** : "Une plateforme complète qui aide les utilisateurs à découvrir des marques durables selon leurs préférences"
- **Apprentissage** : "J'ai appris à créer une API, à utiliser MongoDB, à implémenter un système d'apprentissage, et à développer une extension Chrome"

---

## Phrases clés à retenir

### Pour expliquer l'apprentissage :
> "Le système analyse les interactions utilisateur pour comprendre quels critères sont importants pour chacun. Plus l'utilisateur interagit, plus le système devient précis."

### Pour expliquer les recommandations :
> "Pour chaque marque, on calcule un score en multipliant chaque caractéristique par l'importance que l'utilisateur accorde à ce critère. Les marques avec le score le plus élevé sont recommandées."

### Pour expliquer l'orchestrateur IA :
> "L'IA mémorise quelles sources de données ont fonctionné dans le passé. Si B-Corp a réussi 9 fois sur 10 pour les certifications, l'IA va essayer B-Corp en premier pour la prochaine marque."

### Pour expliquer la détection :
> "L'extension analyse tous les textes de la page et cherche des noms de marques. Elle a une base de données avec des marques connues et leurs alias, comme 'Nike Air' pour Nike."

---

## Questions fréquentes et réponses

### "Comment fonctionne l'apprentissage ?"
**Réponse** :
> "Quand un utilisateur interagit avec une marque, le système regarde quelles caractéristiques a cette marque. Si l'interaction est positive (like), il augmente l'importance des critères qui sont élevés. Si c'est négatif (dislike), il diminue. Au fil du temps, le système apprend quels critères sont vraiment importants pour cet utilisateur."

### "Comment garantissez-vous la qualité des données ?"
**Réponse** :
> "L'IA apprend des sources les plus fiables. Elle essaie plusieurs sources et mémorise lesquelles fonctionnent le mieux. On peut aussi faire une validation croisée entre plusieurs sources pour vérifier les données."

### "Que se passe-t-il pour un nouvel utilisateur ?"
**Réponse** :
> "Au début, tous les critères ont le même poids. Le système recommande les marques avec les meilleurs scores globaux de durabilité. Au fur et à mesure des interactions, le profil se personnalise."

### "Pourquoi MongoDB plutôt qu'une base SQL ?"
**Réponse** :
> "MongoDB est plus flexible. Les marques peuvent avoir des champs différents selon les données collectées. Par exemple, certaines marques ont des certifications, d'autres non. C'est plus facile d'ajouter de nouveaux champs sans modifier toute la structure."

---

## Schéma à dessiner au tableau

### Architecture simplifiée

```
┌─────────────┐
│   Scrapers  │ → Collectent les données de durabilité
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MongoDB   │ → Stocke les marques et utilisateurs
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │ → API REST pour exposer les données
└──────┬──────┘
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│  Learning   │  │  Extension  │
│  Engine     │  │  Chrome     │
└─────────────┘  └─────────────┘
```

### Flux d'apprentissage

```
Utilisateur like une marque
         │
         ▼
Analyse les caractéristiques de la marque
         │
         ▼
Met à jour les poids des critères
         │
         ▼
Prochaines recommandations sont mieux adaptées
```

---

## Ce qu'il faut éviter de dire

❌ "C'est très complexe" → Dites plutôt "C'est modulaire, chaque partie a un rôle clair"
❌ "Je ne sais pas comment ça marche" → Dites plutôt "Je vais vous expliquer le principe"
❌ "C'est pas fini" → Dites plutôt "Voici les fonctionnalités principales implémentées"

---

## Ce qu'il faut mettre en avant

✅ **Modularité** : Chaque composant a un rôle clair
✅ **Apprentissage** : Vous avez appris beaucoup de technologies
✅ **Approche complète** : Du scraping à l'interface utilisateur
✅ **Amélioration continue** : Le système s'améliore avec l'usage

---

## Astuce pour la présentation

**Commencez simple, puis détaillez** :
1. D'abord expliquer le concept global (2 min)
2. Ensuite montrer un exemple concret (3 min)
3. Puis expliquer comment ça marche techniquement (5 min)
4. Enfin répondre aux questions (5 min)

**Si vous bloquez sur un point technique** :
- Dites : "Je peux vous expliquer le principe général, et je peux vous montrer le code si vous voulez plus de détails"
- Montrez le code et expliquez ligne par ligne

---

## Checklist avant la présentation

- [ ] Tester que l'API fonctionne (`uvicorn src.main:app`)
- [ ] Avoir un CSV avec quelques marques prêtes
- [ ] Avoir l'extension Chrome installée et fonctionnelle
- [ ] Préparer un exemple d'interaction utilisateur
- [ ] Avoir le code ouvert pour montrer des exemples si besoin
- [ ] Préparer le schéma d'architecture au tableau

---

## Exemple de script de présentation (à adapter)

### Introduction
> "Bonjour, je vais vous présenter mon projet GreenStyle. C'est une plateforme qui aide les utilisateurs à découvrir des marques de mode durables selon leurs préférences personnelles."

### Architecture
> "Le projet se compose de 4 parties principales : des scrapers Python qui collectent les données, une API FastAPI avec MongoDB pour stocker les données, un système d'IA qui apprend les préférences utilisateur, et une extension Chrome pour détecter les marques sur les pages web."

### Démonstration
> "Je vais vous montrer comment ça fonctionne. D'abord, la collecte de données... Ensuite, l'API... Puis le système d'apprentissage... Et enfin l'extension..."

### Conclusion
> "Pour résumer, j'ai créé un système complet qui collecte des données de durabilité, apprend les préférences de chaque utilisateur, et recommande des marques personnalisées. Le système s'améliore au fur et à mesure que les utilisateurs interagissent avec lui."

---

Bon courage pour votre soutenance !




