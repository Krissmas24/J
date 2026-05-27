import tkinter as tk
import math
from ui.theme import Theme

class SplashScreen:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.configure(bg=Theme.BG)
        
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 400, 500
        self.win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self.canvas = tk.Canvas(self.win, bg=Theme.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.angle = 0
        self.animate()
        self.win.after(3000, self.finish)

    def animate(self):
        if not self.win.winfo_exists(): return
        self.canvas.delete("all")
        
        w, h = 400, 500
        cx, cy, r = w//2, h//2 - 20, 100
        
        self.angle += 0.05
        rotation = self.angle * 180 / math.pi
        
        # Yin-Yang Base
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=Theme.FG, outline=Theme.ACCENT, width=2)
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=rotation, extent=180, fill=Theme.BG, outline="")
        
        # Eyes
        r2 = r / 2
        ex1 = cx + (r2 * math.cos(self.angle))
        ey1 = cy + (r2 * math.sin(self.angle))
        ex2 = cx - (r2 * math.cos(self.angle))
        ey2 = cy - (r2 * math.sin(self.angle))
        
        self.canvas.create_oval(ex1-r2, ey1-r2, ex1+r2, ey1+r2, fill=Theme.BG, outline="")
        self.canvas.create_oval(ex2-r2, ey2-r2, ex2+r2, ey2+r2, fill=Theme.FG, outline="")
        
        # Pupils
        r3 = r / 6
        self.canvas.create_oval(ex1-r3, ey1-r3, ex1+r3, ey1+r3, fill=Theme.ACCENT, outline="")
        self.canvas.create_oval(ex2-r3, ey2-r3, ex2+r3, ey2+r3, fill=Theme.ACCENT, outline="")
        
        # Text
        self.canvas.create_text(cx, cy + r + 50, text="J - REBIRTH", font=Theme.FONT_TITLE, fill=Theme.ACCENT)
        self.canvas.create_text(cx, cy + r + 80, text="INITIALIZING NEURAL LINK...", font=Theme.FONT_MAIN, fill=Theme.FG)
        
        self.win.after(20, self.animate)

    def finish(self):
        self.win.destroy()
        self.on_complete()
