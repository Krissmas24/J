import subprocess
import os
import time

SOCKET_PATH = f"/run/user/{os.getuid()}/j_ydotool.socket"
OS_ENV = os.environ.copy()
OS_ENV["YDOTOOL_SOCKET"] = SOCKET_PATH

class InputController:
    def __init__(self):
        self.ydotool_process = None
        self.ensure_daemon()

    def ensure_daemon(self):
        try:
            if os.path.exists(SOCKET_PATH): os.remove(SOCKET_PATH)
            subprocess.run(["pkill", "-9", "ydotoold"], stderr=subprocess.DEVNULL)
            self.ydotool_process = subprocess.Popen(["ydotoold", "--socket-path", SOCKET_PATH], 
                                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.5)
            if not os.path.exists(SOCKET_PATH):
                self.ydotool_process = subprocess.Popen(["ydotoold", "--socket", SOCKET_PATH], 
                                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Failed to start ydotoold: {e}")

    def click(self, x, y, sw, sh):
        try:
            ax = int((x / sw) * 65535)
            ay = int((y / sh) * 65535)
            subprocess.run(["ydotool", "mousemove", "-a", str(ax), str(ay)], env=OS_ENV, check=False)
            time.sleep(0.02)
            subprocess.run(["ydotool", "click", "0xC0"], env=OS_ENV, check=False)
        except: pass

    def press(self):
        subprocess.run(["ydotool", "click", "0x40"], env=OS_ENV, check=False)

    def release(self):
        subprocess.run(["ydotool", "click", "0x80"], env=OS_ENV, check=False)

    def cleanup(self):
        if self.ydotool_process:
            self.ydotool_process.terminate()

input_ctrl = InputController()
