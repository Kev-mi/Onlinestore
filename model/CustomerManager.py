import view.CustomerMenu as CustomerMenu
from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
import sqlite3

class CustomerManager:

    def __init__(self):

        self.username_input = None
        self.password_input = None
        self.first_name_input = None
        self.last_name_input = None
        self.email_input = None
        self.address_input = None
        self.city_input = None
        self.country_input = None
        self.phone_number_input = None

        self.customer_username_login_input = None
        self.customer_password_login_input = None

        self.customer_logged_in = None
        self.current_user_name = None

    # method that gets all inserted products
    def get_all_products(self,gui):

        gui.cursor.execute("SELECT * FROM Product")
        return gui.cursor.fetchall()

    # method that returns all the products
    def search_products(self, gui, product_id=None, product_name=None, base_price=None, supplier_name=None):

        conditions = []
        values = []

        if product_id:
            conditions.append("product_code = ?")
            values.append(product_id)
        if product_name:
            conditions.append("product_name = ?")
            values.append(product_name)
        if base_price:
            conditions.append("base_price = ?")
            values.append(base_price)
        if supplier_name:
            conditions.append("supplier_name = ?")
            values.append(supplier_name)

        query = "SELECT * FROM Product"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        gui.cursor.execute(query, tuple(values))
        return gui.cursor.fetchall()

    # set and get methods for customer_logged_in
    def set_customer_logged_in(self, logged_in_status):
        self.customer_logged_in = logged_in_status

    def get_customer_logged_in(self):
        return self.customer_logged_in

    # set and get methods for current_user_name
    def set_current_user_name(self, current_user_name):
        self.current_user_name = current_user_name

    def get_current_user_name(self):
        return self.current_user_name
    # method that gets all discounted products

    def set_customer_username(self, username):
        print("here's username in set method")
        print(username)
        self.username_input = username

    def get_customer_username(self):
        return self.username_input

    def set_customer_password(self, password):
        print("here's password in set method ")
        print(password)
        self.password_input = password

    def get_customer_password(self):
        return self.password_input

    def set_customer_first_name(self, first_name):
        self.first_name_input = first_name

    def get_customer_first_name(self):
        return self.first_name_input

    def set_customer_last_name(self, last_name):
        self.last_name_input = last_name

    def get_customer_last_name(self):
        return self.last_name_input

    def set_customer_email(self, email):
        self.email_input = email

    def get_customer_email(self):
        return self.email_input

    def set_customer_address(self, address):
        self.address_input = address

    def get_customer_address(self):
        return self.address_input

    def set_customer_city(self, city):
        self.city_input = city

    def get_customer_city(self):
        return self.city_input

    def set_customer_country(self, country):
        self.country_input = country

    def get_customer_country(self):
        return self.country_input

    def set_customer_phone_number(self, phone_number):
        self.phone_number_input = phone_number

    def get_customer_phone_number(self):
        return self.phone_number

    def set_customer_username_login_input(self,customer_username_login_input):
        self.customer_username_login_input = customer_username_login_input

    def get_customer_username_login_input(self):
        return self.customer_username_login_input

    def set_customer_password_login_input(self, customer_password_login_input):
        self.customer_password_login_input = customer_password_login_input

    def get_customer_password_login_input(self):
        return self.customer_password_login_input

    def get_discounted_products(self, gui):

        gui.cursor.execute("SELECT * FROM Product")
        products = gui.cursor.fetchall()

        discounted_products = []
        for product in products:
            gui.cursor.execute("SELECT * FROM Discount WHERE discount_code = ?", (product[8],))
            discount = gui.cursor.fetchone()
            if discount and discount[4] < discount[3] < discount[5]:
                discounted_products.append((product, discount[1]))

        return discounted_products

    def create_customer(self, gui):

        customer_username = self.username_input
        customer_password = self.password_input
        first_name = self.first_name_input
        last_name = self.last_name_input
        email = self.email_input
        address = self.address_input
        city = self.city_input
        country = self.country_input
        phone_number = self.phone_number_input

        try:
            # insertng customer with that name and password
            gui.cursor.execute('''
                INSERT INTO User (username, password, user_type)
                VALUES (?, ?, ?)
            ''', (customer_username, customer_password, "customer"))

            user_id = gui.cursor.lastrowid

            gui.cursor.execute('''
                    INSERT INTO Customer_info (first_name, last_name, email, address, city, country, phone_number,user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (first_name, last_name, email, address, city, country, phone_number, user_id))

            messagebox.showinfo("Success", "Customer created successfully")

            gui.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f" couldn't create customer reason: {str(e)}")

    def validate_customer_login(self, gui):

        customer_username = self.customer_username_login_input
        customer_password = self.customer_password_login_input

        if not all([customer_username, customer_password]):
            messagebox.showerror("Error", "All fields are required to be filled.")
            return False

        if self.customer_logged_in == True:
            messagebox.showerror("Error", "Customer is already logged in")
            return False

        if len(customer_username) > 30:
            messagebox.showerror("Error", "Username cannot be longer than 30 characters")
            return False

        if len(customer_password) > 30:
            messagebox.showerror("Error", "Password cannot be longer than 30 characters")
            return False

        gui.cursor.execute("SELECT COUNT(*) FROM User WHERE username = ? AND password = ?",
                       (customer_username, customer_password))
        count = gui.cursor.fetchone()[0]
        if count == 0:
            messagebox.showerror("Error", "incorrect login details, couldn't login")
            return False

        return True


    def validate_user_sign_up(self, gui):

        customer_username = self.username_input
        customer_password = self.password_input
        first_name = self.first_name_input
        last_name = self.last_name_input
        email = self.email_input
        address = self.address_input
        city = self.city_input
        country = self.country_input
        phone_number = self.phone_number_input

        if not all([customer_username, customer_password, first_name, last_name, email, address, city, country,
                    phone_number]):
            messagebox.showerror("Error", "All fields are required to be filled.")
            return False

        if len(customer_username) > 30:
            messagebox.showerror("Error", "Username cannot be longer than 30 characters")
            return False

        if len(customer_password) > 30:
            messagebox.showerror("Error", "Password cannot be longer than 30 characters")
            return False

        gui.cursor.execute("SELECT COUNT(*) FROM User WHERE username = ?", (customer_username,))
        count = gui.cursor.fetchone()[0]
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

    def customer_login_fucntion(self):
        self.customer_logged_in = True
        self.current_user_name = self.customer_username_login_input
        self.customer_username_login_input = ""
        messagebox.showinfo("Success", "Customer got logged in")

    def set_customer_login(self, login_status):
        self.customer_logged_in = login_status

    def select_product_customer(self, product_id, gui):
        print("it's in select product customer")
        if not self.customer_logged_in:
            messagebox.showerror("Error", "You need to be logged in to add to order!")
            return None

        gui.cursor.execute('SELECT * FROM Product WHERE product_code = ?', (product_id,))
        product = gui.cursor.fetchone()

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

        gui.cursor.execute('''
            SELECT Shopping_list_id 
            FROM Shopping_list 
            WHERE username = ? AND confirmed_order = FALSE AND placed_order = FALSE
            ORDER BY Shopping_list_id DESC
            LIMIT 1
        ''', (self.current_user_name,))
        active_shopping_list = gui.cursor.fetchone()

        if active_shopping_list is None:
            gui.cursor.execute("SELECT MAX(Shopping_list_id) FROM Shopping_list")
            max_shopping_list_id = gui.cursor.fetchone()[0] or 0
            shopping_list_id = max_shopping_list_id + 1

            gui.cursor.execute('''
                INSERT INTO Shopping_list (Shopping_list_id, username, total_cost, confirmed_order, placed_order)
                VALUES (?, ?, 0, FALSE, FALSE)
            ''', (shopping_list_id, self.current_user_name))
        else:
            shopping_list_id = active_shopping_list[0]

        discount_id = product[8]

        gui.cursor.execute(
            '''SELECT quantity FROM Shopping_list_item 
               WHERE product_code = ? AND Shopping_list_id = ? AND username = ? AND ordered = FALSE''',
            (product_id, shopping_list_id, self.current_user_name)
        )
        current_product_quantity = gui.cursor.fetchone()

        if current_product_quantity:
            new_quantity = current_product_quantity[0] + quantity_ordered
            gui.cursor.execute(
                '''UPDATE Shopping_list_item 
                   SET quantity = ? 
                   WHERE product_code = ? AND Shopping_list_id = ? AND username = ? AND ordered = FALSE''',
                (new_quantity, product_id, shopping_list_id, self.current_user_name)
            )
        else:
            gui.cursor.execute(
                '''INSERT INTO Shopping_list_item (Shopping_list_id, product_code, quantity, username, Discount_ID, ordered) 
                   VALUES (?, ?, ?, ?, ?, FALSE)''',
                (shopping_list_id, product_id, quantity_ordered, self.current_user_name, discount_id)
            )

        gui.cursor.execute(
            '''UPDATE Product 
               SET quantity_in_stock = ? 
               WHERE product_code = ?''',
            (quantity_in_stock - quantity_ordered, product_id)
        )

        gui.conn.commit()
        messagebox.showinfo("Success", "Item got added to order")
        customer_menu()

    def customer_place_order(self, gui):

        gui.cursor.execute(
            "SELECT Shopping_list_id FROM Shopping_list WHERE username = ? AND placed_order = FALSE ORDER BY Shopping_list_id DESC LIMIT 1",
            (self.current_user_name,))
        active_shopping_list = gui.cursor.fetchone()

        if active_shopping_list is None:
            messagebox.showerror("Error", "No items in the shopping list to place an order.")
            return

        shopping_list_id = active_shopping_list[0]

        gui.cursor.execute('SELECT * FROM Shopping_list_item WHERE Shopping_list_id = ? AND ordered = FALSE',
                       (shopping_list_id,))

        products = gui.cursor.fetchall()

        if not products:
            messagebox.showerror("Error", "No items in the shopping list to place an order.")
            return

        total_cost = 0

        for product in products:
            gui.cursor.execute('SELECT * FROM Product WHERE product_code = ?', (product[2],))
            product_details = gui.cursor.fetchone()

            discount_code = product_details[-1]

            gui.cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (discount_code,))
            discount = gui.cursor.fetchone()

            discount_rate = 0
            if discount is not None and discount[4] < discount[3] < discount[5]:
                discount_rate = discount[1]

            if product_details:
                item_total_cost = product[3] * product_details[3]
                discounted_cost = item_total_cost * ((100 - float(discount_rate)) / 100)
                total_cost += discounted_cost

        gui.cursor.execute('UPDATE Shopping_list SET total_cost = ?, placed_order = TRUE WHERE Shopping_list_id = ?',
                       (total_cost, shopping_list_id))

        gui.cursor.execute('UPDATE Shopping_list_item SET ordered = TRUE WHERE Shopping_list_id = ?', (shopping_list_id,))

        gui.conn.commit()

        # after placing the order, create a new shopping list for the next order
        gui.cursor.execute("SELECT MAX(Shopping_list_id) FROM Shopping_list")
        max_shopping_list_id = gui.cursor.fetchone()[0] or 0
        new_shopping_list_id = max_shopping_list_id + 1

        gui.cursor.execute('''
            INSERT INTO Shopping_list (Shopping_list_id, username, total_cost, confirmed_order)
            VALUES (?, ?, 0, FALSE)
        ''', (new_shopping_list_id, self.current_user_name))

        gui.conn.commit()

        messagebox.showinfo("Order Status",
                            f"Order placed successfully! Your total cost is {str(round(total_cost, 2))}")

        customer_order_history_tab()

    def select_shopping_list_customer(self, shopping_list_id, gui):
        gui.cursor.execute('''SELECT * FROM Shopping_list WHERE Shopping_list_id = ?''', (shopping_list_id,))
        shopping_list = gui.cursor.fetchone()

        if shopping_list is None:
            messagebox.showerror("Error", "No shopping list found with the given ID.")
            return

        user_response = messagebox.askyesno("Delete Confirmation", "Click Yes to delete, Click No to cancel deleting")
        # if customer clicks on yes to delete
        if user_response:
            # deleting if admin hasn't confirmed yet
            if not shopping_list[5]:
                gui.cursor.execute('''SELECT product_code, quantity FROM Shopping_list_item WHERE Shopping_list_id = ?''',
                               (shopping_list_id,))
                items = gui.cursor.fetchall()

                if items:
                    for item in items:
                        gui.cursor.execute('''
                            UPDATE Product 
                            SET quantity_in_stock = quantity_in_stock + ? 
                            WHERE product_code = ?
                        ''', (item[1], item[0]))

                gui.cursor.execute('''DELETE FROM Shopping_list_item WHERE Shopping_list_id = ? AND ordered = TRUE''',
                               (shopping_list_id,))
                gui.cursor.execute('''DELETE FROM Shopping_list WHERE Shopping_list_id = ?''', (shopping_list_id,))
                gui.conn.commit()

                if shopping_list_id in order_history_buttons:
                    order_history_buttons[shopping_list_id].destroy()
                    del order_history_buttons[shopping_list_id]

                customer_menu()
            else:
                messagebox.showerror("Error", "Order is already confirmed and can't be cancelled")
                customer_menu()
        else:
            customer_menu()

    def create_order_history_button(self, customer_tab_7, shopping_list_id, gui):
        gui.cursor.execute('SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ?', (shopping_list_id,))
        total_cost = gui.cursor.fetchone()[0]

        order_history_frame = Frame(customer_tab_7)
        order_history_frame.grid(row=len(order_history_buttons), column=0, columnspan=4, padx=5, pady=5)

        btn = Button(order_history_frame,
                     text=f"Shopping List Number: {shopping_list_id} Total Price: {round(total_cost, 2)} \n",
                     command=lambda idx=shopping_list_id: select_shopping_list_customer(idx, gui),
                     width=120)
        btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        order_history_buttons[shopping_list_id] = btn
