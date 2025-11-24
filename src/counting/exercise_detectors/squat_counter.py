"""
Module de détection et de comptage des squats.
Utilise les angles du genou et de la hanche pour détecter les répétitions.
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum
import time
from src.detection.pose_detector import Keypoint
from src.counting.angle_calculator import (
    calculate_knee_angle,
    calculate_hip_angle,
    is_keypoint_visible,
)


class SquatPhase(Enum):
    """États possibles d'un squat."""

    STANDING = "debout"
    DESCENDING = "descente"
    BOTTOM = "position_basse"
    ASCENDING = "montée"


@dataclass
class SquatMetrics:
    """Métriques d'analyse d'un squat."""

    knee_angle: float
    hip_angle: float
    depth_score: float  # Score de profondeur [0-1]
    is_valid: bool
    feedback: str


class SquatCounter:
    """
    Compteur de répétitions pour les squats.

    Détecte les cycles complets (descente -> position basse -> montée)
    basés sur les angles du genou et de la hanche.

    Attributes:
        count: Nombre de répétitions complétées
        current_phase: Phase actuelle du mouvement
        min_knee_angle: Angle minimum du genou pour valider la descente (degrés)
        max_knee_angle: Angle maximum du genou pour la position haute (degrés)
        min_hip_angle: Angle minimum de la hanche pour valider la descente (degrés)
    """

    # Seuils configurables (ajustés pour le dataset)
    MIN_KNEE_ANGLE = 165  # En dessous = position basse (mesuré: min ~162°)
    MAX_KNEE_ANGLE = 175  # Au-dessus = position haute (mesuré: max ~179°)
    MIN_HIP_ANGLE = 160  # En dessous = bonne profondeur (mesuré: min ~157°)
    MIN_TIME_BETWEEN_REPS = 0.5  # Secondes (anti-rebond)

    def __init__(self):
        """Initialise le compteur de squats."""
        self.count = 0
        self.current_phase = SquatPhase.STANDING
        self.last_rep_time = 0
        self.rep_history: List[SquatMetrics] = []

    def reset(self):
        """Réinitialise le compteur."""
        self.count = 0
        self.current_phase = SquatPhase.STANDING
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
        left_hip = keypoints[23]
        right_hip = keypoints[24]
        left_knee = keypoints[25]
        right_knee = keypoints[26]
        left_ankle = keypoints[27]
        right_ankle = keypoints[28]
        left_shoulder = keypoints[11]
        right_shoulder = keypoints[12]

        # Vérifier la visibilité
        required_points = [
            left_hip,
            right_hip,
            left_knee,
            right_knee,
            left_ankle,
            right_ankle,
            left_shoulder,
            right_shoulder,
        ]

        # Vérifier la visibilité (au moins un côté complet visible)
        left_side_visible = all(
            is_keypoint_visible(kp, min_visibility=0.5) 
            for kp in [left_hip, left_knee, left_ankle, left_shoulder]
        )
        right_side_visible = all(
            is_keypoint_visible(kp, min_visibility=0.5) 
            for kp in [right_hip, right_knee, right_ankle, right_shoulder]
        )

        if not (left_side_visible or right_side_visible):
            # Diagnostic plus précis pour guider l'utilisateur
            feedback_msg = "⚠️ Position toi de façon à être entièrement visible"
            
            # Vérifier si on voit au moins les hanches (centre du corps)
            hips_visible = is_keypoint_visible(left_hip) or is_keypoint_visible(right_hip)
            
            if hips_visible:
                # Si on voit les hanches mais pas le reste, c'est probablement un problème de cadrage (trop près)
                ankles_visible = is_keypoint_visible(left_ankle) or is_keypoint_visible(right_ankle)
                shoulders_visible = is_keypoint_visible(left_shoulder) or is_keypoint_visible(right_shoulder)
                
                if not ankles_visible:
                    feedback_msg = "⚠️ Reculez pour qu'on voie vos pieds"
                elif not shoulders_visible:
                    feedback_msg = "⚠️ Reculez pour qu'on voie votre tête"
            
            return {
                "count": self.count,
                "phase": self.current_phase.value,
                "metrics": None,
                "feedback": feedback_msg,
            }

        # Vérifier l'orientation du corps (Doit être vertical pour un squat)
        # On utilise la moyenne des épaules et hanches visibles
        # Note: Y augmente vers le bas (0=haut, 1=bas)
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_y = (left_hip.y + right_hip.y) / 2
        
        # Pour un squat, les épaules doivent être au-dessus des hanches
        # On utilise un seuil très permissif pour juste éviter la position allongée
        is_vertical = (hip_y - shoulder_y) > 0.05
        
        if not is_vertical:
             return {
                "count": self.count,
                "phase": self.current_phase.value,
                "metrics": None,
                "feedback": "⚠️ Mets-toi debout pour les squats",
            }

        # Calculer les angles selon la visibilité
        if left_side_visible and right_side_visible:
            # Vue de face ou dos : moyenne des deux
            left_knee_angle = calculate_knee_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = calculate_knee_angle(right_hip, right_knee, right_ankle)
            avg_knee_angle = (left_knee_angle + right_knee_angle) / 2

            left_hip_angle = calculate_hip_angle(left_shoulder, left_hip, left_knee)
            right_hip_angle = calculate_hip_angle(right_shoulder, right_hip, right_knee)
            avg_hip_angle = (left_hip_angle + right_hip_angle) / 2
        elif left_side_visible:
            # Vue profil gauche
            avg_knee_angle = calculate_knee_angle(left_hip, left_knee, left_ankle)
            avg_hip_angle = calculate_hip_angle(left_shoulder, left_hip, left_knee)
        else:
            # Vue profil droit
            avg_knee_angle = calculate_knee_angle(right_hip, right_knee, right_ankle)
            avg_hip_angle = calculate_hip_angle(right_shoulder, right_hip, right_knee)

        # Créer les métriques
        metrics = self._analyze_squat(avg_knee_angle, avg_hip_angle)

        # Machine à états pour détecter les répétitions
        previous_phase = self.current_phase
        self._update_phase(avg_knee_angle, avg_hip_angle)

        # Détecter une répétition complète
        if (
            previous_phase == SquatPhase.ASCENDING
            and self.current_phase == SquatPhase.STANDING
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
            "phase": self.current_phase.value,
            "metrics": {
                "knee_angle": round(metrics.knee_angle, 1),
                "hip_angle": round(metrics.hip_angle, 1),
                "depth_score": round(metrics.depth_score, 2),
            },
            "feedback": feedback,
        }

    def _update_phase(self, knee_angle: float, hip_angle: float):
        """
        Met à jour la phase actuelle du squat.

        Args:
            knee_angle: Angle du genou
            hip_angle: Angle de la hanche
        """
        # Transitions plus permissives
        if self.current_phase == SquatPhase.STANDING:
            # Commencer la descente dès qu'on quitte la position haute
            if knee_angle < self.MAX_KNEE_ANGLE - 10:
                self.current_phase = SquatPhase.DESCENDING

        elif self.current_phase == SquatPhase.DESCENDING:
            # Atteindre la position basse
            if knee_angle <= self.MIN_KNEE_ANGLE:
                self.current_phase = SquatPhase.BOTTOM

        elif self.current_phase == SquatPhase.BOTTOM:
            # Commencer la remontée dès qu'on quitte la position basse
            if knee_angle > self.MIN_KNEE_ANGLE + 5:
                self.current_phase = SquatPhase.ASCENDING

        elif self.current_phase == SquatPhase.ASCENDING:
            # Revenir debout
            if knee_angle >= self.MAX_KNEE_ANGLE - 10:
                self.current_phase = SquatPhase.STANDING

    def _analyze_squat(self, knee_angle: float, hip_angle: float) -> SquatMetrics:
        """
        Analyse la qualité du squat.

        Args:
            knee_angle: Angle du genou
            hip_angle: Angle de la hanche

        Returns:
            SquatMetrics avec les analyses
        """
        # Calculer le score de profondeur (0 = debout, 1 = très bas)
        depth_score = max(
            0,
            min(
                1,
                (self.MAX_KNEE_ANGLE - knee_angle)
                / (self.MAX_KNEE_ANGLE - self.MIN_KNEE_ANGLE),
            ),
        )

        # Valider si le squat est assez profond
        is_valid = (
            knee_angle <= self.MIN_KNEE_ANGLE and hip_angle <= self.MIN_HIP_ANGLE + 20
        )

        feedback = ""
        if knee_angle > self.MIN_KNEE_ANGLE + 20:
            feedback = "Descends plus bas"
        elif hip_angle > self.MIN_HIP_ANGLE + 30:
            feedback = "Penche-toi plus en avant"
        elif is_valid:
            feedback = "Bonne profondeur !"

        return SquatMetrics(
            knee_angle=knee_angle,
            hip_angle=hip_angle,
            depth_score=depth_score,
            is_valid=is_valid,
            feedback=feedback,
        )

    def _generate_feedback(self, metrics: SquatMetrics, phase: SquatPhase) -> str:
        """
        Génère un feedback textuel basé sur les métriques.

        Args:
            metrics: Métriques du squat
            phase: Phase actuelle

        Returns:
            str: Message de feedback
        """
        if phase == SquatPhase.STANDING:
            return "✅ Prêt pour le prochain squat"

        elif phase == SquatPhase.DESCENDING:
            if metrics.knee_angle > self.MIN_KNEE_ANGLE + 20:
                return "⬇️ Continue de descendre"
            else:
                return "⬇️ Bonne descente"

        elif phase == SquatPhase.BOTTOM:
            if metrics.is_valid:
                return "✅ Parfait ! Remonte maintenant"
            elif metrics.knee_angle > self.MIN_KNEE_ANGLE:
                return "⚠️ Descends encore un peu"
            else:
                return "⬆️ Remonte maintenant"

        elif phase == SquatPhase.ASCENDING:
            return "⬆️ Bonne remontée !"

        return ""

    def get_average_depth(self) -> float:
        """
        Calcule le score de profondeur moyen des répétitions.

        Returns:
            float: Score moyen [0-1]
        """
        if not self.rep_history:
            return 0.0
        return sum(rep.depth_score for rep in self.rep_history) / len(self.rep_history)

    def get_stats(self) -> Dict:
        """
        Retourne les statistiques de la session.

        Returns:
            Dict avec count, average_depth, valid_reps
        """
        valid_reps = sum(1 for rep in self.rep_history if rep.is_valid)
        return {
            "total_reps": self.count,
            "valid_reps": valid_reps,
            "average_depth": round(self.get_average_depth(), 2),
            "success_rate": round(valid_reps / self.count * 100, 1)
            if self.count > 0
            else 0,
        }
