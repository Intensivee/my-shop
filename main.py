"""Main module - runs the app."""
import tkinter as tk
import LoginWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow.LoginWindow(root)
    root.mainloop()
