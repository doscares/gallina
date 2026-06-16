import os
import shutil
import random

# Configuración de rutas
origen = "Dataset_Fallos"
destino_base = "Dataset_Gallina"
porcentaje_train = 0.8  # 80% para train, 20% para val

def organizar_archivos():
    # 1. Asegurar que la estructura de carpetas exista
    estructuras = [
        'train/images', 'train/labels',
        'val/images', 'val/labels'
    ]
    for est in estructuras:
        os.makedirs(os.path.join(destino_base, est), exist_ok=True)

    # 2. Buscar todas las imágenes válidas en Dataset_Fallos
    imagenes = [f for f in os.listdir(origen) if f.endswith(('.jpg', '.png'))]
    
    # Mezclar las fotos para que el reparto sea aleatorio y equilibrado
    random.shuffle(imagenes)

    # Calcular el punto de corte (80%)
    corte = int(len(imagenes) * porcentaje_train)
    
    print(f"📦 Detectadas {len(imagenes)} imágenes nuevas corregidas.")
    print(f"🔄 Repartiendo: {corte} a 'train' y {len(imagenes) - corte} a 'val'...")

    for indice, img_name in enumerate(imagenes):
        base_name = img_name.rsplit('.', 1)[0]
        txt_name = base_name + ".txt"
        
        # Definir destino según el índice
        subcarpeta = "train" if indice < corte else "val"
        
        # Rutas de origen
        ruta_img_origen = os.path.join(origen, img_name)
        ruta_txt_origen = os.path.join(origen, txt_name)
        
        # Rutas de destino
        ruta_img_destino = os.path.join(destino_base, subcarpeta, "images", img_name)
        ruta_txt_destino = os.path.join(destino_base, subcarpeta, "labels", txt_name)

        # Mover la imagen
        if os.path.exists(ruta_img_origen):
            shutil.move(ruta_img_origen, ruta_img_destino)
            
        # Mover el .txt correspondiente
        if os.path.exists(ruta_txt_origen):
            shutil.move(ruta_txt_origen, ruta_txt_destino)

    print("🚀 ¡Todo el dataset fue clasificado, separado y movido automáticamente con éxito!")

if __name__ == "__main__":
    organizar_archivos()