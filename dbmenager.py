import sqlite3

conn = sqlite3.connect('dataa.db')
c = conn.cursor()


def initialize():
    """Create tables if not existing."""
    c.execute(("""
    CREATE TABLE IF NOT EXISTS Customers(
    id_customer   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    login         TEXT    NOT NULL,
    password      TEXT    NOT NULL,
    customer_name TEXT    NOT NULL,
    phone         TEXT    DEFAULT (0) NOT NULL,
    email         TEXT    NOT NULL,
    perm          INT     NOT NULL DEFAULT (0) 
    )"""))

    c.execute("""
    CREATE TABLE IF NOT EXISTS Orders(
    id_order       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id_customer    INTEGER NOT NULL,
    id_product     INTEGER NOT NULL,
    quantity       INTEGER NOT NULL,
    total_price    DOUBLE  NOT NULL,
    payment_status INTEGER NOT NULL DEFAULT (0),
    send_status    INTEGER NOT NULL DEFAULT (0),
    order_date     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    location       TEXT    NOT NULL,
    
    FOREIGN KEY (id_customer) REFERENCES Customers (id_customer) 
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (id_product) REFERENCES Products (id_product) 
    ON DELETE SET NULL
    ON UPDATE CASCADE
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id_product    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    product_name  TEXT    NOT NULL,
    product_price DOUBLE  NOT NULL,
    in_stock      INTEGER NOT NULL,
    description   TEXT
    )""")


def is_customer_exists(login, email):
    """Returns false if not exist, or login/email depending on which exists in db."""
    c.execute("SELECT * from Customers WHERE login = '{}'".format(login))
    if c.fetchone() != None:
        return "login"

    c.execute("SELECT * from Customers WHERE email = '{}'".format(email))
    if c.fetchone() != None:
        return "mail"
    return False


def is_customer_id_exitst(id) -> bool:
    """Returns True or False depending if customer exists."""
    with conn:
        c.execute("SELECT id_customer from Customers WHERE id_customer =?", (id,))
        if c.fetchone() != None:
            return True
        else:
            return False


def addCustomer(login, passw, name, phone, email):
    """Adding new customer to DB."""
    with conn:
        c.execute("INSERT INTO Customers(login,password,customer_name,phone,email) VALUES(?,?,?,?,?)",
                  (login, passw, name, phone, email))


def returnCustomers():
    """Returns list of all customers in DB."""
    c.execute("SELECT id_customer,login,customer_name,phone,email,perm FROM Customers")
    rows = c.fetchall()
    return rows


def returnCustomer(id):
    """Returns single customer or False."""
    with conn:
        c.execute("SELECT * FROM Customers WHERE id_customer=?", (id,))
        row = c.fetchone()
        if row == None:
            return False
        else:
            return row


def searchCustomer(login="", name="", phone="", email="", perm=""):
    """Returns customers that meet at least 1 of passed args."""
    with conn:
        c.execute(
            "SELECT id_customer,login,customer_name,phone,email,perm FROM Customers WHERE login=? OR customer_name=? OR phone=? OR email=? or perm=?",
            (login, name, phone, email, perm))
        rows = c.fetchall()
        return rows


def deleteCustomer(id, check_if_exists=1):
    """Delete or check if customer exists.

    when 0 passed it delete's the customer.
    when 1 passed it returns customer or False depending on if it exists."""
    with conn:
        if check_if_exists == 1:
            c.execute("SELECT login, customer_name, email FROM Customers WHERE id_customer=?", (id,))
            records = c.fetchall()
            if records == None:
                return False
            else:
                return records
        else:
            c.execute("DELETE FROM Customers WHERE id_customer=?", (id,))


def updateCustomer(id, login, name, email, phone="", perm=0):
    """Update's Customer by given id."""
    with conn:
        c.execute("UPDATE Customers SET login=?, customer_name=?, phone=?, email=?, perm=? WHERE id_customer=?",
                  (login, name, phone, email, perm, id))


def editCustomer(id, password, name, email, phone):
    """Edit's Customer by given id."""
    with conn:
        c.execute("UPDATE Customers SET password=?, customer_name=?, phone=?, email=? WHERE id_customer=?",
                  (password, name, phone, email, id))


def customerPerm(login, password):
    """Returns Customer info tuple(id, perm) or (false, -1) if not exists."""
    with conn:
        c.execute("SELECT id_customer,perm from Customers WHERE login=? and password=?", (login, password))
        record = c.fetchone()
        if record == None:
            return False, -1
        else:
            return record[0], record[1]


# products ---------------------------------------------------------------


# returns true or false, whether the product exists
def is_product_exists(prod_name) -> bool:
    """Returns True or False depending if product with given name exists."""
    c.execute("SELECT * from Products WHERE product_name = '{}'".format(prod_name))
    if c.fetchone() != None:
        return True
    return False


def is_product_id_exists(id) -> bool:
    """Returns True or False depending if product with given id exists."""
    with conn:
        c.execute("SELECT id_product from Products WHERE id_product =?", (id,))
        if c.fetchone() != None:
            return True
        else:
            return False

def returnProduct(id):
    """Returns product by given id."""
    with conn:
        c.execute("SELECT * FROM Products WHERE id_product=?", (id,))
        return c.fetchone()


def returnProducts():
    """Returns list of all products."""
    with conn:
        c.execute("SELECT id_product, product_name, product_price, in_stock, description FROM Products")
        records = c.fetchall()
        return records


def addProduct(name, price, stock, desc):
    """Adding new product to DB."""
    with conn:
        c.execute("INSERT INTO Products(product_name, product_price, in_stock, description) VALUES (?,?,?,?)",
                  (name, price, stock, desc,)
                  )


def searchProducts(name='', price='', stock='', desc=''):
    """Returns products that meet at least 1 of passed args."""
    with conn:
        if desc != '':
            c.execute("SELECT * FROM Products WHERE product_name=? OR product_price=? OR in_stock=? OR description=?",
                      (name, price, stock, desc,))
        else:
            c.execute("SELECT * FROM Products WHERE product_name=? OR product_price=? OR in_stock=?",
                      (name, price, stock,))
        records = c.fetchall()
        return records


# if sec value is not passed it only check and return the value if it exists
def deleteProduct(id, check_if_exists=1):
    """Delete or check if product exists.

    when 0 passed it delete's the product.
    when 1 passed it returns product or False depending on if it exists."""
    with conn:
        if check_if_exists == 1:
            c.execute("SELECT * FROM Products WHERE id_product=?", (id,))
            records = c.fetchall()
            if records == None:
                return False
            else:
                return records
        else:
            c.execute("DELETE FROM Products WHERE id_product=?", (id,))


def updateProduct(id, name, price, stock, desc):
    """Updates Customer by given id."""
    with conn:
        c.execute("UPDATE Products SET product_name=?, product_price=?, in_stock=?, description=? WHERE id_product=?",
                  (name, price, stock, desc, id,))


def returnOrders():
    """Returns list of all Orders in DB."""
    with conn:
        c.execute("SELECT * FROM Orders")
    records = c.fetchall()
    return records


def returnProductOrders(id_p):
    """Returns list of Orders that refers to passed product id."""
    with conn:
        c.execute("SELECT * FROM Orders Where id_product=?", (id_p,))
        return c.fetchall()


def returnCustomerOrders(id_c):
    """Returns list of Orders that refers to passed customer id."""
    with conn:
        c.execute("SELECT * FROM Orders Where id_customer=?", (id_c,))
        return c.fetchall()


def addOrder(id_c, id_p, quantity, location, payment_status=0, send_status=0):
    """Add new order to DB, return False if not enough products in stock."""
    in_stock = returnProduct(id_p)[3]
    if in_stock - float(quantity) < 0:
        return False
    else:
        with conn:
            # decreasing number of products in stock
            c.execute("UPDATE Products SET in_stock=? WHERE id_product=?", (in_stock - float(quantity), id_p))

            # adding new Order
            total_price = float(returnProduct(id_p)[2]) * float(quantity)
            c.execute("""INSERT INTO Orders(id_customer, id_product, quantity, total_price, payment_status, 
            send_status, location) VALUES(?,?,?,?,?,?,?)""",
                      (id_c, id_p, quantity, total_price, payment_status, send_status, location))
            return True


def ordersProductInfo(id):
    """Returns specialized columns from Orders and products by given id.

    Returns order id, product name, quantity, total price of order."""
    with conn:
        c.execute(
            "SELECT o.id_order,p.product_name,o.quantity,o.total_price FROM Orders AS o NATURAL JOIN Products AS p WHERE o.id_customer=?",
            (id,))
        rows = c.fetchall()
        return rows


def deleteOrder(id):
    """Delete order by given id."""
    with conn:
        c.execute("DELETE FROM Orders WHERE id_order=?", (id,))


def searchOrders(id_p='', id_c='', quantity='', send='', loc=''):
    """Returns orders that meet at least 1 of passed args."""
    with conn:
        c.execute("""SELECT * FROM Orders WHERE id_customer=? OR id_product=? OR quantity=?
                 OR send_status=? OR location=?""",
                  (id_p, id_c, quantity, send, loc))
    return c.fetchall()


def returnOrder(id_o):
    """Return order by given id."""
    with conn:
        c.execute("SELECT * FROM Orders WHERE id_order=?", (id_o,))
    return c.fetchone()
