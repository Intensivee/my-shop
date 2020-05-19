"""Module contains major customer classes"""
import tkinter as tk
import tkinter.messagebox

import LoginWindow
import dbmanager as db
import shared


class CustomerApp:
    """Main customer window."""
    def __init__(self, master):
        """Initializes main customer window."""
        self.master = master
        self.master.geometry("800x900+0+0")
        self.master.configure(bg=shared.BACKGROUND)
        self.master.title('Mendiona bytes')

        # main frames
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.function_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.function_frame2 = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.function_frame3 = tk.Frame(self.master, bg=shared.BACKGROUND)

        # it contains error messages, for example not all entry are filled.
        self.error_label = tk.Label()

        self.initialize_main_buttons()

    def initialize_main_buttons(self):
        """Initializes main buttons.

        Used in other functions repeatedly, that's why it's not in __init__"""
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.search_button = tk.Button(self.frame, text='List of products',
                                       bg=shared.FOREGROUND, command=self.list_products, width=16)
        self.search_button.grid(row=0, column=0, pady=(10, 3))
        self.edit_button = tk.Button(self.frame, text='Edit account', bg=shared.FOREGROUND, command=self.acc_edit, width=16)
        self.edit_button.grid(row=1, column=0, pady=(0, 3))
        self.orders_button = tk.Button(self.frame, text='My Orders', bg=shared.FOREGROUND, command=self.my_orders, width=16)
        self.orders_button.grid(row=2, column=0, pady=(0, 3))
        self.logoff_button = tk.Button(self.frame, text='Logoff', bg=shared.FOREGROUND, command=self.log_off, width=16)
        self.logoff_button.grid(row=3, column=0, pady=(0, 3))
        self.frame.pack()

    def list_products(self):
        """Lists all of the customer products under menu."""
        self.initialize_main_buttons()

        # frame for listbox
        self.function_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.function_frame.pack()
        self.function_frame2 = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.function_frame2.pack()

        # creating listbox for customers
        list_label = tk.Label(self.function_frame, text='list of products', width=100, bg=shared.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))
        scrollbar = tk.Scrollbar(self.function_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.products_listbox = tk.Listbox(self.function_frame, width=60, height=15,
                                           yscrollcommand=scrollbar.set, bg=shared.FOREGROUND)
        self.products_listbox.bind('<<ListboxSelect>>', self.product_selection)
        self.products_listbox.grid(row=1, column=0, padx=8)

        # adding records from DB to Listbox
        records = db.return_products()
        for record in records:
            self.products_listbox.insert(tk.END, (str(record[0]), record[1], str(record[2]), str(record[3])))

        # crating labels
        id_product_label = tk.Label(self.function_frame2, text='Product ID:', bg=shared.BACKGROUND)
        id_product_label.grid(row=0, column=0, sticky=tk.E)
        quantity_label = tk.Label(self.function_frame2, text='Quantity:', bg=shared.BACKGROUND)
        quantity_label.grid(row=1, column=0, sticky=tk.E)
        location_label = tk.Label(self.function_frame2, text='Order location:', bg=shared.BACKGROUND)
        location_label.grid(row=2, column=0, sticky=tk.E)

        # creating entry boxes
        self.id_product_entry = tk.Entry(self.function_frame2, width=30, bg=shared.FOREGROUND)
        self.id_product_entry.grid(row=0, column=1)
        self.quantity_entry = tk.Entry(self.function_frame2, width=30, bg=shared.FOREGROUND)
        self.quantity_entry.grid(row=1, column=1)
        self.location_entry = tk.Entry(self.function_frame2, width=30, bg=shared.FOREGROUND)
        self.location_entry.grid(row=2, column=1)

        # buttons
        self.place_order_button = tk.Button(self.function_frame2, text='Place order',
                                            bg=shared.FOREGROUND, command=self.place_order, width=16)
        self.place_order_button.grid(row=4, column=0)
        self.details_button = tk.Button(self.function_frame2, text='details',
                                        bg=shared.FOREGROUND, command=self.product_details, width=16)
        self.details_button.grid(row=4, column=1, )

    def place_order(self):
        """Place new order, if all required entry's are filled."""
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled properly
        if self.id_product_entry.get() == '':
            self.error_message("'id product' missing")
        elif not shared.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("'quantity' Must be an positive integer")
        elif self.location_entry.get() == '':
            self.error_message("'location' missing")

        # checking if customer and product exists
        elif not db.is_customer_id_exist(shared.MY_ID) or not db.is_product_id_exists(self.id_product_entry.get()):
            self.error_message("product or customer id not Exists")

        # function itself check if there is enough products, and count total price (quantity*price)
        elif db.add_order(shared.MY_ID, self.id_product_entry.get(), self.quantity_entry.get(), self.location_entry.get()):
            tkinter.messagebox.showinfo("Mendiona bytes", 'successfully added.')
            self.list_products()
        else:
            self.error_message("not enough products in stock.")

    def product_details(self):
        """show details of selected product."""
        if self.error_label:
            self.error_label.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        if self.id_product_entry.get() == '':
            self.error_message("select product.")

        elif db.is_product_id_exists(self.id_product_entry.get()):

            self.function_frame3 = tk.Frame(self.master, bg=shared.BACKGROUND)
            self.function_frame3.pack(side=tk.TOP)

            # creating Message instead of Label (description might be long)
            description = db.return_product(self.id_product_entry.get())[4]
            self.error_label = tk.Message(self.function_frame3, text="Description: {}".format(description), bg=shared.BACKGROUND,
                                          width=300)
            self.error_label.grid(row=5, column=0)
        else:
            self.error_message("Product not exist.")

    def product_selection(self, event):
        """Add's id of selected product to designated entry."""
        # will do sth only if the mouse click was on customer listbox
        if self.products_listbox.curselection():
            search = self.products_listbox.curselection()[0]
            current_record = self.products_listbox.get(search)

            self.id_product_entry.delete(0, tk.END)
            self.id_product_entry.insert(tk.END, current_record[0])

    def order_selection(self, event):
        """Show's details of selected order."""
        if self.my_orders_listbox.curselection():
            search = self.my_orders_listbox.curselection()[0]
            current_record = self.my_orders_listbox.get(search)
            record = db.return_order(current_record[0])

            if self.function_frame2:
                self.function_frame2.destroy()

            self.function_frame2 = tk.Frame(self.master, bg=shared.BACKGROUND)
            self.function_frame2.pack(side=tk.TOP)

            # creating Message instead of Label (long)
            desc = """quantity: \t{}\ntotal_price: \t{}\npayment_status: \t{}
send_status: \t{}\noder_date: \t{}\nlocation: \t{}""" \
                .format(str(record[3]), str(record[4]), str(record[5]), str(record[6]), str(record[7]), str(record[8]))

            self.error_label = tk.Message(self.function_frame2, text="Description:\n{}".format(desc), bg=shared.BACKGROUND,
                                          width=300)
            self.error_label.grid(row=0, column=0)

    def acc_edit(self):
        """Run's new window for editing account."""
        self.master.destroy()
        self.master = tk.Tk()
        AccEdit(self.master)
        self.master.mainloop()

    def my_orders(self):
        """Create's menu with list of user orders."""
        self.initialize_main_buttons()

        self.function_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.function_frame.pack()

        # creating listbox for customers
        list_label = tk.Label(self.function_frame, text='my orders:', width=100, bg=shared.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))
        scrollbar = tk.Scrollbar(self.function_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.my_orders_listbox = tk.Listbox(self.function_frame, width=60, height=15, yscrollcommand=scrollbar.set,
                                            bg=shared.FOREGROUND)
        self.my_orders_listbox.bind('<<ListboxSelect>>', self.order_selection)
        self.my_orders_listbox.grid(row=1, column=0, padx=8)

        # adding records from DB to Listbox
        records = db.orders_product_info(shared.MY_ID)
        for record in records:
            self.my_orders_listbox.insert(tk.END, (str(record[0]), record[1], str(record[2]), str(record[3])))

    def error_message(self, name):
        """Show's passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.function_frame2, text="{}".format(name), bg=shared.BACKGROUND, fg='red')
        self.error_label.grid(row=3, column=1)

    def log_off(self):
        """Return's User to logging window."""
        shared.MY_ID = -1
        self.master.destroy()
        self.master = tk.Tk()
        LoginWindow.LoginWindow(self.master)
        self.master.mainloop()


class AccEdit:
    """Customer window for editing account."""
    def __init__(self, master):
        """Initializes editing account window."""
        self.master = master
        self.master.configure(bg=shared.BACKGROUND)
        self.master.title('Mendiona bytes')

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = tk.Label()

        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()

        # Create text box labels
        new_password_label = tk.Label(self.frame, text='new password(opt):', bg=shared.BACKGROUND)
        new_password_label.grid(row=0, column=0, sticky=tk.E)
        password_label = tk.Label(self.frame, text='password:', bg=shared.BACKGROUND)
        password_label.grid(row=1, column=0, sticky=tk.E)
        name_label = tk.Label(self.frame, text='name:', bg=shared.BACKGROUND)
        name_label.grid(row=2, column=0, sticky=tk.E)
        phone_label = tk.Label(self.frame, text='phone:', bg=shared.BACKGROUND)
        phone_label.grid(row=3, column=0, sticky=tk.E)
        email_label = tk.Label(self.frame, text='email:', bg=shared.BACKGROUND)
        email_label.grid(row=4, column=0, sticky=tk.E)

        # Create Entry box
        self.new_password_entry = tk.Entry(self.frame, width=22, show='*', bg=shared.FOREGROUND)
        self.new_password_entry.grid(row=0, column=1)
        self.password_entry = tk.Entry(self.frame, width=22, show='*', bg=shared.FOREGROUND)
        self.password_entry.grid(row=1, column=1)
        self.name_entry = tk.Entry(self.frame, width=22, bg=shared.FOREGROUND)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = tk.Entry(self.frame, width=22, bg=shared.FOREGROUND)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = tk.Entry(self.frame, width=22, bg=shared.FOREGROUND)
        self.email_entry.grid(row=4, column=1)

        # Create Buttons
        self.change_button = tk.Button(self.frame, text='change', bg=shared.FOREGROUND, command=self.set_change, width=16)
        self.change_button.grid(row=0, column=2, padx=20)
        self.cancel_button = tk.Button(self.frame, text='Cancel', bg=shared.FOREGROUND, command=self.exit, width=16)
        self.cancel_button.grid(row=1, column=2)

        # getting customer info from DB
        customer_info = db.return_customer(shared.MY_ID)
        if customer_info:
            self.name_entry.insert(tk.END, customer_info[3])
            self.phone_entry.insert(tk.END, customer_info[4])
            self.email_entry.insert(tk.END, customer_info[5])
        else:
            tkinter.messagebox.showinfo("Mendiona bytes", 'ERROR: WRONG ID!!!')
            self.exit()

    def set_change(self):
        """Change's customer account details if all required entry's are filled properly."""
        if self.error_label:
            self.error_label.destroy()

        # if new password entry is empty don't update it
        if 0 < len(self.new_password_entry.get()) < 6:
            self.error_message('new password is too short.')

        # checking if all required entry's are filled properly
        elif self.password_entry.get() != db.return_customer(shared.MY_ID)[2]:
            self.error_message('password does not match.')
        elif self.name_entry.get() == '':
            self.error_message('Can not update empty name.')
        elif self.phone_entry.get() != '' and not shared.is_integer(self.phone_entry.get()):
            self.error_message("wrong phone number.")
        elif self.email_entry.get() == '':
            self.error_message('Can not update empty email.')

        else:
            # if all entry's are filled correctly

            if self.new_password_entry != '':
                # passing new password
                db.edit_customer(shared.MY_ID, self.new_password_entry.get(), self.name_entry.get(), self.email_entry.get(),
                                 self.phone_entry.get())
            else:
                # passing old password to function (no change)
                db.edit_customer(shared.MY_ID, db.return_customer(shared.MY_ID)[2], self.name_entry.get(),
                                 self.email_entry.get(), self.phone_entry.get())

            self.error_message("Account has been updated.")

    def error_message(self, name):
        """Show's passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, fg='red', text='{}'.format(name), bg=shared.BACKGROUND)
        self.error_label.grid(row=5, column=1)

    def exit(self):
        """Run's back main customer window."""
        self.master.destroy()
        self.master = tk.Tk()
        CustomerApp(self.master)
        self.master.mainloop()
