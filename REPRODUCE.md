# SmartFit Coach - Instructions de Reproduction

Ce document explique comment reproduire l'environnement et l'entraînement du modèle pour le projet SmartFit Coach.

## 1. Environnement

### Option A : Docker (Recommandé)

Un `Dockerfile` est fourni à la racine du projet pour créer un environnement isolé et reproductible.

**Prérequis :** Docker Desktop installé.

1. **Construire l'image :**
   ```bash
   docker build -t smartfit-coach .
   ```

2. **Lancer le conteneur :**
   ```bash
   docker run -p 8501:8501 smartfit-coach
   ```
   L'application sera accessible sur `http://localhost:8501`.

### Option B : Installation Locale (Python)

**Prérequis :** Python 3.11 ou supérieur.

1. **Créer un environnement virtuel :**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

## 2. Lancer l'Application

Pour démarrer l'interface utilisateur Streamlit :

```bash
streamlit run interface/app.py
```

## 3. Reproduction de l'Entraînement (Modèle LSTM)

Le modèle de classification d'exercices (Squats vs Pompes) est un réseau de neurones LSTM entraîné sur des séquences de coordonnées (landmarks).

### Structure des Données
Les données brutes (vidéos) ne sont pas incluses dans le repo pour des raisons de taille. Cependant, les scripts pour générer le dataset à partir de vos propres vidéos sont fournis.

### Étapes pour ré-entraîner le modèle :

1. **Préparer les vidéos :**
   Placez vos vidéos d'entraînement dans `data/raw/squats` et `data/raw/pushups`.

2. **Extraire les séquences (Landmarks) :**
   Utilisez le script pour convertir les vidéos en fichiers CSV de coordonnées normalisées.
   ```bash
   python scripts/extract_dataset.py
   ```
   *Note : Ce script utilise MediaPipe pour extraire 33 points clés par frame.*

3. **Lancer l'entraînement (Notebook) :**
   Ouvrez le notebook `notebooks/02_train_lstm.ipynb`.
   - Exécutez toutes les cellules.
   - Le notebook va :
     - Charger les fichiers CSV.
     - Créer des séquences temporelles (fenêtres de 30 frames).
     - Entraîner le modèle LSTM.
     - Sauvegarder le modèle sous `models/exercise_classifier_lstm.h5`.

## 4. Architecture du Projet

- `interface/` : Code de l'application Front-end (Streamlit).
- `src/` : Code Back-end et logique métier.
  - `detection/` : Gestion de la caméra et MediaPipe.
  - `counting/` : Algorithmes de comptage géométrique.
  - `recognition/` : Inférence du modèle LSTM.
- `models/` : Fichiers modèles entraînés (.h5).
- `notebooks/` : Expérimentations et entraînement.

## 5. Modèles Fournis

Le dépôt contient déjà un modèle pré-entraîné prêt à l'emploi :
- `models/exercise_classifier_lstm.h5` : Modèle final utilisé par l'application.
