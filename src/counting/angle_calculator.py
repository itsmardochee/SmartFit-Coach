"""
Module de calcul d'angles entre les keypoints pour l'analyse des mouvements.
Fournit des fonctions géométriques pour calculer les angles des articulations.
"""

import numpy as np
from typing import Tuple
from src.detection.pose_detector import Keypoint


def calculate_angle(point_a: Keypoint, point_b: Keypoint, point_c: Keypoint) -> float:
    """
    Calcule l'angle entre trois points (A-B-C) où B est le sommet.

    L'angle est calculé en degrés et représente l'angle formé au point B
    par les segments BA et BC.

    Args:
        point_a: Premier point (extrémité)
        point_b: Point central (sommet de l'angle)
        point_c: Troisième point (autre extrémité)

    Returns:
        float: Angle en degrés [0-180]

    Example:
        >>> # Calculer l'angle du coude
        >>> angle = calculate_angle(shoulder, elbow, wrist)
        >>> print(f"Angle du coude: {angle:.1f}°")
    """
    # Convertir les keypoints en vecteurs 2D (ignorer z pour simplifier)
    a = np.array([point_a.x, point_a.y])
    b = np.array([point_b.x, point_b.y])
    c = np.array([point_c.x, point_c.y])

    # Calculer les vecteurs BA et BC
    ba = a - b
    bc = c - b

    # Calculer le cosinus de l'angle via le produit scalaire
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)

    # Limiter le cosinus entre -1 et 1 pour éviter les erreurs numériques
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    # Convertir en degrés
    angle = np.degrees(np.arccos(cosine_angle))

    return float(angle)


def calculate_angle_3d(
    point_a: Keypoint, point_b: Keypoint, point_c: Keypoint
) -> float:
    """
    Calcule l'angle entre trois points en 3D (utilise x, y, z).

    Plus précis que calculate_angle() car prend en compte la profondeur,
    mais nécessite que les keypoints aient des coordonnées z valides.

    Args:
        point_a: Premier point
        point_b: Point central (sommet)
        point_c: Troisième point

    Returns:
        float: Angle en degrés [0-180]
    """
    # Convertir en vecteurs 3D
    a = np.array([point_a.x, point_a.y, point_a.z])
    b = np.array([point_b.x, point_b.y, point_b.z])
    c = np.array([point_c.x, point_c.y, point_c.z])

    # Calculer les vecteurs
    ba = a - b
    bc = c - b

    # Calculer l'angle
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine_angle))

    return float(angle)


def calculate_vertical_distance(point_a: Keypoint, point_b: Keypoint) -> float:
    """
    Calcule la distance verticale normalisée entre deux points.

    Utile pour mesurer la descente dans un squat ou la position dans une pompe.

    Args:
        point_a: Premier point
        point_b: Second point

    Returns:
        float: Distance verticale normalisée [0-1]
    """
    return abs(point_a.y - point_b.y)


def calculate_horizontal_distance(point_a: Keypoint, point_b: Keypoint) -> float:
    """
    Calcule la distance horizontale normalisée entre deux points.

    Args:
        point_a: Premier point
        point_b: Second point

    Returns:
        float: Distance horizontale normalisée [0-1]
    """
    return abs(point_a.x - point_b.x)


def calculate_euclidean_distance(point_a: Keypoint, point_b: Keypoint) -> float:
    """
    Calcule la distance euclidienne 2D entre deux points.

    Args:
        point_a: Premier point
        point_b: Second point

    Returns:
        float: Distance normalisée [0-1.414 approx]
    """
    dx = point_a.x - point_b.x
    dy = point_a.y - point_b.y
    return float(np.sqrt(dx**2 + dy**2))


def is_keypoint_visible(keypoint: Keypoint, min_visibility: float = 0.5) -> bool:
    """
    Vérifie si un keypoint est suffisamment visible pour être utilisé.

    Args:
        keypoint: Point clé à vérifier
        min_visibility: Seuil minimum de visibilité [0-1]

    Returns:
        bool: True si le point est visible, False sinon
    """
    return keypoint.visibility >= min_visibility


def get_body_center(hip_left: Keypoint, hip_right: Keypoint) -> Tuple[float, float]:
    """
    Calcule le centre du corps basé sur les hanches.

    Utile pour normaliser les mouvements et détecter les déplacements.

    Args:
        hip_left: Hanche gauche
        hip_right: Hanche droite

    Returns:
        Tuple[float, float]: Coordonnées (x, y) du centre
    """
    center_x = (hip_left.x + hip_right.x) / 2
    center_y = (hip_left.y + hip_right.y) / 2
    return center_x, center_y


def calculate_body_alignment(
    shoulder: Keypoint, hip: Keypoint, knee: Keypoint, max_deviation: float = 15.0
) -> Tuple[bool, float]:
    """
    Calcule l'alignement du corps (colonne vertébrale/jambes).

    Vérifie si le corps est bien aligné verticalement, utile pour
    détecter une mauvaise posture dans les squats ou les pompes.

    Args:
        shoulder: Épaule
        hip: Hanche
        knee: Genou
        max_deviation: Écart maximum acceptable en degrés

    Returns:
        Tuple[bool, float]: (est_aligné, angle_avec_verticale)
    """
    # Calculer l'angle avec une ligne verticale imaginaire
    # On crée un point virtuel au-dessus de la hanche
    virtual_point = Keypoint(
        id=-1,
        name="virtual_top",
        x=hip.x,
        y=hip.y - 0.1,  # Point au-dessus
        z=hip.z,
        visibility=1.0,
    )

    angle = calculate_angle(shoulder, hip, virtual_point)

    # L'angle devrait être proche de 180° pour un alignement parfait
    deviation = abs(180 - angle)
    is_aligned = deviation <= max_deviation

    return is_aligned, deviation


def calculate_knee_angle(hip: Keypoint, knee: Keypoint, ankle: Keypoint) -> float:
    """
    Calcule l'angle du genou (raccourci pour squat).

    Args:
        hip: Hanche
        knee: Genou
        ankle: Cheville

    Returns:
        float: Angle du genou en degrés
    """
    return calculate_angle(hip, knee, ankle)


def calculate_elbow_angle(
    shoulder: Keypoint, elbow: Keypoint, wrist: Keypoint
) -> float:
    """
    Calcule l'angle du coude (raccourci pour pompes).

    Args:
        shoulder: Épaule
        elbow: Coude
        wrist: Poignet

    Returns:
        float: Angle du coude en degrés
    """
    return calculate_angle(shoulder, elbow, wrist)


def calculate_hip_angle(shoulder: Keypoint, hip: Keypoint, knee: Keypoint) -> float:
    """
    Calcule l'angle de la hanche (raccourci pour squat).

    Args:
        shoulder: Épaule
        hip: Hanche
        knee: Genou

    Returns:
        float: Angle de la hanche en degrés
    """
    return calculate_angle(shoulder, hip, knee)
