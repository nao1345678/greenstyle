# --- ÉTAPE 1 : BUILD ---
FROM node:22-alpine AS build

WORKDIR /app

# On force Docker à ignorer le cache pour cette étape de copie
# Utilise bien le point devant le slash
COPY ./site-vue/package*.json ./

# On vérifie physiquement si le fichier est là avant de lancer npm install
RUN ls -l /app/package.json

RUN npm install

# Copie du reste
COPY ./site-vue/ .

RUN npm run build

# --- ÉTAPE 2 : PRODUCTION ---
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]