from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.MenuSwitcher import go_to_main_menu


def admin_show_suppliers(admin_tab_1, gui):

    # adjust height and width in the result box
    result_text_supplier = Text(admin_tab_1, width=160, height=60)
    result_text_supplier.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # to format it correctly i choose the different lengths and added them together
    header = f"{'Name':<30} | {'Phone number':<16} | {'Street Name':<30}| {'zip code':<8}| {'City':<30}| {'Country':<30}\n"

    # this is to add dotted lines below
    result_text_supplier.insert('end', header)
    result_text_supplier.insert('end', '-' * 160 + '\n')

    gui.cursor.execute('''SELECT * FROM Supplier''')
    suppliers = gui.cursor.fetchall()

    result_text_supplier.delete('3.0', 'end')
    # inserting the supplier info inputted
    for supplier in suppliers:
        result_text_supplier.insert('end',
                                    f"{supplier[1]:<30} | {supplier[6]:<16} | {supplier[2]:<30}| {supplier[3]:<8}| {supplier[4]:<30}| {supplier[5]:<30}\n")
        result_text_supplier.insert('end', '-' * 160 + '\n')



def admin_menu(gui, admin_manager):
    # this function is to display the different tabs when the tabs are clicked on
    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: admin_tab_changed(gui))

    def admin_tab_change(gui, admin_manager):
        current_tab_index = gui.tabs.index(gui.tabs.select())

        switch_case = {
            0: lambda: admin_show_suppliers(gui.tabs.nametowidget(gui.tabs.select()), gui),
            1: lambda: admin_search_products_tab(gui.tabs.nametowidget(gui.tabs.select()),admin_manager, gui),
            2: lambda: admin_add_supplier_tab(gui.tabs.nametowidget(gui.tabs.select()), gui, admin_manager),
            3: lambda: admin_order_history_tab(gui.tabs.nametowidget(gui.tabs.select()), gui, admin_manager),
            4: lambda: admin_add_product_tab(gui.tabs.nametowidget(gui.tabs.select()), gui, admin_manager),
            5: lambda: admin_add_discount_tab(gui.tabs.nametowidget(gui.tabs.select()),gui, admin_manager),
            6: lambda: admin_assign_discount(gui.tabs.nametowidget(gui.tabs.select()), gui, admin_manager),
            7: lambda: admin_main_menu(gui.tabs.nametowidget(gui.tabs.select()), gui),
            8: lambda: admin_set_date(gui.tabs.nametowidget(gui.tabs.select()), admin_manager,gui),
        }

        # this is because get just gets the number but doesn't call the switch_case dictionairy so if func lines are needed to call the dictionairy
        switch_case.get(current_tab_index)
        func = switch_case.get(current_tab_index)
        if func:
            func()

    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: admin_tab_change(gui, admin_manager))


def unbind_admin_menu_events(gui):
    gui.tabs.unbind("<<NotebookTabChanged>>")


def admin_logout(gui):
    unbind_admin_menu_events(gui)

    go_to_main_menu(
        gui,
        gui.switch_to_customer_menu,
        gui.switch_to_admin_menu,
    )


def admin_search_products_tab(admin_tab_2, admin_manager, gui):

    product_id_search_label = Label(admin_tab_2, text="Product ID:")
    product_id_search_label.grid(row=0, column=0, padx=0, pady=5, sticky="w")
    product_id_search_input = Entry(admin_tab_2, width=40)
    product_id_search_input.grid(row=0, column=1, padx=0, pady=5)

    product_name_search_label = Label(admin_tab_2, text="Product name:")
    product_name_search_label.grid(row=1, column=0, padx=0, pady=5, sticky="w")
    product_name_search_input = Entry(admin_tab_2, width=40)
    product_name_search_input.grid(row=1, column=1, padx=0, pady=5)

    product_base_search_price_label = Label(admin_tab_2, text="Price:")
    product_base_search_price_label.grid(row=0, column=2, padx=0, pady=5, sticky="w")
    product_base_search_price_input = Entry(admin_tab_2, width=40)
    product_base_search_price_input.grid(row=0, column=3, padx=0, pady=5)

    product_supplier_search_label = Label(admin_tab_2, text="Product supplier:")
    product_supplier_search_label.grid(row=1, column=2, padx=0, pady=5, sticky="w")
    product_supplier_search_input = Entry(admin_tab_2, width=40)
    product_supplier_search_input.grid(row=1, column=3, padx=0, pady=5)

    submit_search_box_input_label = Button(admin_tab_2, text="Search for product", width=20,
                                   command=lambda: search_info_setter(gui, admin_manager,
                                                                      product_id_search_input.get().strip(),
                                                                      product_name_search_input.get().strip(),
                                                                      product_base_search_price_input.get().strip(),
                                                                      product_supplier_search_input.get().strip()))

    submit_search_box_input_label.grid(row=2, column=1, padx=0, pady=5, sticky="w")

    gui.cursor.execute('''SELECT * FROM Product''')
    products = gui.cursor.fetchall()
    print("here's the products")

    # adjust height and width in the result box
    result_text = Text(admin_tab_2, width=137, height=40)
    result_text.grid(row=3, column=0, columnspan=4, padx=0, pady=5)

    # to format it correctly i choose the different lengths
    # product id is 10 because len(product ID) == 10, same logic applies to why "product quantity" is 16
    # so result text grid is (10 + 16 + 25 + 10 + 30 - 1) == 100
    result_text.insert('end',
                       f"{'Product ID':<10} | {'Product quantity':<16} | {'Product Name':<25}| {'Base Price':<10}| {'Supplier':<25}| {'number of sales':<15} | {'From':<10} | {'To':<10}\n")
    # this is to add dotted lines below
    result_text.insert('end', '-' * 137 + '\n')

    # inserting the product info inputted
    for product in products:
        # checking if the product has a discount added to it
        print(product[8])
        if product[8] is not None:
            gui.cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[8],))
            discount = gui.cursor.fetchone()
            result_text.insert('end',
                               f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}| {discount[4]}| {discount[5]}\n")
            result_text.insert('end', '-' * 137 + '\n')
        else:
            print(product[8])
            print(product)
            result_text.insert('end',
                               f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}\n")
            result_text.insert('end', '-' * 137 + '\n')


    admin_tab_2.grid_columnconfigure(4, weight=0)
    admin_tab_2.grid_columnconfigure(5, weight=0)

    product_code_label_2 = Label(admin_tab_2, text="Product ID:")
    product_code_label_2.grid(row=0, column=4, padx=(5, 2), pady=5, sticky="w")

    product_code_input_2 = Entry(admin_tab_2, width=35)

    product_code_input_2.place(relx=0.83, rely=0.007)


    submit_product_to_remove_label = Button(admin_tab_2, text="Delete Product", width=20,
                                   command=lambda: submit_product_to_remove())

    submit_product_to_remove_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")

    # showing current date
    current_date_label = Label(admin_tab_2, text="Current date: " + str(admin_manager.get_current_date()))
    current_date_label.place(relx=0.83, rely=0.085)

    def display_search_results(products):

        result_text_search = Text(admin_tab_2, width=137, height=40)
        result_text_search.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        result_text_search.delete('3.0', 'end')

        result_text_search.insert('end',
                           f"{'Product ID':<10} | {'Product quantity':<16} | {'Product Name':<25}| {'Base Price':<10}| {'Supplier':<25}| {'number of sales':<15} | {'From':<10} | {'To':<10}\n")
        # this is to add dotted lines below
        result_text_search.insert('end', '-' * 137 + '\n')

        for product in products:

            if product[8] is not None:
                gui.cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[8],))
                discount = cursor.fetchone()
                result_text_search.insert('end',
                                   f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}| {discount[4]}| {discount[5]}\n")
                result_text_search.insert('end', '-' * 137 + '\n')
            else:
                result_text_search.insert('end',
                                   f"{product[0]:<10} | {product[1]:<16} | {product[6]:<25}| {product[3]:<10}| {product[5]:<25}| {product[2]:<15}\n")
                result_text_search.insert('end', '-' * 137 + '\n')


    def admin_product_search(gui, admin_manager):
        product_id = admin_manager.get_product_id_search_input()
        product_name = admin_manager.get_product_name_search_input()
        product_base_price = admin_manager.get_product_base_price_search_input()
        product_supplier = admin_manager.get_product_supplier_search_input()

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

        gui.cursor.execute(query, tuple(values))

        searched_products = gui.cursor.fetchall()

        display_search_results(searched_products)

    def search_info_setter(gui, admin_manager, product_id, product_name, base_price, product_supplier):

        admin_manager.set_product_id_search_input(product_id)
        admin_manager.set_product_name_search_input(product_name)
        admin_manager.set_product_base_price_search_input(base_price)
        admin_manager.set_product_supplier_search_input(product_supplier)

        submit_search_info(gui, admin_manager)

    def submit_search_info(gui, admin_manager):
        if admin_manager.validate_search_info():
            result_text.grid_forget()
            admin_product_search(gui, admin_manager)


def admin_main_menu(admin_tab_8, gui):

    admin_main_menu_button = ttk.Button(admin_tab_8, text="Logout", width=40,
                                       command=lambda: admin_logout(gui))
    admin_main_menu_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")



def admin_add_discount_tab(admin_tab_6, gui, admin_manager):

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
                                        command=lambda: submit_discount_info_setter(gui, admin_manager,
                                                                                    id_discount_input.get(),
                                                                                    name_discount_input.get(),
                                                                                    discount_input.get(),
                                                                                    lower_date_input.get(),
                                                                                    upper_date_input.get(),
                                                                                    product_code_input.get()))

    submit_discount_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    discount_id_label_2 = Label(admin_tab_6, text="Discount ID:")
    discount_id_label_2.grid(row=0, column=4, padx=10, pady=10, sticky="w")
    discount_id_input_2 = Entry(admin_tab_6, width=30)
    discount_id_input_2.grid(row=0, column=5, padx=10, pady=10)

    submit_discount_to_remove_label = Button(admin_tab_6, text="Delete discount", width=20,
                                            command=lambda: submit_discount_to_remove())

    submit_discount_to_remove_label.grid(row=1, column=5, padx=10, pady=10, sticky="w")


def submit_discount_info_setter(gui, admin_manager, id_discount, name_discount, discount_percentage, lower_date, upper_date, product_id_discount):

    admin_manager.set_id_discount_input(id_discount)
    admin_manager.set_name_discount_input(name_discount)
    admin_manager.set_discount_input(discount_percentage)
    admin_manager.set_lower_date_input(lower_date)
    admin_manager.set_upper_date_input(upper_date)
    admin_manager.set_product_code_input(product_id_discount)

    submit_discount_info(gui, admin_manager)


def submit_discount_info(gui, admin_manager):
    if admin_manager.validate_discount_add(gui):
        admin_manager.admin_add_discount(gui)


def admin_add_supplier_tab(admin_tab_3, gui, admin_manager):

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

    submit_supplier_info_label = Button(
        admin_tab_3, text="Submit supplier", width=40,
        command=lambda: submit_supplier_info_setter(
            admin_manager, gui,
            name_input, street_input, zip_code_input,
            city_input, country_input, phone_number_input
        )
    )
    submit_supplier_info_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")


# function that is setting the inputted values as attributes inside the adminManager class
def submit_supplier_info_setter(admin_manager, gui, name_input, street_input, zip_code_input, city_input, country_input,
                                phone_number_input):

    # setting the input values
    admin_manager.set_name_input(name_input.get())
    admin_manager.set_street_input(street_input.get())
    admin_manager.set_zip_code_input(zip_code_input.get())
    admin_manager.set_city_input(city_input.get())
    admin_manager.set_country_input(country_input.get())
    admin_manager.set_phone_number_input(phone_number_input.get())

    # clears the input fields after supplier info has been submitted
    name_input.delete(0, 'end')
    street_input.delete(0, 'end')
    zip_code_input.delete(0, 'end')
    city_input.delete(0, 'end')
    country_input.delete(0, 'end')
    phone_number_input.delete(0, 'end')

    # function that submits the supplier info
    submit_supplier_info(admin_manager, gui)


def submit_supplier_info(admin_manager, gui):
    if admin_manager.validate_inputs_supplier():
        admin_manager.admin_add_supplier(gui)


def admin_order_history_tab(admin_tab_4, gui, admin_manager):
    gui.cursor.execute("SELECT * FROM Shopping_list")
    shopping_lists = gui.cursor.fetchall()

    order_history_frame = Frame(admin_tab_4)
    order_history_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
    if shopping_lists:
        for shopping_list in shopping_lists:
            gui.cursor.execute('''SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ? ''', (shopping_list[0],))
            total_cost = gui.cursor.fetchone()[0]
            # to make sure it only shows orders
            if total_cost is not None and total_cost > 0:
                btn = Button(order_history_frame,
                             text=f"Shopping List Number: {shopping_list[0]} Total Price: {round(total_cost, 2)} \n",
                             command=lambda idx=shopping_list[0]: admin_manager.select_shopping_list_admin(idx, gui),
                             width=120)
                btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)


def admin_set_date(admin_tab_9, admin_manager, gui):
    set_date = Label(admin_tab_9, text="YYYY-MM-DD Date:")
    set_date.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    set_date_input = Entry(admin_tab_9, width=30)
    set_date_input.grid(row=0, column=1, padx=10, pady=10)

    submit_date_label = Button(admin_tab_9, text="Set new date", width=40,
                                       command=lambda: submit_date_setter(admin_manager, set_date_input.get()))

    submit_date_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    current_date = admin_manager.get_current_date()

    current_date = ttk.Label(admin_tab_9, text="current date YYYY-MM-DD: " + current_date)
    current_date.grid(row=0, column=2, padx=10, pady=10, sticky="w")


def submit_date_setter(admin_manager, input_date):
    valid_input = admin_manager.validate_date_input(input_date)
    if valid_input:
        admin_manager.set_current_date(input_date)



def admin_add_product_tab(admin_tab_5, gui, admin_manager):

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
                                       command=lambda: submit_product_info_setter(gui, admin_manager,
                                                                           id_input_product.get(),
                                                                           product_name_input.get(),
                                                                           product_base_price_input.get(),
                                                                           product_supplier_input.get(),
                                                                           product_quantity_input.get()))

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
                                       command=lambda: submit_product_quantity_edit_info_setter(gui, admin_manager,
                                                                                                product_id_input_2.get().strip(),
                                                                                                product_quantity_input_2.get().strip()))

    submit_product_info_label_2.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    admin_menu(gui, admin_manager)


def submit_product_info_setter(gui, admin_manager,
                               id_input_product,
                               product_name_input,
                               product_base_price_input,
                               product_supplier_input,
                               product_quantity_input):

    admin_manager.set_id_input_product(id_input_product)
    admin_manager.set_product_name_input(product_name_input)
    admin_manager.set_product_base_price_input(product_base_price_input)
    admin_manager.set_product_supplier_input(product_supplier_input)
    admin_manager.set_product_quantity_input(product_quantity_input)

    submit_product_info(gui, admin_manager)


def submit_product_info(gui, admin_manager):
    if admin_manager.validate_inputs_product():
        admin_manager.admin_add_product(gui)

    admin_menu(gui, admin_manager)


def submit_product_quantity_edit_info_setter(gui, admin_manager, product_id, product_quantity):
    admin_manager.set_product_quantity_input_2(product_id)
    admin_manager.set_product_id_input_2(product_quantity)

    submit_product_quantity_edit_info(gui, admin_manager)


def submit_product_quantity_edit_info(gui, admin_manager):
    if admin_manager.validate_product_quantity_edit(gui):
        admin_manager.admin_edit_quantity_product(gui)
    admin_menu(gui, admin_manager)


# this function automatically assign discount to matching product when tab is switched to
def admin_assign_discount(admin_tab_7, gui, admin_manager):

    # creating the frame that shows discount and products
    discount_frame = Frame(admin_tab_7)
    discount_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # getting all the discounts
    gui.cursor.execute('''SELECT product_code, discount_code FROM Discount_item''')
    discounts = gui.cursor.fetchall()

    # assigning the discounts
    for product_code, discount_code in discounts:
        gui.cursor.execute("UPDATE Product SET Discount_ID = ? WHERE product_code = ?", (discount_code, product_code))

    # updating
    #gui.conn.commit()

    gui.cursor.execute('''SELECT * FROM Discount''')
    discounts = gui.cursor.fetchall()

    # clearing the frame before adding new buttons
    for widget in discount_frame.winfo_children():
        widget.destroy()

    # inserting buttons for each discount
    for discount in discounts:
        btn = Button(discount_frame,
                     text=f"'Discount ID' {discount[0]} 'Discount category' {discount[2]} 'Discount Percentage' {discount[1]}% 'From' {discount[3]} 'To' {discount[4]}",
                     command=lambda idx=discount[0]: admin_manager.select_discount(idx), width=80)
        btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)


    # creating a frame for product buttons
    product_frame = Frame(admin_tab_7)
    product_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10)


    # displaying all the discounts
    def display_all_discounts_2(gui):
        gui.cursor.execute('''SELECT * FROM Product''')
        products = gui.cursor.fetchall()

        # clearing the frame before adding new buttons
        for widget in product_frame.winfo_children():
            widget.destroy()

        # inserting buttons for each product
        for product in products:
            discount_info = "None"

            if product[8] is not None:
                gui.cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (product[8],))
                discount = gui.cursor.fetchone()
                if discount[4] < discount[3] < discount[5]:
                    discount_info = f"Discount ID: {discount[0]}  Discount ID: {discount[2]}  Product Price: {float(product[3])*((100-float(discount[1]))/100)}  Discount Percentage:  {discount[1]}%  From:  {discount[4]}  To:  {discount[5]}"
                else:
                    discount_info = f"Discount ID: {discount[0]}  Discount ID: {discount[2]}  Product Price: {float(product[3])}  Discount Percentage:  {discount[1]}%  From:  {discount[4]}  To:  {discount[5]}"
            btn = Button(product_frame, text=f" Product ID: {product[0]}  Product Name:  {product[6]} Discount: {discount_info}",
                         command=lambda idx=product[0]: admin_manager.select_product(idx), width=160)

            btn.pack(side=TOP, padx=5, pady=5, fill="none", expand=False)

    admin_tab_7.bind("<Visibility>", lambda event: display_all_discounts_2(gui))

    # button to manually assign discount to product
    assign_discount_button = Button(admin_tab_7, text="Assign Discount", command=lambda:admin_manager.assign_selected_discount_to_product(gui))
    assign_discount_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    # button to manually remove discount from product
    assign_discount_button = Button(admin_tab_7, text="Remove discount from product", command=lambda:admin_manager.remove_discount(gui))
    assign_discount_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)




def admin_menu_tabs_init(gui, admin_manager):
    selected_tab = gui.tabs.select()
    if selected_tab:
        tab_widget = gui.root.nametowidget(selected_tab)
        if tab_widget in gui.tabs_list:
            gui.remove_tab(tab_widget)

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
    admin_tab_9 = ttk.Frame(gui.tabs)

    gui.add_tab(admin_tab_1, text="Show Suppliers")
    gui.add_tab(admin_tab_2, text="Product Search")
    gui.add_tab(admin_tab_3, text="Add Suppliers")
    gui.add_tab(admin_tab_4, text="Unconfirmed Orders")
    gui.add_tab(admin_tab_5, text="Add Products")
    gui.add_tab(admin_tab_6, text="Add Discounts")
    gui.add_tab(admin_tab_7, text="Assign Discounts")
    gui.add_tab(admin_tab_8, text="Main Menu")
    gui.add_tab(admin_tab_9, text="Set Date")

    admin_menu(gui, admin_manager)


def back_to_main_menu(gui):
    gui.remove_all_tabs()
    init_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu)
