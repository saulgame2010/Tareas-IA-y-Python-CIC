# Tarea 3: Detección de rostros con OpenCV - Saúl García Medina

import cv2
from datetime import datetime
import os


CARPETA_SALIDA = "tarea_3_opencv_rostros/rostros_recortados"


def crear_carpeta_salida():
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)


def generar_nombre_archivo():
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"rostro_{fecha_actual}.png"


def main():
    crear_carpeta_salida()

    detector_rostros = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    print("Presiona 's' para guardar el rostro detectado.")
    print("Presiona 'q' para salir.")

    while True:
        ret, frame = camara.read()

        if not ret:
            print("No se pudo leer la imagen de la cámara.")
            break

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rostros = detector_rostros.detectMultiScale(
            gris,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in rostros:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Deteccion de rostros - OpenCV", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("s"):
            if len(rostros) > 0:
                x, y, w, h = rostros[0]

                rostro_recortado = frame[y:y + h, x:x + w]

                nombre_archivo = generar_nombre_archivo()
                ruta_archivo = os.path.join(CARPETA_SALIDA, nombre_archivo)

                cv2.imwrite(ruta_archivo, rostro_recortado)

                print(f"Rostro guardado en: {ruta_archivo}")
            else:
                print("No se detectó ningún rostro para guardar.")

        elif tecla == ord("q"):
            break

    camara.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()