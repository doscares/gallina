import pyautogui
import time

print("🎯 Radar activado. Mueve el mouse para ver las coordenadas.")
print("Presiona 'Ctrl + C' en la terminal para salir.\n")

try:
    while True:
        # Obtiene la posición actual del mouse
        x, y = pyautogui.position()
        
        # Lo imprime en la misma línea para no llenar la pantalla
        print(f"Posición actual -> X: {x} | Y: {y}", end="\r")
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n\n✅ Radar apagado.")