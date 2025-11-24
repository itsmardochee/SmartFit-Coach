# 🐳 Guide Docker - SmartFit Coach

## 📌 Limitations importantes

### ❌ Webcam non supportée sur Windows/Mac avec Docker Desktop

**Docker Desktop sur Windows et Mac ne supporte PAS l'accès direct aux webcams** car le conteneur s'exécute dans une machine virtuelle Linux (WSL2 ou HyperKit) qui n'a pas accès aux périphériques USB de l'hôte.

### ✅ Quand utiliser Docker ?

- **Déploiement sur serveur Linux** : Docker fonctionne parfaitement sur Linux natif avec accès webcam
- **Tests sans caméra** : Pour tester l'application avec des vidéos préenregistrées
- **Déploiement cloud** : Pour héberger l'application sur Azure, AWS, Google Cloud, etc.

### 💻 Pour le développement local avec webcam

**Utilisez l'environnement Python directement** (sans Docker) :

```bash
# Activer l'environnement virtuel
.\venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run interface/app.py
```

---

## 🚀 Utilisation de Docker

### Construction de l'image

```bash
docker build -t smartfit-coach:latest .
```

### Lancement du conteneur

#### Sans caméra (Mode vidéo uniquement)

```bash
docker run -p 8501:8501 smartfit-coach:latest
```

Accédez à : http://localhost:8501

#### Sur Linux avec accès webcam

```bash
docker run -p 8501:8501 \
  --device=/dev/video0:/dev/video0 \
  -v /dev/video0:/dev/video0 \
  smartfit-coach:latest
```

### Avec Docker Compose

```bash
# Lancer
docker-compose up

# Arrêter
docker-compose down
```

---

## 🔧 Configuration avancée

### Variables d'environnement

Vous pouvez personnaliser le comportement avec des variables d'environnement :

```bash
docker run -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  smartfit-coach:latest
```

### Volumes pour les données

Pour persister les sessions d'entraînement :

```bash
docker run -p 8501:8501 \
  -v ./data/sessions:/app/data/sessions \
  smartfit-coach:latest
```

---

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
docker logs <container_id>

# Vérifier que le port n'est pas déjà utilisé
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/Mac
```

### Erreur "Aucune caméra détectée"

C'est **normal sur Windows/Mac avec Docker Desktop**. Solutions :

1. **Utiliser l'environnement Python local** (recommandé)
2. **Utiliser le mode vidéo** avec des fichiers préenregistrés
3. **Déployer sur Linux** si vous avez besoin de Docker + webcam

### Performances lentes

Docker peut être plus lent que l'exécution native. Pour améliorer :

```bash
# Allouer plus de ressources dans Docker Desktop
# Settings → Resources → Advanced
# - CPU: 4+ cores
# - Memory: 4+ GB
```

---

## 📦 Déploiement Production

### Sur Azure Container Instances

```bash
# Build et push vers Azure Container Registry
az acr build --registry <registry_name> --image smartfit-coach:latest .

# Déployer
az container create \
  --resource-group <rg_name> \
  --name smartfit-coach \
  --image <registry_name>.azurecr.io/smartfit-coach:latest \
  --ports 8501 \
  --cpu 2 \
  --memory 4
```

### Sur Docker Hub

```bash
# Tag
docker tag smartfit-coach:latest <username>/smartfit-coach:latest

# Push
docker push <username>/smartfit-coach:latest
```

---

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Streamlit + Docker](https://docs.streamlit.io/deploy/tutorials/docker)
- [OpenCV dans Docker](https://github.com/opencv/opencv-python)

---

## ⚙️ Spécifications de l'image

- **Image de base** : python:3.11.14-slim
- **Taille approximative** : ~2.5 GB (avec TensorFlow et OpenCV)
- **Port** : 8501
- **Healthcheck** : Intégré
- **Dépendances système** :
  - libgl1 (OpenCV)
  - libglib2.0-0
  - libsm6, libxext6, libxrender-dev
  - libgomp1
  - curl

**Note** : JAX et JAXlib sont installés séparément de TensorFlow pour résoudre les conflits de dépendances ml_dtypes.

---

**Version** : 1.0  
**Date** : Novembre 2025
