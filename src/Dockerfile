# 1. Étape de base : Choisir une image Python stable et légère
FROM python:3.11-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /src

# 3. Copier les dépendances et les installer
COPY requirements.txt .

# Installe les dépendances listées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le reste du code de l'application
COPY . .

# 5. Exposer le port sur lequel l'API tourne
EXPOSE 8000

# 6. Commande pour démarrer l'application
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker", "--workers", "4"]