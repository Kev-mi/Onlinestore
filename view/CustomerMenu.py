from tkinter import ttk, messagebox, simpledialog, filedialog, Button, Text, Scrollbar, Frame, TOP, END, VERTICAL, Entry, Label
import view.MainMenu as MainMenu
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller.Controller import go_to_main_menu
import tkinter as tk


def customer_menu(gui, customer_manager):

    def customer_tab_change(gui, customer_manager):
        current_tab_index = gui.tabs.index(gui.tabs.select())
        print(f"selected customer index is: {current_tab_index}")
        switch_case = {
            0: lambda: customer_search_products_tab(gui.tabs.nametowidget(gui.tabs.select()), customer_manager),
            1: lambda: customer_sign_up(gui.tabs.nametowidget(gui.tabs.select()), customer_manager),
            2: lambda: customer_main_menu(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
            3: lambda: customer_login(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
            4: lambda: customer_logout_menu(gui.tabs.nametowidget(gui.tabs.select())),
            5: lambda: customer_current_order_tab(gui.tabs.nametowidget(gui.tabs.select()), gui, customer_manager),
            6: lambda: customer_order_history_tab(gui, customer_manager),
        }

        # this is because get just gets the number but doesn't call the switch_case dictionairy so if func lines are needed to call the dictionairy
        switch_case.get(current_tab_index)
        func = switch_case.get(current_tab_index)
        if func:
            func()

    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: customer_tab_change(gui, customer_manager))


def customer_search_products_tab(customer_tab_1, customer_manager):
    print("this works")
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
           command=lambda: search_products(
               customer_manager, product_id_input.get(), product_name_input.get(),
               base_price_input.get(), supplier_input.get(), product_frame)
           ).grid(row=2, column=1, padx=10, pady=10, sticky="w")

    Button(customer_tab_1, text="Show Discount Items", width=20,
           command=lambda: show_discounted_products(customer_manager, product_frame)
           ).grid(row=2, column=2, padx=10, pady=10, sticky="w")

    product_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    # Display all products on tab expose
    customer_tab_1.bind("<Expose>", lambda event: display_all_products(customer_manager, product_frame))


# form for customer sign up
def customer_sign_up(customer_tab_2, customer_manager):

    ttk.Label(customer_tab_2, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    customer_manager.username_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.username_input.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    customer_manager.password_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.password_input.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="First Name:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    customer_manager.first_name_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.first_name_input.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="Last Name:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    customer_manager.last_name_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.last_name_input.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="Email:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    customer_manager.email_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.email_input.grid(row=4, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="Address:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
    customer_manager.address_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.address_input.grid(row=5, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="City:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
    customer_manager.city_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.city_input.grid(row=6, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="Country:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
    customer_manager.country_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.country_input.grid(row=7, column=1, padx=10, pady=10)

    ttk.Label(customer_tab_2, text="Phone number:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
    customer_manager.phone_number_input = ttk.Entry(customer_tab_2, width=30)
    customer_manager.phone_number_input.grid(row=8, column=1, padx=10, pady=10)

    ttk.Button(
        customer_tab_2,
        text="Sign Up",
        width=40,
        command=lambda: submit_customer_sign_up_info(customer_manager)
    ).grid(row=9, column=1, padx=10, pady=10, sticky="w")


def display_all_products(customer_manager, product_frame):

    for widget in product_frame.winfo_children():
        widget.destroy()

    products = customer_manager.get_all_products()
    for product in products:
        add_product_to_frame(product_frame, product)


def search_products(customer_manager, product_id, product_name, base_price, supplier_name, product_frame):

    for widget in product_frame.winfo_children():
        widget.destroy()

    products = customer_manager.search_products(product_id, product_name, base_price, supplier_name)
    for product in products:
        add_product_to_frame(product_frame, product)


def show_discounted_products(customer_manager, product_frame):

    for widget in product_frame.winfo_children():
        widget.destroy()

    discounted_products = customer_manager.get_discounted_products()
    for product, discount_rate in discounted_products:
        add_product_to_frame(product_frame, product, discount_rate)


# adds discount as clickable button
def add_product_to_frame(product_frame, product, discount_rate=None):
    discount_text = f" (Discount: {discount_rate}%)" if discount_rate else ""
    btn_text = f"Product ID: {product[0]} | Name: {product[6]} | Price: {round(product[3] * (1 - (discount_rate or 0) / 100), 2)} | Quantity: {product[1]} | Supplier: {product[5]}{discount_text}"

    next_row = len(product_frame.grid_slaves())
    Button(product_frame, text=btn_text, width=120).grid(row=next_row, column=0, padx=5, pady=5, sticky="w")


def customer_main_menu(customer_tab_3, gui, customer_manager):

    customer_login_button = ttk.Button(customer_tab_3, text="Go to main menu", width=40,
                                       command=lambda: customer_go_to_main_menu(gui, customer_manager))
    customer_login_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


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
                                        command=lambda: submit_customer_login_info())
    customer_login_button.grid(row=9, column=1, padx=10, pady=10, sticky="w")

    customer_menu(gui, customer_manager)


def submit_customer_login_info():
    if validate_customer_login():
        customer_login_fucntion()
        customer_menu()


def customer_go_to_main_menu(gui, customer_manager):

    # this is to go back to main menu
    customer_manager.set_current_user_name("")
    customer_manager.set_customer_logged_in(False)

    #this is also to remove the window so windows doesn't keep adding up
    go_to_main_menu(
        gui,
        gui.switch_to_customer_menu,
        gui.switch_to_admin_menu,
        customer_manager
    )


def submit_customer_sign_up_info(customer_manager):
    if customer_manager.validate_user_sign_up():
        customer_manager.create_customer()
        customer_menu()


def customer_logout_menu(customer_tab_5):

    customer_logout_button = ttk.Button(customer_tab_5, text="logout", width=40,
                                       command=lambda: customer_logout_function())

    customer_logout_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")


def customer_logout_function():
    global customer_logged_in
    global current_user_name
    if customer_logged_in == True:
        customer_logged_in = False
        current_user_name = ""
    else:
        messagebox.showerror("Error", "Customer is not logged in")

    customer_menu()


def customer_current_order_tab(customer_tab_6, gui, customer_manager):
    result_text = tk.Text(customer_tab_6, width=137, height=40)
    result_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    def display_all_products(gui):
        gui.cursor.execute('SELECT Shopping_list_id FROM Shopping_list WHERE username = ? AND confirmed_order = FALSE ORDER BY Shopping_list_id DESC LIMIT 1', (current_user_name,))
        active_shopping_list = cursor.fetchone()

        if active_shopping_list:
            shopping_list_id = active_shopping_list[0]
            gui.cursor.execute('SELECT * FROM Shopping_list_item WHERE Shopping_list_id = ? AND ordered = FALSE', (shopping_list_id,))
            products = cursor.fetchall()
        else:
            products = []

        result_text.delete('1.0', tk.END)
        total_cost = 0

        for product in products:
            gui.cursor.execute('SELECT * FROM Product WHERE product_code = ?', (product[2],))
            product_details = cursor.fetchone()

            discount_code = product_details[-1]

            gui.cursor.execute('''SELECT * FROM Discount WHERE discount_code = ?''', (discount_code,))
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

    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: display_all_products(gui))

    submit_supplier_info_label = ttk.Button(customer_tab_6, text="Place order", width=40, command=lambda: customer_place_order())
    submit_supplier_info_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    customer_menu(gui, customer_manager)


def create_order_history_button(shopping_list_id):
    cursor.execute('SELECT total_cost FROM Shopping_list WHERE Shopping_list_id = ?', (shopping_list_id,))
    total_cost = cursor.fetchone()[0]

    order_history_frame = Frame(customer_tab_7)
    order_history_frame.grid(row=len(order_history_buttons), column=0, columnspan=4, padx=5, pady=5)

    btn = Button(order_history_frame,
                 text=f"Shopping List Number: {shopping_list_id} Total Price: {round(total_cost, 2)} \n",
                 command=lambda idx=shopping_list_id: select_shopping_list_customer(idx),
                 width=120)
    btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Use `grid` here for consistency


    order_history_buttons[shopping_list_id] = btn


def customer_order_history_tab(gui, customer_manager):


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
            total_cost = cursor.fetchone()[0]
            if total_cost is not None:
                create_order_history_button(shopping_list_id)


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
