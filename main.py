import tkinter as tk
from threading import Thread
import time
import pyautogui
import random
from vision import VisionController
from logic import GameLogic

pyautogui.FAILSAFE = False 

class AppUI:
    def __init__(self):
        self.vision = VisionController()
        self.logic = GameLogic()
        self.running = True
        self.auto_play = False
        
        self.root = tk.Tk()
        self.setup_gui()
        self.setup_overlay() 
        
        self.thread = Thread(target=self.run_bot, daemon=True)
        self.thread.start()
        
        self.root.mainloop()

    def setup_gui(self):
        self.root.title("Chicken AI VIP")
        self.root.attributes("-topmost", True)
        self.root.geometry("280x200") # Un poco más alto para el subtítulo
        
        # Texto Principal (AVANZA / ESPERA)
        self.lbl_status = tk.Label(self.root, text="INICIANDO...", font=("Arial", 24, "bold"))
        self.lbl_status.pack(pady=(10, 0))
        
        # Texto Secundario (Causa o Timer)
        self.lbl_reason = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.lbl_reason.pack(pady=(0, 10))
        
        self.btn_auto = tk.Button(self.root, text="AUTO-PLAY: OFF", command=self.toggle_auto, bg="#ff9933", fg="white", font=("Arial", 12, "bold"))
        self.btn_auto.pack(pady=5)
        
        tk.Button(self.root, text="CERRAR SCRIPT", command=self.close_app, bg="#ff4c4c", fg="white").pack(pady=5)

    def setup_overlay(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-topmost", True)
        self.overlay.attributes("-transparentcolor", "white")
        self.overlay.overrideredirect(True) 
        
        screen_w, screen_h = pyautogui.size()
        self.overlay.geometry(f"{screen_w}x{screen_h}+0+0")
        
        self.canvas = tk.Canvas(self.overlay, width=screen_w, height=screen_h, bg="white", highlightthickness=0)
        self.canvas.pack()
        
        self.rect_chicken = self.canvas.create_rectangle(0, 0, 0, 0, outline="#00FF00", width=3) 
        self.rect_fire_box = self.canvas.create_rectangle(0, 0, 0, 0, outline="#00FFFF", width=3) # Celeste
        self.rect_car_box = self.canvas.create_rectangle(0, 0, 0, 0, outline="#FF0000", width=3) # Rojo
        self.rect_btn = self.canvas.create_rectangle(0, 0, 0, 0, outline="#800080", width=3) 

    def update_overlay(self, chicken_pos, click_x, click_y, car_box, fire_box):
        if chicken_pos is None:
            self.canvas.coords(self.rect_chicken, 0, 0, 0, 0)
            self.canvas.coords(self.rect_fire_box, 0, 0, 0, 0)
            self.canvas.coords(self.rect_car_box, 0, 0, 0, 0)
            self.canvas.coords(self.rect_btn, 0, 0, 0, 0)
            return

        cx, cy, cw, ch = chicken_pos
        self.canvas.coords(self.rect_chicken, cx, cy, cx+cw, cy+ch)
            
        if car_box:
            cx1, cy1, cx2, cy2 = car_box
            self.canvas.coords(self.rect_car_box, cx1, cy1, cx2, cy2)
            
        if fire_box:
            fx1, fy1, fx2, fy2 = fire_box
            self.canvas.coords(self.rect_fire_box, fx1, fy1, fx2, fy2)

        if self.auto_play and click_x is not None:
            self.canvas.coords(self.rect_btn, click_x - 50, click_y - 20, click_x + 50, click_y + 20)
        else:
            self.canvas.coords(self.rect_btn, 0, 0, 0, 0)

    def toggle_auto(self):
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.btn_auto.config(text="AUTO-PLAY: ON", bg="#2ECC71")
        else:
            self.btn_auto.config(text="AUTO-PLAY: OFF", bg="#ff9933")

    def close_app(self):
        self.running = False
        self.root.destroy()

    def run_bot(self):
        time.sleep(1)
        while self.running:
            try:
                frame = self.vision.capture_screen() 
                chicken_pos, fire_positions, threat_positions = self.vision.get_object_positions(frame)
                
                main_txt, sub_txt, main_col, sub_col, is_ready, click_x, click_y, car_box, fire_box = self.logic.analyze_situation(chicken_pos, fire_positions, threat_positions)
                
                # Actualizar Textos Duales
                self.root.after(0, self.lbl_status.config, {"text": main_txt, "fg": main_col})
                self.root.after(0, self.lbl_reason.config, {"text": sub_txt, "fg": sub_col})
                
                self.root.after(0, self.update_overlay, chicken_pos, click_x, click_y, car_box, fire_box)
                
                if is_ready and self.auto_play and click_x is not None:
                    offset_x = random.randint(-15, 15) 
                    offset_y = random.randint(-5, 5)
                    
                    move_duration = random.uniform(0.15, 0.25)
                    pyautogui.moveTo(click_x + offset_x, click_y + offset_y, duration=move_duration, tween=pyautogui.easeInOutQuad)
                    pyautogui.click()
                    
                    time.sleep(random.uniform(0.7, 1.0)) 
                
                time.sleep(0.02) 
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    AppUI()