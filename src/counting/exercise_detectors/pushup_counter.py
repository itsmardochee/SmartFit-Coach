"""
Module de détection et de comptage des pompes (push-ups).
Utilise les angles des coudes et la position du corps pour détecter les répétitions.
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum
import time
from src.detection.pose_detector import Keypoint
from src.counting.angle_calculator import (
    calculate_elbow_angle,
    calculate_vertical_distance,
    is_keypoint_visible,
)


class PushUpPhase(Enum):
    """États possibles d'une pompe."""

    UP = "position_haute"
    DESCENDING = "descente"
    DOWN = "position_basse"
    ASCENDING = "montée"


@dataclass
class PushUpMetrics:
    """Métriques d'analyse d'une pompe."""

    elbow_angle: float
    body_height: float  # Hauteur du corps par rapport au sol
    is_valid: bool
    feedback: str


class PushUpCounter:
    """
    Compteur de répétitions pour les pompes.

    Détecte les cycles complets (descente -> position basse -> montée)
    basés sur les angles des coudes et la hauteur du corps.

    Attributes:
        count: Nombre de répétitions complétées
        current_phase: Phase actuelle du mouvement
        min_elbow_angle: Angle minimum du coude pour valider la descente (degrés)
        max_elbow_angle: Angle maximum du coude pour la position haute (degrés)
    """

    # Seuils configurables (adaptés au dataset réel)
    MIN_ELBOW_ANGLE = 100  # En dessous = position basse (mesuré: 65-105°)
    MAX_ELBOW_ANGLE = 160  # Au-dessus = position haute (mesuré: 160-171°)
    MIN_TIME_BETWEEN_REPS = 0.3  # Secondes (anti-rebond, réduit pour vidéos courtes)

    def __init__(self):
        """Initialise le compteur de pompes."""
        self.count = 0
        self.current_phase = None  # Sera détecté automatiquement
        self.last_rep_time = 0
        self.rep_history: List[PushUpMetrics] = []

    def reset(self):
        """Réinitialise le compteur."""
        self.count = 0
        self.current_phase = PushUpPhase.UP
        self.last_rep_time = 0
        self.rep_history.clear()

    def update(self, keypoints: List[Keypoint]) -> Dict:
        """
        Met à jour le compteur avec les nouveaux keypoints.

        Args:
            keypoints: Liste des 33 keypoints détectés

        Returns:
            Dict contenant count, phase, metrics, feedback
        """
        # Extraire les keypoints nécessaires
        left_shoulder = keypoints[11]
        right_shoulder = keypoints[12]
        left_elbow = keypoints[13]
        right_elbow = keypoints[14]
        left_wrist = keypoints[15]
        right_wrist = keypoints[16]
        left_hip = keypoints[23]
        right_hip = keypoints[24]

        # Vérifier la visibilité
        required_points = [
            left_shoulder,
            right_shoulder,
            left_elbow,
            right_elbow,
            left_wrist,
            right_wrist,
            left_hip,
            right_hip,
        ]

        # Vérifier la visibilité (au moins un côté complet visible)
        left_side_visible = all(
            is_keypoint_visible(kp, min_visibility=0.5) 
            for kp in [left_shoulder, left_elbow, left_wrist, left_hip]
        )
        right_side_visible = all(
            is_keypoint_visible(kp, min_visibility=0.5) 
            for kp in [right_shoulder, right_elbow, right_wrist, right_hip]
        )

        if not (left_side_visible or right_side_visible):
            return {
                "count": self.count,
                "phase": self.current_phase.value
                if self.current_phase
                else "initialisation",
                "metrics": None,
                "feedback": "⚠️ Position toi de profil ou de face",
            }

        # Calculer les angles des coudes selon la visibilité
        if left_side_visible and right_side_visible:
            # Vue de face ou dos : moyenne des deux
            left_elbow_angle = calculate_elbow_angle(left_shoulder, left_elbow, left_wrist)
            right_elbow_angle = calculate_elbow_angle(right_shoulder, right_elbow, right_wrist)
            avg_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2
        elif left_side_visible:
            # Vue profil gauche
            avg_elbow_angle = calculate_elbow_angle(left_shoulder, left_elbow, left_wrist)
        else:
            # Vue profil droit
            avg_elbow_angle = calculate_elbow_angle(right_shoulder, right_elbow, right_wrist)

        # Calculer la hauteur du corps (épaule par rapport à la hanche)
        body_height = calculate_vertical_distance(left_shoulder, left_hip)

        # Créer les métriques
        metrics = self._analyze_pushup(avg_elbow_angle, body_height)

        # Machine à états pour détecter les répétitions
        previous_phase = self.current_phase
        self._update_phase(avg_elbow_angle)

        # Détecter une répétition complète
        if (
            previous_phase == PushUpPhase.ASCENDING
            and self.current_phase == PushUpPhase.UP
        ):
            current_time = time.time()
            if current_time - self.last_rep_time >= self.MIN_TIME_BETWEEN_REPS:
                self.count += 1
                self.last_rep_time = current_time
                self.rep_history.append(metrics)

        # Générer le feedback
        feedback = self._generate_feedback(metrics, self.current_phase)

        return {
            "count": self.count,
            "phase": self.current_phase.value
            if self.current_phase
            else "initialisation",
            "metrics": {
                "elbow_angle": round(metrics.elbow_angle, 1),
                "body_height": round(metrics.body_height, 3),
            },
            "feedback": feedback,
        }

    def _update_phase(self, elbow_angle: float):
        """
        Met à jour la phase actuelle de la pompe.

        Args:
            elbow_angle: Angle du coude
        """
        # Initialisation automatique si première frame
        if self.current_phase is None:
            if elbow_angle >= self.MAX_ELBOW_ANGLE - 10:
                self.current_phase = PushUpPhase.UP
            elif elbow_angle <= self.MIN_ELBOW_ANGLE + 10:
                self.current_phase = PushUpPhase.DOWN
            else:
                self.current_phase = PushUpPhase.DESCENDING
            # Ne pas retourner, continuer le traitement normal

        # Transitions plus permissives
        if self.current_phase == PushUpPhase.UP:
            # Commencer la descente dès qu'on quitte la position haute
            if elbow_angle < self.MAX_ELBOW_ANGLE - 10:
                self.current_phase = PushUpPhase.DESCENDING

        elif self.current_phase == PushUpPhase.DESCENDING:
            # Atteindre la position basse
            if elbow_angle <= self.MIN_ELBOW_ANGLE:
                self.current_phase = PushUpPhase.DOWN

        elif self.current_phase == PushUpPhase.DOWN:
            # Commencer la remontée dès qu'on quitte la position basse
            if elbow_angle > self.MIN_ELBOW_ANGLE + 5:
                self.current_phase = PushUpPhase.ASCENDING

        elif self.current_phase == PushUpPhase.ASCENDING:
            # Revenir en position haute
            if elbow_angle >= self.MAX_ELBOW_ANGLE - 10:
                self.current_phase = PushUpPhase.UP

    def _analyze_pushup(self, elbow_angle: float, body_height: float) -> PushUpMetrics:
        """
        Analyse la qualité de la pompe.

        Args:
            elbow_angle: Angle du coude
            body_height: Hauteur du corps

        Returns:
            PushUpMetrics avec les analyses
        """
        # Valider si la pompe est assez profonde
        is_valid = elbow_angle <= self.MIN_ELBOW_ANGLE

        feedback = ""
        if elbow_angle > self.MIN_ELBOW_ANGLE + 20:
            feedback = "Descends plus bas"
        elif is_valid:
            feedback = "Bonne profondeur !"

        return PushUpMetrics(
            elbow_angle=elbow_angle,
            body_height=body_height,
            is_valid=is_valid,
            feedback=feedback,
        )

    def _generate_feedback(self, metrics: PushUpMetrics, phase: PushUpPhase) -> str:
        """
        Génère un feedback textuel basé sur les métriques.

        Args:
            metrics: Métriques de la pompe
            phase: Phase actuelle

        Returns:
            str: Message de feedback
        """
        if phase == PushUpPhase.UP:
            return "✅ Prêt pour la prochaine pompe"

        elif phase == PushUpPhase.DESCENDING:
            if metrics.elbow_angle > self.MIN_ELBOW_ANGLE + 20:
                return "⬇️ Continue de descendre"
            else:
                return "⬇️ Bonne descente"

        elif phase == PushUpPhase.DOWN:
            if metrics.is_valid:
                return "✅ Parfait ! Remonte maintenant"
            elif metrics.elbow_angle > self.MIN_ELBOW_ANGLE:
                return "⚠️ Descends encore un peu"
            else:
                return "⬆️ Remonte maintenant"

        elif phase == PushUpPhase.ASCENDING:
            return "⬆️ Bonne poussée !"

        return ""

    def get_stats(self) -> Dict:
        """
        Retourne les statistiques de la session.

        Returns:
            Dict avec count, valid_reps, success_rate
        """
        valid_reps = sum(1 for rep in self.rep_history if rep.is_valid)
        return {
            "total_reps": self.count,
            "valid_reps": valid_reps,
            "success_rate": round(valid_reps / self.count * 100, 1)
            if self.count > 0
            else 0,
        }
