import tkinter as tk
try:
    root = tk.Tk()
    root.title("Test")
    root.geometry("200x200")
    label = tk.Label(root, text="If you see this, Tkinter is working")
    label.pack()
    root.after(2000, root.destroy)
    root.mainloop()
    print("Tkinter test successful")
except Exception as e:
    print(f"Tkinter test failed: {e}")
