import tkinter as tk
from ui.theme import Theme
from core.database import db

class DashboardWindow:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Dashboard")
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.configure(bg=Theme.BG)
        
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 320, 480
        self.win.geometry(f"{w}x{h}+{(sw-w)//2 - 200}+{(sh-h)//2}")
        
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.win, bg=Theme.SECONDARY_BG, height=40)
        header.pack(fill="x")
        tk.Label(header, text="STATISTICS", font=Theme.FONT_BOLD, fg=Theme.ACCENT, bg=Theme.SECONDARY_BG).pack(side="left", padx=10)
        tk.Button(header, text="✕", command=self.win.destroy, bg=Theme.SECONDARY_BG, fg=Theme.DANGER, bd=0).pack(side="right", padx=10)

        content = tk.Frame(self.win, bg=Theme.BG, padx=15, pady=15)
        content.pack(fill="both", expand=True)

        stats = db.get_stats()
        
        # Stat Cards
        self.create_stat_card(content, "TOTAL CATCHES", stats["catches"])
        self.create_stat_card(content, "SUCCESS RATE", f"{stats['success_rate']}%")
        
        # History
        tk.Label(content, text="RECENT LOGS", font=Theme.FONT_BOLD, fg=Theme.ACCENT, bg=Theme.BG).pack(anchor="w", pady=(15, 5))
        history_frame = tk.Frame(content, bg=Theme.SECONDARY_BG)
        history_frame.pack(fill="both", expand=True)
        
        history_text = tk.Text(history_frame, bg=Theme.SECONDARY_BG, fg=Theme.FG, font=("Consolas", 8), bd=0)
        history_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        recent = db.get_recent_history(15)
        for ts, event, details in recent:
            history_text.insert("end", f"[{ts[11:16]}] {event}: {details}\n")
        history_text.config(state="disabled")

    def create_stat_card(self, parent, title, value):
        frame = tk.Frame(parent, bg=Theme.SECONDARY_BG, padx=10, pady=10, bd=1, relief="solid")
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=title, font=("Arial", 8), fg=Theme.FG, bg=Theme.SECONDARY_BG).pack(anchor="w")
        tk.Label(frame, text=str(value), font=Theme.FONT_TITLE, fg=Theme.ACCENT, bg=Theme.SECONDARY_BG).pack(anchor="w")
