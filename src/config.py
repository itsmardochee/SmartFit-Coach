"""
Configuration globale pour SmartFit Coach.
"""

# Paramètres de la caméra
CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Paramètres de détection MediaPipe
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
MODEL_COMPLEXITY = 1  # 0=lite, 1=full, 2=heavy

# Paramètres de visualisation
SKELETON_COLOR = (0, 255, 0)  # Vert en BGR
SKELETON_THICKNESS = 2
TEXT_COLOR = (255, 255, 255)  # Blanc
TEXT_BG_COLOR = (0, 0, 0)  # Noir

# Seuils de visibilité
MIN_VISIBILITY_THRESHOLD = 0.5

# Performance
TARGET_FPS = 30
MIN_ACCEPTABLE_FPS = 20

# Chemins
DATA_DIR = "data"
MODELS_DIR = "models"
LOGS_DIR = "logs"
SESSIONS_DIR = "data/sessions"
EXERCISES_DIR = "data/exercises"

# Exercices supportés
SUPPORTED_EXERCISES = ["squats", "pompes", "fentes"]

# Seuils d'angles pour les exercices (en degrés)
SQUAT_KNEE_ANGLE_DOWN = 90  # Angle minimum du genou en position basse
SQUAT_KNEE_ANGLE_UP = 170  # Angle du genou en position haute

PUSHUP_ELBOW_ANGLE_DOWN = 90  # Angle du coude en position basse
PUSHUP_ELBOW_ANGLE_UP = 160  # Angle du coude en position haute

# Feedback
FEEDBACK_COOLDOWN = 3.0  # Secondes entre deux feedbacks
QUALITY_THRESHOLD_GOOD = 0.8  # Seuil pour "bon mouvement"
QUALITY_THRESHOLD_ACCEPTABLE = 0.6  # Seuil pour "mouvement acceptable"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
