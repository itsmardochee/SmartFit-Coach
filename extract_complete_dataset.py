"""
Script pour extraire les keypoints de TOUTES les données disponibles.
Traite à la fois les vidéos ET les images pour enrichir le dataset.
"""

import cv2
import json
import numpy as np
from pathlib import Path
import sys

sys.path.append("src")

from detection.pose_detector import PoseDetector
from tqdm import tqdm


def extract_keypoints_from_image(image_path: str, detector: PoseDetector, label: str):
    """
    Extrait les keypoints d'une seule image.

    Args:
        image_path: Chemin vers l'image
        detector: Détecteur de pose
        label: Label de l'exercice

    Returns:
        Dict avec les données de l'image ou None
    """
    # Lire l'image
    frame = cv2.imread(image_path)

    if frame is None:
        return None

    # Détecter la pose
    keypoints = detector.detect(frame)

    if keypoints is None or len(keypoints) == 0:
        return None

    # Extraire les features
    frame_data = {}
    for kp in keypoints:
        frame_data[f"kp_{kp.id}_x"] = kp.x
        frame_data[f"kp_{kp.id}_y"] = kp.y
        frame_data[f"kp_{kp.id}_visibility"] = kp.visibility

    frame_data["frame_num"] = 0  # Les images n'ont qu'une seule frame

    return {
        "video_name": Path(image_path).name,
        "label": label,
        "fps": 0,  # Pas de FPS pour les images
        "total_frames": 1,
        "detected_frames": 1,
        "sequence": [frame_data],
        "is_image": True,
    }


def extract_keypoints_from_video(video_path: str, detector: PoseDetector, label: str):
    """
    Extrait les keypoints de chaque frame d'une vidéo.

    Args:
        video_path: Chemin vers la vidéo
        detector: Détecteur de pose
        label: Label de l'exercice

    Returns:
        Dict avec les données de la vidéo ou None
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
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
            # Extraire les features
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
        return None

    return {
        "video_name": Path(video_path).name,
        "label": label,
        "fps": fps,
        "total_frames": frame_count,
        "detected_frames": len(sequence),
        "sequence": sequence,
        "is_image": False,
    }


def process_all_data():
    """
    Traite toutes les vidéos ET images du dataset.
    """
    # Configuration des dossiers
    data_sources = {
        "pushup": [
            ("data/raw/push-up", ["*.mp4", "*.MOV"]),  # Vidéos
            ("data/raw/push up", ["*.jpg", "*.jpeg", "*.png"]),  # Images
        ],
        "squat": [
            (
                "data/raw/squat",
                ["*.mp4", "*.MOV", "*.jpg", "*.jpeg", "*.png"],
            )  # Vidéos + Images
        ],
    }

    # Initialiser le détecteur
    print("Initialisation du detecteur de pose...")
    detector = PoseDetector()

    # Dataset complet
    dataset = []
    stats = {
        "pushup": {"videos": 0, "images": 0, "frames": 0},
        "squat": {"videos": 0, "images": 0, "frames": 0},
    }

    # Traiter chaque catégorie
    for label, sources in data_sources.items():
        print(f"\n{'=' * 60}")
        print(f"TRAITEMENT: {label.upper()}")
        print(f"{'=' * 60}")

        for folder_path, patterns in sources:
            folder = Path(folder_path)

            if not folder.exists():
                print(f"Attention: Dossier {folder} introuvable")
                continue

            # Collecter tous les fichiers
            all_files = []
            for pattern in patterns:
                all_files.extend(folder.glob(pattern))

            if len(all_files) == 0:
                continue

            print(f"\nDossier: {folder}")
            print(f"Fichiers trouves: {len(all_files)}")

            # Traiter chaque fichier
            for file_path in tqdm(all_files, desc=f"Extraction {label}"):
                file_ext = file_path.suffix.lower()

                # Déterminer si c'est une image ou une vidéo
                if file_ext in [".jpg", ".jpeg", ".png", ".bmp"]:
                    data = extract_keypoints_from_image(str(file_path), detector, label)
                    if data:
                        stats[label]["images"] += 1
                else:
                    data = extract_keypoints_from_video(str(file_path), detector, label)
                    if data:
                        stats[label]["videos"] += 1

                if data is not None:
                    dataset.append(data)
                    stats[label]["frames"] += data["detected_frames"]

    # Sauvegarder le dataset
    output_dir = Path("data/processed/keypoints")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "exercise_dataset_complete.json"

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)

    # Afficher les statistiques
    print(f"\n{'=' * 60}")
    print(f"DATASET SAUVEGARDE: {output_file}")
    print(f"{'=' * 60}")
    print(f"\nTotal elements traites: {len(dataset)}")
    print(f"\nStatistiques detaillees:")

    for label, data in stats.items():
        print(f"\n  {label.upper()}:")
        print(f"    Videos: {data['videos']}")
        print(f"    Images: {data['images']}")
        print(f"    Total frames: {data['frames']}")
        if data["videos"] + data["images"] > 0:
            avg = data["frames"] / (data["videos"] + data["images"])
            print(f"    Moyenne frames/element: {avg:.1f}")

    print(f"\n{'=' * 60}")
    print("EXTRACTION TERMINEE!")
    print(f"{'=' * 60}")
    print(f"\nDataset enrichi avec images + videos")
    print(f"Prochaine etape: Retrainer le modele avec le dataset complet")
    print(f"  -> Ouvrir notebooks/02_train_lstm.ipynb")
    print(f"  -> Changer le chemin: exercise_dataset_complete.json")

    return dataset


if __name__ == "__main__":
    print("=" * 60)
    print("EXTRACTION DATASET COMPLET (VIDEOS + IMAGES)")
    print("=" * 60)

    try:
        dataset = process_all_data()

        if dataset and len(dataset) > 0:
            print(f"\nDataset pret pour entrainement!")
        else:
            print(f"\nErreur: Aucune donnee extraite")

    except Exception as e:
        print(f"\nErreur lors de l'extraction: {e}")
        import traceback

        traceback.print_exc()
