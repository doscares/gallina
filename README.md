# Gallina AI - Bot Autónomo con Auto-Aprendizaje

Bot que juega automáticamente y se re-entrena solo usando YOLOv8 + Grounding DINO.

## Requisitos

- Python 3.10+
- GPU NVIDIA con CUDA (recomendado)

## Instalación

```powershell
# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```powershell
# Activar el entorno virtual (si no lo está)
.venv\Scripts\activate

# Ejecutar el bot
python main.py
```

## Controles

| Tecla/Control | Función |
|---|---|
| `Ctrl+Ñ` | Activar/Pausar Auto-Play |
| `F9` | Capturar foto manual para dataset |
| Botón **AUTO-PLAY** | Inicia/Detiene el juego automático |
| Botón **SOLO JUGAR** | Juega sin capturar screens ni auto-entrenar |
| Botón **ENTRENAR IA** | Entrena la IA manualmente |

## Estructura del proyecto

```
gallina/
├── src/               # Código fuente del bot
│   ├── vision.py      # Detección por cámara (YOLO)
│   ├── logic.py       # Lógica de juego y decisiones
│   └── caja_negra.py  # Captura de evidencia en muerte
├── scripts/           # Utilidades
│   ├── entrenar.py    # Entrenamiento YOLO
│   ├── etiquetador_dino.py
│   ├── fusionar_dino.py
│   └── ...
├── assets/            # Imágenes del UI
├── main.py            # Punto de entrada
└── best.pt            # Pesos del modelo (generado)
```
