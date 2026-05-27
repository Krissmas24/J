import tkinter as tk
from ui.splash import SplashScreen
from ui.main_window import MainWindow
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class JApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.splash = SplashScreen(self.root, self.launch_main)
        self.root.mainloop()

    def launch_main(self):
        self.main_win = MainWindow(self.root)
        self.root.deiconify()

if __name__ == "__main__":
    app = JApp()
