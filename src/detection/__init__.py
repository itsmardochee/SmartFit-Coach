"""
Module de détection de pose et capture vidéo.
Gère la détection des points clés du corps en temps réel.
"""

from .video_capture import VideoCapture
from .pose_detector import PoseDetector

__all__ = ["VideoCapture", "PoseDetector"]
