import os

labels_dir = "Dataset_Gallina/train/labels"
images_dir = "Dataset_Gallina/train/images"

print("🧹 Iniciando purga de datos corruptos...")

eliminados = 0

if os.path.exists(labels_dir):
    for txt_name in os.listdir(labels_dir):
        if not txt_name.endswith(".txt"):
            continue
            
        txt_path = os.path.join(labels_dir, txt_name)
        
        # Leemos si el archivo tiene coordenadas adentro
        with open(txt_path, 'r') as f:
            lineas = f.readlines()
            
        # Si el archivo está vacío (la IA no vio nada), es basura
        if len(lineas) == 0:
            os.remove(txt_path)
            
            # Borramos la imagen correspondiente para que no quede huérfana
            img_base = txt_name.replace(".txt", "")
            for ext in [".jpg", ".png"]:
                img_path = os.path.join(images_dir, img_base + ext)
                if os.path.exists(img_path):
                    os.remove(img_path)
                    
            eliminados += 1

print(f"✅ Purga completada. Se eliminaron {eliminados} fotos y etiquetas vacías que estaban cegando a la IA.")