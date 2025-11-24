# 🏋️ SmartFit Coach

## Système de Comptage et Coaching Sportif en Temps Réel

SmartFit Coach est un système intelligent qui utilise la vision par ordinateur pour détecter les mouvements du corps, compter automatiquement les répétitions d'exercices et fournir un feedback en temps réel sur l'exécution.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 Fonctionnalités

- ✅ **Détection de pose en temps réel** : Identification de 33 points clés du corps via MediaPipe
- ✅ **Comptage automatique** : Compte les répétitions pour squats et pompes
- ✅ **Feedback intelligent** : Conseils instantanés pour améliorer l'exécution
- ✅ **Interface intuitive** : Interface web Streamlit avec visualisation en direct
- ✅ **Statistiques de session** : Suivi des performances (répétitions, qualité, temps)

---

## 🛠️ Technologies Utilisées

- **Python 3.8+**
- **OpenCV** : Traitement vidéo et capture webcam
- **MediaPipe** : Détection de pose en temps réel
- **NumPy** : Calculs mathématiques et géométriques
- **Streamlit** : Interface utilisateur web interactive
- **Pytest** : Tests unitaires

---

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- Webcam fonctionnelle
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
│   │       ├── squat_counter.py
│   │       └── pushup_counter.py
│   ├── recognition/            # Reconnaissance d'exercices (à venir)
│   ├── feedback/               # Génération de feedback
│   └── utils/                  # Utilitaires
│       └── visualization.py    # Visualisation du squelette
├── interface/                  # Interface utilisateur
│   └── app.py                  # Application Streamlit
├── tests/                      # Tests unitaires
│   ├── test_detection.py
│   └── test_counting.py
├── data/                       # Datasets
├── models/                     # Modèles ML
├── docs/                       # Documentation
└── notebooks/                  # Jupyter notebooks
│   ├── recognition/        # Classification des exercices
│   ├── feedback/           # Génération du feedback
│   └── utils/              # Fonctions utilitaires
│       └── visualization.py
├── models/                 # Modèles ML entraînés
├── data/                   # Datasets et sessions
├── interface/              # Interface utilisateur
├── tests/                  # Tests unitaires
├── notebooks/              # Jupyter notebooks
├── docs/                   # Documentation
├── demo_detection.py       # Script de démonstration
└── requirements.txt        # Dépendances Python
```

---

## 📊 Étapes de Développement

### ✅ Étape 1 : Détection de Pose (**COMPLÈTE**)

- [x] Module de capture vidéo
- [x] Détection des 33 keypoints avec MediaPipe
- [x] Visualisation du squelette en temps réel
- [x] Tests unitaires (10 tests)

### ✅ Étape 2 : Comptage des Répétitions (**COMPLÈTE**)

- [x] Calcul d'angles entre articulations
- [x] Détecteur de squats avec machine à états
- [x] Détecteur de pompes avec machine à états
- [x] Logique anti-rebond
- [x] Tests unitaires pour le comptage

### 🔄 Étape 3 : Reconnaissance et Feedback (En cours)

- [x] Feedback basique par exercice
- [ ] Modèle de classification d'exercices (ML)
- [ ] Dataset annoté
- [ ] Analyse de qualité avancée

### ✅ Étape 4 : Interface Utilisateur (**COMPLÈTE**)

- [x] Interface Streamlit interactive
- [x] Sélection d'exercice
- [x] Affichage en temps réel (webcam + squelette)
- [x] Compteur et statistiques
- [x] Feedback visuel
- [x] Gestion de session (démarrage/arrêt/reset)

---

## 🏋️ Exercices Supportés

### Actuellement implémentés

- 🏋️ **Squats** : Détection basée sur l'angle des genoux et hanches
- 💪 **Pompes** : Détection basée sur l'angle des coudes

### En développement

- 🦵 **Fentes**
- [x] Visualisation du squelette en temps réel
- [x] Script de démonstration

### 🔄 Étape 2 : Comptage des Répétitions (À venir)
- [ ] Calcul d'angles entre articulations
- [ ] Détection des cycles de mouvement
- [ ] Compteur pour squats
- [ ] Compteur pour pompes

### 🔄 Étape 3 : Reconnaissance et Feedback (À venir)
- [ ] Modèle de classification d'exercices
- [ ] Détection des erreurs de posture
- [ ] Génération de feedback

### 🔄 Étape 4 : Interface Utilisateur (À venir)
- [ ] Interface Streamlit
- [ ] Statistiques de session
- [ ] Historique des performances

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

## 📝 Exercices Supportés

### Actuellement implémentés :
- 🏋️ **Squats** : Détection basée sur l'angle des genoux et hanches
- 💪 **Pompes** : Détection basée sur l'angle des coudes

### En développement :
- 🦵 **Fentes**
- 🏃 **Burpees**
- 🤸 **Abdominaux**

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

---

## 📖 Documentation

La documentation complète est disponible dans le dossier `docs/` :

- [Guide d'installation détaillé](docs/installation.md) (à venir)
- [Guide d'utilisation](docs/usage.md) (à venir)
- [Documentation technique](docs/technical.md) (à venir)
- [API Reference](docs/api.md) (à venir)

---

## 🐛 Problèmes Connus

- La détection peut être moins précise dans des conditions d'éclairage faible
- Le FPS peut varier selon les performances de la machine
- Certains angles de caméra peuvent affecter la précision

Pour signaler un bug, ouvrez une [issue](https://github.com/itsmardochee/SmartFit-Coach/issues).

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Équipe

**SmartFit Coach Development Team**

- Développement : [Votre nom]
- Vision par ordinateur : [Nom]
- Interface utilisateur : [Nom]
- Tests et QA : [Nom]

---

## 🙏 Remerciements

- [MediaPipe](https://google.github.io/mediapipe/) pour leur excellente bibliothèque de détection de pose
- [OpenCV](https://opencv.org/) pour les outils de traitement d'image
- La communauté open-source pour l'inspiration et les ressources

---

## 📞 Contact

Pour toute question ou suggestion :

- Email : [votre-email@example.com]
- GitHub : [@itsmardochee](https://github.com/itsmardochee)

---

**Version :** 1.0.0  
**Dernière mise à jour :** Novembre 2025

---

Made with ❤️ by SmartFit Coach Team
