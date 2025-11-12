# 🏋️ SmartFit Coach

## Système de Comptage et Coaching Sportif en Temps Réel

SmartFit Coach est un système intelligent qui utilise la vision par ordinateur pour détecter les mouvements du corps, compter automatiquement les répétitions d'exercices et fournir un feedback en temps réel sur l'exécution.

---

## 🎯 Fonctionnalités

- ✅ **Détection de pose en temps réel** : Identification de 33 points clés du corps
- ✅ **Comptage automatique** : Compte les répétitions pour différents exercices (squats, pompes, etc.)
- ✅ **Reconnaissance d'exercice** : Identifie automatiquement le type d'exercice effectué
- ✅ **Feedback intelligent** : Conseils pour améliorer l'exécution des mouvements
- ✅ **Interface intuitive** : Visualisation claire avec compteur et retours visuels

---

## 🛠️ Technologies Utilisées

- **Python 3.8+**
- **OpenCV** : Traitement vidéo et capture webcam
- **MediaPipe** : Détection de pose en temps réel
- **NumPy** : Calculs mathématiques
- **Scikit-learn** : Classification des exercices
- **Streamlit** : Interface utilisateur web

---

## 📦 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/itsmardochee/SmartFit-Coach.git
cd SmartFit-Coach
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### Démonstration de la détection de pose

Lancez le script de démonstration pour tester la détection en temps réel :

```bash
python demo_detection.py
```

**Contrôles :**
- Appuyez sur `q` pour quitter

### Lancer l'application complète (à venir)

```bash
streamlit run interface/app.py
```

---

## 📁 Structure du Projet

```
SmartFit-Coach/
├── src/
│   ├── detection/          # Détection de pose et capture vidéo
│   │   ├── video_capture.py
│   │   └── pose_detector.py
│   ├── counting/           # Comptage des répétitions
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

### ✅ Étape 1 : Détection de Pose (En cours)
- [x] Module de capture vidéo
- [x] Détection des 33 keypoints avec MediaPipe
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
