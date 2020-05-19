"""Main module - runs the app."""
import tkinter as tk

import LoginWindow


def main():
    root = tk.Tk()
    app = LoginWindow.LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
