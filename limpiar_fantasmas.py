import os

print("👻 Iniciando protocolo de exterminio de archivos .xml.txt...")

# Las carpetas donde el enemigo podría estar escondido
carpetas_sospechosas = [
    "Dataset_Fallos", 
    "Dataset_Gallina/train/labels",
    "Dataset_Gallina/val/labels"
]

total_arreglados = 0

for carpeta in carpetas_sospechosas:
    if not os.path.exists(carpeta):
        continue
        
    arreglados_aqui = 0
    for archivo in os.listdir(carpeta):
        # Buscamos la firma del archivo fantasma
        if archivo.endswith(".xml.txt") or archivo.endswith(".xml"):
            ruta_vieja = os.path.join(carpeta, archivo)
            
            # Limpiamos el nombre para que quede un .txt puro
            nuevo_nombre = archivo.replace(".xml.txt", ".txt").replace(".xml", ".txt")
            ruta_nueva = os.path.join(carpeta, nuevo_nombre)
            
            # Renombramos el archivo
            os.rename(ruta_vieja, ruta_nueva)
            arreglados_aqui += 1
            total_arreglados += 1
            
    if arreglados_aqui > 0:
        print(f"✅ Se curaron {arreglados_aqui} archivos en: {carpeta}")

print(f"\n🎉 ¡Operación exitosa! {total_arreglados} fantasmas eliminados en total.")
print("Ya puedes continuar con el entrenamiento.")