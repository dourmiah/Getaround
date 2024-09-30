# Utiliser une image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . .

# Exposer le port 80 pour l'application Streamlit
EXPOSE 80

# Démarrer l'application Streamlit
CMD ["streamlit", "run", "getaround.py", "--server.port=80", "--server.enableCORS=false"]