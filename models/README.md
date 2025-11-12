# 🤖 Dossier Models

Ce dossier contient les modèles d'apprentissage automatique entraînés pour SmartFit Coach.

## Structure

```
models/
├── exercise_classifier.pkl    # Modèle de classification d'exercices
├── pose_corrector.h5          # Modèle de correction de posture (optionnel)
└── README.md                  # Ce fichier
```

## Modèles à Développer

### 1. Classificateur d'Exercices
- **Type :** RandomForest ou LSTM
- **Entrée :** Séquence de keypoints (33 points × N frames)
- **Sortie :** Type d'exercice (squat, pompe, fente)
- **Format :** `.pkl` (scikit-learn) ou `.h5` (TensorFlow)

### 2. Correcteur de Posture (optionnel)
- **Type :** CNN ou réseau récurrent
- **Entrée :** Keypoints + angles calculés
- **Sortie :** Score de qualité + suggestions
- **Format :** `.h5` (TensorFlow/Keras)

## Entraînement

Les notebooks d'entraînement se trouvent dans `notebooks/`:
- `02_train_classifier.ipynb` : Entraînement du classificateur d'exercices
- `03_train_corrector.ipynb` : Entraînement du correcteur de posture

## Notes

⚠️ Les modèles entraînés ne sont pas versionnés dans Git (voir `.gitignore`).
📦 Partagez vos modèles via des plateformes comme Hugging Face ou Google Drive.
