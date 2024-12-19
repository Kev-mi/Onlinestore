from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
#from view.MainMenu import init_main_menu

def admin_show_suppliers(admin_tab_1):

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


def admin_menu(gui, admin_manager):
    # this function is to display the different tabs when the tabs are clicked on
    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: admin_tab_changed(gui))

    def admin_tab_change(gui, admin_manager):
        current_tab_index = gui.tabs.index(gui.tabs.select())

        switch_case = {
            0: lambda: admin_show_suppliers(gui.tabs.nametowidget(gui.tabs.select())),
            1: lambda: admin_search_products_tab(gui.tabs.nametowidget(gui.tabs.select(), admin_manager)),
            2: lambda: admin_add_supplier_tab(gui.tabs.nametowidget(gui.tabs.select())),
            3: lambda: admin_order_history_tab(gui.tabs.nametowidget(gui.tabs.select())),
            4: lambda: admin_add_product_tab(gui.tabs.nametowidget(gui.tabs.select())),
            5: lambda: admin_add_discount_tab(gui.tabs.nametowidget(gui.tabs.select())),
            6: lambda: admin_assign_discount(gui.tabs.nametowidget(gui.tabs.select())),
            7: lambda: admin_main_menu(gui.tabs.nametowidget(gui.tabs.select())),
        }

        # this is because get just gets the number but doesn't call the switch_case dictionairy so if func lines are needed to call the dictionairy
        switch_case.get(current_tab_index)
        func = switch_case.get(current_tab_index)
        if func:
            func()

    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: admin_tab_change(gui, admin_manager))


def admin_search_products_tab(admin_tab_2, admin_manager):

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


def admin_main_menu(admin_tab_8):

    admin_main_menu_button = ttk.Button(admin_tab_8, text="Logout", width=40,
                                       command=lambda: admin_logout())
    admin_main_menu_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")



def admin_add_discount_tab(admin_tab_6):

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


def submit_discount_info():
    if validate_discount_add():
        admin_add_discount()


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


def admin_logout():
    #this is to clear all the admin tabs
    for tab_id in tabs.tabs():
        tabs.forget(tab_id)

    # this is to clear the old window before creating a new one
    root.destroy()
    #this is to go back to main menu
    main()


def admin_order_history_tab(admin_tab_4):
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


def admin_add_product_tab(admin_tab_5):
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


def submit_product_info():
    if validate_inputs_product():
        admin_add_product(id_input_product.get(), product_name_input.get(),
                          product_base_price_input.get(), product_supplier_input.get(),
                          product_quantity_input.get())
    admin_menu()

def submit_product_quantity_edit_info():
    if validate_product_quantity_edit():
        admin_edit_quantity_product(product_id_input_2.get().strip(), product_quantity_input_2.get().strip())
    admin_menu()


def admin_assign_discount(admin_tab_7):
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


def admin_menu_tabs_init(gui, admin_manager):

    if gui.user_type_tab in gui.tabs_list:
        gui.remove_tab(gui.user_type_tab)

    # adding the tabs and naming them below

    admin_tab_1 = ttk.Frame(gui.tabs)
    admin_tab_2 = ttk.Frame(gui.tabs)
    admin_tab_3 = ttk.Frame(gui.tabs)
    admin_tab_4 = ttk.Frame(gui.tabs)
    admin_tab_5 = ttk.Frame(gui.tabs)
    admin_tab_6 = ttk.Frame(gui.tabs)
    admin_tab_7 = ttk.Frame(gui.tabs)
    admin_tab_8 = ttk.Frame(gui.tabs)

    gui.add_tab(admin_tab_1, text="Show Suppliers")
    gui.add_tab(admin_tab_2, text="Product Search")
    gui.add_tab(admin_tab_3, text="Add Suppliers")
    gui.add_tab(admin_tab_4, text="Unconfirmed Orders")
    gui.add_tab(admin_tab_5, text="Add Products")
    gui.add_tab(admin_tab_6, text="Add Discounts")
    gui.add_tab(admin_tab_7, text="Assign Discounts")
    gui.add_tab(admin_tab_8, text="Main Menu")

    admin_menu(gui, admin_manager)


def back_to_main_menu(gui):
    gui.remove_all_tabs()
    init_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu)
