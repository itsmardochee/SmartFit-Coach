"""
Tests unitaires pour le module de détection.
"""

import pytest
import numpy as np
import cv2
from src.detection.video_capture import VideoCapture
from src.detection.pose_detector import PoseDetector, Keypoint


class TestVideoCapture:
    """Tests pour la classe VideoCapture."""

    def test_initialization(self):
        """Test de l'initialisation."""
        vc = VideoCapture(camera_id=0)
        assert vc.camera_id == 0
        assert vc.is_opened == False
        assert vc.cap is None

    def test_context_manager(self):
        """Test du context manager."""
        with VideoCapture(camera_id=0) as vc:
            # Le test peut échouer si aucune caméra n'est disponible
            # C'est normal dans un environnement CI/CD
            pass


class TestKeypoint:
    """Tests pour la classe Keypoint."""

    def test_keypoint_creation(self):
        """Test de création d'un keypoint."""
        kp = Keypoint(id=0, name="nose", x=0.5, y=0.5, z=0.0, visibility=0.9)

        assert kp.id == 0
        assert kp.name == "nose"
        assert kp.x == 0.5
        assert kp.y == 0.5
        assert kp.visibility == 0.9

    def test_to_pixel_coords(self):
        """Test de conversion en coordonnées pixels."""
        kp = Keypoint(id=0, name="nose", x=0.5, y=0.5, z=0.0, visibility=0.9)

        x, y = kp.to_pixel_coords(640, 480)
        assert x == 320
        assert y == 240


class TestPoseDetector:
    """Tests pour la classe PoseDetector."""

    def test_initialization(self):
        """Test de l'initialisation du détecteur."""
        detector = PoseDetector(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )

        assert detector.min_detection_confidence == 0.5
        assert detector.min_tracking_confidence == 0.5
        assert len(PoseDetector.KEYPOINT_NAMES) == 33

        detector.release()

    def test_keypoint_names(self):
        """Test que tous les keypoints ont un nom."""
        assert len(PoseDetector.KEYPOINT_NAMES) == 33
        assert "nose" in PoseDetector.KEYPOINT_NAMES
        assert "left_shoulder" in PoseDetector.KEYPOINT_NAMES
        assert "right_knee" in PoseDetector.KEYPOINT_NAMES

    def test_detect_with_dummy_frame(self):
        """Test de détection avec une frame vide."""
        detector = PoseDetector()

        # Créer une frame noire
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # La détection devrait retourner None (pas de personne)
        keypoints = detector.detect(dummy_frame)

        # Sur une frame noire, aucune détection attendue
        assert keypoints is None or len(keypoints) == 0

        detector.release()

    def test_is_visible(self):
        """Test de la vérification de visibilité."""
        detector = PoseDetector()

        kp_visible = Keypoint(0, "test", 0.5, 0.5, 0.0, 0.9)
        kp_invisible = Keypoint(1, "test2", 0.5, 0.5, 0.0, 0.3)

        assert detector.is_visible(kp_visible, threshold=0.5)
        assert not detector.is_visible(kp_invisible, threshold=0.5)

        detector.release()

    def test_keypoints_to_dict(self):
        """Test de conversion en dictionnaire."""
        detector = PoseDetector()

        keypoints = [
            Keypoint(0, "nose", 0.5, 0.5, 0.0, 0.9),
            Keypoint(1, "left_eye", 0.4, 0.4, 0.0, 0.8),
        ]

        result = detector.keypoints_to_dict(keypoints)

        assert "keypoints" in result
        assert len(result["keypoints"]) == 2
        assert result["keypoints"][0]["name"] == "nose"
        assert result["keypoints"][1]["name"] == "left_eye"

        detector.release()

    def test_get_keypoint_by_name(self):
        """Test de récupération d'un keypoint par nom."""
        detector = PoseDetector()

        keypoints = [
            Keypoint(0, "nose", 0.5, 0.5, 0.0, 0.9),
            Keypoint(11, "left_shoulder", 0.4, 0.6, 0.0, 0.8),
        ]

        nose = detector.get_keypoint_by_name(keypoints, "nose")
        assert nose is not None
        assert nose.name == "nose"

        unknown = detector.get_keypoint_by_name(keypoints, "unknown")
        assert unknown is None

        detector.release()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
