import sqlite3
import tkinter as tk
import tkinter.messagebox

import dbmanager as db
import shared

conn = sqlite3.connect('dataa.db')
c = conn.cursor()


class CustomersMenu:

    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500+0+0")
        self.master.configure(bg=shared.BACKGROUND)

        # frame for main muttons (customer,order,product)
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()
        # frame for all entrys, function buttons and labels
        self.entry_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.entry_frame.pack()
        # frame for listbox and scrollbar
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = tk.Label()

        self.initialize_menu()

    def initialize_menu(self):
        # Destroying last frame and creating initializing menu
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()

        self.entry_frame.destroy()
        self.entry_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.entry_frame.pack()

        self.listbox_frame.destroy()
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        if self.error_label:
            self.error_label.destroy()

        # Create Main Buttons To Chose Which Table You Want To Add
        c_chose_button = tk.Button(self.frame, text='Customer', command=self.initialize_menu, width=30, bg=shared.FOREGROUND)
        c_chose_button.grid(row=0, column=0, pady=10)
        o_chose_button = tk.Button(self.frame, text='Order', command=self.goto_order_window, width=30, bg=shared.FOREGROUND)
        o_chose_button.grid(row=0, column=1, )
        p_chose_button = tk.Button(self.frame, text='Product', command=self.goto_product_window, width=30, bg=shared.FOREGROUND)
        p_chose_button.grid(row=0, column=2)

        # Create text box labels for Customers
        login_label = tk.Label(self.entry_frame, text='login:', bg=shared.BACKGROUND)
        login_label.grid(row=1, column=0, sticky=tk.E)
        name_label = tk.Label(self.entry_frame, text='Customer name:', bg=shared.BACKGROUND)
        name_label.grid(row=2, column=0, sticky=tk.E)
        phone_label = tk.Label(self.entry_frame, text='Customer phone(optional):', bg=shared.BACKGROUND)
        phone_label.grid(row=3, column=0, sticky=tk.E)
        email_label = tk.Label(self.entry_frame, text='Customer email:', bg=shared.BACKGROUND)
        email_label.grid(row=4, column=0, sticky=tk.E)
        perm_label = tk.Label(self.entry_frame, text='Perm:', bg=shared.BACKGROUND)
        perm_label.grid(row=5, column=0, sticky=tk.E)

        # Create Entry box for Customers
        self.login_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.login_entry.grid(row=1, column=1)
        self.name_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.email_entry.grid(row=4, column=1)
        self.perm_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.perm_entry.grid(row=5, column=1)

        # search, clear, delete, update, exit buttons
        search_button = tk.Button(self.entry_frame, text='Search', command=self.search_customer, width=20, bg=shared.FOREGROUND)
        search_button.grid(row=1, column=2, padx=20)
        update_button = tk.Button(self.entry_frame, text='Update', command=self.update_customer, width=20, bg=shared.FOREGROUND)
        update_button.grid(row=2, column=2)
        clear_button = tk.Button(self.entry_frame, text='Clear', command=self.clear_customer_entrys, width=20, bg=shared.FOREGROUND)
        clear_button.grid(row=3, column=2)
        exit_button = tk.Button(self.entry_frame, text='Delete', command=self.delete_customer, width=20, bg=shared.FOREGROUND)
        exit_button.grid(row=4, column=2)

        # creating listbox for customers
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        list_label = tk.Label(self.listbox_frame, text='list of customers', width=100, bg=shared.BACKGROUND)
        list_label.grid(row=0, column=0)
        scrollbar = tk.Scrollbar(self.listbox_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.listbox = tk.Listbox(self.listbox_frame, width=60, height=15, yscrollcommand=scrollbar.set, bg=shared.FOREGROUND)
        self.listbox.bind('<<ListboxSelect>>', self.get_selected_customer)
        self.listbox.grid(row=1, column=0, padx=8)

        # adding records from DB to Listbox
        records = db.return_customers()
        for record in records:
            self.listbox.insert(tk.END, (str(record[0]), record[1], record[2], record[3], record[4], str(record[5])))

    def clear_customer_entrys(self):
        if self.error_label:
            self.error_label.destroy()

        self.login_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.perm_entry.delete(0, tk.END)

    def search_customer(self):
        if self.error_label:
            self.error_label.destroy()

        records = db.search_customer(self.login_entry.get(), self.name_entry.get(), self.phone_entry.get(),
                                     self.email_entry.get(), self.perm_entry.get())
        self.listbox.delete(0, tk.END)
        for record in records:
            self.listbox.insert(tk.END, (str(record[0]), record[1], record[2], record[3], record[4], str(record[5])))

    def delete_customer(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if anything is selected from the listbox
        if not self.listbox.curselection():
            self.error_message("please select one from lisbox.")
            return

        # finding selected Customer
        index = self.listbox.curselection()[0]
        selected_record = self.listbox.get(index)
        records = db.delete_customer(selected_record[0], 1)

        # if there is record in DB with such id
        if records:
            # there has to be for loop, because single line return error: 'list out of range'
            customer_info = ''
            for record in records:
                customer_info = "{}\n{}\n{}".format(record[0], record[1], record[2])

            # window asking to delete
            answer = tkinter.messagebox.askquestion('myShop DBMS', "Delete:\n{}".format(customer_info))
            if answer == 'yes':
                db.delete_customer(selected_record[0], 0)
                # refreshing all
                self.initialize_menu()

        # if there was no record with such id
        else:
            self.error_message("record not exists in database.")

    def update_customer(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if any record from LISTBOX is selected
        if not self.listbox.curselection():
            self.error_message("please select one from listbox.")
            return

        # checking if every required value for update is filled properly
        if self.login_entry.get() == '':
            self.error_message("Can not update empty login.")
        elif self.name_entry.get() == '':
            self.error_message("Can not update empty name.")
        elif self.email_entry.get() == '':
            self.error_message("Can not update empty email.")
        elif self.perm_entry.get() != '0' and self.perm_entry.get() != '1':
            self.error_message("perm must be int 0 or 1")

        # phone number is optional but if filled it must be int
        elif self.phone_entry.get() != '' and not shared.is_integer(self.phone_entry.get()):
            self.error_message("wrong phone number.")

        # everything is filled finally updating
        else:
            index = self.listbox.curselection()[0]
            current_record = self.listbox.get(index)
            db.update_customer(current_record[0], self.login_entry.get(), self.name_entry.get(),
                               self.email_entry.get(), self.phone_entry.get(), self.perm_entry.get())

            # refresh all
            self.initialize_menu()

    def get_selected_customer(self, event):
        self.clear_customer_entrys()
        if self.error_label:
            self.error_label.destroy()

        search = self.listbox.curselection()[0]
        current_record = self.listbox.get(search)

        self.login_entry.insert(tk.END, current_record[1])
        self.name_entry.insert(tk.END, current_record[2])
        self.phone_entry.insert(tk.END, current_record[3])
        self.email_entry.insert(tk.END, current_record[4])
        self.perm_entry.insert(tk.END, current_record[5])

    def error_message(self, name):
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.entry_frame, text=("?", (name, )), bg=shared.BACKGROUND)
        self.error_label.grid(row=6, column=1)

    def goto_order_window(self):
        self.master.destroy()
        self.master = tk.Tk()
        app = OrdersMenu(self.master)
        self.master.mainloop()

    def goto_product_window(self):
        self.master.destroy()
        self.master = tk.Tk()
        app = ProductsMenu(self.master)
        self.master.mainloop()


class ProductsMenu:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500+0+0")
        self.master.configure(bg=shared.BACKGROUND)

        # frame for main muttons (customer,order,product)
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()
        # frame for all entrys, function buttons and labels
        self.entry_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.entry_frame.pack()
        # frame for listbox and scrollbar
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = tk.Label()

        self.initialize_menu()

    def initialize_menu(self):
        # Destroying last frame and creating initializing menu
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()

        self.entry_frame.destroy()
        self.entry_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.entry_frame.pack()

        self.listbox_frame.destroy()
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        if self.error_label:
            self.error_label.destroy()

        # Create Main Buttons To Chose Which Table You Want To Add
        c_chose_button = tk.Button(self.frame, text='Customer', command=self.goto_customer_window, width=30, bg=shared.FOREGROUND)
        c_chose_button.grid(row=0, column=0, pady=10)
        o_chose_button = tk.Button(self.frame, text='Order', command=self.goto_order_window, width=30, bg=shared.FOREGROUND)
        o_chose_button.grid(row=0, column=1, )
        p_chose_button = tk.Button(self.frame, text='Product', command=self.initialize_menu, width=30, bg=shared.FOREGROUND)
        p_chose_button.grid(row=0, column=2)

        # Create text box labels for Products
        product_name_label = tk.Label(self.entry_frame, text='Product name:', bg=shared.BACKGROUND)
        product_name_label.grid(row=0, column=0, sticky=tk.E)
        product_price_label = tk.Label(self.entry_frame, text='Product price:', bg=shared.BACKGROUND)
        product_price_label.grid(row=1, column=0, sticky=tk.E)
        in_stock_label = tk.Label(self.entry_frame, text='in stock:', bg=shared.BACKGROUND)
        in_stock_label.grid(row=2, column=0, sticky=tk.E)
        description_label = tk.Label(self.entry_frame, text='description(optional):', bg=shared.BACKGROUND)
        description_label.grid(row=3, column=0, sticky=tk.E)

        # Create Entry Box for Products
        self.product_name_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.product_name_entry.grid(row=0, column=1)
        self.product_price_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.product_price_entry.grid(row=1, column=1)
        self.in_stock_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.in_stock_entry.grid(row=2, column=1)
        self.description_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.description_entry.grid(row=3, column=1)

        # buttons
        # search_button = Button(self.frame, text='Search for ID', width=20)
        add_button = tk.Button(self.entry_frame, text='Add', command=self.add_product, width=20, bg=shared.FOREGROUND)
        add_button.grid(row=0, column=2, padx=20)
        search_button = tk.Button(self.entry_frame, text='Search', command=self.search_product, width=20, bg=shared.FOREGROUND)
        search_button.grid(row=1, column=2)
        update_button = tk.Button(self.entry_frame, text='Update', command=self.update_product, width=20, bg=shared.FOREGROUND)
        update_button.grid(row=2, column=2)
        clear_button = tk.Button(self.entry_frame, text='Clear', command=self.clear_product_entrys, width=20, bg=shared.FOREGROUND)
        clear_button.grid(row=3, column=2)
        delete_button = tk.Button(self.entry_frame, text='Delete', command=self.delete_product, width=20, bg=shared.FOREGROUND)
        delete_button.grid(row=4, column=2)

        # creating listbox for customers
        list_label = tk.Label(self.listbox_frame, text='list of products', width=100, bg=shared.BACKGROUND)
        list_label.grid(row=0, column=0)
        scrollbar = tk.Scrollbar(self.listbox_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.listbox = tk.Listbox(self.listbox_frame, width=60, height=15, yscrollcommand=scrollbar.set, bg=shared.FOREGROUND)
        self.listbox.bind('<<ListboxSelect>>', self.get_selected_product)
        self.listbox.grid(row=1, column=0, padx=8)

        # adding records from DB to Listbox
        records = db.return_products()
        for record in records:
            self.listbox.insert(tk.END, (str(record[0]), record[1], str(record[2]), str(record[3]), record[4]))

    def clear_product_entrys(self):
        if self.error_label:
            self.error_label.destroy()

        self.product_name_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.in_stock_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def add_product(self):
        # deleting missing label from last add_order call, if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled correctly
        if self.product_name_entry.get() == '':
            self.error_message("'product name' missing")
        elif not shared.is_float(self.product_price_entry.get()) or float(self.product_price_entry.get()) < 1.0:
            self.error_message("'product price' must be positive int")
        elif not shared.is_integer(self.in_stock_entry.get()) or int(self.in_stock_entry.get()) < 0:
            self.error_message("'in stock' value must be non negative int")

        # if everything is filled
        else:
            with conn:
                # if product exists -> print error ELSE add
                if db.is_product_exists(self.product_name_entry.get()):
                    self.error_message("'{}' Exists".format(self.product_name_entry.get()))

                else:
                    db.add_product(self.product_name_entry.get(), self.product_price_entry.get(),
                                   self.in_stock_entry.get(), self.description_entry.get())

                    # showing clear new window
                    self.initialize_menu()

    def search_product(self):
        if self.error_label:
            self.error_label.destroy()

        self.listbox.delete(0, tk.END)
        records = db.search_products(self.product_name_entry.get(), self.product_price_entry.get(),
                                     self.in_stock_entry.get(), self.description_entry.get())
        for record in records:
            self.listbox.insert(tk.END, (str(record[0]), record[1], str(record[2]), str(record[3]), record[4]))

    def delete_product(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if anything is selected
        if not self.listbox.curselection():
            self.error_message("please select one from listbox.")
            return

        # finding selected product
        index = self.listbox.curselection()[0]
        selected_record = self.listbox.get(index)
        records = db.delete_product(selected_record[0], 1)

        # if there is record in DB with such id
        if records:
            # there has to be for loop, because single line return error: 'list out of range'
            product_info = ''
            for record in records:
                product_info = "{}\n{}\n{}".format(record[1], record[2], record[3])

            # window asking to delete
            answer = tkinter.messagebox.askquestion('myShop DBMS', "Delete:\n{}".format(product_info))
            if answer == 'yes':
                db.delete_product(selected_record[0], 0)
                # refreshing all
                self.initialize_menu()

        # if there was no record with such id
        else:
            self.error_message("record not exists in database.")

    def update_product(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if any record from LISTBOX is selected
        if not self.listbox.curselection():
            self.error_message("please select one from listbox.")
            return

        # checking if all required entry's are filled correctly
        if self.product_name_entry.get() == '':
            self.error_message("'product name' missing")
        elif not shared.is_float(self.product_price_entry.get()) or float(self.product_price_entry.get()) < 1.0:
            self.error_message("'product price' must be positive int")
        elif not shared.is_integer(self.in_stock_entry.get()) or int(self.in_stock_entry.get()) < 0:
            self.error_message("'in stock' value must be non negative int")

        else:
            # everything is filled updating
            index = self.listbox.curselection()[0]
            current_record = self.listbox.get(index)
            db.update_product(current_record[0], self.product_name_entry.get(), self.product_price_entry.get(),
                              self.in_stock_entry.get(), self.description_entry.get())

            # refresh all
            self.initialize_menu()

    def get_selected_product(self, event):
        self.clear_product_entrys()
        if self.error_label:
            self.error_label.destroy()

        search = self.listbox.curselection()[0]
        current_record = self.listbox.get(search)

        self.product_name_entry.insert(tk.END, current_record[1])
        self.product_price_entry.insert(tk.END, current_record[2])
        self.in_stock_entry.insert(tk.END, current_record[3])
        self.description_entry.insert(tk.END, current_record[4])

    def error_message(self, name):
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.entry_frame, text="{}".format(name), bg=shared.BACKGROUND)
        self.error_label.grid(row=4, column=1)

    def goto_order_window(self):
        self.master.destroy()
        self.master = tk.Tk()
        app = OrdersMenu(self.master)
        self.master.mainloop()

    def goto_customer_window(self):
        self.master.destroy()
        self.master = tk.Tk()
        app = CustomersMenu(self.master)
        self.master.mainloop()


class OrdersMenu:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500+0+0")
        self.master.configure(bg=shared.BACKGROUND)

        # frame for main muttons (customer,order,product)
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()
        # frame for all entrys, function buttons and labels
        self.entry_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.entry_frame.pack()
        # frame for listbox and scrollbar
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = tk.Label()

        self.initialize_menu()

    def initialize_menu(self):
        # Destroying last frame and creating initializing menu
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.frame.pack()

        self.entry_frame.destroy()
        self.entry_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.entry_frame.pack()

        self.listbox_frame.destroy()
        self.listbox_frame = tk.Frame(self.master, bg=shared.BACKGROUND)
        self.listbox_frame.pack()

        if self.error_label:
            self.error_label.destroy()

        # Create Main Buttons To Chose Which Table You Want To Add
        c_chose_button = tk.Button(self.frame, text='Customer', command=self.goto_customer_window, width=30, bg=shared.FOREGROUND)
        c_chose_button.grid(row=0, column=0, pady=10)
        o_chose_button = tk.Button(self.frame, text='Order', command=self.initialize_menu, width=30, bg=shared.FOREGROUND)
        o_chose_button.grid(row=0, column=1, )
        p_chose_button = tk.Button(self.frame, text='Product', command=self.goto_product_window, width=30, bg=shared.FOREGROUND)
        p_chose_button.grid(row=0, column=2)

        # Create text box labels for Orders
        id_customer_label = tk.Label(self.entry_frame, text='Customer ID:', bg=shared.BACKGROUND)
        id_customer_label.grid(row=0, column=0, sticky=tk.E)
        id_product_label = tk.Label(self.entry_frame, text='Product ID:', bg=shared.BACKGROUND)
        id_product_label.grid(row=1, column=0, sticky=tk.E)
        quantity_label = tk.Label(self.entry_frame, text='Quantity:', bg=shared.BACKGROUND)
        quantity_label.grid(row=2, column=0, sticky=tk.E)
        payment_status_label = tk.Label(self.entry_frame, text='payment status:', bg=shared.BACKGROUND)
        payment_status_label.grid(row=3, column=0, sticky=tk.E)
        send_status_label = tk.Label(self.entry_frame, text='send status:', bg=shared.BACKGROUND)
        send_status_label.grid(row=4, column=0, sticky=tk.E)
        location_label = tk.Label(self.entry_frame, text='location:', bg=shared.BACKGROUND)
        location_label.grid(row=5, column=0, sticky=tk.E)

        # Create Entry Box for Orders
        self.id_customer_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.id_customer_entry.grid(row=0, column=1)
        self.id_product_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.id_product_entry.grid(row=1, column=1)
        self.quantity_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.quantity_entry.grid(row=2, column=1)
        self.payment_status_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.payment_status_entry.grid(row=3, column=1)
        self.send_status_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.send_status_entry.grid(row=4, column=1)
        self.location_entry = tk.Entry(self.entry_frame, width=30, bg=shared.FOREGROUND)
        self.location_entry.grid(row=5, column=1)

        # buttons
        search_button = tk.Button(self.entry_frame, text='Search', command=self.search_order, width=20, bg=shared.FOREGROUND)
        search_button.grid(row=0, column=2, padx=20)
        add_button = tk.Button(self.entry_frame, text='Add', command=self.add_order, width=20, bg=shared.FOREGROUND)
        add_button.grid(row=1, column=2, padx=20)
        clear_button = tk.Button(self.entry_frame, text='Clear', command=self.initialize_menu, width=20, bg=shared.FOREGROUND)
        clear_button.grid(row=2, column=2)
        delete_button = tk.Button(self.entry_frame, text='Delete', command=self.delete_order, width=20, bg=shared.FOREGROUND)
        delete_button.grid(row=3, column=2)
        exit_button = tk.Button(self.entry_frame, text='Exit', command=self.master.destroy, width=20, bg=shared.FOREGROUND)
        exit_button.grid(row=4, column=2)

        # Listbox'es
        # creating listbox for orders
        list_label = tk.Label(self.listbox_frame, text='list of orders', bg=shared.BACKGROUND)
        list_label.grid(row=0, column=0)
        scrollbar = tk.Scrollbar(self.listbox_frame)
        scrollbar.grid(row=1, column=0)
        self.order_listbox = tk.Listbox(self.listbox_frame, width=50, height=15, yscrollcommand=scrollbar.set, bg=shared.FOREGROUND)
        self.order_listbox.bind('<<ListboxSelect>>', self.order_list_manager)
        self.order_listbox.grid(row=1, column=0, padx=8)

        # create listbox for products
        list_label1 = tk.Label(self.listbox_frame, text='list of products', width=25, bg=shared.BACKGROUND)
        list_label1.grid(row=0, column=1)
        scrollbar1 = tk.Scrollbar(self.listbox_frame)
        scrollbar1.grid(row=1, column=1)
        self.product_listbox = tk.Listbox(self.listbox_frame, width=40, height=15,
                                          yscrollcommand=scrollbar1.set, bg=shared.FOREGROUND)
        self.product_listbox.bind('<<ListboxSelect>>', self.product_list_manager)
        self.product_listbox.grid(row=1, column=1, padx=8)

        # create listbox for customers
        list_label2 = tk.Label(self.listbox_frame, text='list of customers', width=25, bg=shared.BACKGROUND)
        list_label2.grid(row=0, column=2)
        scrollbar2 = tk.Scrollbar(self.listbox_frame)
        scrollbar2.grid(row=1, column=2)
        self.customer_listbox = tk.Listbox(self.listbox_frame, width=40, height=15, yscrollcommand=scrollbar2.set,
                                           bg=shared.FOREGROUND)
        self.customer_listbox.bind('<<ListboxSelect>>', self.customer_list_manager)
        self.customer_listbox.grid(row=1, column=2, padx=8)

        # adding records from DB to Listbox (orders)
        records = db.return_orders()
        for record in records:
            self.order_listbox.insert(tk.END, (
                str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[5]), str(record[6]),
                str(record[7]), record[8]))

        # adding records from DB to Listbox (products)
        records = db.return_products()
        for record in records:
            self.product_listbox.insert(tk.END, (str(record[0]), record[1], str(record[2]), str(record[3])))

        # adding records from DB to Listbox (customers)
        records = db.return_customers()
        for record in records:
            self.customer_listbox.insert(tk.END, (str(record[0]), record[2], record[4]))

        # adding records from DB to Listbox

    def add_order(self):
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        # checking if all required entry's are filled properly
        if self.id_customer_entry.get() == '':
            self.error_message("'id customer' missing")
        elif self.id_product_entry.get() == '':
            self.error_message("'id product' missing")
        elif not shared.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("'quantity' Must be an positive integer")
        elif self.payment_status_entry.get() != '0' and self.payment_status_entry.get() != '1':
            self.error_message("'payment status' Must be an 0 or 1 int")
        elif self.send_status_entry.get() != '0' and self.send_status_entry.get() != '1':
            self.error_message("'send status' Must be an 0 or 1 int")
        elif self.location_entry.get() == '':
            self.error_message("'location' missing")

        # checking if customer and product exists
        elif not db.is_customer_id_exist(self.id_customer_entry.get()) or not db.is_product_id_exists(
                self.id_product_entry.get()):
            self.error_message("product or customer id not Exists")

        # function itself check if there is enough products, and count total price (quantity*price)
        elif db.add_order(self.id_customer_entry.get(), self.id_product_entry.get(), self.quantity_entry.get(),
                          self.location_entry.get(), self.payment_status_entry.get(), self.send_status_entry.get()):

            self.initialize_menu()
        else:
            self.error_message("insufficient number of products on disposal")

    def delete_order(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if anything is selected
        if not self.order_listbox.curselection():
            self.error_message("please select one from listbox.")
            return

        # window asking to delete
        answer = tkinter.messagebox.askquestion('myShop DBMS', 'Delete:\n')
        if answer == 'yes':
            # finding selected order
            index = self.order_listbox.curselection()[0]
            selected_record = self.order_listbox.get(index)
            db.delete_order(selected_record[0])

            # refreshing all
            self.initialize_menu()

    def search_order(self):
        if self.error_label:
            self.error_label.destroy()

        self.order_listbox.delete(0, tk.END)
        records = db.search_orders(self.id_product_entry.get(), self.id_customer_entry.get(), self.quantity_entry.get(),
                                   self.payment_status_entry.get(), self.location_entry.get())
        for record in records:
            self.order_listbox.insert(tk.END, (
                str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[5]), str(record[6]),
                str(record[7]), record[8]))

    def order_list_manager(self, event):
        if self.error_label:
            self.error_label.destroy()

        # will do sth only if the mouse click was on customer listbox not other listbox'es
        if self.order_listbox.curselection():
            search = self.order_listbox.curselection()[0]
            current_record = self.order_listbox.get(search)

            self.id_customer_entry.delete(0, tk.END)
            self.id_product_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.payment_status_entry.delete(0, tk.END)
            self.send_status_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)

            self.id_customer_entry.insert(tk.END, current_record[1])
            self.id_product_entry.insert(tk.END, current_record[2])
            self.quantity_entry.insert(tk.END, current_record[3])
            self.payment_status_entry.insert(tk.END, current_record[4])
            self.send_status_entry.insert(tk.END, current_record[5])
            self.location_entry.insert(tk.END, current_record[7])

            # inserting customer info
            record = db.return_customer(current_record[1])
            self.customer_listbox.delete(0, tk.END)
            self.customer_listbox.insert(tk.END, (str(record[0]), record[3], record[5]))

            # inserting product info
            record = db.return_product(current_record[2])
            self.product_listbox.delete(0, tk.END)
            self.product_listbox.insert(tk.END, (str(record[0]), record[1], str(record[2]), str(record[3])))

    def product_list_manager(self, event):
        if self.error_label:
            self.error_label.destroy()

        # will do sth only if the mouse click was on product listbox not other listbox'es
        if self.product_listbox.curselection():
            search = self.product_listbox.curselection()[0]
            current_record = self.product_listbox.get(search)
            self.id_product_entry.delete(0, tk.END)
            self.id_product_entry.insert(tk.END, current_record[0])

            # inserting selected customer Orders
            records = db.return_product_orders(current_record[0])
            self.order_listbox.delete(0, tk.END)
            for record in records:
                self.order_listbox.insert(tk.END, (
                    str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[5]), str(record[6]),
                    str(record[7]), record[8]))

    def customer_list_manager(self, event):
        if self.error_label:
            self.error_label.destroy()

        # will do sth only if the mouse click was on customer listbox not other listbox'es
        if self.customer_listbox.curselection():
            search = self.customer_listbox.curselection()[0]
            current_record = self.customer_listbox.get(search)
            self.id_customer_entry.delete(0, tk.END)
            self.id_customer_entry.insert(tk.END, current_record[0])

            # inserting selected customer Orders
            records = db.return_customer_orders(current_record[0])
            self.order_listbox.delete(0, tk.END)
            for record in records:
                self.order_listbox.insert(tk.END, (
                    str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[5]), str(record[6]),
                    str(record[7]), record[8]))

    def error_message(self, name):
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, text="{}".format(name), bg=shared.BACKGROUND)
        self.error_label.grid(row=11, column=1)

    def goto_customer_window(self):
        self.master.destroy()
        self.master = tk.Tk()
        app = CustomersMenu(self.master)
        self.master.mainloop()

    def goto_product_window(self):
        self.master.destroy()
        self.master = tk.Tk()
        app = ProductsMenu(self.master)
        self.master.mainloop()
