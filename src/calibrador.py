import os
import json
import tkinter as tk
import pyautogui
from PIL import ImageTk


class Coordenadas:
    def __init__(self, ruta_base="."):
        self.config_file = os.path.join(ruta_base, "config_botones.json")
        self.apostar = (660, 450)
        self.avanzar = (661, 524)
        self.cargados = False

    def cargar(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file) as f:
                    data = json.load(f)
                self.apostar = tuple(data["apostar"])
                self.avanzar = tuple(data["avanzar"])
                self.cargados = True
                return True
            except Exception:
                pass
        return False

    def guardar(self):
        with open(self.config_file, "w") as f:
            json.dump({"apostar": list(self.apostar), "avanzar": list(self.avanzar)}, f, indent=2)


class CalibradorUI:
    def __init__(self, coords: Coordenadas, parent=None):
        self.coords = coords
        self.resultado = False
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
        self.root.title("Calibrar Botones - Gallina AI")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        screenshot = pyautogui.screenshot()
        self.bg_photo = ImageTk.PhotoImage(screenshot)

        self.canvas = tk.Canvas(self.root, width=screen_w, height=screen_h, highlightthickness=0, cursor="crosshair")
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.canvas.create_text(screen_w // 2, 25, text="Arrastra cada rectángulo sobre su botón en el juego",
                                font=("Arial", 18, "bold"), fill="lime")

        ax, ay = self.coords.apostar
        self._crear_grupo(ax, ay, "APOSTAR / RETIRAR", "#3498DB", "apostar")

        vx, vy = self.coords.avanzar
        self._crear_grupo(vx, vy, "AVANZAR", "#2ECC71", "avanzar")

        btn_listo = tk.Button(self.root, text="LISTO - EMPEZAR A JUGAR",
                              command=self._confirmar, font=("Arial", 12, "bold"),
                              bg="#2ECC71", fg="white", padx=30, pady=8, cursor="hand2")
        self.canvas.create_window(screen_w // 2, screen_h - 40, window=btn_listo)

        self.drag_tag = None
        self.drag_x0 = 0
        self.drag_y0 = 0

        self.canvas.tag_bind("arrastrable", "<Button-1>", self._iniciar)
        self.canvas.tag_bind("arrastrable", "<B1-Motion>", self._mover)
        self.canvas.tag_bind("arrastrable", "<ButtonRelease-1>", self._soltar)

        self.root.protocol("WM_DELETE_WINDOW", self._cerrar)
        self.root.bind("<Escape>", lambda e: self._cerrar())

    def _crear_grupo(self, cx, cy, texto, color, tag):
        w, h = 80, 40
        x1, y1 = cx - w // 2, cy - h // 2
        x2, y2 = cx + w // 2, cy + h // 2
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=4, fill="", tags=(tag, "arrastrable"))
        self.canvas.create_text(cx, cy, text=texto, fill=color, font=("Arial", 10, "bold"),
                                tags=(tag, "arrastrable"))
        self.canvas.create_text(cx, y2 + 14, text="▼", fill=color, font=("Arial", 16, "bold"),
                                tags=(tag, "arrastrable"))

    def _iniciar(self, event):
        items = self.canvas.find_closest(event.x, event.y)
        for item in items:
            tags = self.canvas.gettags(item)
            for t in tags:
                if t in ("apostar", "avanzar"):
                    self.drag_tag = t
                    self.drag_x0 = event.x
                    self.drag_y0 = event.y
                    return

    def _mover(self, event):
        if self.drag_tag is None:
            return
        dx = event.x - self.drag_x0
        dy = event.y - self.drag_y0
        self.canvas.move(self.drag_tag, dx, dy)
        self.drag_x0 = event.x
        self.drag_y0 = event.y

    def _soltar(self, event):
        self.drag_tag = None

    def _confirmar(self):
        for tag in ("apostar", "avanzar"):
            bbox = self.canvas.bbox(tag)
            if bbox:
                cx = (bbox[0] + bbox[2]) // 2
                cy = (bbox[1] + bbox[3]) // 2
                if tag == "apostar":
                    self.coords.apostar = (cx, cy)
                else:
                    self.coords.avanzar = (cx, cy)
        self.coords.guardar()
        self.resultado = True
        self.root.destroy()

    def _cerrar(self):
        self.resultado = False
        self.root.destroy()

    def mostrar(self):
        self.root.mainloop()
        return self.resultado
