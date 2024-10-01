# Utiliser une image Python comme base
FROM continuumio/miniconda3

# Définir le répertoire de travail dans le conteneur
WORKDIR /home/app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . .

# Exposer le port 80 pour l'application Streamlit
EXPOSE 80

# Démarrer l'application Streamlit
CMD streamlit run --server.port $PORT getaround.py