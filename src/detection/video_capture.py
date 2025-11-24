"""
Module de capture vidéo pour SmartFit Coach.
Gère l'accès à la webcam et la lecture des frames.
"""

import cv2
from typing import Optional, Tuple
import numpy as np
import platform


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

    def __init__(self, source: object = 0):
        """
        Initialise la capture vidéo.

        Args:
            source: Identifiant de la caméra (int) ou chemin du fichier vidéo (str)
        """
        self.source = source
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_opened = False

    def start(self) -> bool:
        """
        Démarre la capture vidéo.

        Utilise DirectShow sur Windows pour éviter les problèmes avec Media Foundation
        si la source est une caméra (int).

        Returns:
            bool: True si la source est accessible, False sinon
        """
        # Déterminer si la source est un index de caméra ou un fichier
        is_camera_index = False
        camera_index = 0
        
        if isinstance(self.source, int):
            is_camera_index = True
            camera_index = self.source
        elif isinstance(self.source, str) and self.source.isdigit():
            # Cas où l'index est passé en string "0"
            is_camera_index = True
            camera_index = int(self.source)
            
        if not is_camera_index:
            # C'est un fichier vidéo (chemin)
            self.cap = cv2.VideoCapture(self.source)
        else:
            # C'est une caméra
            # C'est une caméra
            if platform.system() == "Windows":
                # Essayer d'abord avec DirectShow
                self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
                
                # Si ça échoue, essayer le backend par défaut
                if not self.cap.isOpened():
                    self.cap = cv2.VideoCapture(camera_index)
            else:
                self.cap = cv2.VideoCapture(camera_index)

        self.is_opened = self.cap.isOpened()

        if self.is_opened:
            # Configuration pour de meilleures performances (seulement pour webcam)
            if is_camera_index:
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
        
        # Si la lecture échoue et que c'est un fichier vidéo (pas une caméra index en str), on boucle
        is_file = isinstance(self.source, str) and not self.source.isdigit()
        if not success and is_file:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
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


def list_available_cameras(max_cameras: int = 10) -> list:
    """
    Détecte les caméras disponibles sur le système.
    
    Args:
        max_cameras: Nombre maximum de caméras à tester
        
    Returns:
        Liste des IDs de caméras disponibles avec leurs noms
    """
    available_cameras = []
    
    for camera_id in range(max_cameras):
        try:
            # Essayer d'ouvrir la caméra
            if platform.system() == "Windows":
                cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(camera_id)
            
            # Vérifier si elle fonctionne
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    # Récupérer les infos de la caméra
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    camera_info = {
                        'id': camera_id,
                        'name': f"Caméra {camera_id}",
                        'resolution': f"{width}x{height}",
                        'fps': fps if fps > 0 else 30
                    }
                    available_cameras.append(camera_info)
                
                cap.release()
        except Exception:
            continue
    
    return available_cameras
