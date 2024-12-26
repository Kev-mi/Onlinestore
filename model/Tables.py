

# method called from controller that initializes all the tables
def init_tables(cursor):

    cursor.execute('''DROP TABLE IF EXISTS User''')
    cursor.execute('''DROP TABLE IF EXISTS Supplier''')
    cursor.execute('''DROP TABLE IF EXISTS Product''')
    cursor.execute('''DROP TABLE IF EXISTS Discount''')
    cursor.execute('''DROP TABLE IF EXISTS Customer_info''')
    cursor.execute('''DROP TABLE IF EXISTS Shopping_list''')
    cursor.execute('''DROP TABLE IF EXISTS Shopping_list_item''')

    # User table that contains info if the user is a customer or admin
    cursor.execute('''
        CREATE TABLE User (
            user_id INTEGER PRIMARY KEY,
            username varchar(40),
            password varchar(100),
            user_type varchar(8) CHECK(user_type IN ('customer', 'admin'))
        );
    ''')

    # customer table that has user_id
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

    # supplier table
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

    # table for product that also has discount id if it's connected to a discount
    cursor.execute('''
            CREATE TABLE Product (
                product_code INTEGER PRIMARY KEY,
                quantity_in_stock INTEGER CHECK(quantity_in_stock >= 0),
                number_of_sales INTEGER CHECK(number_of_sales >= 0),
                base_price REAL,
                product_revenue REAL,
                supplier_name VARCHAR(30),
                product_name VARCHAR(30),
                maximum_orders_per_month INTEGER,
                Discount_ID INTEGER,
                FOREIGN KEY (Discount_ID) REFERENCES Discount(discount_code),
                FOREIGN KEY (supplier_name) REFERENCES Supplier(supplier_name)
            );
        ''')

    # table for shopping list that contains the username of the customer it's connected to
    # if the order is place by the customer and if the order has been confirmed by admin
    cursor.execute('''
        CREATE TABLE Shopping_list (
            Shopping_list_id INTEGER PRIMARY KEY,
            username VARCHAR(30),
            order_datetime DATE,
            confirmed_order BOOLEAN DEFAULT FALSE,
            total_cost REAL,
            placed_order BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (username) REFERENCES User(username)
        );
    ''')

    # table for the ordered version of product
    # it has quantity and shopping list id to know the amount in the shopping list and which shopping list it's in
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
        start_date DATE CHECK(start_date <= end_date),
        end_date DATE,
        product_code int,
        
        FOREIGN KEY (product_code) REFERENCES Product(product_code)
    );
    ''')



# method that init admin by inserting admin as a user
def init_admin(cursor):
    cursor.execute('''
        INSERT INTO User (username, password, user_type)
        VALUES ('user123', 'pass123', "admin")
    ''')
