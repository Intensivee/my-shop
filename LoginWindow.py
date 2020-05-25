"""Login and create new acc module."""
import tkinter as tk

import AdminWindow
import CustomerWindow
import dbmanager as db
import myConfig

# Module Constants:
LOGIN_WINDOW_SIZE = "300x200"


class LoginWindow:
    """Login and create new acc window."""

    def __init__(self, master):
        """Creates login window."""
        self.master = master
        self.master.title(myConfig.APP_NAME)
        self.master.geometry(LOGIN_WINDOW_SIZE)
        self.master.configure(bg=myConfig.BACKGROUND)
        self.frame = tk.Frame(self.master, bg=myConfig.BACKGROUND, bd=15)

        # it contains error messages, for example not all entry are filled.
        self.error_label = tk.Label()
        self.initialize_login_window()

    def initialize_login_window(self):
        """Initializing login window."""
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=myConfig.BACKGROUND, bd=15)

        # login, password label and entry
        self.login_label = tk.Label(self.frame, bg=myConfig.BACKGROUND, text='login:')
        self.login_label.grid(row=0, column=0)
        self.password_label = tk.Label(self.frame, bg=myConfig.BACKGROUND, text='password:')
        self.password_label.grid(row=1, column=0)
        self.login_entry = tk.Entry(self.frame, bg=myConfig.FOREGROUND, width=18)
        self.login_entry.grid(row=0, column=1)
        self.password_entry = tk.Entry(self.frame, show='*', bg=myConfig.FOREGROUND, width=18)
        self.password_entry.grid(row=1, column=1)

        # buttons
        self.login_button = tk.Button(self.frame, text='Log in', bg=myConfig.FOREGROUND, command=self.login, width=16)
        self.login_button.grid(row=3, column=1, pady=(10, 0))
        self.create_button = tk.Button(self.frame, text='Create new account',
                                       bg=myConfig.FOREGROUND, command=self.create_account, width=16)
        self.create_button.grid(row=4, column=1)
        self.frame.pack()

    def login(self):
        """Method that runs admin/customer, depending on permissions"""
        # deleting error label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled
        if not self.login_entry.get():
            self.error_label = tk.Label(self.frame, text="login missing", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=2, column=1)
        elif not self.password_entry.get():
            self.error_label = tk.Label(self.frame, text="password missing", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=2, column=1)

        else:
            myConfig.my_id, perm = db.customer_perm(self.login_entry.get(), self.password_entry.get())
            if perm == -1 or myConfig.my_id == -1:
                self.error_label = tk.Label(self.frame, text="try again..", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
                self.error_label.grid(row=2, column=1)
            elif perm == myConfig.ADMIN_PERM:
                self.admin_app()
            else:
                self.customer_app()

    def create_account(self):
        """Initializes window for creating new accounts."""
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=myConfig.BACKGROUND)
        self.frame.pack()

        # Create text box labels for Customers
        login_label = tk.Label(self.frame, text='login:', bg=myConfig.BACKGROUND)
        login_label.grid(row=0, column=0, pady=(10, 0), sticky=tk.E)
        password_label = tk.Label(self.frame, text='password:', bg=myConfig.BACKGROUND)
        password_label.grid(row=1, column=0, sticky=tk.E, )
        name_label = tk.Label(self.frame, text='name:', bg=myConfig.BACKGROUND)
        name_label.grid(row=2, column=0, sticky=tk.E)
        phone_label = tk.Label(self.frame, text='phone:', bg=myConfig.BACKGROUND)
        phone_label.grid(row=3, column=0, sticky=tk.E)
        email_label = tk.Label(self.frame, text='email:', bg=myConfig.BACKGROUND)
        email_label.grid(row=4, column=0, sticky=tk.E)

        # Create Entry box for Customers
        self.login_entry = tk.Entry(self.frame, width=18, bg=myConfig.FOREGROUND)
        self.login_entry.grid(row=0, column=1, pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, width=18, show='*', bg=myConfig.FOREGROUND)
        self.password_entry.grid(row=1, column=1)
        self.name_entry = tk.Entry(self.frame, width=18, bg=myConfig.FOREGROUND)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = tk.Entry(self.frame, width=18, bg=myConfig.FOREGROUND)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = tk.Entry(self.frame, width=18, bg=myConfig.FOREGROUND)
        self.email_entry.grid(row=4, column=1)

        # buttons
        self.login_button = tk.Button(self.frame, text='create', command=self.create_account_db,
                                      width=16, bg=myConfig.FOREGROUND)
        self.login_button.grid(row=6, column=0, pady=(20, 0))
        self.create_button = tk.Button(self.frame, text='Cancel', command=self.initialize_login_window,
                                       width=16, bg=myConfig.FOREGROUND)
        self.create_button.grid(row=6, column=1, pady=(20, 0))

    def create_account_db(self):
        """Create new account if all required entry's are filled."""
        # deleting missing label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled.
        if not self.login_entry.get():
            self.error_label = tk.Label(self.frame, text="'login' missing", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif len(self.password_entry.get()) < 6:
            self.error_label = tk.Label(self.frame, text="minimum password length is 6", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif not self.name_entry.get():
            self.error_label = tk.Label(self.frame, text="'name' missing", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif not self.email_entry.get():
            self.error_label = tk.Label(self.frame, text="'email' missing", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif self.phone_entry.get() and not myConfig.is_integer(self.phone_entry.get()):
            self.error_label = tk.Label(self.frame, text="wrong phone number", fg=myConfig.ERROR_FOREGROUND, bg=myConfig.BACKGROUND)
            self.error_label.grid(row=5, column=1)

        else:
            # checking if customer is in DB
            exist = db.is_customer_exists(self.login_entry.get(), self.email_entry.get())
            if exist:
                self.error_label = tk.Label(self.frame, text="'{}' exists".format(exist), fg=myConfig.ERROR_FOREGROUND,
                                            bg=myConfig.BACKGROUND)
                self.error_label.grid(row=5, column=1)
            else:
                db.add_customer(self.login_entry.get(), self.password_entry.get(), self.name_entry.get(),
                                self.phone_entry.get(), self.email_entry.get())
                self.frame.destroy()
                LoginWindow(self.master)

    def admin_app(self):
        """Initializing Admin window."""
        self.frame.destroy()
        AdminWindow.CustomersMenu(self.master)

    def customer_app(self):
        """Initializing Customer window."""
        self.frame.destroy()
        CustomerWindow.CustomerApp(self.master)
