# 🧠 Instructions Copilot - SmartFit Coach

## 📋 Contexte du Projet

SmartFit Coach est un système de comptage et coaching sportif en temps réel utilisant la vision par ordinateur. Le système détecte les mouvements du corps, compte automatiquement les répétitions d'exercices et fournit un feedback sur l'exécution.

## 🎯 Objectifs du Projet

- Détecter les mouvements du corps en temps réel via webcam
- Compter automatiquement les répétitions pour 2 à 3 types d'exercices (squats, pompes, etc.)
- Fournir un feedback simple et clair sur l'exécution des mouvements
- Afficher une interface utilisateur intuitive avec compteur et feedback visuel

## 🛠️ Stack Technique

### Langages et Frameworks Principaux
- **Python 3.8+** : Langage principal du projet
- **OpenCV** : Traitement vidéo et capture webcam
- **MediaPipe Pose** ou **MoveNet** : Détection de pose et extraction des keypoints
- **NumPy** : Calculs mathématiques et traitement des données
- **Scikit-learn** ou **TensorFlow** : Classification et reconnaissance d'exercices

### Interface Utilisateur
- **Streamlit** : Interface web simple et rapide
- Alternative : **Flask** ou **FastAPI** pour une API REST

### Outils Complémentaires
- **Matplotlib/Seaborn** : Visualisation des données d'entraînement
- **Pandas** : Manipulation des datasets
- **TensorFlow Lite** : Déploiement mobile (optionnel)

## 📐 Architecture du Projet

```
SmartFit-Coach/
├── src/
│   ├── detection/          # Modules de détection de pose
│   ├── counting/           # Logique de comptage des répétitions
│   ├── recognition/        # Classification des exercices
│   ├── feedback/           # Génération du feedback
│   └── utils/              # Fonctions utilitaires
├── models/                 # Modèles ML entraînés
├── data/                   # Datasets et vidéos de test
├── interface/              # Code de l'interface utilisateur
├── tests/                  # Tests unitaires et d'intégration
├── docs/                   # Documentation technique
├── notebooks/              # Jupyter notebooks pour expérimentation
└── requirements.txt        # Dépendances Python
```

## 🎓 Règles de Code et Conventions

### Style de Code
- **PEP 8** : Suivre strictement les conventions Python
- **Type hints** : Utiliser les annotations de type pour toutes les fonctions
- **Docstrings** : Format Google ou NumPy pour toutes les classes et fonctions
- **Noms explicites** : Variables et fonctions en anglais clair
- **Constantes** : En MAJUSCULES (ex: `SEUIL_ANGLE_SQUAT = 90`)

### Documentation
- **Langue** : Toute la documentation DOIT être en **français**
- **Clarté** : Explications compréhensibles par des non-experts en IA
- **Exemples** : Inclure des exemples d'utilisation dans les docstrings
- **README** : Maintenir à jour avec instructions d'installation et d'utilisation

### Commentaires
- Expliquer le **pourquoi**, pas le **quoi**
- Documenter les seuils et paramètres critiques
- Justifier les choix d'algorithmes et de valeurs

## 🔄 Plan de Développement par Étapes

### 📍 Étape 1 : Détection de Pose en Temps Réel

**Objectif :** Mettre en place la détection du corps et visualiser les points clés (keypoints).

**Livrables :**
- Module de capture vidéo fonctionnel
- Détection des 33 points clés du corps avec MediaPipe
- Visualisation en temps réel des squelettes sur la vidéo
- Extraction et stockage des coordonnées (x, y, visibilité)

**Fichiers à créer :**
- `src/detection/pose_detector.py` : Classe principale de détection
- `src/detection/video_capture.py` : Gestion de la webcam
- `src/utils/visualization.py` : Fonctions d'affichage
- `notebooks/01_test_detection.ipynb` : Expérimentation

**Critères de validation :**
- Détection fluide à 30 FPS minimum
- Précision acceptable sur différentes morphologies
- Gestion des erreurs (caméra non disponible, etc.)

---

### 📍 Étape 2 : Comptage Automatique des Répétitions

**Objectif :** Implémenter un système de comptage fiable pour 2-3 exercices.

**Exercices prioritaires :**
1. **Squats** : Détection basée sur l'angle genou et hanche
2. **Pompes** : Détection basée sur l'angle coude et distance sol
3. **Fentes** (optionnel) : Angle genou et position jambes

**Livrables :**
- Algorithmes de calcul d'angles entre articulations
- Logique de détection de cycles (phase montée/descente)
- Système anti-rebond pour éviter les faux positifs
- Compteur affiché en temps réel

**Fichiers à créer :**
- `src/counting/angle_calculator.py` : Calculs géométriques
- `src/counting/rep_counter.py` : Logique de comptage
- `src/counting/exercise_detectors/` : Détecteurs par exercice
- `tests/test_counting.py` : Tests unitaires

**Paramètres clés à définir :**
- Seuils d'angles pour chaque exercice
- Durée minimale d'un cycle
- Tolérance sur les positions

---

### 📍 Étape 3 : Reconnaissance d'Exercice et Feedback

**Objectif :** Reconnaître automatiquement l'exercice et générer un feedback simple.

**Livrables :**
- Modèle de classification léger (RandomForest ou LSTM)
- Dataset annoté pour 2-3 exercices
- Système de détection des erreurs de posture
- Génération de feedback textuel et visuel

**Fichiers à créer :**
- `src/recognition/exercise_classifier.py` : Modèle de classification
- `src/feedback/posture_analyzer.py` : Analyse de la posture
- `src/feedback/feedback_generator.py` : Génération des messages
- `data/exercises/` : Datasets annotés
- `notebooks/02_train_classifier.ipynb` : Entraînement du modèle

**Types de feedback à implémenter :**
- "✅ Bon mouvement !"
- "⚠️ Descends plus bas"
- "⚠️ Garde le dos droit"
- "⚠️ Ralentis le mouvement"

**Règles pour le feedback :**
- Messages courts et actionnables
- Couleurs pour l'urgence (vert/orange/rouge)
- Éviter les messages trop fréquents (limite à 1 toutes les 3 secondes)

---

### 📍 Étape 4 : Interface Utilisateur et Intégration

**Objectif :** Créer une interface complète et intuitive intégrant tous les modules.

**Livrables :**
- Interface Streamlit ou Flask
- Vue caméra avec overlay du squelette
- Panneau de statistiques (répétitions, calories, temps)
- Système de session d'entraînement
- Historique des performances
- Vidéo de démonstration

**Fichiers à créer :**
- `interface/app.py` : Application principale
- `interface/components/` : Composants UI réutilisables
- `interface/static/` : Assets (CSS, images, icônes)
- `src/session/workout_session.py` : Gestion des sessions

**Fonctionnalités UI :**
1. Sélection de l'exercice
2. Démarrage/pause/arrêt de la session
3. Affichage en temps réel :
   - Vidéo avec squelette
   - Compteur de répétitions
   - Feedback actuel
   - Chronomètre
4. Résumé de fin de session
5. Export des données (CSV/JSON)

---

## 🧪 Tests et Qualité

### Tests Obligatoires
- **Tests unitaires** : Couverture minimum de 70%
- **Tests d'intégration** : Scénarios bout-en-bout
- **Tests de performance** : FPS, latence, précision

### Validation
- Tester sur au moins 3 personnes différentes
- Vérifier la robustesse aux conditions d'éclairage variées
- Valider avec différents angles de caméra

### Commandes de Test
```bash
# Exécuter tous les tests
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=src --cov-report=html

# Tests de performance
python tests/benchmark_detection.py
```

---

## 📊 Gestion des Données

### Formats de Données

**Keypoints (points clés) :**
```python
{
    "timestamp": float,
    "keypoints": [
        {
            "id": int,
            "name": str,
            "x": float,  # Coordonnée normalisée [0, 1]
            "y": float,  # Coordonnée normalisée [0, 1]
            "z": float,  # Profondeur (optionnel)
            "visibility": float  # Score de confiance [0, 1]
        }
    ]
}
```

**Session d'entraînement :**
```python
{
    "session_id": str,
    "date": datetime,
    "exercise": str,
    "repetitions": int,
    "duration": float,  # en secondes
    "feedback_history": List[str],
    "quality_score": float  # Score moyen de qualité [0, 1]
}
```

### Persistance
- Sessions enregistrées en JSON dans `data/sessions/`
- Modèles sauvegardés dans `models/`
- Logs dans `logs/`

---

## 🚀 Performance et Optimisation

### Objectifs de Performance
- **FPS** : Minimum 30 images/seconde
- **Latence** : < 100ms entre détection et affichage
- **Précision comptage** : > 95% sur exercices bien exécutés
- **Mémoire** : < 500 MB RAM

### Optimisations Recommandées
- Utiliser `MediaPipe` en mode "lite" pour mobile
- Réduire la résolution vidéo si nécessaire (640x480)
- Calculer les angles uniquement pour les keypoints pertinents
- Cache pour les calculs répétitifs
- Threading pour séparer capture et traitement

---

## 🔐 Sécurité et Confidentialité

### Données Personnelles
- **Pas de stockage cloud** par défaut
- Vidéos traitées en local uniquement
- Option d'anonymisation des statistiques
- Consentement explicite pour tout enregistrement

### Bonnes Pratiques
- Ne jamais commit de vidéos personnelles
- Nettoyer les données de test régulièrement
- Documenter toute collecte de données

---

## 📚 Ressources et Références

### Documentation Officielle
- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Streamlit](https://docs.streamlit.io/)

### Datasets Publics
- [Workout Dataset on Kaggle](https://www.kaggle.com/)
- Vidéos YouTube avec licence Creative Commons
- Créer son propre dataset avec l'équipe

### Tutoriels Recommandés
- Détection de pose avec MediaPipe
- Calcul d'angles entre articulations
- Classification de séquences temporelles avec LSTM

---

## 🐛 Gestion des Erreurs Courantes

### Problèmes de Détection
- **Visibilité faible** : Afficher un message "Recule-toi de la caméra"
- **Keypoints manquants** : Utiliser l'interpolation ou ignorer la frame
- **Occlusions** : Détection de confiance basse → feedback "Position non détectée"

### Problèmes de Performance
- **FPS bas** : Réduire la résolution ou désactiver certaines fonctionnalités
- **Latence élevée** : Optimiser la pipeline de traitement
- **Surcharge mémoire** : Libérer les ressources après chaque session

---

## 💬 Messages d'Aide Copilot

### Pour la Génération de Code
- "Crée une fonction pour calculer l'angle entre trois points clés"
- "Implémente le compteur de répétitions pour les squats"
- "Génère une interface Streamlit avec vue caméra et compteur"

### Pour la Documentation
- "Documente cette classe avec des docstrings en français"
- "Explique cet algorithme de manière simple pour des débutants"
- "Crée un README avec instructions d'installation"

### Pour les Tests
- "Écris des tests unitaires pour le module de comptage"
- "Génère des données de test pour la classification"
- "Crée un benchmark de performance pour la détection"

---

## ✅ Checklist de Validation Finale

### Fonctionnalités
- [ ] Détection de pose en temps réel (30 FPS minimum)
- [ ] Comptage automatique pour au moins 2 exercices
- [ ] Reconnaissance automatique du type d'exercice
- [ ] Feedback visuel et textuel sur la posture
- [ ] Interface utilisateur claire et intuitive
- [ ] Enregistrement des sessions d'entraînement

### Qualité du Code
- [ ] Tous les tests passent
- [ ] Couverture de tests > 70%
- [ ] Documentation complète en français
- [ ] Code formaté selon PEP 8
- [ ] Pas d'erreurs de linting
- [ ] README à jour avec instructions claires

### Documentation
- [ ] Docstrings pour toutes les fonctions/classes
- [ ] Commentaires pour les parties complexes
- [ ] Guide d'installation fonctionnel
- [ ] Guide d'utilisation avec captures d'écran
- [ ] Documentation technique (architecture, algorithmes)

### Démo et Présentation
- [ ] Vidéo de démonstration (2-3 minutes)
- [ ] Slides de présentation
- [ ] Tests validés sur plusieurs utilisateurs
- [ ] Gestion des cas limites (éclairage, position, etc.)

---

## 🎯 Philosophie de Développement

### Priorités
1. **Simplicité** : Commencer simple, complexifier progressivement
2. **Robustesse** : Gérer les erreurs gracieusement
3. **Clarté** : Code lisible et documenté
4. **Performance** : Optimiser sans sacrifier la lisibilité
5. **Accessibilité** : Interface compréhensible par tous

### Valeurs
- **Pragmatisme** : Utiliser des solutions éprouvées
- **Itération** : Améliorer continuellement
- **Collaboration** : Code partageable et maintenable
- **Pédagogie** : Documentation claire pour faciliter l'apprentissage

---

## 🔧 Commandes Utiles

### Installation
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Développement
```bash
# Lancer l'application
streamlit run interface/app.py

# Exécuter les tests
pytest tests/ -v

# Formater le code
black src/ tests/ interface/

# Vérifier le style
flake8 src/ tests/ interface/

# Type checking
mypy src/
```

### Notebooks
```bash
# Lancer Jupyter
jupyter notebook notebooks/

# Ou avec JupyterLab
jupyter lab notebooks/
```

---

## 📞 Support et Ressources

### En Cas de Problème
1. Vérifier les logs dans `logs/`
2. Consulter la documentation des librairies
3. Chercher sur Stack Overflow
4. Demander à l'équipe ou au mentor

### Contribuer
- Suivre les conventions de ce document
- Créer une branche par fonctionnalité
- Écrire des tests pour toute nouvelle fonctionnalité
- Mettre à jour la documentation

---

**Version :** 1.0  
**Dernière mise à jour :** Novembre 2025  
**Équipe :** SmartFit Coach Development Team
