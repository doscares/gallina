from ultralytics import YOLO
import cv2
import os

print("🧠 Iniciando Test Visual del Modelo (Versión DEBUG 2.0)...")

# --- PASO 1: VERIFICAR ARCHIVOS ---
ruta_modelo = "best.pt"
carpeta_fallos = "Dataset_Fallos"

if not os.path.exists(ruta_modelo):
    print(f"❌ ERROR CRÍTICO: No encuentro '{ruta_modelo}' en la carpeta actual.")
    exit()

if not os.path.exists(carpeta_fallos):
    print(f"❌ ERROR: No se encontró la carpeta {carpeta_fallos}.")
    exit()

archivos = os.listdir(carpeta_fallos)
imagenes = [f for f in archivos if f.endswith(('.jpg', '.png'))]

if len(imagenes) == 0:
    print("❌ No hay imágenes en Dataset_Fallos para probar.")
    exit()

# --- PASO 2: CARGAR MODELO Y PREGUNTARLE QUÉ SABE ---
modelo = YOLO(ruta_modelo)

# En lugar de forzarlo, le pedimos que nos confiese qué diccionario tiene guardado
print(f"\n📚 DICCIONARIO INTERNO DE LA IA: {modelo.names}\n")

# --- PASO 3: ANALIZAR IMAGEN ---
# Buscamos la primera imagen 
ruta_img = os.path.join(carpeta_fallos, imagenes[0])
print(f"📸 Analizando imagen con súper-baja confianza (0.05): {ruta_img}")

resultados = modelo(ruta_img, conf=0.05, verbose=False)[0]

# --- PASO 4: IMPRIMIR RESULTADOS EN CONSOLA (DEBUG) ---
if len(resultados.boxes) == 0:
    print("❌ El modelo no detectó ABSOLUTAMENTE NADA (ni con conf 0.05).")
    print("Esto significa que el entrenamiento no tuvo impacto o el dataset fue muy pequeño.")
else:
    print(f"✅ Detectados {len(resultados.boxes)} objetos potenciales.")
    for box in resultados.boxes:
        cls_id = int(box.cls[0].item())
        conf_val = float(box.conf[0].item())
        nombre_clase = modelo.names.get(cls_id, f"Desconocido_{cls_id}")
        # Mostramos lo que ve la IA en la terminal
        print(f"   Veo: '{nombre_clase}' con ID: {cls_id} (Seguridad: {conf_val:.4f})")

# --- PASO 5: DIBUJAR Y MOSTRAR ---
imagen_dibujada = resultados.plot()
cv2.imshow("TEST VISUAL DE SEGURIDAD", imagen_dibujada)

print("\nPresiona cualquier tecla en la ventana de la foto para cerrar.")
cv2.waitKey(0)
cv2.destroyAllWindows()