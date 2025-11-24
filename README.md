# 🏋️ SmartFit Coach

## Système de Comptage et Coaching Sportif en Temps Réel

SmartFit Coach est un système intelligent qui utilise la vision par ordinateur pour détecter les mouvements du corps, compter automatiquement les répétitions d'exercices et fournir un feedback en temps réel sur l'exécution.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)

---

## 🎯 Fonctionnalités

- ✅ **Détection de pose en temps réel** : Identification de 33 points clés du corps via MediaPipe
- ✅ **Comptage automatique** : Compte les répétitions pour squats et pompes
- ✅ **Feedback intelligent** : Conseils instantanés pour améliorer l'exécution
- ✅ **Interface intuitive** : Interface web Streamlit avec visualisation en direct
- ✅ **Statistiques de session** : Suivi des performances (répétitions, qualité, temps)

---

## 🛠️ Technologies Utilisées

- **Python 3.11+**
- **OpenCV** : Traitement vidéo et capture webcam
- **MediaPipe** : Détection de pose en temps réel
- **TensorFlow/Keras** : Modèle LSTM pour classification d'exercices
- **NumPy** : Calculs mathématiques et géométriques
- **Streamlit** : Interface utilisateur web interactive
- **Pytest** : Tests unitaires

---

## 📦 Installation

### Prérequis

- Python 3.11 ou supérieur
- Webcam fonctionnelle (pour utilisation locale)
- Windows, macOS ou Linux

### 1. Cloner le dépôt

```bash
git clone https://github.com/itsmardochee/SmartFit-Coach.git
cd SmartFit-Coach
```

### 2. Créer un environnement virtuel (recommandé)

**Windows (PowerShell) :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac :**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### Lancer l'application complète

```bash
streamlit run interface/app.py
```

L'application s'ouvrira dans votre navigateur web par défaut à l'adresse `http://localhost:8501`.

### Instructions d'utilisation

1. **Sélectionner un exercice** dans le menu latéral (Squats ou Pompes)
2. **Cliquer sur "Démarrer"** pour lancer la session
3. **Se positionner** devant la webcam (corps entièrement visible)
4. **Effectuer les exercices** en suivant les instructions et le feedback
5. **Cliquer sur "Arrêter"** pour terminer la session
6. **Consulter les statistiques** affichées à droite

### Démonstration de détection (mode terminal)

Pour tester la détection de pose uniquement :

```bash
python demo_detection.py
```

**Contrôles :**

- Appuyez sur `q` pour quitter

---

## 📁 Structure du Projet

```text
SmartFit-Coach/
├── src/
│   ├── detection/              # Détection de pose et capture vidéo
│   │   ├── video_capture.py    # Gestion de la webcam
│   │   └── pose_detector.py    # Détection MediaPipe
│   ├── counting/               # Comptage des répétitions
│   │   ├── angle_calculator.py # Calculs géométriques
│   │   └── exercise_detectors/ # Compteurs par exercice
│   ├── recognition/            # Classification d'exercices (LSTM)
│   ├── feedback/               # Génération de feedback
│   └── utils/                  # Utilitaires
├── interface/                  # Interface utilisateur Streamlit
├── models/                     # Modèles ML entraînés
├── data/                       # Datasets et sessions
├── tests/                      # Tests unitaires
├── notebooks/                  # Jupyter notebooks
├── scripts/                    # Scripts d'extraction de données
└── requirements.txt            # Dépendances Python
```

---

## 📊 Étapes de Développement

### ✅ Étape 1 : Détection de Pose (**COMPLÈTE**)

- [x] Module de capture vidéo
- [x] Détection des 33 keypoints avec MediaPipe
- [x] Visualisation du squelette en temps réel
- [x] Tests unitaires

### ✅ Étape 2 : Comptage des Répétitions (**COMPLÈTE**)

- [x] Calcul d'angles entre articulations
- [x] Détecteur de squats avec machine à états
- [x] Détecteur de pompes avec machine à états
- [x] Logique anti-rebond
- [x] Tests unitaires pour le comptage

### ✅ Étape 3 : Reconnaissance et Feedback (**COMPLÈTE**)

- [x] Modèle LSTM de classification d'exercices (Squats/Pompes)
- [x] Dataset annoté et extraction de keypoints
- [x] Feedback basique par exercice
- [x] Entraînement et sauvegarde du modèle

### ✅ Étape 4 : Interface Utilisateur (**COMPLÈTE**)

- [x] Interface Streamlit interactive
- [x] Sélection d'exercice
- [x] Affichage en temps réel (webcam + squelette)
- [x] Compteur et statistiques
- [x] Feedback visuel
- [x] Gestion de session (démarrage/arrêt/reset)

---

## 🏋️ Exercices Supportés

### Actuellement implémentés :
- 🏋️ **Squats** : Détection basée sur l'angle des genoux et hanches
- 💪 **Pompes** : Détection basée sur l'angle des coudes

### En développement :
- 🦵 **Fentes**
- 🏃 **Burpees**
- 🤸 **Abdominaux**

---

## 🧪 Tests

Exécuter tous les tests :

```bash
pytest tests/ -v
```

Tests avec couverture :

```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

---

## 🐛 Problèmes Connus

- La détection peut être moins précise dans des conditions d'éclairage faible
- Le FPS peut varier selon les performances de la machine
- Certains angles de caméra peuvent affecter la précision
- Docker Desktop sur Windows/Mac ne supporte pas l'accès aux webcams (utiliser Python local)

Pour signaler un bug, ouvrez une [issue](https://github.com/itsmardochee/SmartFit-Coach/issues).

---

## 🙏 Remerciements

- [MediaPipe](https://google.github.io/mediapipe/) pour leur excellente bibliothèque de détection de pose
- [OpenCV](https://opencv.org/) pour les outils de traitement d'image
- [TensorFlow](https://www.tensorflow.org/) pour le framework de deep learning
- La communauté open-source pour l'inspiration et les ressources

---

## 📞 Contact

- GitHub : [@itsmardochee](https://github.com/itsmardochee)

---

**Version :** 1.0.0  
**Dernière mise à jour :** Novembre 2025

---

Made with ❤️ by SmartFit Coach Team
