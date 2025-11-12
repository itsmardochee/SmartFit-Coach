"""
Module de capture vidéo pour SmartFit Coach.
Gère l'accès à la webcam et la lecture des frames.
"""

import cv2
from typing import Optional, Tuple
import numpy as np


class VideoCapture:
    """
    Classe pour gérer la capture vidéo depuis une webcam.

    Cette classe encapsule les fonctionnalités d'OpenCV pour faciliter
    l'accès à la caméra et la lecture des images.

    Attributes:
        camera_id (int): Identifiant de la caméra (0 par défaut)
        cap (cv2.VideoCapture): Objet de capture OpenCV
        is_opened (bool): État de la connexion à la caméra
    """

    def __init__(self, camera_id: int = 0):
        """
        Initialise la capture vidéo.

        Args:
            camera_id: Identifiant de la caméra (0 pour la caméra par défaut)
        """
        self.camera_id = camera_id
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_opened = False

    def start(self) -> bool:
        """
        Démarre la capture vidéo.

        Returns:
            bool: True si la caméra est accessible, False sinon
        """
        self.cap = cv2.VideoCapture(self.camera_id)
        self.is_opened = self.cap.isOpened()

        if self.is_opened:
            # Configuration pour de meilleures performances
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

        return self.is_opened

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Lit une frame depuis la caméra.

        Returns:
            Tuple[bool, Optional[np.ndarray]]:
                - Success (bool): True si la lecture a réussi
                - Frame (np.ndarray ou None): L'image capturée ou None en cas d'erreur
        """
        if not self.is_opened or self.cap is None:
            return False, None

        success, frame = self.cap.read()
        return success, frame

    def get_frame_dimensions(self) -> Tuple[int, int]:
        """
        Récupère les dimensions de la frame.

        Returns:
            Tuple[int, int]: (largeur, hauteur) de la frame
        """
        if self.cap is None:
            return 0, 0

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def get_fps(self) -> float:
        """
        Récupère le nombre de frames par seconde.

        Returns:
            float: FPS de la caméra
        """
        if self.cap is None:
            return 0.0

        return self.cap.get(cv2.CAP_PROP_FPS)

    def release(self) -> None:
        """
        Libère les ressources de la caméra.
        """
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False

    def __enter__(self):
        """Context manager: entrée."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: sortie."""
        self.release()

    def __del__(self):
        """Destructeur: s'assure que la caméra est libérée."""
        self.release()
