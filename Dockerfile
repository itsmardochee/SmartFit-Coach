# Image de base Python
FROM python:3.11.14-slim

# Variables d'environnement pour éviter les prompts interactifs
ENV DEBIAN_FRONTEND=noninteractive

# Mise à jour et installation des dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tensorflow==2.18.0 && \
    pip install --no-cache-dir jax==0.7.1 jaxlib==0.7.1 && \
    grep -v "^tensorflow==" requirements.txt | grep -v "^jax==" | grep -v "^jaxlib==" | grep -v "^ml_dtypes==" | pip install --no-cache-dir -r /dev/stdin

# Copie du code source
COPY . .

# Exposition du port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Commande de lancement
CMD ["streamlit", "run", "interface/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
