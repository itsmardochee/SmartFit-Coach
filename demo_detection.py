"""
Script de démonstration de la détection de pose en temps réel.
Lance la webcam et affiche les keypoints détectés.

Usage:
    python demo_detection.py
"""

import cv2
import time
from src.detection.video_capture import VideoCapture
from src.detection.pose_detector import PoseDetector
from src.utils.visualization import create_overlay


def main():
    """
    Fonction principale de démonstration.
    """
    print("🚀 Démarrage de SmartFit Coach - Détection de Pose")
    print("=" * 50)

    # Initialisation
    video_capture = VideoCapture(camera_id=0)
    pose_detector = PoseDetector(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    )

    # Démarrage de la caméra
    if not video_capture.start():
        print("❌ Erreur: Impossible d'accéder à la caméra")
        return

    print("✅ Caméra connectée")
    print(f"📐 Résolution: {video_capture.get_frame_dimensions()}")
    print(f"🎬 FPS: {video_capture.get_fps()}")
    print("\nAppuyez sur 'q' pour quitter")
    print("=" * 50)

    # Variables pour le calcul du FPS
    fps = 0
    frame_count = 0
    start_time = time.time()

    try:
        while True:
            # Lecture de la frame
            success, frame = video_capture.read_frame()

            if not success:
                print("⚠️ Erreur de lecture de la frame")
                break

            # Détection des keypoints
            keypoints = pose_detector.detect(frame)

            # Calcul du FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1.0:
                fps = frame_count / elapsed_time
                frame_count = 0
                start_time = time.time()

            # Création de l'overlay
            if keypoints:
                feedback = f"✅ {len(keypoints)} points détectés"
                feedback_type = "success"
            else:
                feedback = "⚠️ Aucune personne détectée"
                feedback_type = "warning"

            frame_with_overlay = create_overlay(
                frame=frame,
                keypoints=keypoints,
                fps=fps,
                feedback=feedback,
                feedback_type=feedback_type,
            )

            # Affichage
            cv2.imshow("SmartFit Coach - Detection", frame_with_overlay)

            # Gestion des touches
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("\n👋 Arrêt de l'application")
                break

    except KeyboardInterrupt:
        print("\n👋 Interruption par l'utilisateur")

    finally:
        # Nettoyage
        video_capture.release()
        pose_detector.release()
        cv2.destroyAllWindows()
        print("✅ Ressources libérées")


if __name__ == "__main__":
    main()
