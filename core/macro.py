import time
import threading
from core.vision import vision
from core.input import input_ctrl
from core.database import db
from core.webhooks import send_webhook
from core.audio import audio
from PIL import ImageStat

class MacroEngine:
    def __init__(self):
        self.is_running = False
        self.state = "IDLE"
        self.thread = None
        self.reeling_held = False
        self.callbacks = []
        
        # PID-like control variables
        self.bar_speed = 0
        self.last_fish_pos = -1

    def add_callback(self, cb):
        self.callbacks.append(cb)

    def log(self, message, level="INFO"):
        db.log_event(level, message)
        for cb in self.callbacks: cb(message)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.log("Protocol Engaged", "CORE")
            db.add_history("START", "Macro engine engaged")
            audio.play_ping()
            self.thread = threading.Thread(target=self.run_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        self.log("Protocol Disengaged", "CORE")
        db.add_history("STOP", "Macro engine disengaged")
        if self.reeling_held:
            input_ctrl.release()
            self.reeling_held = False

    def run_loop(self):
        last_cast = 0
        last_afk = time.time()
        
        while self.is_running:
            try:
                # Anti-AFK
                if db.get_setting("anti_afk", "true") == "true" and time.time() - last_afk > 120:
                    input_ctrl.press()
                    time.sleep(0.1)
                    input_ctrl.release()
                    last_afk = time.time()

                target = vision.get_sober_window()
                if not target:
                    time.sleep(2)
                    continue

                wx, wy = target["at"]
                ww, wh = target["size"]

                if self.state == "IDLE":
                    self.log("Deploying Line...")
                    input_ctrl.click(wx + ww//2, wy + wh//2, vision.sw, vision.sh)
                    self.state = "WAITING"
                    last_cast = time.time()
                    time.sleep(2)

                elif self.state == "WAITING":
                    rw, rh = 300, 300
                    rx, ry = wx + (ww - rw)//2, wy + (wh - rh)//2
                    img = vision.get_screenshot((rx, ry, rw, rh))
                    pos = vision.find_white_pixel(img)
                    if pos:
                        self.log("Bite Confirmed!")
                        audio.play_ping()
                        input_ctrl.click(rx + pos[0], ry + pos[1], vision.sw, vision.sh)
                        self.state = "SHAKING"
                    
                    if time.time() - last_cast > 60:
                        self.state = "IDLE"

                elif self.state == "SHAKING":
                    rw, rh = 300, 300
                    rx, ry = wx + (ww - rw)//2, wy + (wh - rh)//2
                    img = vision.get_screenshot((rx, ry, rw, rh))
                    pos = vision.find_white_pixel(img)
                    if not pos:
                        self.log("Reeling Initiated...")
                        self.state = "REELING"
                        self.last_fish_pos = -1
                    else:
                        input_ctrl.click(rx + pos[0], ry + pos[1], vision.sw, vision.sh)

                elif self.state == "REELING":
                    # Advanced Reeling Logic
                    rw = max(200, min(400, int(ww * 0.8)))
                    rh = max(15, min(40, int(wh * 0.05)))
                    ry = max(wy, wy + wh - int(wh * 0.15))
                    rx = wx + (ww - rw)//2
                    img = vision.get_screenshot((rx, ry, rw, rh))
                    
                    if img:
                        gray = img.convert("L")
                        pixels = gray.load()
                        fish_x = -1
                        bar_start = -1
                        bar_end = -1
                        
                        mid_y = rh // 2
                        for x in range(rw):
                            p = pixels[x, mid_y]
                            if p > 230: fish_x = x
                            elif 140 < p < 210:
                                if bar_start == -1: bar_start = x
                                bar_end = x
                        
                        if fish_x != -1 and bar_start != -1:
                            bar_center = (bar_start + bar_end) // 2
                            # Predictive movement based on fish velocity
                            if self.last_fish_pos != -1:
                                fish_vel = fish_x - self.last_fish_pos
                                target_x = fish_x + (fish_vel * 2)
                            else:
                                target_x = fish_x
                            
                            self.last_fish_pos = fish_x

                            if target_x > bar_center + 5:
                                if not self.reeling_held:
                                    input_ctrl.press()
                                    self.reeling_held = True
                            elif target_x < bar_center - 5:
                                if self.reeling_held:
                                    input_ctrl.release()
                                    self.reeling_held = False
                        else:
                            # UI Gone, check for success
                            stat = ImageStat.Stat(gray)
                            if stat.mean[0] < 40:
                                self.log("Specimen Acquired!", "SUCCESS")
                                audio.play_success()
                                db.add_history("CATCH", "Success")
                                send_webhook("CATCH", "A new specimen has been acquired.")
                                if self.reeling_held: input_ctrl.release(); self.reeling_held = False
                                self.state = "IDLE"
                                time.sleep(3)
                        
                        time.sleep(0.01)
                        continue 

                time.sleep(0.1)
            except Exception as e:
                self.log(f"System Error: {e}", "ERROR")
                time.sleep(1)

macro_engine = MacroEngine()
