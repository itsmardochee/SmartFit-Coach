"""
Module de détection de pose utilisant MediaPipe.
Extrait les 33 points clés du corps humain en temps réel.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Keypoint:
    """
    Représente un point clé du corps détecté.

    Attributes:
        id: Identifiant du point (0-32 pour MediaPipe)
        name: Nom du point (ex: "left_shoulder")
        x: Coordonnée x normalisée [0, 1]
        y: Coordonnée y normalisée [0, 1]
        z: Profondeur relative (optionnel)
        visibility: Score de confiance [0, 1]
    """

    id: int
    name: str
    x: float
    y: float
    z: float
    visibility: float

    def to_pixel_coords(self, width: int, height: int) -> Tuple[int, int]:
        """
        Convertit les coordonnées normalisées en pixels.

        Args:
            width: Largeur de l'image en pixels
            height: Hauteur de l'image en pixels

        Returns:
            Tuple[int, int]: Coordonnées (x, y) en pixels
        """
        return int(self.x * width), int(self.y * height)


class PoseDetector:
    """
    Détecteur de pose utilisant MediaPipe Pose.

    Cette classe détecte les 33 points clés du corps humain et fournit
    des méthodes pour extraire et analyser ces données.

    Attributes:
        min_detection_confidence: Seuil de confiance minimum pour la détection
        min_tracking_confidence: Seuil de confiance minimum pour le suivi
        mp_pose: Module MediaPipe Pose
        pose: Objet de détection MediaPipe
    """

    # Noms des 33 keypoints MediaPipe Pose
    KEYPOINT_NAMES = [
        "nose",
        "left_eye_inner",
        "left_eye",
        "left_eye_outer",
        "right_eye_inner",
        "right_eye",
        "right_eye_outer",
        "left_ear",
        "right_ear",
        "mouth_left",
        "mouth_right",
        "left_shoulder",
        "right_shoulder",
        "left_elbow",
        "right_elbow",
        "left_wrist",
        "right_wrist",
        "left_pinky",
        "right_pinky",
        "left_index",
        "right_index",
        "left_thumb",
        "right_thumb",
        "left_hip",
        "right_hip",
        "left_knee",
        "right_knee",
        "left_ankle",
        "right_ankle",
        "left_heel",
        "right_heel",
        "left_foot_index",
        "right_foot_index",
    ]

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        """
        Initialise le détecteur de pose.

        Args:
            min_detection_confidence: Confiance minimum pour détecter (0.0 à 1.0)
            min_tracking_confidence: Confiance minimum pour suivre (0.0 à 1.0)
        """
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Initialisation de MediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=1,  # 0=lite, 1=full, 2=heavy
        )

    def detect(self, frame: np.ndarray) -> Optional[List[Keypoint]]:
        """
        Détecte les points clés sur une frame.

        Args:
            frame: Image BGR depuis OpenCV

        Returns:
            List[Keypoint] ou None: Liste des keypoints détectés ou None si aucune détection
        """
        # Conversion BGR -> RGB (MediaPipe utilise RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Détection
        results = self.pose.process(frame_rgb)

        # Extraction des keypoints
        if results.pose_landmarks:
            keypoints = []
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                keypoint = Keypoint(
                    id=idx,
                    name=self.KEYPOINT_NAMES[idx],
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                    visibility=landmark.visibility,
                )
                keypoints.append(keypoint)
            return keypoints

        return None

    def get_keypoint_by_name(
        self, keypoints: List[Keypoint], name: str
    ) -> Optional[Keypoint]:
        """
        Récupère un keypoint spécifique par son nom.

        Args:
            keypoints: Liste de tous les keypoints
            name: Nom du keypoint recherché

        Returns:
            Keypoint ou None: Le keypoint trouvé ou None
        """
        for kp in keypoints:
            if kp.name == name:
                return kp
        return None

    def get_keypoints_by_ids(
        self, keypoints: List[Keypoint], ids: List[int]
    ) -> List[Keypoint]:
        """
        Récupère plusieurs keypoints par leurs IDs.

        Args:
            keypoints: Liste de tous les keypoints
            ids: Liste des IDs à récupérer

        Returns:
            List[Keypoint]: Liste des keypoints trouvés
        """
        return [kp for kp in keypoints if kp.id in ids]

    def keypoints_to_dict(self, keypoints: List[Keypoint]) -> Dict:
        """
        Convertit les keypoints en dictionnaire pour export JSON.

        Args:
            keypoints: Liste des keypoints

        Returns:
            Dict: Dictionnaire avec structure standardisée
        """
        return {
            "keypoints": [
                {
                    "id": kp.id,
                    "name": kp.name,
                    "x": float(kp.x),
                    "y": float(kp.y),
                    "z": float(kp.z),
                    "visibility": float(kp.visibility),
                }
                for kp in keypoints
            ]
        }

    def is_visible(self, keypoint: Keypoint, threshold: float = 0.5) -> bool:
        """
        Vérifie si un keypoint est suffisamment visible.

        Args:
            keypoint: Le keypoint à vérifier
            threshold: Seuil de visibilité minimum

        Returns:
            bool: True si le keypoint est visible
        """
        return keypoint.visibility >= threshold

    def release(self) -> None:
        """
        Libère les ressources MediaPipe.
        """
        self.pose.close()

    def __del__(self):
        """Destructeur: s'assure que les ressources sont libérées."""
        self.release()
