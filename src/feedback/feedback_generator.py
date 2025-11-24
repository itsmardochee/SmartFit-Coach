"""
Module de génération de feedback.

Génère des messages de feedback clairs et actionnables
pour guider l'utilisateur pendant l'entraînement.
"""

import time
from typing import Dict, List, Optional, Tuple
from collections import deque


class FeedbackGenerator:
    """
    Générateur de feedback pour l'entraînement.

    Génère des messages clairs avec gestion de fréquence
    et priorité pour éviter de submerger l'utilisateur.
    """

    # Délai minimum entre deux messages (secondes)
    MIN_MESSAGE_INTERVAL = 3.0

    # Priorités des messages
    SEVERITY_PRIORITY = {"high": 3, "medium": 2, "low": 1}

    # Messages de réussite
    SUCCESS_MESSAGES = [
        "✅ Parfait !",
        "✅ Excellent mouvement !",
        "✅ Très bien !",
        "✅ Continue comme ça !",
        "✅ Super forme !",
        "✅ Impeccable !",
    ]

    def __init__(self):
        """Initialise le générateur de feedback."""
        self.last_message_time = 0
        self.current_message = None
        self.message_history = deque(maxlen=50)
        self.success_message_index = 0

    def generate_feedback(
        self, quality_score: float, errors: List[Dict], exercise: str, rep_count: int
    ) -> Optional[Dict]:
        """
        Génère un message de feedback basé sur l'analyse de posture.

        Args:
            quality_score: Score de qualité (0-100)
            errors: Liste des erreurs détectées
            exercise: Nom de l'exercice
            rep_count: Nombre de répétitions

        Returns:
            Dictionnaire avec le message de feedback ou None
        """
        current_time = time.time()

        # Vérifier l'intervalle minimum
        if current_time - self.last_message_time < self.MIN_MESSAGE_INTERVAL:
            return self.current_message

        # Si excellente qualité et pas d'erreurs
        if quality_score >= 85 and not errors:
            message = self._generate_success_message(rep_count)
            feedback = {
                "message": message,
                "color": "green",
                "icon": "✅",
                "priority": "low",
                "quality_score": quality_score,
            }

        # Si erreurs détectées
        elif errors:
            # Prendre l'erreur la plus prioritaire
            priority_error = self._get_highest_priority_error(errors)

            feedback = {
                "message": priority_error["message"],
                "color": self._severity_to_color(priority_error["severity"]),
                "icon": priority_error["icon"],
                "priority": priority_error["severity"],
                "quality_score": quality_score,
                "error_type": priority_error["type"],
            }

        # Qualité moyenne
        elif quality_score >= 50:
            feedback = {
                "message": "💡 Maintiens cette qualité",
                "color": "orange",
                "icon": "💡",
                "priority": "low",
                "quality_score": quality_score,
            }

        # Mauvaise qualité
        else:
            feedback = {
                "message": "🔴 Vérifie ta posture",
                "color": "red",
                "icon": "🔴",
                "priority": "high",
                "quality_score": quality_score,
            }

        # Mettre à jour le message actuel et l'historique
        self.current_message = feedback
        self.last_message_time = current_time
        self.message_history.append(feedback)

        return feedback

    def _generate_success_message(self, rep_count: int) -> str:
        """
        Génère un message de succès varié.

        Args:
            rep_count: Nombre de répétitions

        Returns:
            Message de succès
        """
        # Alterner les messages de succès
        message = self.SUCCESS_MESSAGES[self.success_message_index]
        self.success_message_index = (self.success_message_index + 1) % len(
            self.SUCCESS_MESSAGES
        )

        # Ajouter des encouragements selon le nombre de reps
        if rep_count > 0 and rep_count % 10 == 0:
            message += f" {rep_count} répétitions !"

        return message

    def _get_highest_priority_error(self, errors: List[Dict]) -> Dict:
        """
        Trouve l'erreur la plus prioritaire.

        Args:
            errors: Liste des erreurs

        Returns:
            L'erreur avec la priorité la plus haute
        """
        if not errors:
            return {
                "message": "Position non détectée",
                "severity": "low",
                "icon": "⚪",
                "type": "unknown",
            }

        # Trier par priorité
        sorted_errors = sorted(
            errors,
            key=lambda e: self.SEVERITY_PRIORITY.get(e.get("severity", "low"), 1),
            reverse=True,
        )

        return sorted_errors[0]

    def _severity_to_color(self, severity: str) -> str:
        """
        Convertit une sévérité en couleur.

        Args:
            severity: Niveau de sévérité

        Returns:
            Nom de la couleur
        """
        color_map = {"high": "red", "medium": "orange", "low": "yellow"}
        return color_map.get(severity, "gray")

    def get_workout_summary(self) -> Dict:
        """
        Génère un résumé de la session d'entraînement.

        Returns:
            Dictionnaire avec statistiques de la session
        """
        if not self.message_history:
            return {
                "total_feedback": 0,
                "avg_quality": 0,
                "success_rate": 0,
                "common_errors": [],
            }

        # Calculer statistiques
        total = len(self.message_history)
        quality_scores = [msg["quality_score"] for msg in self.message_history]
        avg_quality = sum(quality_scores) / len(quality_scores)

        # Compter succès
        success_count = sum(
            1 for msg in self.message_history if msg["quality_score"] >= 85
        )
        success_rate = (success_count / total) * 100

        # Identifier erreurs communes
        error_counts = {}
        for msg in self.message_history:
            if "error_type" in msg:
                error_type = msg["error_type"]
                error_counts[error_type] = error_counts.get(error_type, 0) + 1

        # Trier les erreurs par fréquence
        common_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[
            :3
        ]  # Top 3

        return {
            "total_feedback": total,
            "avg_quality": avg_quality,
            "success_rate": success_rate,
            "common_errors": common_errors,
            "quality_distribution": {
                "excellent": sum(1 for q in quality_scores if q >= 85),
                "good": sum(1 for q in quality_scores if 70 <= q < 85),
                "medium": sum(1 for q in quality_scores if 50 <= q < 70),
                "poor": sum(1 for q in quality_scores if q < 50),
            },
        }

    def reset(self) -> None:
        """Réinitialise le générateur."""
        self.last_message_time = 0
        self.current_message = None
        self.message_history.clear()
        self.success_message_index = 0

    def force_message(
        self, message: str, color: str = "blue", icon: str = "💬"
    ) -> Dict:
        """
        Force l'affichage d'un message custom.

        Args:
            message: Texte du message
            color: Couleur du message
            icon: Icône du message

        Returns:
            Dictionnaire avec le message
        """
        feedback = {
            "message": message,
            "color": color,
            "icon": icon,
            "priority": "medium",
            "quality_score": 50,
        }

        self.current_message = feedback
        self.last_message_time = time.time()

        return feedback

    def get_encouragement(self, rep_count: int) -> Optional[str]:
        """
        Génère un message d'encouragement selon la progression.

        Args:
            rep_count: Nombre de répétitions

        Returns:
            Message d'encouragement ou None
        """
        milestones = {
            5: "🎯 5 reps ! Tu démarres fort !",
            10: "🔥 10 reps ! Continue !",
            15: "💪 15 reps ! Tu gères !",
            20: "⭐ 20 reps ! Incroyable !",
            25: "🏆 25 reps ! Champion !",
            30: "👑 30 reps ! Respect !",
            50: "🚀 50 reps ! C'est énorme !",
        }

        return milestones.get(rep_count)

    def get_message_stats(self) -> Dict:
        """
        Retourne des statistiques sur les messages générés.

        Returns:
            Dictionnaire avec statistiques
        """
        if not self.message_history:
            return {"total": 0}

        return {
            "total": len(self.message_history),
            "by_priority": {
                "high": sum(1 for m in self.message_history if m["priority"] == "high"),
                "medium": sum(
                    1 for m in self.message_history if m["priority"] == "medium"
                ),
                "low": sum(1 for m in self.message_history if m["priority"] == "low"),
            },
            "by_color": {
                "green": sum(1 for m in self.message_history if m["color"] == "green"),
                "orange": sum(
                    1 for m in self.message_history if m["color"] == "orange"
                ),
                "red": sum(1 for m in self.message_history if m["color"] == "red"),
            },
        }


# Test du module
if __name__ == "__main__":
    print("🧪 Test du générateur de feedback")
    print("-" * 50)

    generator = FeedbackGenerator()

    # Test 1: Excellente qualité
    print("\n📊 Test 1: Excellente qualité")
    feedback = generator.generate_feedback(
        quality_score=95, errors=[], exercise="squat", rep_count=5
    )
    print(f"  {feedback['icon']} {feedback['message']}")
    print(f"  Couleur: {feedback['color']}, Priorité: {feedback['priority']}")

    # Test 2: Erreurs détectées
    print("\n📊 Test 2: Erreurs détectées")
    time.sleep(3.1)  # Attendre l'intervalle minimum
    feedback = generator.generate_feedback(
        quality_score=60,
        errors=[
            {
                "type": "depth",
                "message": "Descends plus bas",
                "severity": "medium",
                "icon": "⚠️",
            }
        ],
        exercise="squat",
        rep_count=6,
    )
    print(f"  {feedback['icon']} {feedback['message']}")
    print(f"  Couleur: {feedback['color']}, Priorité: {feedback['priority']}")

    # Test 3: Résumé
    print("\n📊 Résumé de session:")
    summary = generator.get_workout_summary()
    print(f"  Feedback total: {summary['total_feedback']}")
    print(f"  Qualité moyenne: {summary['avg_quality']:.1f}/100")
    print(f"  Taux de succès: {summary['success_rate']:.1f}%")

    print("\n✅ Test terminé!")
