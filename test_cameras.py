"""
Script pour tester la détection des caméras disponibles.
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from src.detection.video_capture import list_available_cameras

print("🔍 Détection des caméras disponibles...")
print("-" * 50)

cameras = list_available_cameras()

if cameras:
    print(f"\n✅ {len(cameras)} caméra(s) détectée(s) :\n")
    for cam in cameras:
        print(f"📹 Caméra {cam['id']}")
        print(f"   Nom: {cam['name']}")
        print(f"   Résolution: {cam['resolution']}")
        print(f"   FPS: {cam['fps']}")
        print()
else:
    print("\n❌ Aucune caméra détectée.")
    print("Vérifiez que votre webcam est connectée et accessible.")

print("-" * 50)
