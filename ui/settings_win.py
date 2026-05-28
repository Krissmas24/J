import tkinter as tk
from ui.theme import Theme
from core.database import db

class SettingsWindow:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Settings")
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.configure(bg=Theme.BG)
        
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 320, 480
        self.win.geometry(f"{w}x{h}+{(sw-w)//2 + 200}+{(sh-h)//2}")
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.win, bg=Theme.SECONDARY_BG, height=40)
        header.pack(fill="x")
        tk.Label(header, text="SETTINGS", font=Theme.FONT_BOLD, fg=Theme.ACCENT, bg=Theme.SECONDARY_BG).pack(side="left", padx=10)
        tk.Button(header, text="✕", command=self.win.destroy, bg=Theme.SECONDARY_BG, fg=Theme.DANGER, bd=0).pack(side="right", padx=10)

        content = tk.Frame(self.win, bg=Theme.BG, padx=15, pady=15)
        content.pack(fill="both", expand=True)

        # Webhook
        tk.Label(content, text="DISCORD WEBHOOK", font=Theme.FONT_BOLD, fg=Theme.FG, bg=Theme.BG).pack(anchor="w")
        self.webhook_entry = tk.Entry(content, bg=Theme.SECONDARY_BG, fg=Theme.ACCENT, insertbackground=Theme.ACCENT, bd=1, relief="solid")
        self.webhook_entry.insert(0, db.get_setting("webhook_url", ""))
        self.webhook_entry.pack(fill="x", pady=(5, 15))

        # Toggles
        self.anti_afk = tk.BooleanVar(value=db.get_setting("anti_afk", "true") == "true")
        tk.Checkbutton(content, text="Anti-AFK System", variable=self.anti_afk, 
                      bg=Theme.BG, fg=Theme.FG, selectcolor=Theme.BG, activebackground=Theme.BG,
                      activeforeground=Theme.ACCENT).pack(anchor="w")

        self.auto_sell = tk.BooleanVar(value=db.get_setting("auto_sell", "false") == "true")
        tk.Checkbutton(content, text="Auto-Sell (Experimental)", variable=self.auto_sell, 
                      bg=Theme.BG, fg=Theme.FG, selectcolor=Theme.BG, activebackground=Theme.BG,
                      activeforeground=Theme.ACCENT).pack(anchor="w")

        # Save Button
        save_btn = tk.Button(content, text="SAVE CONFIGURATION", command=self.save_settings)
        Theme.apply_rounded_button(save_btn)
        save_btn.pack(side="bottom", fill="x", pady=10)

    def save_settings(self):
        db.set_setting("webhook_url", self.webhook_entry.get())
        db.set_setting("anti_afk", str(self.anti_afk.get()).lower())
        db.set_setting("auto_sell", str(self.auto_sell.get()).lower())
        self.win.destroy()
