"""Main module that runs the app."""
import tkinter as tk

import LoginWindow


def main():
    """Create and maintains the window."""
    root = tk.Tk()
    application = LoginWindow.LoginWindow(root)
    application.initialize_login_window()
    root.mainloop()


if __name__ == "__main__":
    main()
