import view.CustomerMenu as CustomerMenu
from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
import sqlite3
import re

class AdminManager:

    def __init__(self):

        self.product_id_search_input = None
        self.product_name_search_input = None
        self.product_base_price_search_input = None
        self.product_supplier_search_input = None
        self.product_supplier_search_input = None
        self.product_code_input_2 = None

        self.id_discount_input = None
        self.name_discount_input = None
        self.discount_input = None
        self.lower_date_input = None
        self.upper_date_input = None
        self.product_code_input = None
        self.discount_id_2 = None

        self.name_input = None
        self.street_input = None
        self.zip_code_input = None
        self.city_input = None
        self.country_input = None
        self.phone_number_input = None

        self.id_input_product = None
        self.product_name_input = None
        self.product_base_price_input = None
        self.product_supplier_input = None
        self.product_quantity_input = None

        self.product_id_input_2 = None
        self.product_quantity_input_2 = None

        self.selected_product_id = None
        self.selected_discount_id = None

        self._current_date = None

    def get_current_date(self):
        return self._current_date

    def set_current_date(self, date):
        self._current_date = date

    def get_product_id_search_input(self):
        self.product_id_search_input

    def set_product_id_search_input(self, product_id):
        self.product_id_search_input = product_id

    def get_product_name_search_input(self):
        return self.product_name_search_input

    def set_product_name_search_input(self, product_name):
        self.product_name_search_input = product_name

    def get_product_base_price_search_input(self):
        return self.product_base_price_search_input

    def set_product_base_price_search_input(self, price):
        self.product_base_price_search_input = price

    def get_product_supplier_search_input(self):
        return self.product_supplier_search_input

    def set_product_supplier_search_input(self, product_supplier):
        self.product_supplier_search_input = product_supplier

    def get_product_code_input_2(self):
        return self.product_code_input_2

    def set_product_code_input_2(self, product_code):
        self.product_code_input_2 = product_code

    def get_product_name_input(self):
        return self.product_name_input

    def set_product_name_input(self, product_name_input):
        self.product_name_input = product_name_input

    def get_product_base_price_input(self):
        return self.product_base_price_input

    def set_product_base_price_input(self, base_price):
        self.product_base_price_input = base_price

    def get_id_input_product(self):
        return self.id_input_product

    def set_id_input_product(self, id_input_product):
        self.id_input_product = id_input_product

    def get_product_base_price_input(self):
        return self.product_base_price_input

    def set_product_base_price_input(self, product_base_price_input):
        self.product_base_price_input = product_base_price_input

    def get_product_supplier_input(self):
        return self.product_supplier_input

    def set_product_supplier_input(self, product_supplier_input):
        self.product_supplier_input = product_supplier_input

    def get_product_quantity_input(self):
        return self.product_quantity_input

    def set_product_quantity_input(self, product_quantity_input):
        self.product_quantity_input = product_quantity_input


    def get_product_id_input_2(self):
        return self.product_id_input_2

    def set_product_id_input_2(self, product_id_input_2):
        self.product_id_input_2 = product_id_input_2

    def get_product_quantity_input_2(self):
        return self.product_quantity_input_2

    def set_product_quantity_input_2(self, product_quantity_input_2):
        self.product_quantity_input_2 = product_quantity_input_2

    def set_name_input(self, name_input):
        self.name_input = name_input

    def get_name_input(self):
        return self.name_input

    def set_street_input(self, street_input):
        self.street_input = street_input

    def get_street_input(self):
        return self.street_input

    def set_zip_code_input(self, zip_code_input):
        self.zip_code_input = zip_code_input

    def get_zip_code_input(self):
        return self.zip_code_input

    def set_city_input(self, city_input):
        self.city_input = city_input

    def get_city_input(self):
        return self.city_input

    def set_country_input(self, country_input):
        self.country_input = country_input

    def get_country_input(self):
        return self.country_input

    def set_phone_number_input(self, phone_number_input):
        self.phone_number_input = phone_number_input

    def get_phone_number_input(self):
        return self.phone_number_input

    def set_id_discount_input(self, discount):
        self.id_discount_input = discount

    def get_id_discount_input(self):
        return self.id_discount_input

    def set_name_discount_input(self, discount):
        self.name_discount_input = discount

    def get_name_discount_input(self):
        return self.name_discount_input

    def set_discount_input(self, discount):
        self.discount_input = discount

    def get_discount_input(self):
        return self.discount_input

    def set_lower_date_input(self, lower_input_date):
        self.lower_date_input = lower_input_date

    def get_lower_date_input(self):
        return self.lower_date_input

    def set_upper_date_input(self, upper_date):
        self.upper_date_input = upper_date

    def get_upper_date_input(self):
        return self.upper_date_input

    def set_product_code_input(self, prouct_code):
        self.product_code = prouct_code

    def get_product_code_input(self):
        return self.product_code_input

    def set_discount_id_2(self, discount_id_2):
        self.discount_id_2 = discount_id_2

    def get_discount_id_2(self):
        return self.discount_id_2

    def validate_search_info(self):
        product_id = self.product_id_search_input
        product_name = self.product_name_search_input
        product_base_price = self.product_base_price_search_input
        product_supplier = self.product_supplier_search_input

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

    def submit_product_to_remove(self, gui):
        if validate_product_to_remove():
            product_code = int(self.product_code_input_2)
            try:
                gui.cursor.execute("SELECT COUNT(*) FROM Product WHERE product_code = ?", (product_code,))
                count = cursor.fetchone()[0]
                if count > 0:

                    number_of_sales

                    gui.cursor.execute("SELECT number_of_sales FROM Product WHERE product_code = ?", (product_code,))
                    number_of_sales_selected_product = cursor.fetchall()
                    if number_of_sales_selected_product == 0:

                        gui.cursor.execute("DELETE FROM Product WHERE product_code = ?", (product_code,))
                        messagebox.showinfo("Success", "Product removed successfully!")

                        gui.conn.commit()
                        # this is to update what items are being shown in the menu after product get deleted
                        admin_search_products_tab()
                    else:
                        messagebox.showerror("Error", "Product is sold and can't be deleted")

                else:
                    messagebox.showerror("Error", "There's no product with that id in the database")
            except sqlite3.Error:
                messagebox.showerror("Error", "Failed to remove product.")

    def validate_product_to_remove(self):

        product_id_to_remove = self.product_code_input_2

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

    def validate_inputs_product(self):

        product_name = self.product_name_input
        id_input = self.id_input_product
        base_price = self.product_base_price_input
        supplier = self.product_supplier_input
        quantity = self.product_quantity_input

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

    def admin_add_product(self, gui):

        id = self.id_input_product
        name = self.product_name_input
        base_price = self.product_base_price_input
        supplier_name = self.product_supplier_input
        quantity = self.product_quantity_input

        # here it's trying to insert the info from the text fields
        try:
            gui.cursor.execute('''SELECT * FROM Product WHERE product_code = ? OR product_name = ?''', (id, name))
            existing_product = gui.cursor.fetchone()
            if existing_product:
                # product with the same name already exists
                messagebox.showerror("Error", "Product already exists!")
            else:
                gui.cursor.execute('''
                    INSERT INTO Product (product_code, product_name, base_price, supplier_name, quantity_in_stock, number_of_sales)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (id, name, base_price, supplier_name, quantity, 0))

                messagebox.showinfo("Success", "Product got added")

                gui.conn.commit()

        # this is to prevent crashing if invalid info was inputted into the text fields
        except sqlite3.IntegrityError:
            print("invalid info inputted")

    def validate_product_quantity_edit(self, gui):

        product_quantity = self.product_quantity_input_2
        product_id = self.product_id_input_2

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
        gui.cursor.execute('''SELECT quantity_in_stock FROM Product WHERE product_code = ?''', (product_id,))
        # storing it
        current_quantity = gui.cursor.fetchone()[0]

        # checking if it doesn't cause negative product quantity
        if current_quantity + int(product_quantity) < 0:
            return False

        return True

    def admin_edit_quantity_product(self,gui):
        print("inside quantity product")
        quantity = self.product_quantity_input_2
        id = self.product_id_input_2
        # getting current quantity by using product id
        try:
            gui.cursor.execute('''SELECT quantity_in_stock FROM Product WHERE product_code = ?''', (id,))
            # storing it
            current_quantity = gui.cursor.fetchone()[0]
            print(current_quantity)
            # increasing quantity by inputted amount
            new_quantity = int(current_quantity) + int(quantity)
            # updating the quantity
            gui.cursor.execute("UPDATE Product SET quantity_in_stock = ? WHERE product_code = ?", (new_quantity, id))

            messagebox.showinfo("Success", "Product quantity got updated!")

            gui.conn.commit()


        # if product id doesn't exist it will just pass
        # because cursor.fetchone()[0] will return none and it can't index none
        except TypeError:
            pass

    def validate_inputs_supplier(self):

        name = self.name_input
        street = self.street_input
        zip_code = self.zip_code_input
        city = self.city_input
        country = self.country_input
        phone_number = self.phone_number_input

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

    def admin_add_supplier(self, gui):

        name = self.name_input
        street = self.street_input
        zip_code = self.zip_code_input
        city = self.city_input
        country = self.country_input
        phone_number = self.phone_number_input

        # here it's trying to insert the info from the text fields
        try:
            gui.cursor.execute('''SELECT * FROM Supplier WHERE supplier_name = ?''', (name,))
            existing_supplier = gui.cursor.fetchone()
            if existing_supplier:
                # supplier with the same name already exists
                messagebox.showerror("Error", "Supplier with this name already exists!")
            else:
                gui.cursor.execute('''
                    INSERT INTO Supplier (supplier_name, address, zip_code, city, country, phone_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, street, zip_code, city, country, phone_number))

                messagebox.showinfo("Success", "Supplier added successfully!")

                gui.conn.commit()

        # this is to prevent crashing if invalid info was inputted into the text fields
        except sqlite3.IntegrityError:
            print("invalid info inputted")

    def validate_discount_add(self, gui):

        discount_id = self.id_discount_input
        discount_name = self.name_discount_input
        discount_percentage = self.discount_input
        lower_date = self.lower_date_input
        upper_date = self.upper_date_input
        product_id_discount = self.product_code_input

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

        #checking if the input is in the correct format
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

        # checking if product id input is correct
        print(product_id_discount)
        if product_id_discount != "" and product_id_discount != None:
            if len(product_id_discount) > 8:
                messagebox.showerror("Error", "Product ID cannot be longer than 8 characters.")
                return False

            if not product_id_discount.isdigit():
                messagebox.showerror("Error", "Product ID number must be a number")
                return False

            gui.cursor.execute("SELECT COUNT(*) FROM Product WHERE product_code = ?", (product_id_discount,))
            result = gui.cursor.fetchone()[0]
            if result == 0:
                messagebox.showerror("Error", "Product with the given ID does not exist.")
                return False

        return True

    def admin_add_discount(self, gui):

        id_discount = self.id_discount_input
        name_discount = self.name_discount_input
        discount_percentage = self.discount_input
        lower_date = self.lower_date_input
        upper_date = self.upper_date_input
        product_id_discount = self.product_code_input

        try:
            if product_id_discount != "":
                # insert the discount
                gui.cursor.execute('''
                           INSERT INTO Discount (discount_code, discount_category, discount_percentage, start_date, end_date, product_code)
                           VALUES (?, ?, ?, ?, ?, ?)
                       ''', (
                id_discount, name_discount, discount_percentage, lower_date, upper_date, product_id_discount))

                gui.cursor.execute('''
                               UPDATE Product
                               SET Discount_ID = ?
                               WHERE product_code = ?
                           ''', (id_discount, product_id_discount))

                gui.conn.commit()

                messagebox.showinfo("Success", "Discount added!")

                gui.conn.commit()
            else:
                gui.cursor.execute('''
                                INSERT INTO Discount (discount_code, discount_category, discount_percentage, start_date, end_date)
                                VALUES (?, ?, ?, ?, ?)
                                     ''', (
                    id_discount, name_discount, discount_percentage, lower_date, upper_date))

                messagebox.showinfo("Success", "Discount added!")

                gui.conn.commit()

        except sqlite3.IntegrityError:
            print("invalid info inputted")

    def select_discount(self, discount_id):
        self.selected_discount_id = discount_id
        messagebox.showinfo("Success", "Discount got selected!")

    def select_product(self, product_id):
        self.selected_product_id = product_id
        messagebox.showinfo("Success", "Product got selected!")

    def remove_discount(self, gui):
        # checking if the user has selected a product and a discount to delete from the product
        if self.selected_discount_id == None:
            messagebox.showinfo("Failure", "No Discount selected!")

        elif self.selected_product_id == None:
            messagebox.showinfo("Failure", "No Product selected!")

        else:
            gui.cursor.execute("UPDATE Product SET Discount_ID = NULL WHERE product_code = ?", (self.selected_product_id,))
            messagebox.showinfo("Success", "Discount removed from product!")

            gui.conn.commit()

    def assign_selected_discount_to_product(self, gui):
        # checking if the user has selected a product and a discount to assign to the product
        if self.selected_discount_id == None:
            messagebox.showinfo("Failure", "No Discount selected!")

        elif self.selected_product_id == None:
            messagebox.showinfo("Failure", "No Product selected!")

        else:
            gui.cursor.execute("UPDATE Product SET Discount_ID = ? WHERE product_code = ?",
                               (self.selected_discount_id, self.selected_product_id))
            messagebox.showinfo("Success", "Discount assigned to product!")

            gui.conn.commit()

    def select_shopping_list_admin(self, shopping_list_id, gui):
        gui.cursor.execute('''SELECT * FROM Shopping_list WHERE Shopping_list_id = ?''', (shopping_list_id,))
        shopping_list = gui.cursor.fetchone()

        user_response = messagebox.askyesno("Confirmation", "Yes to Confirm order, No to cancel confirmation")

        if user_response:
            if not shopping_list[5]:
                gui.cursor.execute('''UPDATE Shopping_list SET confirmed_order  = ? WHERE Shopping_list_id = ?''',
                               (True, shopping_list_id))
                gui.conn.commit()
            else:
                messagebox.showerror("Error", "Order is already confirmed!")

