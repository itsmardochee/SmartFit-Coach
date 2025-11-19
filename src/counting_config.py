# Configuration des seuils pour le comptage d'exercices
# Ces valeurs peuvent être ajustées selon votre dataset

# POMPES (Push-ups)
PUSHUP_MIN_ELBOW_ANGLE = 90  # Angle minimum du coude en position basse
PUSHUP_MAX_ELBOW_ANGLE = 170  # Angle maximum du coude en position haute
PUSHUP_MIN_TIME_BETWEEN_REPS = 0.3  # Temps minimum entre répétitions (secondes)

# SQUATS
SQUAT_MIN_KNEE_ANGLE = 90  # Angle minimum du genou en position basse
SQUAT_MAX_KNEE_ANGLE = 170  # Angle maximum du genou debout
SQUAT_MIN_HIP_ANGLE = 70  # Angle minimum de la hanche
SQUAT_MIN_TIME_BETWEEN_REPS = 0.3  # Temps minimum entre répétitions (secondes)

# TRANSITIONS (Marges pour les changements d'état)
ANGLE_TRANSITION_MARGIN = 10  # Marge pour les transitions d'état (degrés)
