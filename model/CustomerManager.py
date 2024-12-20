import view.CustomerMenu as CustomerMenu

class CustomerManager:

    def __init__(self, cursor):
        self.cursor = cursor

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

    # method for creating a customer
    def create_customer(self):

        username = self.username_input.get().strip()
        password = self.password_input.get().strip()
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        email = self.email_input.get().strip()
        address = self.address_input.get().strip()
        city = self.city_input.get().strip()
        country = self.country_input.get().strip()
        phone_number = self.phone_number_input.get().strip()

        # checking if the username and password fields have been filled
        if not username or not password:
            raise ValueError("Username and password are required.")

        self.cursor.execute(
            """
            INSERT INTO Customer (username, password, first_name, last_name, email, address, city, country, phone_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (username, password, first_name, last_name, email, address, city, country, phone_number),
        )

    # method that gets all inserted products
    def get_all_products(self):

        self.cursor.execute("SELECT * FROM Product")
        return self.cursor.fetchall()

    # method that returns all the products
    def search_products(self, product_id=None, product_name=None, base_price=None, supplier_name=None):

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

        self.cursor.execute(query, tuple(values))
        return self.cursor.fetchall()


    def set_customer_logged_in(self, logged_in_status):
        self.customer_logged_in = logged_in_status

    def set_current_user_name(self, current_user_name):
        self.current_user_name = current_user_name

    def get_current_user_name(self):
        return self.current_user_name
    # method that gets all discounted products


    def get_discounted_products(self):

        self.cursor.execute("SELECT * FROM Product")
        products = self.cursor.fetchall()

        discounted_products = []
        for product in products:
            self.cursor.execute("SELECT * FROM Discount WHERE discount_code = ?", (product[9],))
            discount = self.cursor.fetchone()
            if discount and discount[4] < discount[3] < discount[5]:
                discounted_products.append((product, discount[1]))

        return discounted_products

    def create_customer(self):

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
            # insertng customer with that name and password
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


    def validate_user_sign_up(self):

        customer_username = customer_username_input.get().strip()
        customer_password = customer_password_input.get().strip()
        first_name = customer_first_name_input.get().strip()
        last_name = customer_last_name_input.get().strip()
        email = customer_email_input.get().strip()
        address = customer_address_input.get().strip()
        city = customer_city_input.get().strip()
        country = customer_country_input.get().strip()
        phone_number = customer_phone_number_input.get().strip()

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

    def customer_login_fucntion(self):
        customer_logged_in = True
        current_user_name = customer_username_login_input.get().strip()
        customer_username_login_input = ""
        messagebox.showinfo("Success", "Customer got logged in")
