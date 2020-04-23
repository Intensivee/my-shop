from tkinter import *
import main as m
import shared as s
import dbmenager as db
import CustomerWindow
import AdminWindow

class LoginWindow:

    def __init__(self, master):
        self.master = master
        self.master.title('Mendiona bytes')
        self.frame = Frame(self.master, bg=s.bgg, bd=15)

        self.error_label = Label()

        # login, password label and entry
        self.login_label = Label(self.frame, bg=s.bgg, text='login:')
        self.login_label.grid(row=0, column=0)
        self.password_label = Label(self.frame, bg=s.bgg, text='password:')
        self.password_label.grid(row=1, column=0)
        self.login_entry = Entry(self.frame, bg=s.lgg, width=18)
        self.login_entry.grid(row=0, column=1)
        self.password_entry = Entry(self.frame, show='*', bg=s.lgg , width=18)
        self.password_entry.grid(row=1, column=1)

        # buttons
        self.login_button = Button(self.frame, text='Log in', bg=s.lgg, command=self.login, width=16)
        self.login_button.grid(row=3, column=1, pady=(10, 0))
        self.create_button = Button(self.frame, text='Create new account', bg=s.lgg, command=self.create_acc, width=16)
        self.create_button.grid(row=4, column=1)
        self.frame.pack()

    def login(self):
        # deleting missing label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        #checking if all required entry's are filled
        if self.login_entry.get() == '':
            self.error_label = Label(self.frame, text="login missing", fg='red', bg=s.bgg)
            self.error_label.grid(row=2, column=1)
        elif self.password_entry.get() == '':
            self.error_label = Label(self.frame, text="password missing", fg='red', bg=s.bgg)
            self.error_label.grid(row=2, column=1)

        else:
            s.my_id, perm = db.customerPerm(self.login_entry.get(), self.password_entry.get())
            if perm == -1 or s.my_id == -1:
                self.error_label = Label(self.frame, text="try again..", fg='red', bg=s.bgg)
                self.error_label.grid(row=2, column=1)
            elif perm == 1:
                self.admin_app()
            else:
                self.customer_app()

    def create_acc(self):
        self.frame.destroy()
        self.frame = Frame(self.master, bg=s.bgg)
        self.frame.pack()

        # Create text box labels for Customers
        login_label = Label(self.frame, text='login:', bg=s.bgg)
        login_label.grid(row=0, column=0, pady=(10, 0), sticky=E)
        password_label = Label(self.frame, text='password:', bg=s.bgg)
        password_label.grid(row=1, column=0, sticky=E,)
        name_label = Label(self.frame, text='name:', bg=s.bgg)
        name_label.grid(row=2, column=0, sticky=E)
        phone_label = Label(self.frame, text='phone:', bg=s.bgg)
        phone_label.grid(row=3, column=0, sticky=E)
        email_label = Label(self.frame, text='email:', bg=s.bgg)
        email_label.grid(row=4, column=0, sticky=E)

        # Create Entry box for Customers
        self.login_entry = Entry(self.frame, width=18, bg=s.lgg)
        self.login_entry.grid(row=0, column=1, pady=(10, 0))
        self.password_entry = Entry(self.frame, width=18, show='*', bg=s.lgg)
        self.password_entry.grid(row=1, column=1)
        self.name_entry = Entry(self.frame, width=18, bg=s.lgg)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = Entry(self.frame, width=18, bg=s.lgg)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = Entry(self.frame, width=18, bg=s.lgg)
        self.email_entry.grid(row=4, column=1)

        # buttons
        self.login_button = Button(self.frame, text='create', command=self.create_acc_db, width=16, bg=s.lgg)
        self.login_button.grid(row=6, column=0, pady=(20, 0))
        self.create_button = Button(self.frame, text='Cancel', command=self.master.destroy, width=16, bg=s.lgg)
        self.create_button.grid(row=6, column=1, pady=(20, 0))

    def create_acc_db(self):
        # deleting missing label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled.
        if self.login_entry.get() == '':
            self.error_label = Label(self.frame, text="'login' missing", fg='red', bg=s.bgg)
            self.error_label.grid(row=5, column=1)
        elif len(self.password_entry.get()) < 6:
            self.error_label = Label(self.frame, text="password to short", fg='red', bg=s.bgg)
            self.error_label.grid(row=5, column=1)
        elif self.name_entry.get() == '':
            self.error_label = Label(self.frame, text="'name' missing", fg='red', bg=s.bgg)
            self.error_label.grid(row=5, column=1)
        elif self.email_entry.get() == '':
            self.error_label = Label(self.frame, text="'email' missing", fg='red', bg=s.bgg)
            self.error_label.grid(row=5, column=1)
        elif self.phone_entry.get() != '' and not s.is_integer(self.phone_entry.get()):
            self.error_label = Label(self.frame, text="wrong phone number", fg='red', bg=s.bgg)
            self.error_label.grid(row=5, column=1)

        else:
            # checking if customer is in DB
            exist = db.is_customer_exists(self.login_entry.get(), self.email_entry.get())
            if exist:
                self.error_label = Label(self.frame, text="'{}' exists".format(exist), fg='red', bg=s.bgg)
                self.error_label.grid(row=5, column=1)
            else:
                db.addCustomer(self.login_entry.get(), self.password_entry.get(), self.name_entry.get(),
                               self.phone_entry.get(), self.email_entry.get())
                self.master.destroy()
                self.master = Tk()
                m.app = LoginWindow(self.master)
                self.master.mainloop()

    def admin_app(self):
        self.master.destroy()
        self.master = Tk()
        # app is new variable
        app = AdminWindow.CustomersMenu(self.master)
        self.master.mainloop()

    def customer_app(self):
        self.master.destroy()
        self.master = Tk()
        app = CustomerWindow.CustomerApp(self.master)
        self.master.mainloop()