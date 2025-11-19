"""
Module de classification d'exercices basé sur LSTM.

Ce module charge le modèle LSTM entraîné et permet de classifier
les exercices en temps réel à partir d'une séquence de keypoints.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import deque

try:
    import tensorflow as tf
    from tensorflow import keras

    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow non disponible. Classification LSTM désactivée.")


class ExerciseClassifier:
    """
    Classificateur d'exercices basé sur un modèle LSTM.

    Utilise un buffer de frames pour accumuler les keypoints et
    faire des prédictions en temps réel.
    """

    def __init__(
        self, model_path: Optional[str] = None, metadata_path: Optional[str] = None
    ):
        """
        Initialise le classificateur.

        Args:
            model_path: Chemin vers le modèle .h5 (optionnel)
            metadata_path: Chemin vers les métadonnées JSON (optionnel)
        """
        self.model = None
        self.metadata = None
        self.classes = []
        self.max_sequence_length = 0
        self.n_features = 0
        self.frame_buffer = deque(
            maxlen=60
        )  # Buffer de 60 frames (~2 secondes à 30 FPS)
        self.prediction_interval = 15  # Prédire tous les 15 frames
        self.frame_count = 0
        self.current_exercise = None
        self.confidence = 0.0
        self.confidence_threshold = 0.85  # Seuil de confiance augmenté

        if not TENSORFLOW_AVAILABLE:
            print("⚠️ TensorFlow requis pour la classification")
            return

        # Charger le modèle par défaut si disponible
        if model_path is None:
            model_path = (
                Path(__file__).parent.parent.parent
                / "models"
                / "exercise_classifier_lstm.h5"
            )
        if metadata_path is None:
            metadata_path = (
                Path(__file__).parent.parent.parent
                / "models"
                / "exercise_classifier_metadata.json"
            )

        if Path(model_path).exists() and Path(metadata_path).exists():
            self.load_model(str(model_path), str(metadata_path))
        else:
            print(f"⚠️ Modèle non trouvé. Utilisez load_model() pour charger un modèle.")

    def load_model(self, model_path: str, metadata_path: str) -> bool:
        """
        Charge le modèle et les métadonnées.

        Args:
            model_path: Chemin vers le fichier .h5
            metadata_path: Chemin vers le fichier JSON

        Returns:
            True si le chargement a réussi, False sinon
        """
        if not TENSORFLOW_AVAILABLE:
            print("❌ TensorFlow requis pour charger le modèle")
            return False

        try:
            # Charger le modèle
            self.model = keras.models.load_model(model_path)
            print(f"✅ Modèle chargé: {model_path}")

            # Charger les métadonnées
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)

            self.classes = self.metadata["classes"]
            self.max_sequence_length = self.metadata["max_sequence_length"]
            self.n_features = self.metadata["n_features"]

            print(f"✅ Métadonnées chargées: {len(self.classes)} classes")
            print(f"   Classes: {', '.join(self.classes)}")
            print(f"   Accuracy: {self.metadata.get('test_accuracy', 0):.2%}")

            # Réinitialiser le buffer
            self.frame_buffer = deque(maxlen=self.max_sequence_length)

            return True

        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            return False

    def extract_features_from_keypoints(
        self, keypoints: List[Dict]
    ) -> Optional[List[float]]:
        """
        Extrait les features à partir des keypoints détectés.

        Args:
            keypoints: Liste des keypoints avec 'x', 'y', 'visibility'

        Returns:
            Liste de features ou None si extraction échouée
        """
        try:
            features = []

            # Extraire x, y, visibility pour chaque keypoint
            for kp in keypoints:
                # Support pour dictionnaire ou objet (Keypoint)
                if isinstance(kp, dict):
                    features.extend([kp["x"], kp["y"], kp.get("visibility", 1.0)])
                else:
                    # Supposons que c'est un objet Keypoint
                    features.extend([kp.x, kp.y, getattr(kp, "visibility", 1.0)])

            return features

        except Exception as e:
            print(f"❌ Erreur extraction features: {e}")
            return None

    def add_frame(self, keypoints: List[Dict]) -> None:
        """
        Ajoute une frame de keypoints au buffer.

        Args:
            keypoints: Liste des keypoints de la frame
        """
        features = self.extract_features_from_keypoints(keypoints)

        if features is not None:
            self.frame_buffer.append(features)
            self.frame_count += 1

    def predict(
        self, force: bool = False
    ) -> Optional[Tuple[str, float, Dict[str, float]]]:
        """
        Fait une prédiction sur le buffer actuel.

        Args:
            force: Forcer la prédiction même si l'intervalle n'est pas atteint

        Returns:
            Tuple (exercice_prédit, confiance, probabilités) ou None
        """
        if not TENSORFLOW_AVAILABLE or self.model is None:
            return None

        # Vérifier si on doit prédire
        if not force and self.frame_count % self.prediction_interval != 0:
            return None

        # Vérifier qu'on a assez de frames
        if len(self.frame_buffer) < 30:  # Minimum 30 frames (~1 seconde)
            return None

        try:
            # Préparer la séquence
            sequence = np.array(list(self.frame_buffer))

            # Padding si nécessaire
            if len(sequence) < self.max_sequence_length:
                padded = np.zeros((self.max_sequence_length, self.n_features))
                padded[: len(sequence)] = sequence
                sequence = padded
            else:
                sequence = sequence[: self.max_sequence_length]

            # Ajouter dimension batch
            sequence = sequence.reshape(1, self.max_sequence_length, self.n_features)

            # Prédiction
            predictions = self.model.predict(sequence, verbose=0)
            probabilities = predictions[0]

            # Classe prédite
            predicted_class_idx = np.argmax(probabilities)
            predicted_class = self.classes[predicted_class_idx]
            confidence = probabilities[predicted_class_idx]

            # Créer dictionnaire de probabilités
            prob_dict = {
                self.classes[i]: float(probabilities[i])
                for i in range(len(self.classes))
            }

            # Mettre à jour l'état si confiance suffisante
            if confidence >= self.confidence_threshold:
                # Logique de lissage : confirmer la prédiction plusieurs fois
                if not hasattr(self, 'prediction_history'):
                    self.prediction_history = deque(maxlen=10)
                
                self.prediction_history.append(predicted_class)
                
                # Si l'historique est plein et contient une majorité de la même classe (8/10)
                if len(self.prediction_history) == 10:
                    most_common = max(set(self.prediction_history), key=self.prediction_history.count)
                    count = self.prediction_history.count(most_common)
                    
                    if count >= 8:
                        self.current_exercise = most_common
                        self.confidence = confidence
            else:
                # Si confiance faible, on peut reset l'historique pour éviter les faux positifs
                if hasattr(self, 'prediction_history'):
                    self.prediction_history.clear()

            return predicted_class, float(confidence), prob_dict

        except Exception as e:
            print(f"❌ Erreur prédiction: {e}")
            return None

    def get_current_exercise(self) -> Optional[str]:
        """
        Retourne l'exercice actuellement détecté.

        Returns:
            Nom de l'exercice ou None
        """
        return self.current_exercise

    def get_confidence(self) -> float:
        """
        Retourne la confiance de la prédiction actuelle.

        Returns:
            Score de confiance entre 0 et 1
        """
        return self.confidence

    def reset(self) -> None:
        """Réinitialise le buffer et l'état."""
        self.frame_buffer.clear()
        self.frame_count = 0
        self.current_exercise = None
        self.confidence = 0.0

    def is_ready(self) -> bool:
        """
        Vérifie si le classificateur est prêt à faire des prédictions.

        Returns:
            True si le modèle est chargé et le buffer a assez de frames
        """
        return (
            TENSORFLOW_AVAILABLE
            and self.model is not None
            and len(self.frame_buffer) >= 30
        )

    def get_info(self) -> Dict:
        """
        Retourne les informations sur le classificateur.

        Returns:
            Dictionnaire avec les infos du classificateur
        """
        return {
            "model_loaded": self.model is not None,
            "classes": self.classes,
            "buffer_size": len(self.frame_buffer),
            "max_buffer_size": self.frame_buffer.maxlen,
            "current_exercise": self.current_exercise,
            "confidence": self.confidence,
            "ready": self.is_ready(),
            "tensorflow_available": TENSORFLOW_AVAILABLE,
        }


# Test du module
if __name__ == "__main__":
    print("🧪 Test du classificateur d'exercices")
    print("-" * 50)

    # Créer le classificateur
    classifier = ExerciseClassifier()

    # Afficher les infos
    info = classifier.get_info()
    print(f"\n📊 Informations:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    if classifier.model is not None:
        print(f"\n✅ Classificateur prêt!")
        print(f"   Classes supportées: {', '.join(classifier.classes)}")
    else:
        print(f"\n⚠️ Aucun modèle chargé")
