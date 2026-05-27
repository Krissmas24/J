class Theme:
    VERSION = "v0.01.000.0000"  # Big Update / Remaster Start
    
    BG = "#0A0A0A"          # Deep Black
    DARK_GREY = "#222222"    # Splash Background
    FG = "#FFFFFF"          # Pure White
    BLACK = "#000000"
    ACCENT = "#FFD700"      # Gold
    SECONDARY_BG = "#1A1A1A"
    BORDER = "#333333"
    SUCCESS = "#00FF88"
    DANGER = "#FF4444"
    
    FONT_MAIN = ("Arial", 10)
    FONT_BOLD = ("Arial", 10, "bold")
    FONT_TITLE = ("Arial", 14, "bold")
    FONT_LOGO = ("Arial", 80, "bold italic")

    @staticmethod
    def apply_rounded_button(btn):
        btn.config(
            bg=Theme.SECONDARY_BG,
            fg=Theme.ACCENT,
            activebackground=Theme.ACCENT,
            activeforeground=Theme.BG,
            relief="solid",
            bd=1,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=Theme.ACCENT, fg=Theme.BG))
        btn.bind("<Leave>", lambda e: btn.config(bg=Theme.SECONDARY_BG, fg=Theme.ACCENT))
