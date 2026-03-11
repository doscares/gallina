import cv2
import numpy as np
import mss

def mouse_click(event, x, y, flags, param):
    """Detecta el clic del mouse y extrae el color exacto del píxel."""
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param
        
        # Obtener el color BGR del píxel exacto donde hiciste clic
        bgr_color = frame[y, x]
        
        # Convertir ese único píxel a HSV
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # Calcular rangos sugeridos (con un margen de tolerancia)
        h, s, v = hsv_color
        lower_bound = [max(0, h - 10), max(50, s - 50), max(50, v - 50)]
        upper_bound = [min(179, h + 10), 255, 255]
        
        print(f"\n--- CLIC EN COORDENADA (X:{x}, Y:{y}) ---")
        print(f"Color Exacto HSV: {hsv_color}")
        print(f"-> Copia esto en vision.py (LOWER): np.array({lower_bound})")
        print(f"-> Copia esto en vision.py (UPPER): np.array({upper_bound})")
        print("-" * 40)

def start_calibration():
    sct = mss.mss()
    # ¡OJO! Debe ser la misma región de captura que pusiste en vision.py
    monitor = {"top": 100, "left": 100, "width": 800, "height": 600}
    
    window_name = "Calibrador de Vision - Presiona 'q' para salir"
    cv2.namedWindow(window_name)
    
    print("Calibrador iniciado. Haz clic en el fuego o los autos de la ventana emergente.")
    
    while True:
        # Captura en tiempo real
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Pasamos el frame actual a la función del mouse
        cv2.setMouseCallback(window_name, mouse_click, param=frame)
        
        # Mostrar la ventana
        cv2.imshow(window_name, frame)
        
        # Si presionas la tecla 'q', se cierra
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_calibration()