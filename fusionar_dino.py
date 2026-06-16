import os
import shutil

origen_base = "Dataset_DINO_Limpio"
destino_base = "Dataset_Gallina"
fallos_base = "Dataset_Fallos"

def fusionar_datasets():
    print("📦 Iniciando la fusión automática del conocimiento del Profesor DINO...")
    
    # Mapeo estratégico: Origen (Autodistill) -> Destino (Tu estructura YOLO)
    # Corregimos 'valid' para que se transforme en 'val' automáticamente
    mapeo = {
        "train/images": "train/images",
        "train/labels": "train/labels",
        "valid/images": "val/images",   
        "valid/labels": "val/labels"    
    }
    
    archivos_movidos = 0
    
    # 1. Mover los archivos de forma ordenada
    for sub_origen, sub_destino in mapeo.items():
        ruta_origen = os.path.join(origen_base, sub_origen)
        ruta_destino = os.path.join(destino_base, sub_destino)
        
        # Asegurar que las carpetas de destino existan
        os.makedirs(ruta_destino, exist_ok=True)
        
        if os.path.exists(ruta_origen):
            archivos = os.listdir(ruta_origen)
            for arch in archivos:
                shutil.move(
                    os.path.join(ruta_origen, arch),
                    os.path.join(ruta_destino, arch)
                )
                archivos_movidos += 1

    print(f"✅ ¡Éxito! Se han inyectado {archivos_movidos} archivos perfectos en '{destino_base}'.")
    
    # 2. LIMPIEZA TOTAL (Dejar la casa limpia para la siguiente ronda de juego)
    print("🗑️ Ejecutando limpieza de carpetas temporales...")
    
    # Eliminar la carpeta de salida de DINO ya procesada
    if os.path.exists(origen_base):
        shutil.rmtree(origen_base)
    
    # Vaciar Dataset_Fallos para que el bot empiece a recolectar fotos nuevas desde cero
    if os.path.exists(fallos_base):
        for arch in os.listdir(fallos_base):
            ruta_arch = os.path.join(fallos_base, arch)
            try:
                if os.path.isfile(ruta_arch) or os.path.islink(ruta_arch):
                    os.remove(ruta_arch)
                elif os.path.isdir(ruta_arch):
                    shutil.rmtree(ruta_arch)
            except Exception as e:
                print(f"⚠️ No se pudo borrar {arch}: {e}")
                
    print("🚀 ¡PROCESO COMPLETADO! Tu espacio de trabajo está limpio y reseteado.")

if __name__ == "__main__":
    # Validar que exista el origen antes de hacer nada
    if not os.path.exists(origen_base):
        print(f"❌ Error: No se encuentra la carpeta '{origen_base}'. ¿Corriste antes el etiquetador?")
    else:
        fusionar_datasets()