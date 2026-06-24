# gallina stake experimento IA

Bot autónomo que juega y se re-entrena solo usando YOLOv8 + Grounding DINO.

## Requisitos

- Python 3.10+
- GPU NVIDIA con CUDA (obligatorio, el programa verifica al iniciar)

## Opción 1: Ejecutable (más simple)

Genera el .exe con doble clic en `build.bat` (necesitas Python y CUDA instalados).

> **Descarga el .exe ya compilado:** [gallina.exe en Google Drive](https://drive.google.com/file/d/1EYU_tfq_Ess4Mfi5HQhynzUZMXDX1go2/view?usp=sharing) (~2.5GB)

## Opción 2: Desde código (Python)

```powershell
# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el bot
python main.py
```

## Calibración inicial (obligatorio la primera vez)

Al iniciar el programa por primera vez, se abre un calibrador **fullscreen** con una foto de tu pantalla y dos rectángulos arrastrables:

| Rectángulo | Color | Botón del juego |
|---|---|---|
| **APOSTAR / RETIRAR** | Azul | El botón para apostar fichas o retirar ganancias |
| **AVANZAR** | Verde | El botón para avanzar de carril |

1. Arrastra cada rectángulo con el mouse y colócalo exactamente sobre el botón correspondiente en la imagen de fondo
2. Presiona **"LISTO - EMPEZAR A JUGAR"**
3. Las coordenadas se guardan en `config_botones.json` para no tener que repetirlo

Si mueves la ventana del juego o cambias de monitor, puedes recalibrar en cualquier momento con el botón **🎯 Calibrar Botones** de la interfaz principal.

## Controles

| Tecla/Control | Función |
|---|---|
| `Ctrl+Ñ` | Activar/Pausar Auto-Play |
| `F9` | Capturar foto manual para dataset |
| Botón **AUTO-PLAY** | Inicia/Detiene el juego automático |
| Botón **SOLO JUGAR** | Juega sin capturar screens ni auto-entrenar |
| Botón **ENTRENAR IA** | Entrena la IA manualmente |
| Botón **🎯 Calibrar Botones** | Recalibrar la posición de los botones en pantalla |

## Funcionalidades

- **Calibrador visual de botones** — Al iniciar, muestra un overlay con la pantalla actual y dos rectángulos arrastrables para indicar dónde están los botones de "Apostar/Retirar" y "Avanzar". Las coordenadas se guardan y reutilizan.
- **Detector de GPU automático** — Verifica que el hardware sea compatible al iniciar. Si no detecta una GPU NVIDIA con CUDA, muestra las series compatibles y se cierra para proteger equipos de gama baja.
- **Solo Jugar** — Botón que desactiva la captura de screenshots y el auto-entrenamiento. Solo juega con lo ya aprendido. Al desactivarlo, vuelve al modo normal con captura y re-entrenamiento automático.
- **Auto-aprendizaje** — Cuando se acumulan suficientes fotos de fallos, la IA se re-entrena sola usando DINO para etiquetar y YOLO para aprender.

## Estructura del proyecto

```
gallina/
├── src/               # Código fuente del bot
│   ├── vision.py      # Detección por cámara (YOLO)
│   ├── logic.py       # Lógica de juego y decisiones
│   ├── calibrador.py  # Calibración visual de botones arrastrables
│   └── caja_negra.py  # Captura de evidencia en muerte
├── scripts/           # Utilidades
│   ├── entrenar.py    # Entrenamiento YOLO
│   ├── etiquetador_dino.py
│   ├── fusionar_dino.py
│   └── ...
├── assets/            # Imágenes del UI
├── dist/              # Ejecutable compilado
│   └── gallina.exe
├── main.py            # Punto de entrada
├── main.spec          # Configuración de PyInstaller
└── best.pt            # Pesos del modelo (generado)
```
