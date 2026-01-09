# Site Web - Fichiers copiés depuis Git

Ce dossier contient tous les fichiers liés au site web copiés depuis le dépôt Git.

## Structure

### 1. `frontend/` - Version principale du site

**Configuration Docker :**
- `Dockerfile` - Configuration Docker pour le frontend
- `nginx/default.conf` - Configuration Nginx
- `index.html` - Point d'entrée HTML

**Application Vue.js :** `frontend/site-vue/`

**Fichiers principaux :**
- `package.json` - Dépendances Node.js
- `vite.config.js` - Configuration Vite
- `src/main.js` - Point d'entrée de l'application
- `src/App.vue` - Composant principal

**API (TypeScript) :**
- `src/api/brand.ts` - API pour les marques
- `src/api/categories.ts` - API pour les catégories
- `src/api/favorite.ts` - API pour les favoris
- `src/api/users.ts` - API pour les utilisateurs
- `src/api/alternatives.ts` - API pour les alternatives
- `src/api/http.ts` - Client HTTP

**Composants Vue :**
- `src/components/navbar.vue` - Barre de navigation
- `src/components/heroSection.vue` - Section héro
- `src/components/ProductCard.vue` - Carte produit
- `src/components/ProductGrid.vue` - Grille de produits
- `src/components/clothCard.vue` - Carte vêtement
- `src/components/clothGrid.vue` - Grille de vêtements
- `src/components/SearchBar.vue` - Barre de recherche
- `src/components/favorites.vue` - Favoris
- `src/components/intro.vue` - Introduction

**Pages :**
- `src/pages/index.vue` - Page d'accueil
- `src/pages/marques/[id].vue` - Page détail marque

**Router :**
- `src/router/router.ts` - Configuration du routeur

**Styles :**
- `src/style.css` - Styles globaux

**Assets :**
- Images dans `src/assets/` (flower.png, heels.png, etc.)

### 2. `site-vue/` - Version alternative du site

**Différences avec `frontend/site-vue/` :**
- `src/router/router.js` (JavaScript au lieu de TypeScript)
- `src/components/IntroductionSection.vue` - Section d'introduction
- `src/components/TeamSection.vue` - Section équipe
- `src/pages/AProposDeNous.vue` - Page "À propos de nous"
- Plus d'images dans `src/assets/` (photos de l'équipe : Chat.png, Hery.png, Mael.png, etc.)

## Statistiques

- **Total de fichiers dans Git :** 1075 fichiers (incluant node_modules)
- **Fichiers source :** ~50 fichiers Vue/TypeScript/JavaScript
- **2 versions du site :** `frontend/site-vue/` et `site-vue/`

## Technologies utilisées

- **Vue.js 3** - Framework JavaScript
- **TypeScript** - Typage statique
- **Vite** - Build tool
- **Vue Router** - Routing
- **Axios** - Client HTTP

## Installation et utilisation

### Pour `frontend/site-vue/` :

```bash
cd site_web_local/frontend/site-vue
npm install
npm run dev
```

### Pour `site-vue/` :

```bash
cd site_web_local/site-vue
npm install
npm run dev
```

## Docker

Pour déployer avec Docker :

```bash
cd site_web_local/frontend
docker build -t greenstyle-frontend .
docker run -p 80:80 greenstyle-frontend
```

## Notes

- Les fichiers ont été copiés depuis le dépôt Git (branche main)
- Les `node_modules/` ne sont pas inclus dans la copie (trop volumineux)
- Exécutez `npm install` dans chaque dossier pour installer les dépendances
- Les deux versions semblent être des variantes du même site

## Date de copie

Fichiers copiés depuis Git le : $(date)


