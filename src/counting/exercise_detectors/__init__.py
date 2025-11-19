"""Package des détecteurs d'exercices spécifiques."""

from src.counting.exercise_detectors.squat_counter import SquatCounter
from src.counting.exercise_detectors.pushup_counter import PushUpCounter

__all__ = ["SquatCounter", "PushUpCounter"]
