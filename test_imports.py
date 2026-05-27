import os
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

print("Testing imports...")
try:
    from ui.theme import Theme
    print("Theme imported")
    from core.database import db
    print("Database imported")
    from core.vision import vision
    print("Vision imported")
    from core.input import input_ctrl
    print("Input imported")
    from core.macro import macro_engine
    print("Macro imported")
    from ui.splash import SplashScreen
    print("Splash imported")
    from ui.main_window import MainWindow
    print("Main Window imported")
    print("All imports successful!")
except Exception as e:
    import traceback
    traceback.print_exc()
