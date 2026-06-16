import os
import glob

carpeta = "Dataset_Fallos"
clases_validas = ["gallina", "auto", "fuego"]

def sanitizar_dataset():
    ruta_classes = os.path.join(carpeta, "classes.txt")
    
    # 1. Reescribir classes.txt de forma perfecta y blindada
    with open(ruta_classes, "w", encoding="utf-8") as f:
        f.write("\n".join(clases_validas))
    print("📝 Archivo classes.txt reescrito correctamente.")

    # 2. Escanear y limpiar todos los .txt de la IA
    archivos_txt = glob.glob(os.path.join(carpeta, "*.txt"))
    
    for txt in archivos_txt:
        if "classes.txt" in txt:
            continue
            
        with open(txt, "r") as f:
            lineas = f.readlines()
            
        lineas_limpias = []
        for linea in lineas:
            partes = linea.strip().split()
            if len(partes) >= 5:
                try:
                    clase_id = int(partes[0])
                    # Si el número de clase es mayor a 2, es una alucinación y lo borramos
                    if clase_id < len(clases_validas):
                        lineas_limpias.append(linea)
                    else:
                        print(f"👻 ¡Bug de IA detectado! Clase fantasma '{clase_id}' eliminada de {os.path.basename(txt)}")
                except ValueError:
                    pass
                    
        # Sobreescribir el archivo solo con las coordenadas sanas
        with open(txt, "w") as f:
            f.writelines(lineas_limpias)
            
    print("✅ ¡Dataset sanitizado! Ya es a prueba de crasheos.")

if __name__ == "__main__":
    sanitizar_dataset()