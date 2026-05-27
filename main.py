import tkinter as tk
from ui.splash import SplashScreen
from ui.main_window import MainWindow
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class JApp:
    def __init__(self):
        print("Starting J App...")
        try:
            self.root = tk.Tk()
            print("Tkinter root initialized")
            self.root.withdraw()
            print("Showing splash screen...")
            self.splash = SplashScreen(self.root, self.launch_main)
            print("Entering mainloop")
            self.root.mainloop()
        except Exception as e:
            print(f"Error during initialization: {e}")
            import traceback
            traceback.print_exc()

    def launch_main(self):
        print("Launching main window...")
        self.main_win = MainWindow(self.root)
        self.root.deiconify()
        print("Main window ready")

if __name__ == "__main__":
    app = JApp()
