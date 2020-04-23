from tkinter import *
import tkinter.messagebox
import shared as s
import dbmenager as db
import LoginWindow


class CustomerApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x900+0+0")
        self.master.configure(bg=s.bgg)
        self.master.title('Mendiona bytes')

        # main frames
        self.frame = Frame(self.master, bg=s.bgg)
        self.function_frame = Frame(self.master, bg=s.bgg)
        self.function_frame2 = Frame(self.master, bg=s.bgg)
        self.function_frame3 = Frame(self.master, bg=s.bgg)

        # error label
        self.error_label = Label()

        self.initialize_main_buttons()

    def initialize_main_buttons(self):
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        self.frame = Frame(self.master, bg=s.bgg)
        self.search_button = Button(self.frame, text='List of products', bg=s.lgg, command=self.list_products, width=16)
        self.search_button.grid(row=0, column=0, pady=(10, 3))
        self.edit_button = Button(self.frame, text='Edit account', bg=s.lgg, command=self.acc_edit, width=16)
        self.edit_button.grid(row=1, column=0, pady=(0, 3))
        self.orders_button = Button(self.frame, text='My Orders', bg=s.lgg, command=self.my_orders, width=16)
        self.orders_button.grid(row=2, column=0, pady=(0, 3))
        self.logOff_button = Button(self.frame, text='Logoff', bg=s.lgg, command=self.log_off, width=16)
        self.logOff_button.grid(row=3, column=0, pady=(0, 3))
        self.frame.pack()

    def list_products(self):
        self.initialize_main_buttons()

        # frame for listbox
        self.function_frame = Frame(self.master, bg=s.bgg)
        self.function_frame.pack()
        self.function_frame2 = Frame(self.master, bg=s.bgg)
        self.function_frame2.pack()

        # creating listbox for customers
        list_label = Label(self.function_frame, text='list of products', width=100, bg=s.bgg)
        list_label.grid(row=0, column=0, pady=(10,0))
        scrollbar = Scrollbar(self.function_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.listbox = Listbox(self.function_frame, width=60, height=15, yscrollcommand=scrollbar.set, bg=s.lgg)
        self.listbox.bind('<<ListboxSelect>>', self.select)
        self.listbox.grid(row=1, column=0, padx=8)

        # adding records from DB to Listbox
        records = db.returnProducts()
        for record in records:
            self.listbox.insert(END, (str(record[0]), record[1], str(record[2]), str(record[3])))

        # crating labels
        id_product_label = Label(self.function_frame2, text='Product ID:', bg=s.bgg)
        id_product_label.grid(row=0, column=0, sticky=E)
        quantity_label = Label(self.function_frame2, text='Quantity:', bg=s.bgg)
        quantity_label.grid(row=1, column=0, sticky=E)
        location_label = Label(self.function_frame2, text='Order location:', bg=s.bgg)
        location_label.grid(row=2, column=0, sticky=E)

        # creating entry boxes
        self.id_product_entry = Entry(self.function_frame2, width=30, bg=s.lgg)
        self.id_product_entry.grid(row=0, column=1)
        self.quantity_entry = Entry(self.function_frame2, width=30, bg=s.lgg)
        self.quantity_entry.grid(row=1, column=1)
        self.location_entry = Entry(self.function_frame2, width=30, bg=s.lgg)
        self.location_entry.grid(row=2, column=1)

        # buttons
        self.place_order_button = Button(self.function_frame2, text='Place order', bg=s.lgg, command=self.place_order, width=16)
        self.place_order_button.grid(row=4, column=0)
        self.details_button = Button(self.function_frame2, text='details', bg=s.lgg, command=self.product_details, width=16)
        self.details_button.grid(row=4, column=1,)

    def place_order(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled properly
        if self.id_product_entry.get() == '':
            self.error_message("'id product' missing")
        elif not s.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("'quantity' Must be an positive integer")
        elif self.location_entry.get() == '':
            self.error_message("'location' missing")

        # checking if customer and product exists
        elif not db.is_customer_id_exitst(s.my_id) or not db.is_product_id_exists(self.id_product_entry.get()):
            self.error_message("product or customer id not Exists")

        # function itself check if there is enough products, and count total price (quantity*price)
        elif db.addOrder(s.my_id, self.id_product_entry.get(), self.quantity_entry.get(), self.location_entry.get()):
                tkinter.messagebox.showinfo("Mendiona bytes", 'successfully added.')

                self.list_products()
        else:
            self.error_message("not enough products in stock.")

    def product_details(self):
        if self.error_label:
            self.error_label.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        if self.id_product_entry.get() == '':
            self.error_message("select product.")

        elif db.is_product_id_exists(self.id_product_entry.get()):

            self.function_frame3 = Frame(self.master, bg=s.bgg)
            self.function_frame3.pack(side=TOP)

            # creating Message instead of Label (description might be long)
            description = db.returnProduct(self.id_product_entry.get())[4]
            self.error_label = Message(self.function_frame3, text="Description: {}".format(description), bg=s.bgg, width=300)
            self.error_label.grid(row=5, column=0)
        else:
            self.error_message("Product not exist.")

    def select(self, event):

         # will do sth only if the mouse click was on customer listbox
        if self.listbox.curselection():
            search = self.listbox.curselection()[0]
            current_record = self.listbox.get(search)

            self.id_product_entry.delete(0, END)
            self.id_product_entry.insert(END, current_record[0])

        pass

    def acc_edit(self):
        self.master.destroy()
        self.master = Tk()
        app = AccEdit(self.master)
        self.master.mainloop()

    def my_orders(self):
        self.initialize_main_buttons()

        self.function_frame = Frame(self.master, bg=s.bgg)
        self.function_frame.pack()

        # creating listbox for customers
        list_label = Label(self.function_frame, text='my orders:', width=100, bg=s.bgg)
        list_label.grid(row=0, column=0, pady=(10,0))
        scrollbar = Scrollbar(self.function_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.listbox = Listbox(self.function_frame, width=60, height=15, yscrollcommand=scrollbar.set, bg=s.lgg)
        self.listbox.grid(row=1, column=0, padx=8)

        # adding records from DB to Listbox
        records = db.ordersProductInfo(s.my_id)
        for record in records:
            self.listbox.insert(END, (str(record[0]), record[1], str(record[2])))

    def error_message(self, name):
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = Label(self.function_frame2, text="{}".format(name), bg=s.bgg, fg='red')
        self.error_label.grid(row=3, column=1)

    def log_off(self):
        s.my_id = -1
        self.master.destroy()
        self.master = Tk()
        app = LoginWindow.LoginWindow(self.master)
        self.master.mainloop()


class AccEdit:

    def __init__(self, master):
        self.master = master
        self.master.configure(bg=s.bgg)
        self.master.title('Mendiona bytes')

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = Label()

        self.frame = Frame(self.master, bg=s.bgg)
        self.initialize()

    def initialize(self):
        if self.frame:
            self.frame.destroy()
        self.frame = Frame(self.master, bg=s.bgg)
        self.frame.pack()

        # Create text box labels
        new_password_label = Label(self.frame, text='new password(opt):', bg=s.bgg)
        new_password_label.grid(row=0, column=0, sticky=E)
        password_label = Label(self.frame, text='password:', bg=s.bgg)
        password_label.grid(row=1, column=0, sticky=E)
        name_label = Label(self.frame, text='name:', bg=s.bgg)
        name_label.grid(row=2, column=0, sticky=E)
        phone_label = Label(self.frame, text='phone:', bg=s.bgg)
        phone_label.grid(row=3, column=0, sticky=E)
        email_label = Label(self.frame, text='email:', bg=s.bgg)
        email_label.grid(row=4, column=0, sticky=E)

        # Create Entry box
        self.new_password_entry = Entry(self.frame, width=22, show='*', bg=s.lgg)
        self.new_password_entry.grid(row=0, column=1)
        self.password_entry = Entry(self.frame, width=22, show='*', bg=s.lgg)
        self.password_entry.grid(row=1, column=1)
        self.name_entry = Entry(self.frame, width=22, bg=s.lgg)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = Entry(self.frame, width=22, bg=s.lgg)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = Entry(self.frame, width=22, bg=s.lgg)
        self.email_entry.grid(row=4, column=1)

        # Create Buttons
        self.change_button = Button(self.frame, text='change', bg=s.lgg, command=self.set_change, width=16)
        self.change_button.grid(row=0, column=2, padx=20)
        self.cancel_button = Button(self.frame, text='Cancel', bg=s.lgg, command=self.exit, width=16)
        self.cancel_button.grid(row=1, column=2)

        #getting customer info from DB
        customerInfo = db.returnCustomer(s.my_id)
        if customerInfo:
            self.name_entry.insert(END, customerInfo[3])
            self.phone_entry.insert(END, customerInfo[4])
            self.email_entry.insert(END, customerInfo[5])
        else:
            tkinter.messagebox.showinfo("Mendiona bytes", 'ERROR: WRONG ID!!!')
            self.exit()

    def set_change(self):
        if self.error_label:
            self.error_label.destroy()

        # if new password entry is empty don't update it
        if 0 < len(self.new_password_entry.get()) < 6:
            self.error_message('new password is too short.')

        # checking if all required entry's are filled properly
        elif self.password_entry.get() != db.returnCustomer(s.my_id)[2]:
            self.error_message('password does not match.')
        elif self.name_entry.get() == '':
            self.error_message('Can not update empty name.')
        elif self.phone_entry.get() != '' and not s.is_integer(self.phone_entry.get()):
            self.error_message("wrong phone number.")
        elif self.email_entry.get() == '':
            self.error_message('Can not update empty email.')

        else:
            # if all entry's are filled correctly

            if self.new_password_entry != '':
                # passing new password
                db.editCustomer(s.my_id, self.new_password_entry.get(), self.name_entry.get(), self.email_entry.get(), self.phone_entry.get())
            else:
                # passing old password to function (no change)
                db.editCustomer(s.my_id, db.returnCustomer(s.my_id)[2], self.name_entry.get(), self.email_entry.get(), self.phone_entry.get() )

            self.error_message("Account has been updated.")

    def error_message(self, name):
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = Label(self.frame, fg='red', text='{}'.format(name), bg=s.bgg)
        self.error_label.grid(row=5, column=1)

    def exit(self):
        self.master.destroy()
        self.master = Tk()
        app = CustomerApp(self.master)
        self.master.mainloop()




