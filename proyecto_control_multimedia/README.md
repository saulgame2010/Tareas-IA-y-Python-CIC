# Control Multimedia por Gestos

Proyecto desarrollado en Python utilizando OpenCV y MediaPipe Tasks para controlar funciones multimedia mediante gestos de la mano detectados por cámara web.

## Descripción

La aplicación detecta la mano del usuario en tiempo real y utiliza la posición del dedo índice para interactuar con botones virtuales mostrados en pantalla.

Las acciones disponibles son:

- Play / Pause
- Siguiente canción
- Canción anterior
- Subir volumen
- Bajar volumen

## Tecnologías utilizadas

- Python 3
- OpenCV
- MediaPipe Tasks

## Arquitectura

El proyecto está dividido en módulos con responsabilidades específicas:

- `vision/`
  - Captura de cámara y detección de manos.

- `ui/`
  - Renderizado de interfaz y elementos visuales.

- `services/`
  - Control multimedia del sistema operativo.

- `domain/`
  - Modelos y lógica del dominio.

## Instalación

### Crear entorno virtual

```bash
python -m venv .venv
```

### Activar entorno virtual

Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## Dependencias adicionales Linux

```bash
sudo apt install playerctl
sudo apt install pulseaudio-utils
```

## Ejecutar proyecto

Entrar a la carpeta:

```bash
cd proyecto_control_multimedia
```

Ejecutar:

```bash
python3 main.py
```

## Funcionamiento

- La cámara detecta la mano del usuario.
- MediaPipe identifica los landmarks de la mano.
- Se rastrea la punta del dedo índice.
- Cuando el dedo entra en un botón virtual:
  - el botón cambia de color,
  - y se ejecuta la acción multimedia correspondiente.

## Características técnicas

- Detección de mano en tiempo real.
- Uso de MediaPipe Tasks API moderna.
- Arquitectura modular basada en POO.
- Separación de responsabilidades.
- Cooldown para evitar múltiples activaciones consecutivas.

## Autor

Proyecto desarrollado como parte del curso IA con Python.

Saúl García Medina
