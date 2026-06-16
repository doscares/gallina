import os
import shutil
import random

print("🃏 Barajando y repartiendo el nuevo dataset...")

fallos_dir = "Dataset_Fallos"
train_img = "Dataset_Gallina/train/images"
train_lbl = "Dataset_Gallina/train/labels"
val_img = "Dataset_Gallina/val/images"
val_lbl = "Dataset_Gallina/val/labels"

# 1. Agrupar las imágenes válidas
archivos = os.listdir(fallos_dir)
imagenes = [f for f in archivos if f.endswith(('.jpg', '.png'))]

pares_validos = []
for img in imagenes:
    base = img.rsplit('.', 1)[0]
    txt = base + ".txt"
    if txt in archivos:
        pares_validos.append((img, txt))

# 2. Mezclar al azar para que el examen sea justo
random.shuffle(pares_validos)

# 3. Calcular el 80%
limite = int(len(pares_validos) * 0.8)
train_set = pares_validos[:limite]
val_set = pares_validos[limite:]

# 4. Mover a las carpetas
def mover_set(dataset, dest_img, dest_lbl):
    for img, txt in dataset:
        shutil.move(os.path.join(fallos_dir, img), os.path.join(dest_img, img))
        shutil.move(os.path.join(fallos_dir, txt), os.path.join(dest_lbl, txt))

mover_set(train_set, train_img, train_lbl)
mover_set(val_set, val_img, val_lbl)

print(f"✅ ¡Listo! {len(train_set)} pares enviados a TRAIN y {len(val_set)} pares enviados a VAL.")