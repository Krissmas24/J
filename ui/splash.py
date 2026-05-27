import tkinter as tk
import math
import random
import time
from ui.theme import Theme

class Particle:
    def __init__(self, x, y, color, canvas, floor_y):
        self.x = x
        self.y = y
        self.color = color
        self.canvas = canvas
        self.floor_y = floor_y
        
        # Initial pulse outwards
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        self.gravity = 0.35
        self.friction = 0.7
        self.radius = random.randint(2, 4)
        self.id = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill=color, outline="")
        self.alive = True

    def update(self):
        if not self.alive: return
        
        # Apply physics
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        
        # Floor collision
        if self.y + self.radius >= self.floor_y:
            self.y = self.floor_y - self.radius
            self.vy = -self.vy * self.friction
            self.vx *= self.friction
            
            # Stop if movement is tiny
            if abs(self.vy) < 0.5 and abs(self.vx) < 0.5:
                self.alive = False

        self.canvas.coords(self.id, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)

class SplashScreen:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.configure(bg=Theme.DARK_GREY)
        
        # 3:5 Aspect Ratio
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.w = 360
        self.h = 600
        self.win.geometry(f"{self.w}x{self.h}+{(sw-self.w)//2}+{(sh-self.h)//2}")
        
        self.canvas = tk.Canvas(self.win, bg=Theme.DARK_GREY, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.start_time = time.time()
        self.duration = 5.0
        self.particles = []
        self.yy_size = 60.0
        self.yy_target_size = 120.0
        self.hatching_phase = 0 # 0: Hatching up, 1: Pulsing/Exploding, 2: Deflating
        self.dots_emitted = False
        
        self.animate()

    def draw_split_j(self, x, y):
        # Splatter effect (random polygons for "splat")
        random.seed(42) # Consistent splatter
        for _ in range(12):
            sx = x + random.randint(-60, 60)
            sy = y + random.randint(-60, 60)
            sr = random.randint(5, 25)
            # Inverted logic: where J is white (bottom), splash is black. Where J is black (top), splash is white.
            color = Theme.BLACK if sy > y else Theme.FG
            self.canvas.create_oval(sx-sr, sy-sr, sx+sr, sy+sr, fill=color, outline="")

        # Italic J split color
        # Top half (Black)
        self.canvas.create_text(x, y, text="J", font=Theme.FONT_LOGO, fill=Theme.BLACK, anchor="center")
        # Mask bottom half
        self.canvas.create_rectangle(x-100, y, x+100, y+100, fill=Theme.DARK_GREY, outline="")
        # Bottom half (White)
        self.canvas.create_text(x, y, text="J", font=Theme.FONT_LOGO, fill=Theme.FG, anchor="center")
        # Mask top half
        self.canvas.create_rectangle(x-100, y-100, x+100, y, fill=Theme.DARK_GREY, outline="")

    def draw_yin_yang(self, cx, cy, r, alpha=1.0):
        # Dullness logic (50% dullness = greyish/transparent)
        fg = Theme.FG if alpha > 0.5 else "#888888"
        bg = Theme.BLACK if alpha > 0.5 else "#333333"
        accent = Theme.ACCENT if alpha > 0.5 else "#997A00"

        # Main circles
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=fg, outline=accent, width=2)
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=90, extent=180, fill=bg, outline="")
        
        # Eyes
        r2 = r / 2
        self.canvas.create_oval(cx-r2, cy-r-r2, cx+r2, cy-r+r2, fill=fg, outline="") # Needs adjustment for center
        # Simplified eyes for procedural animation
        self.canvas.create_oval(cx-r2/2, cy-r2-r2/2, cx+r2/2, cy-r2+r2/2, fill=bg, outline="")
        self.canvas.create_oval(cx-r2/2, cy+r2-r2/2, cx+r2/2, cy+r2+r2/2, fill=fg, outline="")

    def animate(self):
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.finish()
            return

        self.canvas.delete("all")
        
        # Draw Version (Bottom Left)
        self.canvas.create_text(10, self.h-10, text=Theme.VERSION, font=("Arial", 8), fill="#555555", anchor="sw")

        cx, cy = self.w // 2, self.h // 2
        
        # 1. Logo and Splat (Always there)
        self.draw_split_j(cx, cy - 100)

        # 2. Yin-Yang Hatching Logic
        # Time segments: 0-2s hatching, 2-3s pulse/dots, 3-5s deflate
        jitter = random.uniform(-2, 2)
        alpha = 1.0

        if elapsed < 2.0:
            # Hatching up: increase size with oscillation
            progress = elapsed / 2.0
            self.yy_size = 60 + (self.yy_target_size - 60) * progress + jitter
        elif elapsed < 3.0:
            # Pulse at Max Size
            self.yy_size = self.yy_target_size + random.uniform(-5, 5)
            if not self.dots_emitted:
                for _ in range(40):
                    color = random.choice([Theme.BLACK, Theme.FG])
                    self.particles.append(Particle(cx, cy + 100, color, self.canvas, self.h - 5))
                self.dots_emitted = True
        else:
            # Deflate: decrease size with oscillation and dullness
            progress = (elapsed - 3.0) / 2.0
            self.yy_size = self.yy_target_size - (self.yy_target_size - 60) * progress + jitter
            alpha = 0.5 # 50% dullness

        self.draw_yin_yang(cx, cy + 100, self.yy_size / 2, alpha)

        # 3. Particle Update
        for p in self.particles:
            p.update()

        self.win.after(20, self.animate)

    def finish(self):
        self.win.destroy()
        self.on_complete()
