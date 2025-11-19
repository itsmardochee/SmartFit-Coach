"""
Module de gestion de session d'entraînement.

Gère les sessions d'entraînement avec statistiques,
historique et export des données.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class WorkoutSession:
    """
    Gestionnaire de session d'entraînement.

    Enregistre les répétitions, la qualité, le feedback
    et génère des statistiques de performance.
    """

    def __init__(self, exercise: str, user_name: str = "User"):
        """
        Initialise une nouvelle session.

        Args:
            exercise: Nom de l'exercice
            user_name: Nom de l'utilisateur
        """
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.exercise = exercise
        self.user_name = user_name
        self.start_time = time.time()
        self.end_time = None

        # Statistiques
        self.rep_count = 0
        self.quality_scores = []
        self.feedback_history = []
        self.errors_detected = {}

        # Données détaillées
        self.rep_details = []  # Détails de chaque répétition

        # État
        self.is_active = True
        self.is_paused = False
        self.pause_time = 0
        self.total_pause_duration = 0

    def add_repetition(self, quality_score: float, angles: Dict = None) -> None:
        """
        Enregistre une répétition complétée.

        Args:
            quality_score: Score de qualité (0-100)
            angles: Dictionnaire des angles mesurés (optionnel)
        """
        self.rep_count += 1
        self.quality_scores.append(quality_score)

        rep_detail = {
            "rep_number": self.rep_count,
            "timestamp": time.time() - self.start_time,
            "quality_score": quality_score,
            "angles": angles or {},
        }
        self.rep_details.append(rep_detail)

    def add_feedback(self, feedback: Dict) -> None:
        """
        Enregistre un feedback donné à l'utilisateur.

        Args:
            feedback: Dictionnaire de feedback
        """
        feedback_entry = {
            "timestamp": time.time() - self.start_time,
            "message": feedback.get("message", ""),
            "priority": feedback.get("priority", "low"),
            "quality_score": feedback.get("quality_score", 0),
            "error_type": feedback.get("error_type"),
        }
        self.feedback_history.append(feedback_entry)

        # Compter les erreurs
        if "error_type" in feedback and feedback["error_type"]:
            error_type = feedback["error_type"]
            self.errors_detected[error_type] = (
                self.errors_detected.get(error_type, 0) + 1
            )

    def pause(self) -> None:
        """Met la session en pause."""
        if self.is_active and not self.is_paused:
            self.is_paused = True
            self.pause_time = time.time()

    def resume(self) -> None:
        """Reprend la session après une pause."""
        if self.is_paused:
            self.is_paused = False
            self.total_pause_duration += time.time() - self.pause_time
            self.pause_time = 0

    def end_session(self) -> Dict:
        """
        Termine la session et retourne les statistiques finales.

        Returns:
            Dictionnaire avec toutes les statistiques
        """
        self.end_time = time.time()
        self.is_active = False

        return self.get_statistics()

    def get_duration(self) -> float:
        """
        Calcule la durée de la session (sans les pauses).

        Returns:
            Durée en secondes
        """
        end = self.end_time if self.end_time else time.time()
        total_duration = end - self.start_time
        active_duration = total_duration - self.total_pause_duration

        if self.is_paused:
            active_duration -= time.time() - self.pause_time

        return max(0, active_duration)

    def get_average_quality(self) -> float:
        """
        Calcule le score de qualité moyen.

        Returns:
            Score moyen (0-100)
        """
        if not self.quality_scores:
            return 0.0
        return sum(self.quality_scores) / len(self.quality_scores)

    def get_calories_estimate(self) -> float:
        """
        Estime les calories brûlées (approximation simple).

        Returns:
            Calories estimées
        """
        # Calories approximatives par exercice (par répétition)
        calories_per_rep = {
            "squat": 0.32,
            "push-up": 0.29,
            "pompe": 0.29,
            "lunge": 0.35,
            "fente": 0.35,
        }

        exercise_lower = self.exercise.lower()
        base_calories = 0

        for exercise_type, cal_per_rep in calories_per_rep.items():
            if exercise_type in exercise_lower:
                base_calories = cal_per_rep
                break

        if base_calories == 0:
            base_calories = 0.3  # Valeur par défaut

        # Calories = reps * calories_par_rep
        # Ajuster selon la durée (si exercice long = plus de calories)
        duration_minutes = self.get_duration() / 60
        duration_factor = 1 + (duration_minutes * 0.1)  # +10% par minute

        calories = self.rep_count * base_calories * min(duration_factor, 2.0)

        return round(calories, 1)

    def get_statistics(self) -> Dict:
        """
        Génère toutes les statistiques de la session.

        Returns:
            Dictionnaire complet des statistiques
        """
        duration = self.get_duration()
        avg_quality = self.get_average_quality()

        # Distribution des scores de qualité
        quality_distribution = {
            "excellent": sum(1 for q in self.quality_scores if q >= 85),
            "good": sum(1 for q in self.quality_scores if 70 <= q < 85),
            "medium": sum(1 for q in self.quality_scores if 50 <= q < 70),
            "poor": sum(1 for q in self.quality_scores if q < 50),
        }

        # Top 3 erreurs
        top_errors = sorted(
            self.errors_detected.items(), key=lambda x: x[1], reverse=True
        )[:3]

        # Rythme (reps par minute)
        reps_per_minute = (self.rep_count / duration * 60) if duration > 0 else 0

        return {
            "session_id": self.session_id,
            "user_name": self.user_name,
            "exercise": self.exercise,
            "date": datetime.fromtimestamp(self.start_time).isoformat(),
            "duration": duration,
            "duration_formatted": self._format_duration(duration),
            "repetitions": self.rep_count,
            "average_quality": avg_quality,
            "quality_distribution": quality_distribution,
            "top_errors": top_errors,
            "total_feedback": len(self.feedback_history),
            "calories_estimate": self.get_calories_estimate(),
            "reps_per_minute": round(reps_per_minute, 1),
            "is_active": self.is_active,
            "rep_details": self.rep_details,
        }

    def _format_duration(self, seconds: float) -> str:
        """
        Formate une durée en chaîne lisible.

        Args:
            seconds: Durée en secondes

        Returns:
            Chaîne formatée (ex: "2m 30s")
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)

        if minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    def save_to_file(self, output_dir: str = None) -> str:
        """
        Sauvegarde la session dans un fichier JSON.

        Args:
            output_dir: Répertoire de sortie (optionnel)

        Returns:
            Chemin du fichier sauvegardé
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "sessions"
        else:
            output_dir = Path(output_dir)

        # Créer le répertoire s'il n'existe pas
        output_dir.mkdir(parents=True, exist_ok=True)

        # Nom du fichier
        filename = f"session_{self.session_id}_{self.exercise.replace(' ', '_')}.json"
        filepath = output_dir / filename

        # Sauvegarder
        data = self.get_statistics()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def export_to_csv(self, output_path: str) -> None:
        """
        Export les détails des répétitions en CSV.

        Args:
            output_path: Chemin du fichier CSV
        """
        import csv

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # En-tête
            writer.writerow(["Rep Number", "Timestamp", "Quality Score", "Angles"])

            # Données
            for rep in self.rep_details:
                writer.writerow(
                    [
                        rep["rep_number"],
                        f"{rep['timestamp']:.2f}",
                        f"{rep['quality_score']:.1f}",
                        str(rep["angles"]),
                    ]
                )

    def get_summary_text(self) -> str:
        """
        Génère un résumé textuel de la session.

        Returns:
            Résumé en texte formaté
        """
        stats = self.get_statistics()

        summary = f"""
🏋️ SESSION D'ENTRAÎNEMENT - {stats["exercise"].upper()}
{"=" * 50}

📊 Statistiques Générales:
  • Répétitions: {stats["repetitions"]}
  • Durée: {stats["duration_formatted"]}
  • Rythme: {stats["reps_per_minute"]} reps/min
  • Calories estimées: {stats["calories_estimate"]} kcal

⭐ Qualité d'Exécution:
  • Score moyen: {stats["average_quality"]:.1f}/100
  • Excellent: {stats["quality_distribution"]["excellent"]} reps
  • Bon: {stats["quality_distribution"]["good"]} reps
  • Moyen: {stats["quality_distribution"]["medium"]} reps
  • À améliorer: {stats["quality_distribution"]["poor"]} reps

💬 Feedback:
  • Messages donnés: {stats["total_feedback"]}
"""

        if stats["top_errors"]:
            summary += "\n⚠️ Erreurs Fréquentes:\n"
            for error_type, count in stats["top_errors"]:
                summary += f"  • {error_type}: {count} fois\n"

        summary += "\n" + "=" * 50

        return summary

    def __repr__(self) -> str:
        """Représentation de la session."""
        return (
            f"WorkoutSession(exercise='{self.exercise}', "
            f"reps={self.rep_count}, "
            f"duration={self._format_duration(self.get_duration())}, "
            f"quality={self.get_average_quality():.1f})"
        )


# Test du module
if __name__ == "__main__":
    print("🧪 Test de la gestion de session")
    print("-" * 50)

    # Créer une session
    session = WorkoutSession("squat", "TestUser")
    print(f"\n✅ Session créée: {session}")

    # Simuler quelques répétitions
    print("\n📊 Simulation de répétitions:")
    for i in range(5):
        quality = 85 - (i * 5)  # Qualité décroissante
        session.add_repetition(quality, {"knee": 90 + i * 5})
        print(f"  Rep {i + 1}: qualité {quality}")
        time.sleep(0.1)

    # Ajouter du feedback
    session.add_feedback(
        {
            "message": "Descends plus bas",
            "priority": "medium",
            "quality_score": 70,
            "error_type": "depth",
        }
    )

    # Terminer la session
    print("\n📈 Statistiques finales:")
    stats = session.end_session()
    print(f"  Reps: {stats['repetitions']}")
    print(f"  Durée: {stats['duration_formatted']}")
    print(f"  Qualité moyenne: {stats['average_quality']:.1f}/100")
    print(f"  Calories: {stats['calories_estimate']} kcal")

    # Afficher le résumé
    print(session.get_summary_text())

    # Sauvegarder
    filepath = session.save_to_file()
    print(f"\n💾 Session sauvegardée: {filepath}")

    print("\n✅ Test terminé!")
