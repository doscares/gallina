import os

def arreglar_nombres(carpeta):
    if not os.path.exists(carpeta):
        return
    
    contador = 0
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".xml.txt"):
            viejo = os.path.join(carpeta, archivo)
            # Le quitamos el ".xml" al nombre
            nuevo = os.path.join(carpeta, archivo.replace(".xml.txt", ".txt"))
            os.rename(viejo, nuevo)
            contador += 1
            
    print(f"✅ Se arreglaron {contador} archivos en {carpeta}")

# Apuntamos a tus dos carpetas de etiquetas
arreglar_nombres("Dataset_Gallina/train/labels")
arreglar_nombres("Dataset_Gallina/val/labels")