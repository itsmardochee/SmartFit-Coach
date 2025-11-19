"""
Script pour extraire les keypoints de toutes les vidéos du dataset.
Génère un dataset structuré pour l'entraînement du modèle LSTM.
"""

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Masquer les messages INFO de TensorFlow

import cv2
import json
import numpy as np
from pathlib import Path
import sys

sys.path.append("src")

from detection.pose_detector import PoseDetector
from tqdm import tqdm


def extract_keypoints_from_video(video_path: str, detector: PoseDetector, label: str):
    """
    Extrait les keypoints de chaque frame d'une vidéo.

    Args:
        video_path: Chemin vers la vidéo
        detector: Détecteur de pose
        label: Label de l'exercice (squat, pushup)

    Returns:
        Dict avec les données de la vidéo
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Erreur: Impossible d'ouvrir {video_path}")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    sequence = []
    frame_num = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Détecter la pose
        keypoints = detector.detect(frame)

        if keypoints is not None and len(keypoints) > 0:
            # Extraire seulement les coordonnées normalisées (x, y, visibility)
            frame_data = {}
            for kp in keypoints:
                frame_data[f"kp_{kp.id}_x"] = kp.x
                frame_data[f"kp_{kp.id}_y"] = kp.y
                frame_data[f"kp_{kp.id}_visibility"] = kp.visibility

            frame_data["frame_num"] = frame_num
            sequence.append(frame_data)

        frame_num += 1

    cap.release()

    if len(sequence) == 0:
        print(f"Attention: Aucun keypoint detecte dans {video_path}")
        return None

    return {
        "video_name": Path(video_path).name,
        "label": label,
        "fps": fps,
        "total_frames": frame_count,
        "detected_frames": len(sequence),
        "sequence": sequence,
    }


def process_all_videos():
    """
    Traite toutes les vidéos du dataset.
    """
    # Dossiers des vidéos
    video_dirs = {"pushup": Path("data/raw/push-up"), "squat": Path("data/raw/squat")}

    # Vérifier que les dossiers existent
    for label, path in video_dirs.items():
        if not path.exists():
            print(f"Erreur: Dossier {path} introuvable")
            return

    # Initialiser le détecteur
    print("Initialisation du detecteur de pose...")
    detector = PoseDetector()

    # Dataset complet
    dataset = []

    # Traiter chaque catégorie
    for label, video_dir in video_dirs.items():
        print(f"\n=== Traitement des videos: {label.upper()} ===")

        # Trouver toutes les vidéos
        video_files = list(video_dir.glob("*.mp4")) + list(video_dir.glob("*.MOV"))

        if len(video_files) == 0:
            print(f"Attention: Aucune video trouvee dans {video_dir}")
            continue

        print(f"Trouve {len(video_files)} videos")

        # Traiter chaque vidéo avec barre de progression
        for video_path in tqdm(video_files, desc=f"Extraction {label}"):
            video_data = extract_keypoints_from_video(str(video_path), detector, label)

            if video_data is not None:
                dataset.append(video_data)

    # Sauvegarder le dataset
    output_dir = Path("data/processed/keypoints")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "exercise_dataset.json"

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Dataset sauvegarde dans: {output_file}")
    print(f"Total videos traitees: {len(dataset)}")

    # Statistiques
    stats = {}
    for item in dataset:
        label = item["label"]
        if label not in stats:
            stats[label] = {"count": 0, "total_frames": 0}
        stats[label]["count"] += 1
        stats[label]["total_frames"] += item["detected_frames"]

    print(f"\nStatistiques:")
    for label, data in stats.items():
        avg_frames = data["total_frames"] / data["count"] if data["count"] > 0 else 0
        print(
            f"  {label}: {data['count']} videos, {data['total_frames']} frames totales, {avg_frames:.1f} frames/video en moyenne"
        )

    print(f"\n{'=' * 60}")
    print("Extraction terminee avec succes!")

    return dataset


if __name__ == "__main__":
    print("=" * 60)
    print("EXTRACTION DES KEYPOINTS POUR DATASET D'ENTRAINEMENT")
    print("=" * 60)

    try:
        dataset = process_all_videos()

        if dataset and len(dataset) > 0:
            print("\nLe dataset est pret pour l'entrainement!")
            print("Prochaine etape: Ouvrir le notebook notebooks/02_train_lstm.ipynb")
        else:
            print("\nErreur: Aucune donnee extraite")

    except Exception as e:
        print(f"\nErreur lors de l'extraction: {e}")
        import traceback

        traceback.print_exc()
