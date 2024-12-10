from tkinter import *
import os.path
import os
import sqlite3
import threading
import datetime
from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
import re
import tkinter as tk
root = None
tabs = None

global customer_logged_in
customer_logged_in = False
global current_user_name
current_user_name = ""

current_datetime = datetime.date.today()
global current_date_str
current_date_str = current_datetime.strftime("%Y-%m-%d")
conn = sqlite3.connect('online_store.db')

cursor = conn.cursor()


cursor.execute('''DROP TABLE IF EXISTS User''')
cursor.execute('''DROP TABLE IF EXISTS Supplier''')
cursor.execute('''DROP TABLE IF EXISTS Product''')
cursor.execute('''DROP TABLE IF EXISTS Discount''')
cursor.execute('''DROP TABLE IF EXISTS Customer_info''')
cursor.execute('''DROP TABLE IF EXISTS Shopping_list''')
cursor.execute('''DROP TABLE IF EXISTS Shopping_list_item''')


cursor.execute('''
    CREATE TABLE User (
        user_id INTEGER PRIMARY KEY,
        username varchar(40),
        password varchar(100),
        user_type varchar(8) CHECK(user_type IN ('customer', 'admin'))
    );
''')


cursor.execute('''
    CREATE TABLE Customer_info (
        customer_id INTEGER PRIMARY KEY,
        first_name varchar(40),
        last_name varchar(40),
        email varchar(100),
        address varchar(40),
        city varchar(50),
        country varchar(40),
        phone_number varchar(15),
        user_id int,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    );
''')

cursor.execute('''
    INSERT INTO User (username, password, user_type)
    VALUES ('user123', 'pass123', "admin")
''')

cursor.execute('''
    CREATE TABLE Supplier (
        supplier_id INTEGER PRIMARY KEY,
        supplier_name VARCHAR(30),
        address VARCHAR(30),
        zip_code VARCHAR(8),
        city VARCHAR(30),
        country VARCHAR(30),
        phone_number VARCHAR(15),
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    );
''')

cursor.execute('''
    CREATE TABLE Product (
        product_code INTEGER PRIMARY KEY,
        quantity_in_stock INTEGER CHECK(quantity_in_stock >= 0),
        number_of_sales INTEGER CHECK(number_of_sales >= 0),
        base_price REAL,
        product_revenue REAL,
        supplier_name VARCHAR(30),
        product_name VARCHAR(30),
        Shopping_list_id INTEGER,
        maximum_orders_per_month INTEGER,
        Discount_ID INTEGER,
        FOREIGN KEY (Discount_ID) REFERENCES Discount(discount_code),
        FOREIGN KEY (supplier_name) REFERENCES Supplier(supplier_name),
        FOREIGN KEY (Shopping_list_id) REFERENCES Shopping_list(Shopping_list_id)
    );
''')


cursor.execute('''
    CREATE TABLE Shopping_list (
        Shopping_list_id INTEGER PRIMARY KEY,
        phone_number VARCHAR(40),
        address VARCHAR(100),
        username VARCHAR(30),
        order_datetime DATE,
        confirmed_order BOOLEAN DEFAULT FALSE,
        total_cost REAL,
        placed_order BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (username) REFERENCES User(username)
    );
''')


cursor.execute('''
    CREATE TABLE Shopping_list_item (
        Shopping_list_item_id INTEGER PRIMARY KEY,
        Shopping_list_id INTEGER,
        product_code INTEGER,
        quantity INTEGER,
        item_price REAL DEFAULT 0,
        username VARCHAR(30),
        Discount_ID INTEGER,
        ordered BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (Shopping_list_id) REFERENCES Shopping_list(Shopping_list_id),
        FOREIGN KEY (product_code) REFERENCES Product(product_code)
    );
''')

cursor.execute('''
    CREATE TABLE Discount (
    discount_code INTEGER PRIMARY KEY,
    discount_percentage double,
    discount_category varchar(40),
    current_date DATE DEFAULT '{}',
    start_date DATE CHECK(start_date <= end_date),
    end_date DATE,
    product_code int,
    FOREIGN KEY (product_code) REFERENCES Product(product_code)
);
'''.format(current_date_str))


def customer_sign_up():

    global customer_username_input, customer_password_input, customer_first_name_input, customer_last_name_input, customer_email_input, customer_address_input
    global customer_city_input, customer_country_input, customer_phone_number_input

    customer_username_label = ttk.Label(customer_tab_2, text="Username:")
    customer_username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    customer_username_input = ttk.Entry(customer_tab_2, width=30)
    customer_username_input.grid(row=0, column=1, padx=10, pady=10)

    customer_password_label = ttk.Label(customer_tab_2, text="Password:")
    customer_password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    customer_password_input = ttk.Entry(customer_tab_2, width=30)
    customer_password_input.grid(row=1, column=1, padx=10, pady=10)

    customer_first_name_label = ttk.Label(customer_tab_2, text="First Name:")
    customer_first_name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    customer_first_name_input = ttk.Entry(customer_tab_2, width=30)
    customer_first_name_input.grid(row=2, column=1, padx=10, pady=10)

    customer_last_name_label = ttk.Label(customer_tab_2, text="Last Name:")
    customer_last_name_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    customer_last_name_input = ttk.Entry(customer_tab_2, width=30)
    customer_last_name_input.grid(row=3, column=1, padx=10, pady=10)

    customer_email_label = ttk.Label(customer_tab_2, text="Email:")
    customer_email_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    customer_email_input = ttk.Entry(customer_tab_2, width=30)
    customer_email_input.grid(row=4, column=1, padx=10, pady=10)

    customer_address_label = ttk.Label(customer_tab_2, text="Address:")
    customer_address_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    customer_address_input = ttk.Entry(customer_tab_2, width=30)
    customer_address_input.grid(row=5, column=1, padx=10, pady=10)

    customer_city_label = ttk.Label(customer_tab_2, text="City:")
    customer_city_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    customer_city_input = ttk.Entry(customer_tab_2, width=30)
    customer_city_input.grid(row=6, column=1, padx=10, pady=10)

    customer_country_label = ttk.Label(customer_tab_2, text="Country:")
    customer_country_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")

    customer_country_input = ttk.Entry(customer_tab_2, width=30)
    customer_country_input.grid(row=7, column=1, padx=10, pady=10)

    customer_phone_number_label = ttk.Label(customer_tab_2, text="Phone number:")
    customer_phone_number_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

    customer_phone_number_input = ttk.Entry(customer_tab_2, width=30)
    customer_phone_number_input.grid(row=8, column=1, padx=10, pady=10)

    customer_signup_button = ttk.Button(customer_tab_2, text="Sign Up", width=40,
                                       command=lambda: submit_customer_sign_up_info())
    customer_signup_button.grid(row=9, column=1, padx=10, pady=10, sticky="w")


def admin_login_handler(username, password):
    if admin_checker(username, password):
        admin_menu_tabs_init()
    else:
        print("Invalid username or password")


# this is querying admin, it is checking if the admin username and password combination exists
def admin_checker(username, password):
    # this is to prevent query of empty field

    if not username or not password:
        return False

    try:
        cursor.execute('''
                SELECT user_type FROM User
                WHERE username = ? AND password = ?
            ''', (username, password))
        user_type = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"here is the error type: {e}")
        return False

    if user_type and user_type[0] == "admin":
        return True
    return False


def admin_add_product(id, name, base_price, supplier_name, quantity):

    print(id, name, base_price, supplier_name, quantity)

    # here it's trying to insert the info from the text fields
    try:
        cursor.execute('''SELECT * FROM Product WHERE product_code = ? OR product_name = ?''', (id, name))
        existing_product = cursor.fetchone()
        if existing_product:
            # product with the same name already exists
            messagebox.showerror("Error", "Product already exists!")
        else:
            cursor.execute('''
                INSERT INTO Product (product_code, product_name, base_price, supplier_name, quantity_in_stock, number_of_sales)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id, name, base_price, supplier_name, quantity, 0))

            messagebox.showinfo("Success", "Product got added")

            conn.commit()

            # this is to clear the text input if insertion worked
            id_input_product.delete(0, END)
            product_name_input.delete(0, END)
            product_base_price_input.delete(0, END)
            product_supplier_input.delete(0, END)
            product_quantity_input.delete(0, END)
    # this is to prevent crashing if invalid info was inputted into the text fields
    except sqlite3.IntegrityError:
        print("invalid info inputted")


def admin_add_supplier(name, street, zip_code, city, country, phone_number):

    # here it's trying to insert the info from the text fields
    try:
        cursor.execute('''SELECT * FROM Supplier WHERE supplier_name = ?''', (name,))
        existing_supplier = cursor.fetchone()
        if existing_supplier:
            # supplier with the same name already exists
            messagebox.showerror("Error", "Supplier with this name already exists!")
        else:
            cursor.execute('''
                INSERT INTO Supplier (supplier_name, address, zip_code, city, country, phone_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, street, zip_code, city, country, phone_number))

            messagebox.showinfo("Success", "Supplier added successfully!")

            conn.commit()

            # this is to clear the text input if insertion worked
            name_input.delete(0, END)
            street_input.delete(0, END)
            zip_code_input.delete(0, END)
            city_input.delete(0, END)
            country_input.delete(0, END)
            phone_number_input.delete(0, END)
    # this is to prevent crashing if invalid info was inputted into the text fields
    except sqlite3.IntegrityError:
        print("invalid info inputted")


def admin_login():
    tabs.forget(tabs.select())

    global admin_login_tab

    admin_login_tab = ttk.Frame(tabs)

    tabs.add(admin_login_tab, text="Admin login")

    username_label = ttk.Label(admin_login_tab, text="username:")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    username_input = ttk.Entry(admin_login_tab, width=30)
    username_input.grid(row=0, column=1, padx=10, pady=10)

    password_label = ttk.Label(admin_login_tab, text="password:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    password_input = ttk.Entry(admin_login_tab, width=30)
    password_input.grid(row=1, column=1, padx=10, pady=10)

    admin_login_hint = ttk.Label(admin_login_tab, text="username: user123, password: pass123")
    admin_login_hint .grid(row=0, column=2, padx=10, pady=10, sticky="w")

    login_label = ttk.Button(admin_login_tab, text="login", width=40,
                                            command=lambda: admin_login_handler(username_input.get(), password_input.get()))
    login_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")


def admin_add_product_tab():
    global id_input_product, product_name_input, product_base_price_input, product_supplier_input, product_quantity_input

    global product_id_input_2, product_quantity_input_2

    id_label = Label(admin_tab_5, text="Id:")
    id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    id_input_product = Entry(admin_tab_5, width=30)
    id_input_product.grid(row=0, column=1, padx=10, pady=10)

    product_name_label = Label(admin_tab_5, text="Name:")
    product_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    product_name_input = Entry(admin_tab_5, width=30)
    product_name_input.grid(row=1, column=1, padx=10, pady=10)

    base_price_label = Label(admin_tab_5, text="Base price:")
    base_price_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    product_base_price_input = Entry(admin_tab_5, width=30)
    product_base_price_input.grid(row=2, column=1, padx=10, pady=10)

    supplier_label = Label(admin_tab_5, text="Supplier name:")
    supplier_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    product_supplier_input = Entry(admin_tab_5, width=30)
    product_supplier_input.grid(row=3, column=1, padx=10, pady=10)

    quantity_label = Label(admin_tab_5, text="Quantity:")
    quantity_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    product_quantity_input = Entry(admin_tab_5, width=30)
    product_quantity_input.grid(row=4, column=1, padx=10, pady=10)

    submit_product_info_label = Button(admin_tab_5, text="Add new product", width=40,
                                       command=lambda: submit_product_info())

    submit_product_info_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    id_label_2 = Label(admin_tab_5, text="ID:")
    id_label_2.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    product_id_input_2 = Entry(admin_tab_5, width=30)
    product_id_input_2.grid(row=0, column=3, padx=10, pady=10)

    quantity_label_2 = Label(admin_tab_5, text="Quantity:")
    quantity_label_2.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    product_quantity_input_2 = Entry(admin_tab_5, width=30)
    product_quantity_input_2.grid(row=1, column=3, padx=10, pady=10)

    submit_product_info_label_2 = Button(admin_tab_5, text="Increase quantity of product", width=40,
                                       command=lambda: submit_product_quantity_edit_info())

    submit_product_info_label_2.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    admin_menu()


def submit_customer_sign_up_info():
    if validate_user_sign_up():
        create_customer()
        customer_menu()


def submit_discount_info():
    if validate_discount_add():
        admin_add_discount()


def validate_user_sign_up():

    customer_username = customer_username_input.get().strip()
    customer_password = customer_password_input.get().strip()
    first_name = customer_first_name_input.get().strip()
    last_name = customer_last_name_input.get().strip()
    email = customer_email_input.get().strip()
    address = customer_address_input.get().strip()
    city = customer_city_input.get().strip()
    country = customer_country_input.get().strip()
    phone_number = customer_phone_number_input.get().strip()

    if not all([customer_username, customer_password, first_name, last_name, email, address, city, country, phone_number]):
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(customer_username) > 30:
        messagebox.showerror("Error", "Username cannot be longer than 30 characters")
        return False

    if len(customer_password) > 30:
        messagebox.showerror("Error", "Password cannot be longer than 30 characters")
        return False


    cursor.execute("SELECT COUNT(*) FROM User WHERE username = ?", (customer_username,))
    count = cursor.fetchone()[0]
    if count > 0:
        messagebox.showerror("Error", "User with that username already exists")
        return False


    if len(first_name) > 30:
        messagebox.showerror("Error", "first name cannot be longer than 30 characters")
        return False

    if len(last_name) > 30:
        messagebox.showerror("Error", "last name cannot be longer than 30 characters")
        return False

    if len(email) > 30:
        messagebox.showerror("Error", "email cannot be longer than 30 characters")
        return False

    if len(address) > 30:
        messagebox.showerror("Error", "address cannot be longer than 30 characters")
        return False

    if len(city) > 30:
        messagebox.showerror("Error", "city cannot be longer than 30 characters")
        return False

    if len(country) > 30:
        messagebox.showerror("Error", "country cannot be longer than 30 characters")
        return False

    if len(phone_number) > 16:
        messagebox.showerror("Error", "phone number cannot be longer than 16 characters")
        return False

    if not phone_number.isdigit():
        messagebox.showerror("Error", "Phone number must be a number")
        return False

    return True


def create_customer():

    customer_username = customer_username_input.get().strip()
    customer_password = customer_password_input.get().strip()
    first_name = customer_first_name_input.get().strip()
    last_name = customer_last_name_input.get().strip()
    email = customer_email_input.get().strip()
    address = customer_address_input.get().strip()
    city = customer_city_input.get().strip()
    country = customer_country_input.get().strip()
    phone_number = customer_phone_number_input.get().strip()

    try:
        #insertng customer with that name and password
        cursor.execute('''
            INSERT INTO User (username, password, user_type)
            VALUES (?, ?, ?)
        ''', (customer_username, customer_password, "customer"))

        user_id = cursor.lastrowid

        cursor.execute('''
                INSERT INTO Customer_info (first_name, last_name, email, address, city, country, phone_number,user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, address, city, country, phone_number, user_id))

        messagebox.showinfo("Success", "Customer created successfully")

        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", f" couldn't create customer reason: {str(e)}")


def validate_discount_add():

    discount_id = id_discount_input.get()
    discount_name = name_discount_input.get()
    discount_percentage = discount_input.get()
    lower_date = lower_date_input.get()
    upper_date = upper_date_input.get()
    product_id_discount = product_code_input.get()

    if not all([discount_id, discount_name, discount_percentage, lower_date, upper_date]):
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(discount_id) > 8:
        messagebox.showerror("Error", "Discount ID cannot be longer than 8 characters.")
        return False

    if not discount_id.isdigit():
        messagebox.showerror("Error", "Discount ID number must be a number")
        return False

    if len(discount_name) > 30:
        messagebox.showerror("Error", "Quantity cannot be longer than 8 digits.")
        return False

    if len(discount_percentage) > 10:
        messagebox.showerror("Error", "Discount percentage cannot be longer than 10 digits.")
        return False

    try:
        discount_percentage = float(discount_percentage)
        if discount_percentage <= 0 or discount_percentage >= 100:
            messagebox.showerror("Error", "Discount percentage must be greater than 0 and less than 100.")
            return False
    except ValueError:
        messagebox.showerror("Error", "Discount percentage must be a number.")
        return False


    # using regex to check if inputted date is in the correct format
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    if not date_pattern.match(lower_date):
        messagebox.showerror("Error", "Lower date must be in YYYY-MM-DD format.")
        return False

    if not date_pattern.match(upper_date):
        messagebox.showerror("Error", "Upper date must be in YYYY-MM-DD format.")
        return False

    # lower date being greater than upper date is impossible for a discount to work

    if lower_date > upper_date:
        messagebox.showerror("Error", "Upper date must be equal to or greater than lower date.")
        return False

    if product_id_discount != "":
        if len(product_id_discount) > 8:
            messagebox.showerror("Error", "Product ID cannot be longer than 8 characters.")
            return False

        if not product_id_discount.isdigit():
            messagebox.showerror("Error", "Product ID number must be a number")
            return False

        cursor.execute("SELECT COUNT(*) FROM Product WHERE product_code = ?", (product_id_discount,))
        result = cursor.fetchone()[0]
        if result == 0:
            messagebox.showerror("Error", "Product with the given ID does not exist.")
            return False

    return True


def validate_inputs_discount_to_remove():

    discount_id_to_remove = discount_id_2.get().strip()

    if discount_id_to_remove == None:
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(discount_id_to_remove) > 8:
        messagebox.showerror("Error", "Discount ID cannot be longer than 8 characters.")
        return False

    if not discount_id_to_remove.isdigit():
        messagebox.showerror("Error", "Discount ID number must be a number")
        return False

    return True


def validate_product_to_remove():

    product_id_to_remove = product_code_input_2.get().strip()

    print(product_id_to_remove)

    if product_id_to_remove == None:
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(product_id_to_remove) > 8:
        messagebox.showerror("Error", "Product ID cannot be longer than 8 characters.")
        return False

    if not product_id_to_remove.isdigit():
        messagebox.showerror("Error", "Product ID number must be a number")
        return False

    return True


def validate_inputs_product():

    product_name = product_name_input.get().strip()
    id_input = id_input_product.get().strip()
    base_price = product_base_price_input.get().strip()
    supplier = product_supplier_input.get().strip()
    quantity = product_quantity_input.get().strip()

    if not all([product_name, id_input, base_price, supplier, quantity]):
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(product_name) > 30:
        messagebox.showerror("Error", "Product name cannot be longer than 30 characters.")
        return False


    if len(id_input) > 8:
        messagebox.showerror("Error", "Product ID cannot be longer than 8 digits.")
        return False

    if not id_input.isdigit():
        messagebox.showerror("Error", "Product ID number must be a number")
        return False

    if len(base_price) > 10:
        messagebox.showerror("Error", "Base Price cannot be longer than 10 digits.")
        return False

    # checking if base price is integer or float value
    try:
        float_value = float(base_price)
    except ValueError:
        messagebox.showerror("Error", "Base Price must be a number.")
        return False

    if not base_price.replace('.', '').isdigit() or base_price.startswith('0'):
        messagebox.showerror("Error", "Base Price must be a number.")
        return False

    if len(quantity) > 8:
        messagebox.showerror("Error", "Quantity cannot be longer than 8 characters.")
        return False

    if not quantity.isdigit() or quantity.startswith("0"):
        messagebox.showerror("Error", "Quantity number must be a number")
        return False

    return True

def customer_product_validate_search_info():

    customer_product_id_search_input = customer_product_id_search_input.get().strip()
    customer_product_name_search_input = customer_product_name_search_input.get().strip()
    customer_product_base_search_price_input = customer_product_base_search_price_input.get().strip()
    customer_product_supplier_search_input = customer_product_supplier_search_input.get().strip()


    if customer_product_id_search_input == "" and customer_product_name_search_input == "" and customer_product_base_search_price_input == "" and customer_product_supplier_search_input == "":
        messagebox.showerror("Error", "All search fields are empty")
        return False

    if customer_product_id_search_input != "":
        if len(customer_product_id_search_input) > 8:
            messagebox.showerror("Error", "Product ID cannot be longer than 8 digits.")
            return False

        if not customer_product_id_search_input.isdigit():
            messagebox.showerror("Error", "Product ID number must be a number")
            return False

    if customer_product_base_search_price_input != "":
        if len(customer_product_base_search_price_input) > 10:
            messagebox.showerror("Error", "Base Price cannot be longer than 10 digits.")
            return False

        # checking if base price is integer or float value
        try:
            float_value = float(customer_product_base_search_price_input)
        except ValueError:
            messagebox.showerror("Error", "Base Price must be a number.")
            return False

        if not customer_product_base_search_price_input.replace('.', '').isdigit() or customer_product_base_search_price_input.startswith("0"):
            messagebox.showerror("Error", "Base Price must be a number.")
            return False

    if customer_product_name_search_input != "":

        if len(customer_product_name_search_input) > 30:
            messagebox.showerror("Error", "product name cannot be longer than 30 characters.")
            return False

    if customer_product_supplier_search_input != "":

        if len(customer_product_supplier_search_input) > 30:
            messagebox.showerror("Error", "Product supplier name cannot be longer than 30 characters.")
            return False


def validate_search_info():
    product_id = product_id_search_input.get().strip()
    product_name = product_name_search_input.get().strip()
    product_base_price = product_base_search_price_input.get().strip()
    product_supplier = product_supplier_search_input.get().strip()

    print(product_id)

    if product_id == "" and product_name == "" and product_base_price == "" and product_supplier == "":
        messagebox.showerror("Error", "All search fields are empty")
        return False

    if product_id != "":
        if len(product_id) > 8:
            messagebox.showerror("Error", "Product ID cannot be longer than 8 digits.")
            return False

        if not product_id.isdigit():
            messagebox.showerror("Error", "Product ID number must be a number")
            return False

    print("this is base price")
    print(product_base_price)

    if product_base_price != "":
        if len(product_base_price) > 10:
            messagebox.showerror("Error", "Base Price cannot be longer than 10 digits.")
            return False

        # checking if base price is integer or float value
        try:
            float_value = float(product_base_price)
        except ValueError:
            messagebox.showerror("Error", "Base Price must be a number.")
            return False

        if not product_base_price.replace('.', '').isdigit() or product_base_price.startswith("0"):
            messagebox.showerror("Error", "Base Price must be a number.")
            return False

    if product_name != "":

        if len(product_name) > 30:
            messagebox.showerror("Error", "product name cannot be longer than 30 characters.")
            return False

    if product_supplier != "":

        if len(product_supplier) > 30:
            messagebox.showerror("Error", "Product supplier name cannot be longer than 30 characters.")
            return False

    return True


def validate_product_quantity_edit():

    product_quantity = product_quantity_input_2.get().strip()
    product_id = product_id_input_2.get().strip()

    if not all([product_quantity, product_id]):
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(product_id) > 8:
        messagebox.showerror("Error", "Product ID cannot be longer than 8 characters.")
        return False

    if not product_id.isdigit():
        messagebox.showerror("Error", "Product ID number must be a number")
        return False

    if len(product_quantity) > 8:
        messagebox.showerror("Error", "Quantity cannot be longer than 8 digits.")
        return False

    try:
        int(product_quantity)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a valid integer")
        return False

    # getting current quantity from product id
    cursor.execute('''SELECT quantity_in_stock FROM Product WHERE product_code = ?''', (product_id,))
    # storing it
    current_quantity = cursor.fetchone()[0]

    # checking if it doesn't cause negative product quantity
    if current_quantity + int(product_quantity) < 0:
        return False

    return True


def admin_edit_quantity_product(id, quantity):
    print("inside quantity product")
    # getting current quantity by using product id
    try:
        cursor.execute('''SELECT quantity_in_stock FROM Product WHERE product_code = ?''', (id,))
        # storing it
        current_quantity = cursor.fetchone()[0]
        print(current_quantity)
        # increasing quantity by inputted amount
        new_quantity = int(current_quantity) + int(quantity)
        # updating the quantity
        cursor.execute("UPDATE Product SET quantity_in_stock = ? WHERE product_code = ?", (new_quantity, id))

        messagebox.showinfo("Success", "Product quantity got updated!")

        conn.commit()

        product_id_input_2.delete(0, END)
        product_quantity_input_2.delete(0, END)


    # if product id doesn't exist it will just pass
    # because cursor.fetchone()[0] will return none and it can't index none
    except TypeError:
        pass


def submit_product_quantity_edit_info():
    if validate_product_quantity_edit():
        admin_edit_quantity_product(product_id_input_2.get().strip(), product_quantity_input_2.get().strip())
    admin_menu()


def submit_product_info():
    if validate_inputs_product():
        admin_add_product(id_input_product.get(), product_name_input.get(),
                          product_base_price_input.get(), product_supplier_input.get(),
                          product_quantity_input.get())
    admin_menu()


def submit_discount_to_remove():
    if validate_inputs_discount_to_remove():
        discount_id_to_remove = int(product_code_input_2.get().strip())
        try:
            cursor.execute("SELECT COUNT(*) FROM Discount WHERE discount_code = ?", (discount_id_to_remove,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute("DELETE FROM Discount WHERE discount_code = ?", (discount_id_to_remove,))
                messagebox.showinfo("Success", "Discount removed successfully!")

                conn.commit()
                # this is to update what items are being shown in the menu after product get deleted
                admin_add_discount_tab()
            else:
                messagebox.showerror("Error", "There's no discount with that id in the database")
        except sqlite3.Error:
            messagebox.showerror("Error", "Failed to remove discount.")


def submit_product_to_remove():
    if validate_product_to_remove():
        product_code = int(product_code_input_2.get().strip())
        try:
            cursor.execute("SELECT COUNT(*) FROM Product WHERE product_code = ?", (product_code,))
            count = cursor.fetchone()[0]
            if count > 0:

                number_of_sales

                cursor.execute("SELECT number_of_sales FROM Product WHERE product_code = ?", (product_code,))
                number_of_sales_selected_product = cursor.fetchall()
                if number_of_sales_selected_product == 0:

                    cursor.execute("DELETE FROM Product WHERE product_code = ?", (product_code,))
                    messagebox.showinfo("Success", "Product removed successfully!")

                    conn.commit()
                    # this is to update what items are being shown in the menu after product get deleted
                    admin_search_products_tab()
                else:
                    messagebox.showerror("Error", "Product is sold and can't be deleted")

            else:
                messagebox.showerror("Error", "There's no product with that id in the database")
        except sqlite3.Error:
            messagebox.showerror("Error", "Failed to remove product.")


def validate_inputs_supplier():

    name = name_input.get().strip()
    street = street_input.get().strip()
    zip_code = zip_code_input.get().strip()
    city = city_input.get().strip()
    country = country_input.get().strip()
    phone_number = phone_number_input.get().strip()

    if not all([name, street, zip_code, city, country, phone_number]):
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if len(name) > 30:
        messagebox.showerror("Error", "Supplier name cannot be longer than 30 characters.")
        return False

    if len(street) > 30:
        messagebox.showerror("Error", "Street Address cannot be longer than 30 characters.")
        return False

    if len(zip_code) > 8:
        messagebox.showerror("Error", "Zip Code cannot be longer than 8 characters.")
        return False

    if not zip_code.isdigit():
        messagebox.showerror("Error", "Zip Code must be a number")
        return False

    if len(city) > 30:
        messagebox.showerror("Error", "City cannot be longer than 30 characters.")
        return False

    if len(country) > 30:
        messagebox.showerror("Error", "Country cannot be longer than 30 characters.")
        return False

    if len(phone_number) > 15:
        messagebox.showerror("Error", "Phone number cannot be longer than 15 characters.")
        return False

    if not phone_number.isdigit():
        messagebox.showerror("Error", "Phone number must be a number")
        return False

    return True


def admin_add_supplier_tab():
    global name_input, street_input, zip_code_input, city_input, country_input, phone_number_input

    name_label = Label(admin_tab_3, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    name_input = Entry(admin_tab_3, width=30)
    name_input.grid(row=0, column=1, padx=10, pady=10)

    street_label = Label(admin_tab_3, text="Street Address:")
    street_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    street_input = Entry(admin_tab_3, width=30)
    street_input.grid(row=1, column=1, padx=10, pady=10)

    zip_code_label = Label(admin_tab_3, text="Zip Code:")
    zip_code_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    zip_code_input = Entry(admin_tab_3, width=30)
    zip_code_input.grid(row=2, column=1, padx=10, pady=10)

    city_label = Label(admin_tab_3, text="City:")
    city_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    city_input = Entry(admin_tab_3, width=30)
    city_input.grid(row=3, column=1, padx=10, pady=10)

    country_label = Label(admin_tab_3, text="Country:")
    country_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    country_input = Entry(admin_tab_3, width=30)
    country_input.grid(row=4, column=1, padx=10, pady=10)

    phone_number_label = Label(admin_tab_3, text="Phone number:")
    phone_number_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    phone_number_input = Entry(admin_tab_3, width=30)
    phone_number_input.grid(row=5, column=1, padx=10, pady=10)

    submit_supplier_info_label = Button(admin_tab_3, text="Submit supplier", width=40,
                                        command=lambda: submit_supplier_info())
    submit_supplier_info_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")


def submit_supplier_info():
    if validate_inputs_supplier():
        admin_add_supplier(name_input.get(), street_input.get(), zip_code_input.get(), city_input.get(), country_input.get(), phone_number_input.get())


def admin_assign_discount():
    global selected_product_id, selected_discount_id

    # creating the frame that shows discount and products
    discount_frame = Frame(admin_tab_7)
    discount_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # this function automatically assign discount to matching product when tab is switched to
    def assign_discounts_to_products():

        cursor.execute('''SELECT product_code, discount_code FROM Discount''')
        discounts = cursor.fetchall()
        print(discounts)
        for product_code, discount_code in discounts:
            cursor.execute("UPDATE Product SET Discount_ID = ? WHERE product_code = ?", (discount_code, product_code))

        conn.commit()

    admin_tab_7.bind("<Visibility>", lambda event: assign_discounts_to_products())
    assign_discounts_to_products()

    def display_all_discounts():
        cursor.execute('''SELECT * FROM Discount''')
        discounts = cursor.fetchall()

        # clearing the frame before adding new buttons
        for widget in discount_frame.winfo_children():
            widget.destroy()

        # inserting buttons for each discount
        for discount in discounts:
            btn = Button(discount_frame,
                         text=f"'Discount ID' {discount[0]} 'Discount category' {discount[2]} 'Discount Percentage' {discount[1]}% 'From' {discount[4]} 'To' {discount[5]}",
                         command=lambda idx=discount[0]: select_discount(idx), width=80)
            btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)

    admin_tab_7.bind("<Visibility>", lambda event: display_all_discounts())
    display_all_discounts()

    # creating a frame for product buttons
    product_frame = Frame(admin_tab_7)
    product_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    def display_all_discounts_2():
        cursor.execute('''SELECT * FROM Product''')
        products = cursor.fetchall()

        # clearing the frame before adding new buttons
        for widget in product_frame.winfo_children():
            widget.destroy()

        # inserting buttons for each product
        for product in products:
            discount_info = "None"

            if product[9] is not None:
                cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[9],))
                discount = cursor.fetchone()
                if discount[4] < discount[3] < discount[5]:
                    discount_info = f"Discount ID: {discount[0]}  Discount ID: {discount[2]}  Product Price: {float(product[3])*((100-float(discount[1]))/100)}  Discount Percentage:  {discount[1]}%  From:  {discount[4]}  To:  {discount[5]}"
                else:
                    discount_info = f"Discount ID: {discount[0]}  Discount ID: {discount[2]}  Product Price: {float(product[3])}  Discount Percentage:  {discount[1]}%  From:  {discount[4]}  To:  {discount[5]}"
            btn = Button(product_frame, text=f" Product ID: {product[0]}  Product Name:  {product[6]}  {discount_info}",
                         command=lambda idx=product[0]: select_product(idx), width=160)
            btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)

    admin_tab_7.bind("<Visibility>", lambda event: display_all_discounts_2())
    display_all_discounts_2()

    assign_discount_button = Button(admin_tab_7, text="Assign Discount", command=assign_selected_discount_to_product)
    assign_discount_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    assign_discount_button = Button(admin_tab_7, text="Remove discount from product", command=remove_discount)
    assign_discount_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)


def assign_selected_discount_to_product():
    cursor.execute("UPDATE Product SET Discount_ID = ? WHERE product_code = ?", (selected_discount_id, selected_product_id))
    messagebox.showinfo("Success", "Discount assigned to product!")

    conn.commit()


def remove_discount():
    cursor.execute("UPDATE Product SET Discount_ID = NULL WHERE product_code = ?", (selected_product_id,))


def select_discount(discount_id):
    global selected_discount_id
    selected_discount_id = discount_id


def select_product(product_id):
    global selected_product_id
    selected_product_id = product_id


def assign_discount_to_product():
    global selected_product_id, selected_discount_id
    if selected_product_id and selected_discount_id:
        print(f"Assigned Discount ID {selected_discount_id} to Product ID {selected_product_id}")
    else:
        print("Please select both a product and a discount.")


def admin_add_discount():
    id_discount = id_discount_input.get()
    name_discount = name_discount_input.get()
    discount_percentage = discount_input.get()
    lower_date = lower_date_input.get()
    upper_date = upper_date_input.get()
    product_id_discount = product_code_input.get()

    try:
        if product_id_discount != "":
        # insert the discount
            cursor.execute('''
                INSERT INTO Discount (discount_code, discount_category, discount_percentage, start_date, end_date, product_code)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_discount, name_discount, discount_percentage, lower_date, upper_date, product_id_discount))

            cursor.execute('''
                    UPDATE Product
                    SET Discount_ID = ?
                    WHERE product_code = ?
                ''', (id_discount, product_id_discount))

            conn.commit()

            messagebox.showinfo("Success", "Discount added!")

            conn.commit()
        else:
            cursor.execute('''
                          INSERT INTO Discount (discount_code, discount_category, discount_percentage, start_date, end_date)
                          VALUES (?, ?, ?, ?, ?)
                      ''', (
            id_discount, name_discount, discount_percentage, lower_date, upper_date))

            messagebox.showinfo("Success", "Discount added!")

            conn.commit()

        id_discount_input.delete(0, END)
        name_discount_input.delete(0, END)
        discount_input.delete(0, END)
        lower_date_input.delete(0, END)
        upper_date_input.delete(0, END)
        product_code_input.delete(0, END)

    except sqlite3.IntegrityError:
        print("invalid info inputted")


def admin_add_discount_tab():

    global id_discount_input, name_discount_input, discount_input, lower_date_input, upper_date_input, product_code_input

    global discount_id_2

    id_discount_label = Label(admin_tab_6, text="Discount ID:")
    id_discount_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    id_discount_input = Entry(admin_tab_6, width=30)
    id_discount_input.grid(row=0, column=1, padx=10, pady=10)

    name_discount_label = Label(admin_tab_6, text="Discount name:")
    name_discount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    name_discount_input = Entry(admin_tab_6, width=30)
    name_discount_input.grid(row=1, column=1, padx=10, pady=10)

    discount_label = Label(admin_tab_6, text="Discount percentage:")
    discount_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    discount_input = Entry(admin_tab_6, width=30)
    discount_input.grid(row=0, column=3, padx=10, pady=10)

    lower_date_label = Label(admin_tab_6, text="YYYY-MM-DD From:")
    lower_date_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    lower_date_input = Entry(admin_tab_6, width=30)
    lower_date_input.grid(row=2, column=1, padx=10, pady=10)

    upper_date_label = Label(admin_tab_6, text="YYYY-MM-DD To:")
    upper_date_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    upper_date_input = Entry(admin_tab_6, width=30)
    upper_date_input.grid(row=2, column=3, padx=10, pady=10)

    product_code_label = Label(admin_tab_6, text="Product code:")
    product_code_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    product_code_input = Entry(admin_tab_6, width=30)
    product_code_input.grid(row=3, column=1, padx=10, pady=10)

    submit_discount_label = Button(admin_tab_6, text="Submit discount", width=40,
                                        command=lambda: submit_discount_info())

    submit_discount_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    discount_id_label_2 = Label(admin_tab_6, text="Discount ID:")
    discount_id_label_2.grid(row=0, column=4, padx=10, pady=10, sticky="w")
    discount_id_input_2 = Entry(admin_tab_6, width=30)
    discount_id_input_2.grid(row=0, column=5, padx=10, pady=10)

    submit_discount_to_remove_label = Button(admin_tab_6, text="Delete discount", width=20,
                                            command=lambda: submit_discount_to_remove())

    submit_discount_to_remove_label.grid(row=1, column=5, padx=10, pady=10, sticky="w")


def admin_show_suppliers():

    # adjust height and width in the result box
    result_text_supplier = Text(admin_tab_1, width=160, height=60)
    result_text_supplier.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # to format it correctly i choose the different lengths and added them together
    header = f"{'Name':<30} | {'Phone number':<16} | {'Street Name':<30}| {'zip code':<8}| {'City':<30}| {'Country':<30}\n"

    # this is to add dotted lines below
    result_text_supplier.insert('end', header)
    result_text_supplier.insert('end', '-' * 160 + '\n')

    def display_all_supplier():
        cursor.execute('''SELECT * FROM Supplier''')
        suppliers = cursor.fetchall()

        result_text_supplier.delete('3.0', 'end')
        # inserting the supplier info inputted
        for supplier in suppliers:
            result_text_supplier.insert('end',
                                        f"{supplier[1]:<30} | {supplier[6]:<16} | {supplier[2]:<30}| {supplier[3]:<8}| {supplier[4]:<30}| {supplier[5]:<30}\n")
            result_text_supplier.insert('end', '-' * 160 + '\n')

    # function that displays suppliers when the tab is clicked on
    admin_tab_1.bind("<Visibility>", lambda event: display_all_supplier())

    display_all_supplier()


def admin_search_products_tab():

    global product_id_search_input, product_name_search_input, product_base_search_price_input, product_supplier_search_input, product_supplier_search_input

    global product_code_input_2

    product_id_search_label = Label(admin_tab_2, text="Product ID:")
    product_id_search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    product_id_search_input = Entry(admin_tab_2, width=30)
    product_id_search_input.grid(row=0, column=1, padx=10, pady=10)

    product_name_search_label = Label(admin_tab_2, text="Product name:")
    product_name_search_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    product_name_search_input = Entry(admin_tab_2, width=30)
    product_name_search_input.grid(row=1, column=1, padx=10, pady=10)

    product_base_search_price_label = Label(admin_tab_2, text="Price:")
    product_base_search_price_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    product_base_search_price_input = Entry(admin_tab_2, width=30)
    product_base_search_price_input.grid(row=0, column=3, padx=10, pady=10)

    product_supplier_search_label = Label(admin_tab_2, text="Product supplier:")
    product_supplier_search_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    product_supplier_search_input = Entry(admin_tab_2, width=30)
    product_supplier_search_input.grid(row=1, column=3, padx=10, pady=10)

    submit_search_box_input_label = Button(admin_tab_2, text="Search for product", width=20,
                                   command=lambda: submit_search_info())

    submit_search_box_input_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    #adjust height and width in the result box
    result_text = Text(admin_tab_2, width=137, height=40)
    result_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    # to format it correctly i choose the different lengths
    # product id is 10 because len(product ID) == 10, same logic applies to why "product quantity" is 16
    # so result text grid is (10 + 16 + 25 + 10 + 30 - 1) == 100
    result_text.insert('end', f"{'Product ID':<10} | {'Product quantity':<16} | {'Product Name':<25}| {'Base Price':<10}| {'Supplier':<25}| {'number of sales':<15} | {'From':<10} | {'To':<10}\n")
    # this is to add dotted lines below
    result_text.insert('end', '-' * 137 + '\n')

    def display_all_products():
        cursor.execute('''SELECT * FROM Product''')
        products = cursor.fetchall()

        result_text.delete('3.0', 'end')
        # inserting the product info inputted
        for product in products:

            if product[9] is not None:
                cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[9],))
                discount = cursor.fetchone()
                result_text.insert('end',
                                   f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}| {discount[4]}| {discount[5]}\n")
                result_text.insert('end', '-' * 137 + '\n')
            else:
                result_text.insert('end',
                                   f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}\n")
                result_text.insert('end', '-' * 137 + '\n')

    # function that displays products when the tab is clicked on
    admin_tab_2.bind("<Visibility>", lambda event: display_all_products())

    product_code_label_2 = Label(admin_tab_2, text="Product ID:")
    product_code_label_2.grid(row=0, column=4, padx=10, pady=10, sticky="w")
    product_code_input_2 = Entry(admin_tab_2, width=30)
    product_code_input_2.grid(row=0, column=5, padx=10, pady=10)

    submit_product_to_remove_label = Button(admin_tab_2, text="Delete Product", width=20,
                                   command=lambda: submit_product_to_remove())

    submit_product_to_remove_label.grid(row=1, column=4, padx=10, pady=10, sticky="w")

    # showing current date
    current_date_label = Label(admin_tab_2, text="Current date: " + str(current_date_str))
    current_date_label.grid(row=2, column=4, padx=10, pady=10, sticky="w")

    def display_search_results(products):

        result_text_search = Text(admin_tab_2, width=137, height=40)
        result_text_search.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        result_text_search.delete('3.0', 'end')

        result_text_search.insert('end',
                           f"{'Product ID':<10} | {'Product quantity':<16} | {'Product Name':<25}| {'Base Price':<10}| {'Supplier':<25}| {'number of sales':<15} | {'From':<10} | {'To':<10}\n")
        # this is to add dotted lines below
        result_text_search.insert('end', '-' * 137 + '\n')

        for product in products:

            if product[9] is not None:
                cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[9],))
                discount = cursor.fetchone()
                result_text_search.insert('end',
                                   f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}| {discount[4]}| {discount[5]}\n")
                result_text_search.insert('end', '-' * 137 + '\n')
            else:
                result_text_search.insert('end',
                                   f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}\n")
                result_text_search.insert('end', '-' * 137 + '\n')


    def admin_product_search():
        product_id = product_id_search_input.get().strip()
        product_name = product_name_search_input.get().strip()
        product_base_price = product_base_search_price_input.get().strip()
        product_supplier = product_supplier_search_input.get().strip()

        conditions = []
        values = []

        if product_id:
            conditions.append("product_code = ?")
            values.append(product_id)

        if product_name:
            conditions.append("product_name = ?")
            values.append(product_name)

        if product_base_price:
            conditions.append("base_price = ?")
            values.append(product_base_price)

        if product_supplier:
            conditions.append("supplier_name = ?")
            values.append(product_supplier)

        where_clause = " AND ".join(conditions)

        query = f"SELECT * FROM Product"
        if where_clause:
            query += " WHERE " + where_clause

        cursor.execute(query, tuple(values))

        searched_products = cursor.fetchall()

        display_search_results(searched_products)

    def submit_search_info():
        if validate_search_info():
            result_text.grid_forget()
            admin_product_search()

    display_all_products()


def admin_logout():
    #this is to clear all the admin tabs
    for tab_id in tabs.tabs():
        tabs.forget(tab_id)

    # this is to clear the old window before creating a new one
    root.destroy()
    #this is to go back to main menu
    main()


def admin_main_menu():

    admin_main_menu_button = ttk.Button(admin_tab_8, text="Logout", width=40,
                                       command=lambda: admin_logout())
    admin_main_menu_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def select_shopping_list_customer(shopping_list_id):
    cursor.execute('''SELECT * FROM Shopping_list WHERE Shopping_list_id = ?''', (shopping_list_id,))
    shopping_list = cursor.fetchone()

    if shopping_list is None:
        messagebox.showerror("Error", "No shopping list found with the given ID.")
        return

    user_response = messagebox.askyesno("Delete Confirmation", "Click Yes to delete, Click No to cancel deleting")
    # if customer clicks on yes to delete
    if user_response:
        # deleting if admin hasn't confirmed yet
        if not shopping_list[5]:
            cursor.execute('''SELECT product_code, quantity FROM Shopping_list_item WHERE Shopping_list_id = ?''', (shopping_list_id,))
            items = cursor.fetchall()

            if items:
                for item in items:
                    cursor.execute('''
                        UPDATE Product 
                        SET quantity_in_stock = quantity_in_stock + ? 
                        WHERE product_code = ?
                    ''', (item[1], item[0]))

            cursor.execute('''DELETE FROM Shopping_list_item WHERE Shopping_list_id = ? AND ordered = TRUE''', (shopping_list_id,))
            cursor.execute('''DELETE FROM Shopping_list WHERE Shopping_list_id = ?''', (shopping_list_id,))
            conn.commit()

            if shopping_list_id in order_history_buttons:
                order_history_buttons[shopping_list_id].destroy()
                del order_history_buttons[shopping_list_id]

            customer_menu()
        else:
            messagebox.showerror("Error", "Order is already confirmed and can't be cancelled")
            customer_menu()
    else:
        customer_menu()


def customer_order_history_tab():

    global order_history_buttons
    cursor.execute("SELECT * FROM Shopping_list WHERE username = ? AND placed_order = TRUE", (current_user_name,))
    shopping_lists = cursor.fetchall()

    # iterating of the orders placed
    for button in order_history_buttons.values():
        button.destroy()
    order_history_buttons.clear()

    if shopping_lists:
        for shopping_list in shopping_lists:
            shopping_list_id = shopping_list[0]
            cursor.execute('SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ?', (shopping_list_id,))
            total_cost = cursor.fetchone()[0]
            if total_cost is not None:
                create_order_history_button(shopping_list_id)


def admin_order_history_tab():
    cursor.execute("SELECT * FROM Shopping_list")
    shopping_lists = cursor.fetchall()

    order_history_frame = Frame(admin_tab_4)
    order_history_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
    if shopping_lists:
        for shopping_list in shopping_lists:
            cursor.execute('''SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ? ''', (shopping_list[0],))
            total_cost = cursor.fetchone()[0]
            if total_cost is not None:
                btn = Button(order_history_frame,
                             text=f"Shopping List Number: {shopping_list[0]} Total Price: {round(total_cost, 2)} \n",
                             command=lambda idx=shopping_list[0]: select_shopping_list_admin(idx),
                             width=120)
                btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)


def select_shopping_list_admin(shopping_list_id):
    cursor.execute('''SELECT * FROM Shopping_list WHERE Shopping_list_id = ?''', (shopping_list_id,))
    shopping_list = cursor.fetchone()

    user_response = messagebox.askyesno("Confirmation", "Yes to Confirm order, No to cancel confirmation")

    if user_response:
        if not shopping_list[5]:
            cursor.execute('''UPDATE Shopping_list SET confirmed_order  = ? WHERE Shopping_list_id = ?''', (True, shopping_list_id))
            conn.commit()
        else:
            messagebox.showerror("Error", "Order is already confirmed!")


def customer_current_order_tab():
    result_text = tk.Text(customer_tab_6, width=137, height=40)
    result_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    def display_all_products():
        cursor.execute('SELECT Shopping_list_id FROM Shopping_list WHERE username = ? AND confirmed_order = FALSE ORDER BY Shopping_list_id DESC LIMIT 1', (current_user_name,))
        active_shopping_list = cursor.fetchone()

        if active_shopping_list:
            shopping_list_id = active_shopping_list[0]
            cursor.execute('SELECT * FROM Shopping_list_item WHERE Shopping_list_id = ? AND ordered = FALSE', (shopping_list_id,))
            products = cursor.fetchall()
        else:
            products = []

        result_text.delete('1.0', tk.END)
        total_cost = 0

        for product in products:
            cursor.execute('SELECT * FROM Product WHERE product_code = ?', (product[2],))
            product_details = cursor.fetchone()

            discount_code = product_details[-1]

            cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (discount_code,))
            discount = cursor.fetchone()

            if discount is not None:
                if discount[4] < discount[3] < discount[5]:
                    discount_rate = discount[1]
                else:
                    discount_rate = 0
            else:
                discount_rate = 0

            if product_details:
                item_total_cost = product[3] * product_details[3]
                discounted_cost = item_total_cost * ((100 - float(discount_rate)) / 100)
                total_cost += discounted_cost
                result_text.insert(tk.END, f"Product Name: {product_details[6]} Quantity in order: {product[3]} Order cost: {round(discounted_cost, 2)}\n")

    tabs.bind("<<NotebookTabChanged>>", lambda event: display_all_products())
    display_all_products()

    submit_supplier_info_label = ttk.Button(customer_tab_6, text="Place order", width=40, command=lambda: customer_place_order())
    submit_supplier_info_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    customer_menu()


def customer_place_order():
    cursor.execute(
        "SELECT Shopping_list_id FROM Shopping_list WHERE username = ? AND placed_order = FALSE ORDER BY Shopping_list_id DESC LIMIT 1",
        (current_user_name,))
    active_shopping_list = cursor.fetchone()

    if active_shopping_list is None:
        messagebox.showerror("Error", "No items in the shopping list to place an order.")
        return

    shopping_list_id = active_shopping_list[0]

    cursor.execute('SELECT * FROM Shopping_list_item WHERE Shopping_list_id = ? AND ordered = FALSE',
                   (shopping_list_id,))
    products = cursor.fetchall()

    if not products:
        messagebox.showerror("Error", "No items in the shopping list to place an order.")
        return

    total_cost = 0

    for product in products:
        cursor.execute('SELECT * FROM Product WHERE product_code = ?', (product[2],))
        product_details = cursor.fetchone()

        discount_code = product_details[-1]

        cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (discount_code,))
        discount = cursor.fetchone()

        discount_rate = 0
        if discount is not None and discount[4] < discount[3] < discount[5]:
            discount_rate = discount[1]

        if product_details:
            item_total_cost = product[3] * product_details[3]
            discounted_cost = item_total_cost * ((100 - float(discount_rate)) / 100)
            total_cost += discounted_cost

    cursor.execute('UPDATE Shopping_list SET total_cost = ?, placed_order = TRUE WHERE Shopping_list_id = ?',
                   (total_cost, shopping_list_id))
    cursor.execute('UPDATE Shopping_list_item SET ordered = TRUE WHERE Shopping_list_id = ?', (shopping_list_id,))

    conn.commit()

    # after placing the order, create a new shopping list for the next order
    cursor.execute("SELECT MAX(Shopping_list_id) FROM Shopping_list")
    max_shopping_list_id = cursor.fetchone()[0] or 0
    new_shopping_list_id = max_shopping_list_id + 1

    cursor.execute('''
        INSERT INTO Shopping_list (Shopping_list_id, username, total_cost, confirmed_order)
        VALUES (?, ?, 0, FALSE)
    ''', (new_shopping_list_id, current_user_name))

    conn.commit()

    messagebox.showinfo("Order Status", f"Order placed successfully! Your total cost is {str(round(total_cost, 2))}")
    customer_order_history_tab()


def create_order_history_buttons():
    cursor.execute('SELECT Shopping_list_id FROM Shopping_list WHERE confirmed_order = FALSE')
    shopping_list_ids = cursor.fetchall()

    for shopping_list_id in shopping_list_ids:
        if shopping_list_id not in order_history_buttons:
            create_order_history_button(shopping_list_id[0])


def create_order_history_button(shopping_list_id):
    cursor.execute('SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ?', (shopping_list_id,))
    total_cost = cursor.fetchone()[0]

    order_history_frame = Frame(customer_tab_7)
    order_history_frame.grid(row=len(order_history_buttons), column=0, columnspan=4, padx=5, pady=5)

    btn = Button(order_history_frame,
                 text=f"Shopping List Number: {shopping_list_id} Total Price: {round(total_cost, 2)} \n",
                 command=lambda idx=shopping_list_id: select_shopping_list_customer(idx),
                 width=120)
    btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)
    order_history_buttons[shopping_list_id] = btn


def select_product_customer(product_id):
    if not customer_logged_in:
        messagebox.showerror("Error", "You need to be logged in to add to order!")
        return None

    cursor.execute('SELECT * FROM Product WHERE product_code = ?', (product_id,))
    product = cursor.fetchone()

    if not product:
        messagebox.showerror("Error", "Product not found!")
        return None

    quantity_in_stock = product[1]
    user_input = simpledialog.askinteger("Quantity", "Select quantity of product you want to order")
    if user_input is None:
        messagebox.showinfo("Cancelled", "No quantity selected.")
        return None

    try:
        quantity_ordered = int(user_input)
        if quantity_ordered <= 0:
            raise ValueError("Quantity must be positive")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid quantity.")
        return None

    if quantity_ordered > quantity_in_stock:
        messagebox.showerror("Error", "Not enough stock available!")
        return None

    cursor.execute('''
        SELECT Shopping_list_id 
        FROM Shopping_list 
        WHERE username = ? AND confirmed_order = FALSE AND placed_order = FALSE
        ORDER BY Shopping_list_id DESC
        LIMIT 1
    ''', (current_user_name,))
    active_shopping_list = cursor.fetchone()

    if active_shopping_list is None:
        cursor.execute("SELECT MAX(Shopping_list_id) FROM Shopping_list")
        max_shopping_list_id = cursor.fetchone()[0] or 0
        shopping_list_id = max_shopping_list_id + 1

        cursor.execute('''
            INSERT INTO Shopping_list (Shopping_list_id, username, total_cost, confirmed_order, placed_order)
            VALUES (?, ?, 0, FALSE, FALSE)
        ''', (shopping_list_id, current_user_name))
    else:
        shopping_list_id = active_shopping_list[0]

    discount_id = product[9]

    cursor.execute(
        '''SELECT quantity FROM Shopping_list_item 
           WHERE product_code = ? AND Shopping_list_id = ? AND username = ? AND ordered = FALSE''',
        (product_id, shopping_list_id, current_user_name)
    )
    current_product_quantity = cursor.fetchone()

    if current_product_quantity:
        new_quantity = current_product_quantity[0] + quantity_ordered
        cursor.execute(
            '''UPDATE Shopping_list_item 
               SET quantity = ? 
               WHERE product_code = ? AND Shopping_list_id = ? AND username = ? AND ordered = FALSE''',
            (new_quantity, product_id, shopping_list_id, current_user_name)
        )
    else:
        cursor.execute(
            '''INSERT INTO Shopping_list_item (Shopping_list_id, product_code, quantity, username, Discount_ID, ordered) 
               VALUES (?, ?, ?, ?, ?, FALSE)''',
            (shopping_list_id, product_id, quantity_ordered, current_user_name, discount_id)
        )

    cursor.execute(
        '''UPDATE Product 
           SET quantity_in_stock = ? 
           WHERE product_code = ?''',
        (quantity_in_stock - quantity_ordered, product_id)
    )

    conn.commit()

    customer_menu()


def customer_search_products_tab():

    global customer_product_id_search_input, customer_product_name_search_input, customer_product_base_search_price_input, customer_product_supplier_search_input

    global customer_product_code_input_2

    def submit_search_info():
        if customer_product_validate_search_info():
            customer_product_search()

    def display_all_products():
        for widget in product_frame.winfo_children():
            widget.destroy()

        cursor.execute('''SELECT * FROM Product''')
        products = cursor.fetchall()

        # inserting the product info inputted
        for product in products:

            cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[9],))

            discount = cursor.fetchone()

            if discount!= None:
                if discount[4] < discount[3] < discount[5]:
                    discount_rate = discount[1]
                else:
                    discount_rate = 0
            else:
                discount_rate = 0

            btn = Button(product_frame,
                         text=f" Product ID: {product[0]}  Product name: {product[6]} Product Price: {round(float(product[3])*((100-float(discount_rate))/100),2)}  Product quantity: {product[1]} Supplier: {product[5]}\n",
                         command=lambda idx=product[0]: select_product_customer(idx), width=120)

            btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)


    def display_search_results(products):

        for widget in product_frame.winfo_children():
            widget.destroy()

        search_results_products_customer = Frame(customer_tab_1)
        search_results_products_customer.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        for product in products:

            cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[9],))

            discount = cursor.fetchone()

            print("here is discounts: " + str(discount))
            if discount[4] < discount[3] < discount[5]:

                btn = Button(product_frame,
                        text=f"'Product ID: ' {product[0]:<10} 'Product Price: ' {float(product[3])*((100-float(discount[1]))/100):<10}  'Product quantity:' {product[1]:<16} 'Product name: ' {product[6]:<25}  'Supplier: ' {product[5]:<25}\n",
                        command=lambda idx=product[0]: select_product_customer(idx), width=120)

                btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)

            else:
                btn = Button(product_frame,
                             text=f"'Product ID: ' {product[0]:<10}'' 'Product quantity:' {product[1]:<16} 'Product name: '{product[6]:<25}  'Supplier: ' {product[5]:<25}\n",
                             command=lambda idx=product[0]: select_product_customer(idx), width=80)

                btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)


    def customer_product_search():

        product_id = customer_product_id_search_input.get().strip()
        product_name = customer_product_name_search_input.get().strip()
        product_base_price = customer_product_base_search_price_input.get().strip()
        product_supplier = customer_product_supplier_search_input.get().strip()


        conditions = []
        values = []

        if product_id:
            conditions.append("product_code = ?")
            values.append(product_id)

        if product_name:
            conditions.append("product_name = ?")
            values.append(product_name)

        if product_base_price:
            conditions.append("base_price = ?")
            values.append(product_base_price)

        if product_supplier:
            conditions.append("supplier_name = ?")
            values.append(product_supplier)

        where_clause = " AND ".join(conditions)

        query = f"SELECT * FROM Product"
        if where_clause:
            query += " WHERE " + where_clause

        cursor.execute(query, tuple(values))

        searched_products = cursor.fetchall()

        display_search_results(searched_products)


    def display_discounted_items():

        for widget in product_frame.winfo_children():
            widget.destroy()

        cursor.execute('''SELECT * FROM Product''')
        products = cursor.fetchall()

        discounted_products_customer = Frame(customer_tab_1)
        discounted_products_customer.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        for product in products:

            cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[9],))

            discount = cursor.fetchone()
            print("here is discounts: " + str(discount))
            if discount[4] < discount[3] < discount[5]:

                btn = Button(product_frame,
                             text=f"Product ID: {product[0]:<10} Product Price:  {float(product[3]) * ((100 - float(discount[1])) / 100):<10} Product quantity: {product[1]:<16} Product name: {product[6]:<25}  Supplier: {product[5]:<25}\n",
                             command=lambda idx=product[0]: select_product_customer(idx), width=120)

                btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)


    search_products_tab_customer = Frame(customer_tab_1)
    search_products_tab_customer.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    customer_product_id_search_label = Label(customer_tab_1, text="Product ID:")
    customer_product_id_search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    customer_product_id_search_input = Entry(customer_tab_1, width=30)
    customer_product_id_search_input.grid(row=0, column=1, padx=10, pady=10)

    customer_product_name_search_label = Label(customer_tab_1, text="Product name:")
    customer_product_name_search_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    customer_product_name_search_input = Entry(customer_tab_1, width=30)
    customer_product_name_search_input.grid(row=1, column=1, padx=10, pady=10)

    customer_product_base_search_price_label = Label(customer_tab_1, text="Price:")
    customer_product_base_search_price_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    customer_product_base_search_price_input = Entry(customer_tab_1, width=30)
    customer_product_base_search_price_input.grid(row=0, column=3, padx=10, pady=10)

    customer_product_supplier_search_label = Label(customer_tab_1, text="Product supplier:")
    customer_product_supplier_search_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    customer_product_supplier_search_input = Entry(customer_tab_1, width=30)
    customer_product_supplier_search_input.grid(row=1, column=3, padx=10, pady=10)

    customer_submit_search_box_input_label = Button(customer_tab_1, text="Search for product", width=20,
                                   command=lambda: submit_search_info())

    customer_submit_search_box_input_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    customer_show_discounted_products_input_label = Button(customer_tab_1, text="Show Discount items", width=20,
                                                    command=lambda: display_discounted_items())

    customer_show_discounted_products_input_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    # function that displays products when the tab is clicked on
    customer_tab_1.bind("<Expose>", lambda event: display_all_products())

    product_frame = Frame(customer_tab_1)
    product_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    customer_menu()


def customer_go_to_main_menu():
    global customer_logged_in
    global current_user_name
    # this is to clear all the admin tabs
    for tab_id in tabs.tabs():
        tabs.forget(tab_id)
    # this is to go back to main menu
    customer_logged_in = False
    current_user_name = ""
    #this is also to remove the window so windows doesn't keep adding up
    root.destroy()
    main()


def customer_main_menu():

    customer_login_button = ttk.Button(customer_tab_3, text="Go to main menu", width=40,
                                       command=lambda: customer_go_to_main_menu())
    customer_login_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def customer_logout_menu():

    customer_logout_button = ttk.Button(customer_tab_5, text="logout", width=40,
                                       command=lambda: customer_logout_function())

    customer_logout_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def validate_customer_login():

    customer_username = customer_username_login_input.get().strip()
    customer_password = customer_password_login_input.get().strip()

    if not all([customer_username, customer_password]):
        messagebox.showerror("Error", "All fields are required to be filled.")
        return False

    if customer_logged_in == True:
        messagebox.showerror("Error", "Customer is already logged in")
        return False

    if len(customer_username) > 30:
        messagebox.showerror("Error", "Username cannot be longer than 30 characters")
        return False

    if len(customer_password) > 30:
        messagebox.showerror("Error", "Password cannot be longer than 30 characters")
        return False

    cursor.execute("SELECT COUNT(*) FROM User WHERE username = ? AND password = ?", (customer_username, customer_password))
    count = cursor.fetchone()[0]
    if count == 0:
        messagebox.showerror("Error", "incorrect login details, couldn't login")
        return False

    return True


def customer_login():

    global customer_username_login_input, customer_password_login_input

    customer_username_login_label = ttk.Label(customer_tab_4, text="Username:")
    customer_username_login_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    customer_username_login_input = ttk.Entry(customer_tab_4, width=30)
    customer_username_login_input.grid(row=0, column=1, padx=10, pady=10)

    customer_password_login_label = ttk.Label(customer_tab_4, text="Password:")
    customer_password_login_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    customer_password_login_input = ttk.Entry(customer_tab_4, width=30)
    customer_password_login_input.grid(row=1, column=1, padx=10, pady=10)

    customer_login_button = ttk.Button(customer_tab_4, text="Log in", width=40,
                                        command=lambda: submit_customer_login_info())
    customer_login_button.grid(row=9, column=1, padx=10, pady=10, sticky="w")

    customer_menu()


def submit_customer_login_info():
    if validate_customer_login():
        customer_login_fucntion()
        customer_menu()


def customer_login_fucntion():
    global customer_logged_in
    global current_user_name
    global customer_username_login_input
    customer_logged_in = True
    current_user_name = customer_username_login_input.get().strip()
    customer_username_login_input = ""
    messagebox.showinfo("Success", "Customer got logged in")


def customer_logout_function():
    global customer_logged_in
    global current_user_name
    if customer_logged_in == True:
        customer_logged_in = False
        current_user_name = ""
    else:
        messagebox.showerror("Error", "Customer is not logged in")

    customer_menu()


def admin_menu_tabs_init():

    global admin_tab_1, admin_tab_2, admin_tab_3, admin_tab_4, admin_tab_5, admin_tab_6, admin_tab_7, admin_tab_8

    # this is to delete user type menu so tabs doesn't keep adding up
    tabs.forget(tabs.select())

    # this is to display the menu tabs for the customer
    admin_tab_1 = ttk.Frame(tabs)
    admin_tab_2 = ttk.Frame(tabs)
    admin_tab_3 = ttk.Frame(tabs)
    admin_tab_4 = ttk.Frame(tabs)
    admin_tab_5 = ttk.Frame(tabs)
    admin_tab_6 = ttk.Frame(tabs)
    admin_tab_7 = ttk.Frame(tabs)
    admin_tab_8 = ttk.Frame(tabs)

    tabs.add(admin_tab_1, text="Show Suppliers")
    tabs.add(admin_tab_2, text="Product Search")
    tabs.add(admin_tab_3, text="Add Suppliers")
    tabs.add(admin_tab_4, text="Unconfirmed Orders")
    tabs.add(admin_tab_5, text="Add Products")
    tabs.add(admin_tab_6, text="Add Discounts")
    tabs.add(admin_tab_7, text="Assign Discounts")
    tabs.add(admin_tab_8, text="Main Menu")

    admin_menu()


def customer_menu_tabs_init():

    global customer_tab_1, customer_tab_2, customer_tab_3, customer_tab_4, customer_tab_5, customer_tab_6, customer_tab_7

    # this is to delete user type menu so tabs doesn't keep adding up
    tabs.forget(tabs.select())

    # this is to display the menu tabs for the customer
    customer_tab_1 = ttk.Frame(tabs)
    customer_tab_2 = ttk.Frame(tabs)
    customer_tab_3 = ttk.Frame(tabs)
    customer_tab_4 = ttk.Frame(tabs)
    customer_tab_5 = ttk.Frame(tabs)
    customer_tab_6 = ttk.Frame(tabs)
    customer_tab_7 = ttk.Frame(tabs)

    tabs.add(customer_tab_1, text="Search Product")
    tabs.add(customer_tab_2, text="Sign up")
    tabs.add(customer_tab_3, text="Main Menu")
    tabs.add(customer_tab_4, text="Login")
    tabs.add(customer_tab_5, text="Logout")
    tabs.add(customer_tab_6, text="Place Order")
    tabs.add(customer_tab_7, text="Show order history")

    customer_menu()


def admin_menu():

    # this function is to display the different tabs when the tabs are clicked on
    tabs.bind("<<NotebookTabChanged>>", lambda event: admin_tab_changed())

    def admin_tab_changed():
        current_tab_index = tabs.index(tabs.select())
        if current_tab_index == 4:
            admin_add_product_tab()
        elif current_tab_index == 1:
            admin_search_products_tab()
        elif current_tab_index == 2:
            admin_add_supplier_tab()
        elif current_tab_index == 0:
            admin_show_suppliers()
        elif current_tab_index == 3:
            admin_order_history_tab()
        elif current_tab_index == 5:
            admin_add_discount_tab()
        elif current_tab_index == 6:
            admin_assign_discount()
        elif current_tab_index == 7:
            admin_main_menu()


def customer_menu():

    def customer_tab_change():
        current_tab_index = tabs.index(tabs.select())
        print(f"selected customer index is: {current_tab_index}")
        if current_tab_index == 0:
            customer_search_products_tab()
        elif current_tab_index == 1:
            customer_sign_up()
        elif current_tab_index == 3:
            customer_login()
        elif current_tab_index == 2:
            customer_main_menu()
        elif current_tab_index == 4:
            customer_logout_menu()
        elif current_tab_index == 5:
            customer_current_order_tab()
        elif current_tab_index == 6:
            customer_order_history_tab()

    tabs.bind("<<NotebookTabChanged>>", lambda event: customer_tab_change())


def main():
    global root, tabs
    global order_history_buttons
    order_history_buttons = {}

    root = tk.Tk()
    root.title("Online store")

    tabs = ttk.Notebook(root)
    tabs.pack(fill=tk.BOTH, expand=True)

    tab1 = ttk.Frame(tabs)
    tabs.add(tab1, text="User Type")

    submit_url = ttk.Button(tab1, text="Click here to get customer menu", width=40, command=customer_menu_tabs_init)
    submit_url.pack(side=tk.TOP, padx=0, pady=20)

    submit_url_2 = ttk.Button(tab1, text="Click here to get admin menu", width=40, command=admin_login)
    submit_url_2.pack(side=tk.TOP, padx=0, pady=30)

    admin_login_tab = ttk.Frame(tabs)

    username_label = ttk.Label(admin_login_tab, text="username:")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    username_input = ttk.Entry(admin_login_tab, width=30)
    username_input.grid(row=0, column=1, padx=10, pady=10)

    password_label = ttk.Label(admin_login_tab, text="password:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    password_input = ttk.Entry(admin_login_tab, width=30)
    password_input.grid(row=1, column=1, padx=10, pady=10)

    admin_login_hint = ttk.Label(admin_login_tab, text="username: user123, password: pass123")
    admin_login_hint.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    login_label = ttk.Button(admin_login_tab, text="login", width=40,
                             command=lambda: admin_login_handler(username_input.get(), password_input.get()))
    login_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    tabs.select(tab1)

    root.attributes('-fullscreen', True)
    root.mainloop()


if __name__ == '__main__':
    main()

