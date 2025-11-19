"""
Script de test du comptage de répétitions sur les vidéos du dataset.

Ce script permet de valider la précision du système de comptage
en traitant des vidéos d'exercices enregistrées.

Usage:
    python test_video_counting.py --video data/raw/squat/squat_1.MOV --exercise squat
    python test_video_counting.py --video data/raw/push\ up/push_up_g1.jpg --exercise push-up
"""

import sys
from pathlib import Path
import argparse
import cv2
import time

# Ajout du répertoire racine au path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Imports locaux (après modification du path)
# pylint: disable=wrong-import-position
from src.detection.pose_detector import PoseDetector
from src.counting.exercise_detectors.squat_counter import SquatCounter
from src.counting.exercise_detectors.pushup_counter import PushUpCounter
from src.utils.visualization import draw_skeleton, draw_text_with_background


class VideoTester:
    """Testeur de comptage sur vidéos."""

    def __init__(self, exercise_type: str):
        """
        Initialise le testeur.

        Args:
            exercise_type: Type d'exercice ('squat' ou 'push-up')
        """
        self.exercise_type = exercise_type
        self.pose_detector = PoseDetector()

        # Sélection du compteur approprié
        if exercise_type == "squat":
            self.counter = SquatCounter()
        elif exercise_type == "push-up":
            self.counter = PushUpCounter()
        else:
            raise ValueError(
                f"Exercise type '{exercise_type}' non supporté. Utilisez 'squat' ou 'push-up'."
            )

    def process_video(
        self, video_path: str, display: bool = True, save_output: bool = False
    ) -> dict:
        """
        Traite une vidéo et compte les répétitions.

        Args:
            video_path: Chemin vers la vidéo à traiter
            display: Afficher la vidéo pendant le traitement
            save_output: Sauvegarder la vidéo annotée

        Returns:
            Dictionnaire avec les statistiques de traitement
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Vidéo non trouvée: {video_path}")

        # Ouvrir la vidéo
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(f"Impossible d'ouvrir la vidéo: {video_path}")

        # Informations sur la vidéo
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"\n{'=' * 60}")
        print(f"📹 Vidéo: {video_path.name}")
        print(f"📊 Résolution: {width}x{height}")
        print(f"⏱️  FPS: {fps:.1f}")
        print(f"🎞️  Frames totales: {total_frames}")
        print(f"💪 Exercice: {self.exercise_type}")
        print(f"{'=' * 60}\n")

        # Préparation de la sauvegarde (optionnel)
        out = None
        if save_output:
            output_path = Path("data/processed") / f"{video_path.stem}_annotated.mp4"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            print(f"💾 Sauvegarde de la sortie dans: {output_path}")

        # Statistiques de traitement
        frame_count = 0
        start_time = time.time()
        detection_times = []

        # Reset du compteur
        self.counter.reset()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # Détection de la pose
                det_start = time.time()
                keypoints = self.pose_detector.detect(frame)
                detection_times.append(time.time() - det_start)

                # Comptage des répétitions
                if keypoints:
                    result = self.counter.update(keypoints)

                    # Dessin du squelette
                    frame = draw_skeleton(frame, keypoints)
                else:
                    result = {"count": 0, "phase": "inconnu"}

                # Informations à l'écran
                reps = result.get("count", 0)
                state = result.get("phase", "inconnu")

                # Titre avec compteur
                title = f"{self.exercise_type.upper()} - Repetitions: {reps}"
                draw_text_with_background(
                    frame,
                    title,
                    (20, 40),
                    font_scale=1.2,
                    font_thickness=2,
                    text_color=(255, 255, 255),
                    bg_color=(0, 100, 255),
                )

                # État actuel
                state_text = f"Etat: {state}"
                state_color = (
                    (0, 255, 0)
                    if state == "debout" or state == "haut"
                    else (255, 165, 0)
                )
                draw_text_with_background(
                    frame,
                    state_text,
                    (20, 90),
                    font_scale=0.8,
                    font_thickness=2,
                    text_color=(255, 255, 255),
                    bg_color=state_color,
                )

                # Progression
                progress = f"Frame: {frame_count}/{total_frames} ({frame_count / total_frames * 100:.1f}%)"
                draw_text_with_background(
                    frame,
                    progress,
                    (20, height - 30),
                    font_scale=0.7,
                    font_thickness=1,
                    text_color=(255, 255, 255),
                    bg_color=(50, 50, 50),
                )

                # Affichage
                if display:
                    cv2.imshow("Test Comptage - Appuyez sur Q pour quitter", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        print("\n⚠️  Arrêt demandé par l'utilisateur")
                        break

                # Sauvegarde
                if out:
                    out.write(frame)

                # Feedback de progression (tous les 10%)
                if total_frames > 0 and frame_count % (total_frames // 10) == 0:
                    print(
                        f"⏳ Progression: {frame_count}/{total_frames} frames ({frame_count / total_frames * 100:.0f}%) - Reps: {reps}"
                    )

        finally:
            # Nettoyage
            cap.release()
            if out:
                out.release()
            if display:
                cv2.destroyAllWindows()

        # Statistiques finales
        elapsed_time = time.time() - start_time
        avg_detection_time = (
            sum(detection_times) / len(detection_times) if detection_times else 0
        )
        processing_fps = frame_count / elapsed_time if elapsed_time > 0 else 0

        results = {
            "video": video_path.name,
            "exercise": self.exercise_type,
            "total_reps": self.counter.count,  # Accès direct à l'attribut
            "total_frames": frame_count,
            "expected_frames": total_frames,
            "processing_time": elapsed_time,
            "processing_fps": processing_fps,
            "avg_detection_time": avg_detection_time,
            "video_fps": fps,
        }

        # Affichage des résultats
        print(f"\n{'=' * 60}")
        print("✅ RÉSULTATS DU TEST")
        print(f"{'=' * 60}")
        print(f"🏋️  Répétitions détectées: {results['total_reps']}")
        print(
            f"🎞️  Frames traitées: {results['total_frames']}/{results['expected_frames']}"
        )
        print(f"⏱️  Temps de traitement: {results['processing_time']:.2f}s")
        print(f"⚡ FPS de traitement: {results['processing_fps']:.1f} FPS")
        print(
            f"🔍 Temps moyen de détection: {results['avg_detection_time'] * 1000:.1f}ms/frame"
        )
        print(
            f"📈 Ratio performance: {results['processing_fps'] / results['video_fps'] * 100:.0f}% du temps réel"
        )
        print(f"{'=' * 60}\n")

        return results


def main():
    """Point d'entrée du script."""
    parser = argparse.ArgumentParser(
        description="Test du comptage de répétitions sur des vidéos du dataset."
    )
    parser.add_argument(
        "--video", type=str, required=True, help="Chemin vers la vidéo à tester"
    )
    parser.add_argument(
        "--exercise",
        type=str,
        required=True,
        choices=["squat", "push-up"],
        help="Type d'exercice dans la vidéo",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Ne pas afficher la vidéo pendant le traitement (traitement plus rapide)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Sauvegarder la vidéo annotée dans data/processed/",
    )

    args = parser.parse_args()

    try:
        # Création du testeur
        tester = VideoTester(args.exercise)

        # Traitement de la vidéo
        tester.process_video(
            args.video, display=not args.no_display, save_output=args.save
        )

        # Suggestions
        print("💡 SUGGESTIONS:")
        print("   - Pour traiter sans affichage (plus rapide): ajoutez --no-display")
        print("   - Pour sauvegarder la vidéo annotée: ajoutez --save")
        print("   - Pour tester une autre vidéo: changez le paramètre --video")

        return 0

    except Exception as e:
        print(f"\n❌ ERREUR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
