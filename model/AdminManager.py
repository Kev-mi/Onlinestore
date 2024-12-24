import view.CustomerMenu as CustomerMenu
from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
import sqlite3

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
