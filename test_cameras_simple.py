"""
Test simple de détection des caméras disponibles.
"""

import cv2

def test_cameras():
    """Teste les caméras disponibles sans importer les modules src."""
    print("🎥 Détection des caméras disponibles...\n")
    
    available_cameras = []
    
    for camera_id in range(10):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
                camera_info = {
                    'id': camera_id,
                    'name': f"Caméra {camera_id}",
                    'resolution': (width, height),
                    'fps': fps
                }
                available_cameras.append(camera_info)
                print(f"✅ Caméra {camera_id} détectée:")
                print(f"   - Résolution: {width}x{height}")
                print(f"   - FPS: {fps}")
                print()
            cap.release()
    
    if not available_cameras:
        print("❌ Aucune caméra détectée")
    else:
        print(f"\n✅ Total: {len(available_cameras)} caméra(s) disponible(s)")
    
    return available_cameras

if __name__ == "__main__":
    cameras = test_cameras()
