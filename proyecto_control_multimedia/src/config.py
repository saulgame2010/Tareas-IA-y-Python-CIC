# Esta es la configuración de constantes que nos ayudarán a centralizar valores que se utilizan en varias partes del proyecto.

from pathlib import Path


# =========================
# RUTAS DEL PROYECTO
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "hand_landmarker.task"


# =========================
# CONFIGURACIÓN DE CÁMARA
# =========================

CAMERA_INDEX = 0
WINDOW_NAME = "Control multimedia por gestos"

FRAME_WIDTH = 960
FRAME_HEIGHT = 720


# =========================
# CONFIGURACIÓN DE MEDIAPIPE
# =========================

NUM_HANDS = 1
MIN_HAND_DETECTION_CONFIDENCE = 0.7
MIN_HAND_PRESENCE_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7


# =========================
# COLORES BGR - OpenCV, como se nos explicó en clase, OpenCV usa el formato BGR en lugar de RGB, así que definimos los colores en ese formato para usarlos fácilmente en el proyecto.
# =========================

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_GRAY = (80, 80, 80)


# =========================
# BOTONES VIRTUALES
# =========================

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 90
BUTTON_Y = 560

BUTTONS_CONFIG = [
    {
        "label": "ANT",
        "action": "previous",
        "x": 70,
        "y": BUTTON_Y,
    },
    {
        "label": "PLAY",
        "action": "play_pause",
        "x": 245,
        "y": BUTTON_Y,
    },
    {
        "label": "SIG",
        "action": "next",
        "x": 420,
        "y": BUTTON_Y,
    },
    {
        "label": "VOL-",
        "action": "volume_down",
        "x": 595,
        "y": BUTTON_Y,
    },
    {
        "label": "VOL+",
        "action": "volume_up",
        "x": 770,
        "y": BUTTON_Y,
    },
]


# =========================
# CONTROL DE ACTIVACIÓN
# =========================

# Evita que una acción se ejecute muchas veces por segundo
ACTION_COOLDOWN_SECONDS = 1.0