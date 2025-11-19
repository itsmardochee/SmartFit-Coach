"""
Tests unitaires pour les modules de comptage d'exercices.
"""

import pytest
import numpy as np
from src.detection.pose_detector import Keypoint
from src.counting.angle_calculator import (
    calculate_angle,
    calculate_angle_3d,
    calculate_vertical_distance,
    calculate_horizontal_distance,
    calculate_euclidean_distance,
    is_keypoint_visible,
    calculate_knee_angle,
    calculate_elbow_angle,
)
from src.counting.exercise_detectors.squat_counter import SquatCounter, SquatPhase
from src.counting.exercise_detectors.pushup_counter import PushUpCounter, PushUpPhase


# Fixtures pour créer des keypoints de test
@pytest.fixture
def create_keypoint():
    """Factory pour créer des keypoints de test."""

    def _create(x, y, z=0.0, visibility=1.0, kp_id=0, name="test"):
        return Keypoint(id=kp_id, name=name, x=x, y=y, z=z, visibility=visibility)

    return _create


@pytest.fixture
def standing_pose_keypoints(create_keypoint):
    """Crée des keypoints pour une position debout (squat haut)."""
    keypoints = [create_keypoint(0.5, 0.5, kp_id=i) for i in range(33)]

    # Épaules
    keypoints[11] = create_keypoint(0.4, 0.3, kp_id=11, name="left_shoulder")
    keypoints[12] = create_keypoint(0.6, 0.3, kp_id=12, name="right_shoulder")

    # Hanches
    keypoints[23] = create_keypoint(0.4, 0.5, kp_id=23, name="left_hip")
    keypoints[24] = create_keypoint(0.6, 0.5, kp_id=24, name="right_hip")

    # Genoux (presque droits - 170°)
    keypoints[25] = create_keypoint(0.4, 0.7, kp_id=25, name="left_knee")
    keypoints[26] = create_keypoint(0.6, 0.7, kp_id=26, name="right_knee")

    # Chevilles
    keypoints[27] = create_keypoint(0.4, 0.9, kp_id=27, name="left_ankle")
    keypoints[28] = create_keypoint(0.6, 0.9, kp_id=28, name="right_ankle")

    return keypoints


@pytest.fixture
def squat_bottom_keypoints(create_keypoint):
    """Crée des keypoints pour une position basse de squat."""
    keypoints = [create_keypoint(0.5, 0.5, kp_id=i) for i in range(33)]

    # Épaules
    keypoints[11] = create_keypoint(0.4, 0.4, kp_id=11, name="left_shoulder")
    keypoints[12] = create_keypoint(0.6, 0.4, kp_id=12, name="right_shoulder")

    # Hanches (descente)
    keypoints[23] = create_keypoint(0.4, 0.65, kp_id=23, name="left_hip")
    keypoints[24] = create_keypoint(0.6, 0.65, kp_id=24, name="right_hip")

    # Genoux (angle ~85°)
    keypoints[25] = create_keypoint(0.35, 0.75, kp_id=25, name="left_knee")
    keypoints[26] = create_keypoint(0.65, 0.75, kp_id=26, name="right_knee")

    # Chevilles
    keypoints[27] = create_keypoint(0.35, 0.9, kp_id=27, name="left_ankle")
    keypoints[28] = create_keypoint(0.65, 0.9, kp_id=28, name="right_ankle")

    return keypoints


@pytest.fixture
def pushup_up_keypoints(create_keypoint):
    """Crée des keypoints pour une pompe en position haute."""
    keypoints = [create_keypoint(0.5, 0.5, kp_id=i) for i in range(33)]

    # Épaules
    keypoints[11] = create_keypoint(0.35, 0.4, kp_id=11, name="left_shoulder")
    keypoints[12] = create_keypoint(0.65, 0.4, kp_id=12, name="right_shoulder")

    # Coudes (presque droits)
    keypoints[13] = create_keypoint(0.3, 0.5, kp_id=13, name="left_elbow")
    keypoints[14] = create_keypoint(0.7, 0.5, kp_id=14, name="right_elbow")

    # Poignets
    keypoints[15] = create_keypoint(0.25, 0.6, kp_id=15, name="left_wrist")
    keypoints[16] = create_keypoint(0.75, 0.6, kp_id=16, name="right_wrist")

    # Hanches
    keypoints[23] = create_keypoint(0.35, 0.6, kp_id=23, name="left_hip")
    keypoints[24] = create_keypoint(0.65, 0.6, kp_id=24, name="right_hip")

    return keypoints


# Tests pour angle_calculator.py
class TestAngleCalculator:
    """Tests pour les fonctions de calcul d'angles."""

    def test_calculate_angle_90_degrees(self, create_keypoint):
        """Test calcul d'un angle à 90°."""
        a = create_keypoint(0.0, 0.0)
        b = create_keypoint(0.0, 0.5)
        c = create_keypoint(0.5, 0.5)

        angle = calculate_angle(a, b, c)
        assert 85 <= angle <= 95  # Tolérance de ±5°

    def test_calculate_angle_180_degrees(self, create_keypoint):
        """Test calcul d'un angle à 180° (ligne droite)."""
        a = create_keypoint(0.0, 0.5)
        b = create_keypoint(0.5, 0.5)
        c = create_keypoint(1.0, 0.5)

        angle = calculate_angle(a, b, c)
        assert 175 <= angle <= 180

    def test_calculate_angle_3d(self, create_keypoint):
        """Test calcul d'angle en 3D."""
        a = create_keypoint(0.0, 0.0, 0.0)
        b = create_keypoint(0.0, 0.5, 0.0)
        c = create_keypoint(0.5, 0.5, 0.0)

        angle = calculate_angle_3d(a, b, c)
        assert 85 <= angle <= 95

    def test_calculate_vertical_distance(self, create_keypoint):
        """Test calcul de distance verticale."""
        a = create_keypoint(0.5, 0.3)
        b = create_keypoint(0.5, 0.7)

        distance = calculate_vertical_distance(a, b)
        assert abs(distance - 0.4) < 0.01

    def test_calculate_horizontal_distance(self, create_keypoint):
        """Test calcul de distance horizontale."""
        a = create_keypoint(0.2, 0.5)
        b = create_keypoint(0.8, 0.5)

        distance = calculate_horizontal_distance(a, b)
        assert abs(distance - 0.6) < 0.01

    def test_calculate_euclidean_distance(self, create_keypoint):
        """Test calcul de distance euclidienne."""
        a = create_keypoint(0.0, 0.0)
        b = create_keypoint(0.3, 0.4)

        distance = calculate_euclidean_distance(a, b)
        expected = np.sqrt(0.3**2 + 0.4**2)
        assert abs(distance - expected) < 0.01

    def test_is_keypoint_visible(self, create_keypoint):
        """Test vérification de visibilité."""
        visible = create_keypoint(0.5, 0.5, visibility=0.8)
        not_visible = create_keypoint(0.5, 0.5, visibility=0.3)

        assert is_keypoint_visible(visible, min_visibility=0.5)
        assert not is_keypoint_visible(not_visible, min_visibility=0.5)

    def test_calculate_knee_angle(self, standing_pose_keypoints):
        """Test calcul d'angle du genou."""
        hip = standing_pose_keypoints[23]
        knee = standing_pose_keypoints[25]
        ankle = standing_pose_keypoints[27]

        angle = calculate_knee_angle(hip, knee, ankle)
        assert angle > 160  # Debout = presque droit

    def test_calculate_elbow_angle(self, pushup_up_keypoints):
        """Test calcul d'angle du coude."""
        shoulder = pushup_up_keypoints[11]
        elbow = pushup_up_keypoints[13]
        wrist = pushup_up_keypoints[15]

        angle = calculate_elbow_angle(shoulder, elbow, wrist)
        assert angle > 140  # Position haute = bras presque droits


# Tests pour SquatCounter
class TestSquatCounter:
    """Tests pour le compteur de squats."""

    def test_initialization(self):
        """Test initialisation du compteur."""
        counter = SquatCounter()
        assert counter.count == 0
        assert counter.current_phase == SquatPhase.STANDING

    def test_reset(self):
        """Test réinitialisation du compteur."""
        counter = SquatCounter()
        counter.count = 5
        counter.reset()
        assert counter.count == 0
        assert counter.current_phase == SquatPhase.STANDING

    def test_update_standing_position(self, standing_pose_keypoints):
        """Test mise à jour avec position debout."""
        counter = SquatCounter()
        result = counter.update(standing_pose_keypoints)

        assert result["count"] == 0
        assert "phase" in result
        assert "metrics" in result
        assert "feedback" in result

    def test_update_squat_bottom(self, squat_bottom_keypoints):
        """Test mise à jour avec position basse."""
        counter = SquatCounter()
        result = counter.update(squat_bottom_keypoints)

        assert result["metrics"] is not None
        assert result["metrics"]["knee_angle"] < 100

    def test_get_stats(self):
        """Test récupération des statistiques."""
        counter = SquatCounter()
        counter.count = 10

        stats = counter.get_stats()
        assert "total_reps" in stats
        assert "valid_reps" in stats
        assert "success_rate" in stats


# Tests pour PushUpCounter
class TestPushUpCounter:
    """Tests pour le compteur de pompes."""

    def test_initialization(self):
        """Test initialisation du compteur."""
        counter = PushUpCounter()
        assert counter.count == 0
        assert counter.current_phase == PushUpPhase.UP

    def test_reset(self):
        """Test réinitialisation du compteur."""
        counter = PushUpCounter()
        counter.count = 3
        counter.reset()
        assert counter.count == 0
        assert counter.current_phase == PushUpPhase.UP

    def test_update_up_position(self, pushup_up_keypoints):
        """Test mise à jour avec position haute."""
        counter = PushUpCounter()
        result = counter.update(pushup_up_keypoints)

        assert result["count"] == 0
        assert "phase" in result
        assert "feedback" in result

    def test_get_stats(self):
        """Test récupération des statistiques."""
        counter = PushUpCounter()
        counter.count = 5

        stats = counter.get_stats()
        assert "total_reps" in stats
        assert "valid_reps" in stats
        assert stats["total_reps"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
