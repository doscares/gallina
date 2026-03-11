import cv2
import numpy as np
import mss
import pyautogui
import os

class VisionController:
    def __init__(self):
        screen_w, screen_h = pyautogui.size()
        self.monitor = {"top": 200, "left": 350, "width": screen_w - 350, "height": screen_h - 200}
        self.sct = None 

        ruta_gallina = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gallina.png')
        self.template_chicken = cv2.imread(ruta_gallina, cv2.IMREAD_GRAYSCALE)
        
        if self.template_chicken is None:
            print("🚨 ERROR: No se encontró 'gallina.png'.")
            self.chicken_w, self.chicken_h = 0, 0
        else:
            self.chicken_w, self.chicken_h = self.template_chicken.shape[::-1]

        # Fuego
        self.lower_fire = np.array([0, 150, 150]) 
        self.upper_fire = np.array([35, 255, 255]) 
        
        # Colores de Autos (Ignoramos grises y sombras)
        self.lower_blue = np.array([100, 150, 100])
        self.upper_blue = np.array([130, 255, 255])
        self.lower_green = np.array([40, 100, 100])
        self.upper_green = np.array([80, 255, 255])
        self.lower_yellow = np.array([15, 100, 100])
        self.upper_yellow = np.array([35, 255, 255])
        self.lower_red = np.array([0, 150, 100])
        self.upper_red = np.array([10, 255, 255])
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 30, 255])

    def capture_screen(self):
        if self.sct is None:
            self.sct = mss.mss()
        img = np.array(self.sct.grab(self.monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def get_object_positions(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        chicken_pos = None
        if self.template_chicken is not None:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, self.template_chicken, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= 0.70: 
                x, y = max_loc
                chicken_pos = (x + self.monitor["left"], y + self.monitor["top"], self.chicken_w, self.chicken_h)
                
        # Contornos de Fuego
        mask_fire = cv2.inRange(hsv, self.lower_fire, self.upper_fire)
        contours_fire, _ = cv2.findContours(mask_fire, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        fire_positions = [(cv2.boundingRect(c)[0] + self.monitor["left"], 
                           cv2.boundingRect(c)[1] + self.monitor["top"], 
                           cv2.boundingRect(c)[2], cv2.boundingRect(c)[3]) 
                          for c in contours_fire if cv2.contourArea(c) > 30]
        
        # Contornos de Autos
        mask_threats = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        mask_threats |= cv2.inRange(hsv, self.lower_green, self.upper_green)
        mask_threats |= cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        mask_threats |= cv2.inRange(hsv, self.lower_red, self.upper_red)
        mask_threats |= cv2.inRange(hsv, self.lower_white, self.upper_white)
        
        contours_threats, _ = cv2.findContours(mask_threats, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        threat_positions = [(cv2.boundingRect(c)[0] + self.monitor["left"], 
                             cv2.boundingRect(c)[1] + self.monitor["top"], 
                             cv2.boundingRect(c)[2], cv2.boundingRect(c)[3]) 
                            for c in contours_threats if cv2.contourArea(c) > 150]
        
        return chicken_pos, fire_positions, threat_positions