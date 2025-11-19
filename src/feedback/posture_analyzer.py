"""
Module d'analyse de posture.

Analyse la qualité d'exécution des exercices et détecte
les erreurs communes de posture.
"""

from typing import Dict, List, Tuple
from src.counting.angle_calculator import calculate_angle


class PostureAnalyzer:
    """
    Analyseur de posture pour différents exercices.

    Détecte les erreurs communes et évalue la qualité d'exécution.
    """

    # Seuils de qualité pour chaque exercice
    QUALITY_THRESHOLDS = {
        "squat": {
            "knee_angle_min": 80,  # Angle minimum genou pour descente complète
            "knee_angle_max": 170,  # Angle maximum genou en position haute
            "back_angle_tolerance": 20,  # Tolérance pour l'alignement du dos
            "hip_knee_alignment": 15,  # Tolérance alignement hanche-genou
        },
        "push-up": {
            "elbow_angle_min": 70,  # Angle minimum coude en position basse
            "elbow_angle_max": 165,  # Angle maximum coude en position haute
            "body_alignment": 15,  # Tolérance pour l'alignement du corps
            "hip_height_tolerance": 0.1,  # Tolérance position hanches (normalisée)
        },
    }

    def __init__(self):
        """Initialise l'analyseur de posture."""
        self.quality_history = []  # Historique des scores de qualité
        self.error_counts = {}  # Compteur d'erreurs par type

    def analyze_squat(self, keypoints: List[Dict]) -> Dict:
        """
        Analyse la posture d'un squat.

        Args:
            keypoints: Liste des keypoints détectés

        Returns:
            Dictionnaire avec score de qualité et erreurs détectées
        """
        errors = []
        quality_score = 100.0

        try:
            # Calculer les angles importants
            # Calculer les angles importants
            # Les keypoints sont des objets Keypoint, pas des dictionnaires
            left_knee = calculate_angle(
                keypoints[23],  # left_hip
                keypoints[25],  # left_knee
                keypoints[27],  # left_ankle
            )
            right_knee = calculate_angle(
                keypoints[24],  # right_hip
                keypoints[26],  # right_knee
                keypoints[28],  # right_ankle
            )
            knee_angle = (left_knee + right_knee) / 2

            # Vérifier la profondeur du squat
            thresholds = self.QUALITY_THRESHOLDS["squat"]
            if knee_angle > thresholds["knee_angle_min"] + 20:
                errors.append(
                    {
                        "type": "depth",
                        "message": "Descends plus bas",
                        "severity": "medium",
                        "icon": "⚠️",
                    }
                )
                quality_score -= 20

            # Vérifier l'alignement des genoux
            knee_diff = abs(left_knee - right_knee)
            if knee_diff > 15:
                errors.append(
                    {
                        "type": "knee_alignment",
                        "message": "Équilibre tes genoux",
                        "severity": "medium",
                        "icon": "⚠️",
                    }
                )
                quality_score -= 15

            # Vérifier l'alignement du dos
            back_angle = calculate_angle(
                keypoints[11],  # left_shoulder
                keypoints[23],  # left_hip
                keypoints[25],  # left_knee
            )

            # Le dos doit rester relativement droit (angle proche de 180°)
            if back_angle < 150:
                errors.append(
                    {
                        "type": "back_posture",
                        "message": "Garde le dos droit",
                        "severity": "high",
                        "icon": "🔴",
                    }
                )
                quality_score -= 25

            # Vérifier que les genoux ne dépassent pas les orteils
            left_knee_x = keypoints[25].x
            left_ankle_x = keypoints[27].x

            if abs(left_knee_x - left_ankle_x) > 0.1:  # 10% de l'image
                errors.append(
                    {
                        "type": "knee_forward",
                        "message": "Genoux en arrière",
                        "severity": "medium",
                        "icon": "⚠️",
                    }
                )
                quality_score -= 15

        except Exception as e:
            print(f"❌ Erreur analyse squat: {e}")
            errors.append(
                {
                    "type": "detection_error",
                    "message": "Position non détectée",
                    "severity": "low",
                    "icon": "⚪",
                }
            )
            quality_score = 0

        # Mettre à jour l'historique
        self.quality_history.append(quality_score)
        if len(self.quality_history) > 100:
            self.quality_history.pop(0)

        # Compter les erreurs
        for error in errors:
            error_type = error["type"]
            self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        return {
            "quality_score": max(0, quality_score),
            "errors": errors,
            "angles": {"knee": knee_angle if "knee_angle" in locals() else None},
        }

    def analyze_pushup(self, keypoints: List[Dict]) -> Dict:
        """
        Analyse la posture d'une pompe.

        Args:
            keypoints: Liste des keypoints détectés

        Returns:
            Dictionnaire avec score de qualité et erreurs détectées
        """
        errors = []
        quality_score = 100.0

        try:
            # Calculer les angles des coudes
            # Calculer les angles des coudes
            # Les keypoints sont des objets Keypoint
            left_elbow = calculate_angle(
                keypoints[11],  # left_shoulder
                keypoints[13],  # left_elbow
                keypoints[15],  # left_wrist
            )
            right_elbow = calculate_angle(
                keypoints[12],  # right_shoulder
                keypoints[14],  # right_elbow
                keypoints[16],  # right_wrist
            )
            elbow_angle = (left_elbow + right_elbow) / 2

            # Vérifier la profondeur de la descente
            thresholds = self.QUALITY_THRESHOLDS["push-up"]
            if elbow_angle > thresholds["elbow_angle_min"] + 30:
                errors.append(
                    {
                        "type": "depth",
                        "message": "Descends plus bas",
                        "severity": "medium",
                        "icon": "⚠️",
                    }
                )
                quality_score -= 20

            # Vérifier l'alignement du corps (épaules-hanches-chevilles)
            shoulder_y = (keypoints[11].y + keypoints[12].y) / 2
            hip_y = (keypoints[23].y + keypoints[24].y) / 2
            ankle_y = (keypoints[27].y + keypoints[28].y) / 2

            # Les hanches ne doivent pas être trop hautes ou trop basses
            body_alignment = abs(hip_y - (shoulder_y + ankle_y) / 2)

            if body_alignment > thresholds["hip_height_tolerance"]:
                if hip_y < shoulder_y:
                    errors.append(
                        {
                            "type": "hips_low",
                            "message": "Remonte les hanches",
                            "severity": "high",
                            "icon": "🔴",
                        }
                    )
                else:
                    errors.append(
                        {
                            "type": "hips_high",
                            "message": "Baisse les hanches",
                            "severity": "high",
                            "icon": "🔴",
                        }
                    )
                quality_score -= 25

            # Vérifier la symétrie des coudes
            elbow_diff = abs(left_elbow - right_elbow)
            if elbow_diff > 15:
                errors.append(
                    {
                        "type": "elbow_symmetry",
                        "message": "Équilibre tes bras",
                        "severity": "medium",
                        "icon": "⚠️",
                    }
                )
                quality_score -= 15

            # Vérifier la position des mains (largeur des épaules)
            left_hand_x = keypoints[15].x
            right_hand_x = keypoints[16].x
            left_shoulder_x = keypoints[11].x
            right_shoulder_x = keypoints[12].x

            hand_width = abs(right_hand_x - left_hand_x)
            shoulder_width = abs(right_shoulder_x - left_shoulder_x)

            if hand_width < shoulder_width * 0.8 or hand_width > shoulder_width * 1.5:
                errors.append(
                    {
                        "type": "hand_position",
                        "message": "Ajuste la largeur des mains",
                        "severity": "low",
                        "icon": "💡",
                    }
                )
                quality_score -= 10

        except Exception as e:
            print(f"❌ Erreur analyse push-up: {e}")
            errors.append(
                {
                    "type": "detection_error",
                    "message": "Position non détectée",
                    "severity": "low",
                    "icon": "⚪",
                }
            )
            quality_score = 0

        # Mettre à jour l'historique
        self.quality_history.append(quality_score)
        if len(self.quality_history) > 100:
            self.quality_history.pop(0)

        # Compter les erreurs
        for error in errors:
            error_type = error["type"]
            self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        return {
            "quality_score": max(0, quality_score),
            "errors": errors,
            "angles": {"elbow": elbow_angle if "elbow_angle" in locals() else None},
        }

    def analyze(self, exercise: str, keypoints: List[Dict]) -> Dict:
        """
        Analyse la posture pour un exercice donné.

        Args:
            exercise: Nom de l'exercice
            keypoints: Liste des keypoints détectés

        Returns:
            Dictionnaire avec résultats de l'analyse
        """
        exercise_lower = exercise.lower()

        if "squat" in exercise_lower:
            return self.analyze_squat(keypoints)
        elif "push" in exercise_lower or "pompe" in exercise_lower:
            return self.analyze_pushup(keypoints)
        else:
            # Exercice non supporté, retourner analyse neutre
            return {
                "quality_score": 50,
                "errors": [
                    {
                        "type": "unsupported",
                        "message": "Exercice non analysé",
                        "severity": "low",
                        "icon": "💡",
                    }
                ],
                "angles": {},
            }

    def get_average_quality(self, last_n: int = 10) -> float:
        """
        Calcule le score de qualité moyen sur les N dernières frames.

        Args:
            last_n: Nombre de frames à considérer

        Returns:
            Score moyen entre 0 et 100
        """
        if not self.quality_history:
            return 0.0

        recent = self.quality_history[-last_n:]
        return sum(recent) / len(recent)

    def get_error_summary(self) -> Dict[str, int]:
        """
        Retourne un résumé des erreurs détectées.

        Returns:
            Dictionnaire avec compteur d'erreurs par type
        """
        return self.error_counts.copy()

    def reset(self) -> None:
        """Réinitialise l'historique et les compteurs."""
        self.quality_history.clear()
        self.error_counts.clear()

    def get_quality_category(self, score: float) -> Tuple[str, str]:
        """
        Catégorise un score de qualité.

        Args:
            score: Score entre 0 et 100

        Returns:
            Tuple (catégorie, couleur)
        """
        if score >= 85:
            return "Excellent", "green"
        elif score >= 70:
            return "Bon", "lightgreen"
        elif score >= 50:
            return "Moyen", "orange"
        else:
            return "À améliorer", "red"


# Test du module
if __name__ == "__main__":
    print("🧪 Test de l'analyseur de posture")
    print("-" * 50)

    analyzer = PostureAnalyzer()

    # Simuler des keypoints pour un squat
    dummy_keypoints = [{"x": 0.5, "y": 0.5, "visibility": 1.0} for _ in range(33)]

    print("\n📊 Test analyse squat:")
    result = analyzer.analyze("squat", dummy_keypoints)
    print(f"  Score de qualité: {result['quality_score']:.1f}/100")
    print(f"  Nombre d'erreurs: {len(result['errors'])}")

    if result["errors"]:
        print("\n  Erreurs détectées:")
        for error in result["errors"]:
            print(f"    {error['icon']} {error['message']} ({error['severity']})")

    print("\n✅ Test terminé!")
