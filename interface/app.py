"""
Application principale SmartFit Coach.
Interface Streamlit pour le coaching sportif en temps réel.
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import streamlit as st
import cv2
import time
from src.detection.video_capture import VideoCapture
from src.detection.pose_detector import PoseDetector
from src.utils.visualization import draw_skeleton, draw_text_with_background
from src.counting.exercise_detectors import SquatCounter, PushUpCounter
from src.recognition.exercise_classifier import ExerciseClassifier
from src.feedback.posture_analyzer import PostureAnalyzer
from src.feedback.feedback_generator import FeedbackGenerator
from src.session.workout_session import WorkoutSession


# Configuration de la page
st.set_page_config(
    page_title="SmartFit Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styles CSS personnalisés
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .feedback-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: 500;
    }
    .feedback-success {
        background: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .feedback-warning {
        background: #fff3cd;
        color: #856404;
        border: 2px solid #ffeeba;
    }
    .feedback-info {
        background: #d1ecf1;
        color: #0c5460;
        border: 2px solid #bee5eb;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialise les variables de session Streamlit."""
    if "exercise_type" not in st.session_state:
        st.session_state.exercise_type = "Auto-détection"
    if "session_active" not in st.session_state:
        st.session_state.session_active = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "counter" not in st.session_state:
        st.session_state.counter = None
    if "classifier" not in st.session_state:
        st.session_state.classifier = ExerciseClassifier()
    if "posture_analyzer" not in st.session_state:
        st.session_state.posture_analyzer = PostureAnalyzer()
    if "feedback_generator" not in st.session_state:
        st.session_state.feedback_generator = FeedbackGenerator()
    if "workout_session" not in st.session_state:
        st.session_state.workout_session = None
    if "auto_detect" not in st.session_state:
        st.session_state.auto_detect = True
    if "selected_camera" not in st.session_state:
        st.session_state.selected_camera = 0
    if "available_cameras" not in st.session_state:
        # Détecter les caméras au démarrage
        from src.detection.video_capture import list_available_cameras
        st.session_state.available_cameras = list_available_cameras()
        if not st.session_state.available_cameras:
            st.session_state.available_cameras = [{'id': 0, 'name': 'Caméra 0', 'resolution': 'N/A', 'fps': 30}]


def get_counter(exercise_type: str):
    """
    Retourne le compteur approprié pour l'exercice sélectionné.

    Args:
        exercise_type: Type d'exercice ("Squats", "Pompes")

    Returns:
        Compteur approprié
    """
    if exercise_type == "Squats":
        return SquatCounter()
    elif exercise_type == "Pompes":
        return PushUpCounter()
    return None


def get_feedback_class(feedback: str) -> str:
    """
    Détermine la classe CSS pour le feedback.

    Args:
        feedback: Message de feedback

    Returns:
        Classe CSS appropriée
    """
    if "✅" in feedback or "Parfait" in feedback or "Bonne" in feedback:
        return "feedback-success"
    elif "⚠️" in feedback:
        return "feedback-warning"
    else:
        return "feedback-info"


def main():
    """Fonction principale de l'application."""
    initialize_session_state()

    # Titre principal
    st.markdown('<h1 class="main-title">💪 SmartFit Coach</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem;">Votre coach sportif intelligent en temps réel</p>',
        unsafe_allow_html=True,
    )

    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Mode de détection
        detection_mode = st.radio(
            "Mode de détection", ["Auto-détection", "Manuel"], key="detection_mode"
        )

        st.session_state.auto_detect = detection_mode == "Auto-détection"

        # Sélection manuelle de l'exercice
        if not st.session_state.auto_detect:
            exercise_type = st.selectbox(
                "Type d'exercice", ["Squats", "Pompes"], key="exercise_selector"
            )
        else:
            # En mode auto, afficher l'exercice détecté
            classifier = st.session_state.classifier
            detected = classifier.get_current_exercise()
            if detected:
                st.info(f"🎯 **Exercice détecté:** {detected.upper()}")
                exercise_type = "Squats" if "squat" in detected.lower() else "Pompes"
            else:
                st.info("🔍 En attente de détection...")
                exercise_type = "Squats"  # Par défaut

        # Vérifier si l'exercice a changé
        if exercise_type != st.session_state.exercise_type:
            st.session_state.exercise_type = exercise_type
            if st.session_state.counter:
                st.session_state.counter = get_counter(exercise_type)

        st.divider()

        st.divider()

        # Sélection de la source vidéo
        st.subheader("📹 Source Vidéo")
        
        input_source = st.radio(
            "Source",
            ["Webcam", "Fichier Vidéo"],
            key="input_source_selector",
            disabled=st.session_state.session_active
        )

        if input_source == "Webcam":
            available_cameras = st.session_state.available_cameras
            
            if len(available_cameras) > 1:
                # Plusieurs caméras disponibles
                camera_options = [
                    f"{cam['name']} ({cam['resolution']})" 
                    for cam in available_cameras
                ]
                
                selected_index = st.selectbox(
                    "Choisir la caméra",
                    range(len(camera_options)),
                    format_func=lambda i: camera_options[i],
                    key="camera_selector",
                    disabled=st.session_state.session_active
                )
                
                st.session_state.selected_camera = available_cameras[selected_index]['id']
                
                # Afficher les infos
                cam_info = available_cameras[selected_index]
                st.caption(f"📊 {cam_info['resolution']} • {cam_info['fps']} FPS")
            else:
                # Une seule caméra
                st.info(f"📷 {available_cameras[0]['name']}")
                st.session_state.selected_camera = available_cameras[0]['id']
            
            # Bouton pour rafraîchir les caméras
            if st.button("🔄 Détecter caméras", disabled=st.session_state.session_active):
                from src.detection.video_capture import list_available_cameras
                st.session_state.available_cameras = list_available_cameras()
                st.rerun()

        else:
            # Mode Fichier Vidéo
            uploaded_file = st.file_uploader(
                "Choisir une vidéo", 
                type=['mp4', 'avi', 'mov', 'mkv'],
                disabled=st.session_state.session_active
            )
            
            if uploaded_file is not None:
                # Sauvegarder le fichier temporairement
                import tempfile
                import os
                
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                
                st.session_state.selected_camera = tfile.name
                st.success(f"✅ Vidéo chargée: {uploaded_file.name}")
            else:
                st.warning("Veuillez charger une vidéo pour commencer.")
                # Empêcher le démarrage si pas de vidéo
                st.session_state.selected_camera = None

        st.divider()

        # Boutons de contrôle
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "▶️ Démarrer",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.session_active,
            ):
                if st.session_state.selected_camera is None:
                    st.error("❌ Aucune source vidéo sélectionnée")
                else:
                    st.session_state.session_active = True
                    st.session_state.start_time = time.time()
                    st.session_state.counter = get_counter(exercise_type)
                    # Créer une nouvelle session d'entraînement
                    st.session_state.workout_session = WorkoutSession(exercise_type)
                    # Réinitialiser les analyseurs
                    st.session_state.posture_analyzer.reset()
                    st.session_state.feedback_generator.reset()
                    st.session_state.classifier.reset()
                    st.rerun()

        with col2:
            if st.button(
                "⏹️ Arrêter",
                type="secondary",
                use_container_width=True,
                disabled=not st.session_state.session_active,
            ):
                st.session_state.session_active = False

                # Terminer la session et afficher les statistiques
                if st.session_state.workout_session:
                    stats = st.session_state.workout_session.end_session()

                    # Sauvegarder la session
                    filepath = st.session_state.workout_session.save_to_file()
                    st.success(f"💾 Session sauvegardée!")

                    # Afficher le résumé
                    st.sidebar.markdown("---")
                    st.sidebar.markdown("### 📊 Résumé de session")
                    st.sidebar.write(
                        st.session_state.workout_session.get_summary_text()
                    )

                # Libérer la webcam
                if "video_capture" in st.session_state:
                    st.session_state.video_capture.release()
                    del st.session_state.video_capture
                if "pose_detector" in st.session_state:
                    del st.session_state.pose_detector
                st.rerun()

        if st.button("🔄 Réinitialiser", use_container_width=True):
            if st.session_state.counter:
                st.session_state.counter.reset()
            if st.session_state.workout_session:
                st.session_state.workout_session = WorkoutSession(exercise_type)
            st.session_state.posture_analyzer.reset()
            st.session_state.feedback_generator.reset()
            st.session_state.start_time = time.time()
            st.rerun()

        st.divider()

        # Paramètres avancés
        with st.expander("🔧 Paramètres avancés"):
            confidence = st.slider("Confiance de détection", 0.3, 1.0, 0.5, 0.1)
            show_skeleton = st.checkbox("Afficher le squelette", value=True)

        st.divider()

        # Informations
        st.markdown("### 📖 Instructions")
        if exercise_type == "Squats":
            st.info("""
            **Comment faire un squat :**
            1. Pieds écartés largeur d'épaules
            2. Descends en pliant les genoux
            3. Garde le dos droit
            4. Remonte en position debout
            """)
        else:
            st.info("""
            **Comment faire une pompe :**
            1. Mains au sol, corps aligné
            2. Descends en pliant les coudes
            3. Coudes à 90° en position basse
            4. Pousse pour remonter
            """)

    # Zone principale - Vidéo et métriques
    if not st.session_state.session_active:
        # Message d'accueil
        st.info(
            "👆 Clique sur **Démarrer** dans le menu de gauche pour commencer ta session d'entraînement !"
        )

        # Image de placeholder
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "https://via.placeholder.com/640x480/667eea/ffffff?text=Prêt+à+t'entraîner+?",
                width="stretch",
            )

    else:
        # Session active
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📹 Vue en direct")
            video_placeholder = st.empty()

        with col2:
            st.subheader("📊 Statistiques")

            # Métriques en temps réel
            count_container = st.empty()
            quality_container = st.empty()
            phase_container = st.empty()
            time_container = st.empty()
            calories_container = st.empty()
            feedback_container = st.empty()

            st.divider()

            # Afficher l'exercice en cours
            # Afficher l'exercice en cours
            exercise_info_container = st.empty()
            exercise_info_container.markdown(f"""
                <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 10px;">
                    <h3 style="margin:0; color: #333;">🏋️ {exercise_type}</h3>
                    <small style="color: #666;">Mode: {"Auto" if st.session_state.auto_detect else "Manuel"}</small>
                </div>
            """, unsafe_allow_html=True)

            # Statistiques de session
            stats_container = st.empty()

        # Initialiser la capture vidéo dans session_state si nécessaire
        if "video_capture" not in st.session_state:
            # Utiliser la caméra sélectionnée
            selected_cam_id = st.session_state.selected_camera
            st.session_state.video_capture = VideoCapture(source=selected_cam_id)
            
            if not st.session_state.video_capture.start():
                st.error(
                    f"❌ Impossible d'accéder à la caméra {selected_cam_id}. "
                    "Vérifiez qu'elle est bien connectée et qu'aucune autre application ne l'utilise."
                )
                st.session_state.session_active = False
                return

        # Initialiser le détecteur dans session_state si nécessaire
        if "pose_detector" not in st.session_state:
            st.session_state.pose_detector = PoseDetector(
                min_detection_confidence=confidence
            )

        video_capture = st.session_state.video_capture
        pose_detector = st.session_state.pose_detector
        counter = st.session_state.counter
        classifier = st.session_state.classifier
        posture_analyzer = st.session_state.posture_analyzer
        feedback_generator = st.session_state.feedback_generator
        workout_session = st.session_state.workout_session

        # Boucle de traitement vidéo (sans rerun, juste mise à jour des placeholders)
        try:
            while st.session_state.session_active:
                # Capturer une frame
                ret, frame = video_capture.read_frame()

                if not ret:
                    st.error("❌ Impossible de lire la webcam")
                    st.session_state.session_active = False
                    break

                # Détecter la pose
                keypoints = pose_detector.detect(frame)

                if keypoints and show_skeleton:
                    # Dessiner le squelette
                    frame = draw_skeleton(frame, keypoints)

                # Auto-détection de l'exercice (si activée)
                if st.session_state.auto_detect and keypoints:
                    classifier.add_frame(keypoints)
                    prediction = classifier.predict()

                    if prediction:
                        detected_exercise, confidence, probs = prediction
                        if confidence >= 0.7:
                            # Mettre à jour l'exercice si détecté avec confiance
                            if "squat" in detected_exercise.lower():
                                exercise_type = "Squats"
                            elif "push" in detected_exercise.lower():
                                exercise_type = "Pompes"

                            # Mettre à jour le compteur si l'exercice a changé
                            if exercise_type != st.session_state.exercise_type:
                                st.session_state.exercise_type = exercise_type
                                counter = get_counter(exercise_type)
                                st.session_state.counter = counter
                                
                                # Mettre à jour l'affichage de l'exercice
                                exercise_info_container.markdown(f"""
                                    <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 10px;">
                                        <h3 style="margin:0; color: #333;">🏋️ {exercise_type}</h3>
                                        <small style="color: #666;">Mode: Auto</small>
                                    </div>
                                """, unsafe_allow_html=True)

                # Mettre à jour le compteur
                result = (
                    counter.update(keypoints)
                    if keypoints
                    else {
                        "count": 0,
                        "phase": "non détecté",
                        "metrics": None,
                        "feedback": "⚠️ Aucune personne détectée",
                    }
                )

                # En mode auto, si on détecte une mauvaise position (ex: au sol pour des squats),
                # on masque le message d'erreur car l'auto-détection va probablement changer l'exercice.
                if st.session_state.auto_detect and "Mets-toi" in result["feedback"]:
                    result["feedback"] = "Analyse du mouvement en cours..."

                # Vérifier si la visibilité est suffisante avant de continuer
                is_visible = "⚠️" not in result["feedback"]

                # Analyser la posture et générer le feedback seulement si visible
                posture_result = None
                feedback = None
                
                if is_visible and keypoints:
                    posture_result = posture_analyzer.analyze(exercise_type, keypoints)
                    
                    if posture_result:
                        feedback = feedback_generator.generate_feedback(
                            quality_score=posture_result["quality_score"],
                            errors=posture_result["errors"],
                            exercise=exercise_type,
                            rep_count=result["count"],
                        )

                # Déterminer le message à afficher
                if not is_visible:
                    # Priorité absolue au message de visibilité
                    feedback_message = result["feedback"]
                    bg_color = (0, 100, 255) # Bleu pour info/warning
                
                elif feedback:
                    feedback_message = feedback["message"]
                    feedback_color_map = {
                        "green": (0, 255, 0),
                        "orange": (0, 165, 255),
                        "red": (0, 0, 255),
                        "yellow": (0, 255, 255),
                    }
                    bg_color = feedback_color_map.get(
                        feedback["color"], (100, 100, 100)
                    )
                else:
                    feedback_message = result["feedback"]
                    bg_color = (0, 100, 255)

                # Enregistrer la répétition dans la session
                if workout_session and result["count"] > workout_session.rep_count:
                    quality_score = (
                        posture_result["quality_score"] if posture_result else 50
                    )
                    angles = posture_result.get("angles", {}) if posture_result else {}
                    workout_session.add_repetition(quality_score, angles)

                    # Vérifier les encouragements
                    encouragement = feedback_generator.get_encouragement(
                        result["count"]
                    )
                    if encouragement:
                        feedback_message = encouragement

                # Enregistrer le feedback dans la session
                if workout_session and feedback:
                    workout_session.add_feedback(feedback)

                # Afficher le compteur sur la vidéo
                cv2.putText(
                    frame,
                    f"Reps: {result['count']}",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    3,
                )
                
                # Afficher l'exercice détecté sur la vidéo (seulement si visible)
                if is_visible:
                    cv2.putText(
                        frame,
                        f"{exercise_type}",
                        (frame.shape[1] - 250, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        2,
                    )

                # Afficher la qualité sur la vidéo
                if posture_result:
                    quality_text = f"Qualite: {posture_result['quality_score']:.0f}%"
                    cv2.putText(
                        frame,
                        quality_text,
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 0),
                        2,
                    )

                # Nettoyer le message pour OpenCV (supprimer les émojis et caractères spéciaux)
                # OpenCV ne gère pas bien l'UTF-8 par défaut
                clean_message = (
                    feedback_message.replace("⚠️", "!")
                    .replace("✅", "")
                    .replace("⬇️", "Bas")
                    .replace("⬆️", "Haut")
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("ê", "e")
                    .replace("à", "a")
                    .replace("ç", "c")
                    .strip()
                )
                
                # Afficher le feedback sur la vidéo
                frame = draw_text_with_background(
                    frame,
                    clean_message,
                    (20, frame.shape[0] - 30),
                    font_scale=0.8,
                    text_color=(255, 255, 255),
                    bg_color=bg_color,
                )

                # Convertir BGR vers RGB pour Streamlit
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(
                    frame_rgb, channels="RGB", width="stretch"
                )

                # Mettre à jour les métriques
                elapsed_time = int(time.time() - st.session_state.start_time)
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60

                count_container.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-value">{result["count"]}</div>
                        <div class="metric-label">Répétitions</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                # Afficher la qualité
                if posture_result:
                    quality_score = posture_result["quality_score"]
                    quality_category, quality_color = (
                        posture_analyzer.get_quality_category(quality_score)
                    )
                    quality_container.markdown(
                        f"""**Qualité :** <span style="color: {quality_color}; font-weight: bold;">{quality_category} ({quality_score:.0f}/100)</span>""",
                        unsafe_allow_html=True,
                    )

                phase_container.markdown(f"**Phase :** {result['phase']}")
                time_container.markdown(f"**Temps :** {minutes:02d}:{seconds:02d}")

                # Afficher les calories
                if workout_session:
                    calories = workout_session.get_calories_estimate()
                    calories_container.markdown(f"**Calories :** {calories} kcal")

                # Afficher le feedback
                if feedback:
                    feedback_class = get_feedback_class(feedback_message)
                    feedback_container.markdown(
                        f"""
                        <div class="feedback-box {feedback_class}">
                            {feedback_message}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # Statistiques de session
                stats = counter.get_stats()
                avg_quality = (
                    workout_session.get_average_quality() if workout_session else 0
                )

                stats_container.markdown(f"""
                    **📈 Résumé en direct**
                    - Total : {stats["total_reps"]} reps
                    - Qualité moyenne : {avg_quality:.1f}/100
                    - Calories : {workout_session.get_calories_estimate() if workout_session else 0} kcal
                """)

                # Délai minimal pour ne pas surcharger le CPU, mais fluide
                time.sleep(0.01)

        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
            st.session_state.session_active = False


if __name__ == "__main__":
    main()
