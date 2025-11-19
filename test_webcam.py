"""
Script de test simple pour vérifier l'accès à la webcam.
"""

import cv2
import sys

print("Test d'accès à la webcam avec DirectShow...")
print(f"Version OpenCV: {cv2.__version__}")

# Essayer d'ouvrir la webcam avec DirectShow (Windows)
print("\nUtilisation de DirectShow (recommandé pour Windows)...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ ERREUR: Impossible d'ouvrir la webcam (index 0)")

    # Essayer avec l'index 1
    print("\nEssai avec l'index 1...")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("❌ ERREUR: Impossible d'ouvrir la webcam (index 1)")

        # Essayer avec DirectShow (Windows)
        print("\nEssai avec DirectShow (Windows)...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("❌ ERREUR: Impossible d'ouvrir la webcam avec DirectShow")
            print("\n⚠️ Vérifications à faire:")
            print("1. La webcam est-elle branchée?")
            print("2. Une autre application utilise-t-elle la webcam?")
            print("3. Les pilotes sont-ils à jour?")
            sys.exit(1)
        else:
            print("✅ Webcam accessible avec DirectShow!")
    else:
        print("✅ Webcam accessible avec l'index 1!")
else:
    print("✅ Webcam accessible avec l'index 0!")

# Lire une frame de test
ret, frame = cap.read()
if ret:
    print(f"✅ Frame capturée avec succès!")
    print(f"   Dimensions: {frame.shape[1]}x{frame.shape[0]}")
    print(f"   Format: {frame.dtype}")
else:
    print("❌ ERREUR: Impossible de lire une frame")

# Libérer la ressource
cap.release()
print("\n✅ Test terminé avec succès!")
print("\n💡 La webcam fonctionne correctement avec OpenCV.")
