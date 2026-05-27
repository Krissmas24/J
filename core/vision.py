import subprocess
import io
import json
from PIL import Image, ImageStat

class VisionProvider:
    def __init__(self):
        self.sw = 1920
        self.sh = 1080
        self.update_screen_size()

    def update_screen_size(self):
        try:
            m_out = subprocess.check_output(["hyprctl", "monitors", "-j"], text=True)
            monitors = json.loads(m_out)
            primary = next((m for m in monitors if m.get("focused")), monitors[0])
            self.sw = primary["width"]
            self.sh = primary["height"]
        except: pass

    def get_screenshot(self, region=None):
        try:
            cmd = ["grim"]
            if region:
                x, y, w, h = region
                x = max(0, min(x, self.sw - 1))
                y = max(0, min(y, self.sh - 1))
                w = max(1, min(w, self.sw - x))
                h = max(1, min(h, self.sh - y))
                cmd.extend(["-g", f"{x},{y} {w}x{h}"])
            cmd.append("-")
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            data = proc.communicate()[0]
            if not data: return None
            return Image.open(io.BytesIO(data))
        except: return None

    def find_white_pixel(self, img):
        if not img: return None
        gray = img.convert("L")
        pixels = gray.load()
        w, h = gray.size
        for y in range(0, h, 10):
            for x in range(0, w, 10):
                if pixels[x, y] > 250:
                    return x, y
        return None

    def get_sober_window(self):
        try:
            output = subprocess.check_output(["hyprctl", "clients", "-j"], text=True)
            clients = json.loads(output)
            return next((c for c in clients if "sober" in c.get("class", "").lower()), None)
        except: return None

vision = VisionProvider()
