# --- ÉTAPE 1 : BUILD (Construction et compilation de l'application Vue) ---
FROM node:18-alpine AS build

# Le répertoire de travail
WORKDIR /usr/src/app

# Copier les fichiers de dépendances et installer
COPY package*.json ./
RUN npm install
COPY . .

# Lancer la commande de compilation de l'application Vue
RUN npm run build


# --- ÉTAPE 2 : PRODUCTION (Service des fichiers avec Nginx) ---
FROM nginx:stable-alpine

# 1. Copie du fichier de configuration Nginx

COPY --from=build /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]