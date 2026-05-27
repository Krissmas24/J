import time
import threading
from core.vision import vision
from core.input import input_ctrl
from core.database import db

class MacroEngine:
    def __init__(self):
        self.is_running = False
        self.state = "IDLE"
        self.thread = None
        self.reeling_held = False
        self.callbacks = []

    def add_callback(self, cb):
        self.callbacks.append(cb)

    def log(self, message, level="INFO"):
        db.log_event(level, message)
        for cb in self.callbacks: cb(message)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.log("Macro started", "CORE")
            db.add_history("START", "Macro engine engaged")
            db.create_checkpoint({"state": "IDLE", "running": True})
            self.thread = threading.Thread(target=self.run_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        self.log("Macro stopped", "CORE")
        db.add_history("STOP", "Macro engine disengaged")
        db.create_checkpoint({"state": "IDLE", "running": False})
        if self.reeling_held:
            input_ctrl.release()
            self.reeling_held = False

    def run_loop(self):
        last_cast = 0
        while self.is_running:
            try:
                target = vision.get_sober_window()
                if not target:
                    self.log("Waiting for Sober window...", "WARN")
                    time.sleep(2)
                    continue

                wx, wy = target["at"]
                ww, wh = target["size"]

                if self.state == "IDLE":
                    self.log("Casting line...")
                    input_ctrl.click(wx + ww//2, wy + wh//2, vision.sw, vision.sh)
                    self.state = "WAITING"
                    last_cast = time.time()
                    db.create_checkpoint({"state": "WAITING", "last_cast": last_cast})
                    time.sleep(2)

                elif self.state == "WAITING":
                    rw, rh = 300, 300
                    rx, ry = wx + (ww - rw)//2, wy + (wh - rh)//2
                    img = vision.get_screenshot((rx, ry, rw, rh))
                    pos = vision.find_white_pixel(img)
                    if pos:
                        self.log("Bite detected!")
                        input_ctrl.click(rx + pos[0], ry + pos[1], vision.sw, vision.sh)
                        self.state = "SHAKING"
                        db.add_history("BITE", f"Pos: {pos}")
                    
                    if time.time() - last_cast > 60:
                        self.log("Cast timeout, resetting...")
                        self.state = "IDLE"

                elif self.state == "SHAKING":
                    # Simplified shake logic
                    rw, rh = 300, 300
                    rx, ry = wx + (ww - rw)//2, wy + (wh - rh)//2
                    img = vision.get_screenshot((rx, ry, rw, rh))
                    pos = vision.find_white_pixel(img)
                    if not pos:
                        self.log("Reeling phase started")
                        self.state = "REELING"
                    else:
                        input_ctrl.click(rx + pos[0], ry + pos[1], vision.sw, vision.sh)

                elif self.state == "REELING":
                    # Logic for reeling
                    # (Simplified for now, will refine in later phase)
                    # We'll assume successful catch for skeleton
                    self.log("Fish caught!")
                    db.add_history("CATCH", "Success")
                    self.state = "IDLE"
                    time.sleep(3)

                time.sleep(0.1)
            except Exception as e:
                self.log(f"Error: {e}", "ERROR")
                time.sleep(1)

macro_engine = MacroEngine()
