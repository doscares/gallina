import os

img_dir = "Dataset_Gallina/train/images"
lbl_dir = "Dataset_Gallina/train/labels"

print("🕵️‍♂️ Buscando imágenes sin etiquetas (Causantes de la ceguera)...")
eliminadas = 0

if os.path.exists(img_dir):
    for img_name in os.listdir(img_dir):
        if not img_name.endswith(('.jpg', '.png')):
            continue
            
        # Sacamos el nombre sin la extensión (.jpg o .png)
        base_name = img_name.rsplit('.', 1)[0]
        txt_path = os.path.join(lbl_dir, base_name + ".txt")
        
        # Si la imagen NO tiene su archivo .txt, la borramos sin piedad
        if not os.path.exists(txt_path):
            os.remove(os.path.join(img_dir, img_name))
            eliminadas += 1

print(f"✅ Cirugía completada. Se eliminaron {eliminadas} imágenes huérfanas.")
print("Tu dataset ha vuelto a su estado original de alta calidad.")