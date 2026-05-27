import tkinter as tk
from ui.theme import Theme
from core.macro import macro_engine
from core.database import db

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("J")
        self.root.wm_class = "J"
        self.root.configure(bg=Theme.BG)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.lift()
        self.root.focus_force()
        
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 300, 400
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self.setup_ui()
        macro_engine.add_callback(self.on_macro_log)

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=Theme.SECONDARY_BG, height=40)
        header.pack(fill="x")
        
        title = tk.Label(header, text="J - MACRO", font=Theme.FONT_BOLD, fg=Theme.ACCENT, bg=Theme.SECONDARY_BG)
        title.pack(side="left", padx=10)
        
        close_btn = tk.Button(header, text="✕", command=self.root.destroy, bg=Theme.SECONDARY_BG, fg=Theme.DANGER, bd=0)
        close_btn.pack(side="right", padx=10)

        # Status Badge
        self.status_frame = tk.Frame(self.root, bg=Theme.BG, pady=20)
        self.status_frame.pack()
        
        self.status_label = tk.Label(self.status_frame, text="OFFLINE", font=Theme.FONT_TITLE, fg=Theme.FG, bg=Theme.BG)
        self.status_label.pack()
        
        self.toggle_btn = tk.Button(self.status_frame, text="START PROTOCOL", command=self.toggle_macro)
        Theme.apply_rounded_button(self.toggle_btn)
        self.toggle_btn.pack(pady=10)

        # Logs
        log_frame = tk.Frame(self.root, bg=Theme.SECONDARY_BG)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, bg=Theme.BG, fg=Theme.SUCCESS, font=("Consolas", 8), state="disabled", bd=0)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def toggle_macro(self):
        if not macro_engine.is_running:
            macro_engine.start()
            self.status_label.config(text="ACTIVE", fg=Theme.SUCCESS)
            self.toggle_btn.config(text="STOP PROTOCOL")
        else:
            macro_engine.stop()
            self.status_label.config(text="OFFLINE", fg=Theme.FG)
            self.toggle_btn.config(text="START PROTOCOL")

    def on_macro_log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def stop_drag(self, event):
        self.x = None
        self.y = None

    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
