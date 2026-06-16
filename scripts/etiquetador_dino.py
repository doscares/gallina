import os
from autodistill_grounding_dino import GroundingDINO
from autodistill.detection import CaptionOntology

def invocar_profesor():
    print("🧠 Despertando al Profesor DINO Expansivo en la RTX 4060...")
    
    # --- LA NUEVA ONTOLOGÍA (7 CLASES) ---
    # Diccionario: {"Lo que DINO busca en inglés": "La etiqueta que guardará para YOLO"}
    ontologia = CaptionOntology({
        "alive chicken": "gallina",
        "car": "auto",
        "fire": "fuego",
        "large victory popup banner with numbers": "victoria_cartel",
        "flattened squashed dead chicken": "muerte_aplastada",
        "roasted burnt black chicken": "muerte_quemada",
        "chicken falling into a dark hole": "muerte_caida"
    })

    modelo_maestro = GroundingDINO(ontology=ontologia)
    
    carpeta_entrada = "Dataset_Fallos"
    
    archivos_jpg = [f for f in os.listdir(carpeta_entrada) if f.endswith('.jpg')]
    if len(archivos_jpg) == 0:
        print(f"❌ No hay fotos '.jpg' en '{carpeta_entrada}'. ¡Deja al bot jugar y morir un rato primero!")
        return

    print(f"👀 Profesor DINO analizando {len(archivos_jpg)} situaciones extremas...")
    print("⏳ Etiquetando (Buscando victorias, quemaduras, caídas y atropellos)...")
    
    dataset = modelo_maestro.label(
        input_folder=carpeta_entrada,
        extension=".jpg",
        output_folder="Dataset_DINO_Limpio"
    )

    print("\n✅ ¡Etiquetado Multiclase Completado!")
    print("📁 Revisa 'Dataset_DINO_Limpio'. Ahora puedes ejecutar 'fusionar_dino.py' y entrenar.")

if __name__ == "__main__":
    invocar_profesor()