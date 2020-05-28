"""Main module that runs the app."""
import tkinter as tk

import login_window


def main():
    """Create and maintains the window."""
    root = tk.Tk()
    application = login_window.LoginWindow(root)
    application.initialize_login_window()
    root.mainloop()


if __name__ == "__main__":
    main()
