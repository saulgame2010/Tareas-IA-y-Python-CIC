# Tarea 4: Detección de manos con MediaPipe - Saúl García Medina

import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Ruta del modelo moderno de MediaPipe Tasks
MODELO_MANOS = "models/hand_landmarker.task"

# Coordenadas del cuadrado fijo
CUADRADO_X1 = 220
CUADRADO_Y1 = 120
CUADRADO_X2 = 420
CUADRADO_Y2 = 320


def punto_dentro_cuadrado(x, y):
    return CUADRADO_X1 <= x <= CUADRADO_X2 and CUADRADO_Y1 <= y <= CUADRADO_Y2


def dibujar_landmarks(frame, landmarks_mano, ancho, alto):
    """
    Dibuja manualmente los puntos y conexiones de la mano.
    Esto evita usar mp.solutions.drawing_utils.
    """

    conexiones = [
        (0, 1), (1, 2), (2, 3), (3, 4),          # Pulgar
        (0, 5), (5, 6), (6, 7), (7, 8),          # Índice
        (5, 9), (9, 10), (10, 11), (11, 12),     # Medio
        (9, 13), (13, 14), (14, 15), (15, 16),   # Anular
        (13, 17), (17, 18), (18, 19), (19, 20),  # Meñique
        (0, 17)
    ]

    puntos = []

    for landmark in landmarks_mano:
        x = int(landmark.x * ancho)
        y = int(landmark.y * alto)
        puntos.append((x, y))

    for inicio, fin in conexiones:
        cv2.line(frame, puntos[inicio], puntos[fin], (255, 255, 255), 2)

    for punto in puntos:
        cv2.circle(frame, punto, 4, (0, 255, 255), -1)


def crear_detector_manos():
    base_options = python.BaseOptions(model_asset_path=MODELO_MANOS)

    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.7,
        min_tracking_confidence=0.7
    )

    return vision.HandLandmarker.create_from_options(options)


def main():
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    detector_manos = crear_detector_manos()

    print("Presiona 'q' para salir.")

    while True:
        ret, frame = camara.read()

        if not ret:
            print("No se pudo leer la cámara.")
            break

        frame = cv2.flip(frame, 1)
        alto, ancho, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        timestamp_ms = int(time.time() * 1000)

        resultado = detector_manos.detect_for_video(mp_image, timestamp_ms)

        tocando_cuadrado = False

        if resultado.hand_landmarks:
            for landmarks_mano in resultado.hand_landmarks:
                dibujar_landmarks(frame, landmarks_mano, ancho, alto)

                # Landmark 8 = punta del dedo índice
                dedo_indice = landmarks_mano[8]

                x_indice = int(dedo_indice.x * ancho)
                y_indice = int(dedo_indice.y * alto)

                cv2.circle(frame, (x_indice, y_indice), 10, (255, 0, 0), -1)

                if punto_dentro_cuadrado(x_indice, y_indice):
                    tocando_cuadrado = True

        if tocando_cuadrado:
            color_cuadrado = (0, 255, 0)
            texto = "TOCANDO EL CUADRADO"
        else:
            color_cuadrado = (0, 0, 255)
            texto = "Mueve el dedo indice al cuadrado"

        cv2.rectangle(
            frame,
            (CUADRADO_X1, CUADRADO_Y1),
            (CUADRADO_X2, CUADRADO_Y2),
            color_cuadrado,
            3
        )

        cv2.putText(
            frame,
            texto,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color_cuadrado,
            2
        )

        cv2.imshow("Deteccion de manos con MediaPipe Tasks", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            break

    detector_manos.close()
    camara.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()