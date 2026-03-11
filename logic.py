import time

class GameLogic:
    def __init__(self):
        self.LANE_WIDTH = 142 
        self.BTN_AVANZAR_X = 350 
        self.BTN_AVANZAR_Y = 460 
        
        self.fire_was_active = False
        self.last_fire_time = 0
        self.FIRE_COOLDOWN = 0.5 
        
        self.safe_since = None
        self.SAFETY_DELAY = 2.0 # Segundos de espera perfectos

    def analyze_situation(self, chicken_pos, fire_positions, threat_positions):
        if chicken_pos is None:
            self.safe_since = None
            return "ESPERANDO JUEGO...", "", "gray", "gray", False, None, None, None, None

        cx, cy, cw, ch = chicken_pos
        chicken_center_x = cx + int(cw / 2)
        chicken_center_y = cy + int(ch / 2)
        
        target_lane_x = chicken_center_x + self.LANE_WIDTH
        
        # 1. Hitbox de Fuego (Cuadrado Celeste/Azul abajo)
        fire_box = (target_lane_x - 40, chicken_center_y + 10, 
                    target_lane_x + 40, chicken_center_y + 90)
        
        # 2. Hitbox de Autos (Cuadrado Rojo arriba, como en Guitar Hero)
        car_box = (target_lane_x - 35, chicken_center_y - 120, 
                   target_lane_x + 35, chicken_center_y - 30)
        
        # --- DETECCIÓN DE COLISIONES ESTILO GUITAR HERO ---
        car_danger = False
        for (tx, ty, tw, th) in threat_positions:
            tcx = tx + int(tw / 2)
            tcy = ty + int(th / 2)
            # ¿El centro del auto está dentro del cuadrado rojo?
            if (car_box[0] < tcx < car_box[2]) and (car_box[1] < tcy < car_box[3]):
                car_danger = True
                break

        lane_fire_active = False
        for (fx, fy, fw, fh) in fire_positions:
            fcx = fx + int(fw / 2)
            fcy = fy + int(fh / 2)
            # ¿El fuego está dentro del cuadrado celeste?
            if (fire_box[0] < fcx < fire_box[2]) and (fire_box[1] < fcy < fire_box[3]):
                lane_fire_active = True
                break

        # Cooldown del fuego
        current_time = time.time()
        fire_danger = False
        if lane_fire_active:
            self.fire_was_active = True
            self.last_fire_time = current_time
            fire_danger = True
        else:
            if self.fire_was_active:
                if current_time - self.last_fire_time > self.FIRE_COOLDOWN:
                    self.fire_was_active = False 
                else:
                    fire_danger = True 

        # --- GESTIÓN DE TEXTOS SEPARADOS ---
        main_text = ""
        main_color = ""
        sub_text = ""
        sub_color = ""
        is_ready_to_click = False

        if car_danger and fire_danger:
            main_text = "ESPERA"
            main_color = "red"
            sub_text = "Causa: FUEGO Y AUTO"
            sub_color = "red"
            self.safe_since = None
        elif car_danger:
            main_text = "ESPERA"
            main_color = "red"
            sub_text = "Causa: AUTO"
            sub_color = "orange"
            self.safe_since = None
        elif fire_danger:
            main_text = "ESPERA"
            main_color = "red"
            sub_text = "Causa: FUEGO"
            sub_color = "orange"
            self.safe_since = None
        else:
            # Temporizador de 2 a 3 segundos
            if self.safe_since is None:
                self.safe_since = current_time

            time_passed = current_time - self.safe_since
            if time_passed >= self.SAFETY_DELAY:
                main_text = "AVANZA"
                main_color = "green"
                sub_text = "VÍA LIBRE"
                sub_color = "green"
                is_ready_to_click = True
            else:
                countdown = round(self.SAFETY_DELAY - time_passed, 1)
                main_text = "ESPERA"
                main_color = "orange"
                sub_text = f"Seguro en: {countdown}s"
                sub_color = "orange"

        return main_text, sub_text, main_color, sub_color, is_ready_to_click, self.BTN_AVANZAR_X, self.BTN_AVANZAR_Y, car_box, fire_box