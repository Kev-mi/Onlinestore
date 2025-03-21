from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
import view.MainMenu as MainMenu
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.MenuSwitcher import go_to_main_menu
import tkinter as tk
from tkinter import StringVar

def customer_menu(gui, customer_manager):

    def customer_tab_change(gui, customer_manager):
        current_tab_index = gui.tabs.index(gui.tabs.select())
        print(f"selected customer index is: {current_tab_index}")
        switch_case = {
            0: lambda: customer_search_products_tab(gui, gui.tabs.nametowidget(gui.tabs.select()), customer_manager),
            1: lambda: customer_sign_up(gui,gui.tabs.nametowidget(gui.tabs.select()), customer_manager),
            2: lambda: customer_main_menu(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
            3: lambda: customer_login(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
            4: lambda: customer_logout_menu(gui.tabs.nametowidget(gui.tabs.select()), customer_manager, gui),
            5: lambda: customer_current_order_tab(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
            6: lambda: customer_order_history_tab(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
        }

        # this is because get just gets the number but doesn't call the switch_case dictionairy so if func lines are needed to call the dictionairy
        switch_case.get(current_tab_index)
        func = switch_case.get(current_tab_index)
        if func:
            func()

    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: customer_tab_change(gui, customer_manager))


def customer_search_products_tab(gui, customer_tab_1, customer_manager):

    # Input fields
    product_id_input = Entry(customer_tab_1, width=30)
    product_name_input = Entry(customer_tab_1, width=30)
    base_price_input = Entry(customer_tab_1, width=30)
    supplier_input = Entry(customer_tab_1, width=30)
    product_frame = Frame(customer_tab_1)

    # Layout
    Label(customer_tab_1, text="Product ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    product_id_input.grid(row=0, column=1, padx=10, pady=10)

    Label(customer_tab_1, text="Product Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    product_name_input.grid(row=1, column=1, padx=10, pady=10)

    Label(customer_tab_1, text="Price:").grid(row=0, column=2, padx=10, pady=10, sticky="w")
    base_price_input.grid(row=0, column=3, padx=10, pady=10)

    Label(customer_tab_1, text="Product Supplier:").grid(row=1, column=2, padx=10, pady=10, sticky="w")
    supplier_input.grid(row=1, column=3, padx=10, pady=10)

    Button(customer_tab_1, text="Search for Product", width=20,
           command=lambda: search_products(gui,
               customer_manager, product_id_input.get(), product_name_input.get(),
               base_price_input.get(), supplier_input.get(), product_frame)
           ).grid(row=2, column=1, padx=10, pady=10, sticky="w")

    Button(customer_tab_1, text="Show Discount Items", width=20,
           command=lambda: show_discounted_products(customer_manager, product_frame, gui)
           ).grid(row=2, column=2, padx=10, pady=10, sticky="w")

    Button(customer_tab_1, text="Show All Items", width=20,
           command=lambda: show_all_products(customer_manager, product_frame, gui)
           ).grid(row=2, column=3, padx=10, pady=10, sticky="w")

    product_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    # Display all products on tab expose
    customer_tab_1.bind("<Expose>", lambda event: display_all_products(customer_manager, product_frame, gui))


# form for customer sign up
def customer_sign_up(gui,customer_tab_2, customer_manager):
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

    ttk.Button(
        customer_tab_2,
        text="Sign Up",
        width=40,
        command=lambda: customer_sign_up_setter(gui,customer_manager,
                                                customer_username_input.get().strip(),
                                                customer_password_input.get().strip(),
                                                customer_first_name_input.get().strip(),
                                                customer_last_name_input.get().strip(),
                                                customer_email_input.get().strip(),
                                                customer_address_input.get().strip(),
                                                customer_city_input.get().strip(),
                                                customer_country_input.get().strip(),
                                                customer_phone_number_input.get().strip()
                                                )
    ).grid(row=9, column=1, padx=10, pady=10, sticky="w")


def customer_sign_up_setter(gui,customer_manager,
                            customer_username_input,
                            customer_password_input,
                            customer_first_name_input,
                            customer_last_name_input,
                            customer_email_input,
                            customer_address_input,
                            customer_city_input,
                            customer_country_input,
                            customer_phone_number_input):

    customer_manager.set_customer_username(customer_username_input)
    customer_manager.set_customer_password(customer_password_input)
    customer_manager.set_customer_first_name(customer_first_name_input)
    customer_manager.set_customer_last_name(customer_last_name_input)
    customer_manager.set_customer_email(customer_email_input)
    customer_manager.set_customer_address(customer_address_input)
    customer_manager.set_customer_city(customer_city_input)
    customer_manager.set_customer_country(customer_country_input)
    customer_manager.set_customer_phone_number(customer_phone_number_input)

    submit_customer_sign_up_info(gui, customer_manager)


def customer_login(customer_tab_4, gui, customer_manager):
    customer_username_login_label = ttk.Label(customer_tab_4, text="Username:")
    customer_username_login_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    customer_username_login_input = ttk.Entry(customer_tab_4, width=30)
    customer_username_login_input.grid(row=0, column=1, padx=10, pady=10)

    customer_password_login_label = ttk.Label(customer_tab_4, text="Password:")
    customer_password_login_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    customer_password_login_input = ttk.Entry(customer_tab_4, width=30)
    customer_password_login_input.grid(row=1, column=1, padx=10, pady=10)

    customer_login_button = ttk.Button(customer_tab_4, text="Log in", width=40,
                                       command=lambda: customer_login_info_setter(gui, customer_manager,
                                                                                  customer_username_login_input.get().strip(),
                                                                                  customer_password_login_input.get().strip()))
    customer_login_button.grid(row=9, column=1, padx=10, pady=10, sticky="w")

    customer_menu(gui, customer_manager)


def customer_login_info_setter(gui, customer_manager,customer_username_login_input, customer_password_login_input):

    customer_manager.set_customer_username_login_input(customer_username_login_input)
    customer_manager.set_customer_password_login_input(customer_password_login_input)

    submit_customer_login_info(gui, customer_manager)


def submit_customer_login_info(gui, customer_manager):
    if customer_manager.validate_customer_login(gui):
        customer_manager.customer_login_fucntion()
        customer_menu(gui, customer_manager)


def show_all_products(customer_manager, product_frame, gui):

    for widget in product_frame.winfo_children():
        widget.destroy()

    products = customer_manager.get_all_products(gui)

    for product in products:

        discount_rate = customer_manager.get_discount_rate(gui, product)

        add_product_to_frame(product_frame, product, gui, customer_manager, discount_rate)

def display_all_products(customer_manager, product_frame, gui):

    for widget in product_frame.winfo_children():
        widget.destroy()

    products = customer_manager.get_all_products(gui)
    for product in products:

        discount_rate = customer_manager.get_discount_rate(gui, product)

        add_product_to_frame(product_frame, product, gui, customer_manager, discount_rate)


def search_products(gui, customer_manager, product_id, product_name, base_price, supplier_name, product_frame):

    for widget in product_frame.winfo_children():
        widget.destroy()

    products = customer_manager.search_products(gui, product_id, product_name, base_price, supplier_name)
    for product in products:

        discount_rate = customer_manager.get_discount_rate(gui, product)

        add_product_to_frame(product_frame, product, gui, customer_manager, discount_rate)


def show_discounted_products(customer_manager, product_frame, gui):

    for widget in product_frame.winfo_children():
        widget.destroy()

    discounted_products = customer_manager.get_discounted_products(gui)
    for product, discount_rate in discounted_products:
        discount_rate = customer_manager.get_discount_rate(gui, product)
        add_product_to_frame(product_frame, product, gui, customer_manager, discount_rate)


# adds products as clickable button
def add_product_to_frame(product_frame, product, gui , customer_manager, discount_rate=0):

    print("here's discount rates in customer menu product menu")
    print(discount_rate)

    next_row = len(product_frame.grid_slaves())

    select_product_button = ttk.Button(
        product_frame,
        text=f"Product ID: {product[0]}  Product name: {product[6]} Product Price: {round(float(product[3]) * ((100 - float(discount_rate)) / 100), 2)}  Product quantity: {product[1]} Supplier: {product[5]}",
        width=120,
        command=lambda: customer_manager.select_product_customer(product[0], gui)
    )
    select_product_button.grid(row=next_row + 1, column=0, padx=5, pady=5, sticky="w")



def customer_main_menu(customer_tab_3, gui, customer_manager):

    customer_login_button = ttk.Button(customer_tab_3, text="Go to main menu", width=40,
                                       command=lambda: customer_go_to_main_menu(gui, customer_manager))
    customer_login_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def customer_go_to_main_menu(gui, customer_manager):

    # this is to go back to main menu
    customer_manager.set_current_user_name("")
    customer_manager.set_customer_logged_in(False)

    unbind_customer_menu_events(gui)

    #this is also to remove the window so windows doesn't keep adding up
    go_to_main_menu(
        gui,
        gui.switch_to_customer_menu,
        gui.switch_to_admin_menu,
    )


def submit_customer_sign_up_info(gui, customer_manager):
    if customer_manager.validate_user_sign_up(gui):
        customer_manager.create_customer(gui)
        customer_menu(gui, customer_manager)


def unbind_customer_menu_events(gui):
    gui.tabs.unbind("<<NotebookTabChanged>>")

def customer_logout_menu(customer_tab_5, customer_manager, gui):

    customer_logout_button = ttk.Button(customer_tab_5, text="logout", width=40,
                                       command=lambda: customer_logout_function(gui, customer_manager))

    customer_logout_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def customer_logout_function(gui, customer_manager):

    if customer_manager.get_customer_logged_in() == True:
        customer_manager.set_customer_logged_in(False)
        customer_manager.set_current_user_name("")
        messagebox.showerror("Error", "Customer got logged out")
    else:
        messagebox.showerror("Error", "Customer is not logged in")


    customer_menu(gui, customer_manager)


def customer_current_order_tab(customer_tab_6, gui, customer_manager):

    result_text = tk.Text(customer_tab_6, width=137, height=40)
    result_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    current_user_name = customer_manager.get_current_user_name()

    print("current user")
    print(current_user_name)

    # gets the shopping list from the current user that hasn't been confirmed by admin
    gui.cursor.execute(
        'SELECT Shopping_list_id FROM Shopping_list WHERE username = ? AND confirmed_order = FALSE ORDER BY Shopping_list_id DESC LIMIT 1',
        (current_user_name,))
    active_shopping_list = gui.cursor.fetchone()


    if active_shopping_list:
        shopping_list_id = active_shopping_list[0]
        gui.cursor.execute('''
                SELECT sli.product_code, sli.quantity, p.product_name, p.base_price, p.discount_id
                FROM Shopping_list_item sli
                JOIN Product p ON sli.product_code = p.product_code
                WHERE sli.Shopping_list_id = ? AND sli.ordered = FALSE
            ''', (shopping_list_id,))
        products = gui.cursor.fetchall()
    else:
        products = []

    total_cost = 0

    for product in products:
        product_code, quantity, product_name, base_price, discount_code = product
        discount_rate = customer_manager.get_discount_rate_current_order(gui, discount_code)

        # calculate item cost
        item_total_cost = quantity * base_price
        discounted_cost = item_total_cost * ((100 - discount_rate) / 100)
        total_cost += discounted_cost

        # display product details
        result_text.insert(
            tk.END,
            f"Product Name: {product_name} | Quantity in order: {quantity} | Order cost: {round(discounted_cost, 2)}\n"
        )

    submit_supplier_info_label = ttk.Button(customer_tab_6, text="Place order", width=40,
                                            command=lambda: customer_manager.customer_place_order(gui))
    submit_supplier_info_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    customer_menu(gui, customer_manager)


def customer_order_history_tab(customer_tab_7, gui, customer_manager):

    gui.cursor.execute("SELECT * FROM Shopping_list WHERE username = ? AND placed_order = TRUE", (customer_manager.get_current_user_name(),))
    shopping_lists = gui.cursor.fetchall()

    # iterating of the orders placed
    for button in gui.order_history_buttons.values():
        button.destroy()
    gui.order_history_buttons.clear()

    if shopping_lists:
        for shopping_list in shopping_lists:
            shopping_list_id = shopping_list[0]
            gui.cursor.execute('SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ?', (shopping_list_id,))
            total_cost = gui.cursor.fetchone()[0]
            if total_cost is not None:
                customer_manager.create_order_history_button(customer_tab_7,shopping_list_id, gui)


def customer_menu_tabs_init(gui, customer_manager):
    # this is to display the menu tabs for the customer
    if gui.user_type_tab in gui.tabs_list:
        gui.remove_tab(gui.user_type_tab)

    customer_tab_1 = ttk.Frame(gui.tabs)
    customer_tab_2 = ttk.Frame(gui.tabs)
    customer_tab_3 = ttk.Frame(gui.tabs)
    customer_tab_4 = ttk.Frame(gui.tabs)
    customer_tab_5 = ttk.Frame(gui.tabs)
    customer_tab_6 = ttk.Frame(gui.tabs)
    customer_tab_7 = ttk.Frame(gui.tabs)

    gui.add_tab(customer_tab_1, text="Search Product")
    gui.add_tab(customer_tab_2, text="Sign up")
    gui.add_tab(customer_tab_3, text="Main Menu")
    gui.add_tab(customer_tab_4, text="Login")
    gui.add_tab(customer_tab_5, text="Logout")
    gui.add_tab(customer_tab_6, text="Place Order")
    gui.add_tab(customer_tab_7, text="Show order history")

    customer_menu(gui, customer_manager)
