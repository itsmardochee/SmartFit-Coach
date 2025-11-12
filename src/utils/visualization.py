"""
Module de visualisation pour SmartFit Coach.
Fonctions pour dessiner les squelettes et le feedback sur les frames vidéo.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Tuple, Optional
from ..detection.pose_detector import Keypoint


# Couleurs prédéfinies (BGR)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)


class SkeletonDrawer:
    """
    Classe pour dessiner les squelettes sur les frames vidéo.
    """

    # Connexions entre les keypoints (format MediaPipe)
    POSE_CONNECTIONS = [
        # Visage
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 7),
        (0, 4),
        (4, 5),
        (5, 6),
        (6, 8),
        (9, 10),
        # Épaules et bras
        (11, 12),
        (11, 13),
        (13, 15),
        (15, 17),
        (15, 19),
        (15, 21),
        (12, 14),
        (14, 16),
        (16, 18),
        (16, 20),
        (16, 22),
        # Torse
        (11, 23),
        (12, 24),
        (23, 24),
        # Jambes
        (23, 25),
        (25, 27),
        (27, 29),
        (27, 31),
        (24, 26),
        (26, 28),
        (28, 30),
        (28, 32),
    ]

    def __init__(self, draw_connections: bool = True, draw_landmarks: bool = True):
        """
        Initialise le dessinateur de squelette.

        Args:
            draw_connections: Dessiner les connexions entre points
            draw_landmarks: Dessiner les points clés
        """
        self.draw_connections = draw_connections
        self.draw_landmarks = draw_landmarks
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def draw(
        self,
        frame: np.ndarray,
        keypoints: List[Keypoint],
        color: Tuple[int, int, int] = COLOR_GREEN,
        thickness: int = 2,
    ) -> np.ndarray:
        """
        Dessine le squelette sur une frame.

        Args:
            frame: Image BGR sur laquelle dessiner
            keypoints: Liste des keypoints détectés
            color: Couleur des lignes (BGR)
            thickness: Épaisseur des lignes

        Returns:
            np.ndarray: Frame avec le squelette dessiné
        """
        height, width = frame.shape[:2]
        frame_copy = frame.copy()

        # Dessiner les connexions
        if self.draw_connections:
            for connection in self.POSE_CONNECTIONS:
                start_idx, end_idx = connection

                if start_idx < len(keypoints) and end_idx < len(keypoints):
                    start_kp = keypoints[start_idx]
                    end_kp = keypoints[end_idx]

                    # Ne dessiner que si les deux points sont visibles
                    if start_kp.visibility > 0.5 and end_kp.visibility > 0.5:
                        start_pos = start_kp.to_pixel_coords(width, height)
                        end_pos = end_kp.to_pixel_coords(width, height)

                        cv2.line(frame_copy, start_pos, end_pos, color, thickness)

        # Dessiner les landmarks
        if self.draw_landmarks:
            for kp in keypoints:
                if kp.visibility > 0.5:
                    pos = kp.to_pixel_coords(width, height)
                    cv2.circle(frame_copy, pos, 4, color, -1)
                    cv2.circle(frame_copy, pos, 5, COLOR_WHITE, 1)

        return frame_copy


def draw_text_with_background(
    frame: np.ndarray,
    text: str,
    position: Tuple[int, int],
    font_scale: float = 1.0,
    font_thickness: int = 2,
    text_color: Tuple[int, int, int] = COLOR_WHITE,
    bg_color: Tuple[int, int, int] = COLOR_BLACK,
    padding: int = 10,
) -> np.ndarray:
    """
    Dessine du texte avec un fond coloré sur une frame.

    Args:
        frame: Image sur laquelle dessiner
        text: Texte à afficher
        position: Position (x, y) du coin supérieur gauche
        font_scale: Taille de la police
        font_thickness: Épaisseur du texte
        text_color: Couleur du texte (BGR)
        bg_color: Couleur du fond (BGR)
        padding: Espacement autour du texte

    Returns:
        np.ndarray: Frame avec le texte dessiné
    """
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Calculer la taille du texte
    (text_width, text_height), baseline = cv2.getTextSize(
        text, font, font_scale, font_thickness
    )

    x, y = position

    # Dessiner le rectangle de fond
    cv2.rectangle(
        frame,
        (x - padding, y - text_height - padding),
        (x + text_width + padding, y + baseline + padding),
        bg_color,
        -1,
    )

    # Dessiner le texte
    cv2.putText(
        frame, text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
    )

    return frame


def draw_fps(frame: np.ndarray, fps: float) -> np.ndarray:
    """
    Affiche le FPS dans le coin supérieur droit.

    Args:
        frame: Image sur laquelle dessiner
        fps: Frames par seconde

    Returns:
        np.ndarray: Frame avec le FPS affiché
    """
    text = f"FPS: {fps:.1f}"
    height, width = frame.shape[:2]
    position = (width - 150, 30)

    return draw_text_with_background(
        frame,
        text,
        position,
        font_scale=0.6,
        font_thickness=2,
        text_color=COLOR_GREEN if fps >= 25 else COLOR_RED,
        bg_color=(0, 0, 0),
    )


def draw_counter(
    frame: np.ndarray, count: int, exercise_name: str = "Répétitions"
) -> np.ndarray:
    """
    Affiche le compteur de répétitions.

    Args:
        frame: Image sur laquelle dessiner
        count: Nombre de répétitions
        exercise_name: Nom de l'exercice

    Returns:
        np.ndarray: Frame avec le compteur affiché
    """
    text = f"{exercise_name}: {count}"
    position = (20, 50)

    return draw_text_with_background(
        frame,
        text,
        position,
        font_scale=1.2,
        font_thickness=3,
        text_color=COLOR_YELLOW,
        bg_color=(0, 0, 0),
        padding=15,
    )


def draw_feedback(
    frame: np.ndarray, feedback: str, feedback_type: str = "info"
) -> np.ndarray:
    """
    Affiche un message de feedback sur l'écran.

    Args:
        frame: Image sur laquelle dessiner
        feedback: Message à afficher
        feedback_type: Type de feedback ("success", "warning", "error", "info")

    Returns:
        np.ndarray: Frame avec le feedback affiché
    """
    # Couleurs selon le type
    color_map = {
        "success": COLOR_GREEN,
        "warning": COLOR_YELLOW,
        "error": COLOR_RED,
        "info": COLOR_BLUE,
    }

    text_color = color_map.get(feedback_type, COLOR_WHITE)
    height, width = frame.shape[:2]
    position = (20, height - 50)

    return draw_text_with_background(
        frame,
        feedback,
        position,
        font_scale=0.8,
        font_thickness=2,
        text_color=text_color,
        bg_color=(0, 0, 0),
        padding=12,
    )


def draw_skeleton(
    frame: np.ndarray,
    keypoints: List[Keypoint],
    color: Tuple[int, int, int] = COLOR_GREEN,
) -> np.ndarray:
    """
    Fonction simplifiée pour dessiner un squelette.

    Args:
        frame: Image sur laquelle dessiner
        keypoints: Liste des keypoints
        color: Couleur du squelette

    Returns:
        np.ndarray: Frame avec le squelette
    """
    drawer = SkeletonDrawer()
    return drawer.draw(frame, keypoints, color=color)


def create_overlay(
    frame: np.ndarray,
    keypoints: Optional[List[Keypoint]] = None,
    fps: Optional[float] = None,
    count: Optional[int] = None,
    exercise_name: str = "Répétitions",
    feedback: Optional[str] = None,
    feedback_type: str = "info",
) -> np.ndarray:
    """
    Crée un overlay complet avec squelette, FPS, compteur et feedback.

    Args:
        frame: Image de base
        keypoints: Points clés à dessiner (optionnel)
        fps: FPS à afficher (optionnel)
        count: Compteur de répétitions (optionnel)
        exercise_name: Nom de l'exercice
        feedback: Message de feedback (optionnel)
        feedback_type: Type de feedback

    Returns:
        np.ndarray: Frame avec tous les overlays
    """
    result = frame.copy()

    # Dessiner le squelette
    if keypoints:
        result = draw_skeleton(result, keypoints)

    # Afficher le FPS
    if fps is not None:
        result = draw_fps(result, fps)

    # Afficher le compteur
    if count is not None:
        result = draw_counter(result, count, exercise_name)

    # Afficher le feedback
    if feedback:
        result = draw_feedback(result, feedback, feedback_type)

    return result
