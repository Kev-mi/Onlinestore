from tkinter import ttk


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


def admin_menu(gui):

    # this function is to display the different tabs when the tabs are clicked on
    gui.tabs.bind("<<NotebookTabChanged>>", lambda event: admin_tab_changed(gui))

    def admin_tab_changed(gui):
        current_tab_index = gui.tabs.index(gui.tabs.select())

        switch_case = {
            0: admin_show_suppliers(),
            1: admin_search_products_tab(),
            2: admin_add_supplier_tab(),
            3: admin_order_history_tab(),
            4: admin_add_product_tab(),
            5: admin_add_discount_tab(),
            6: admin_assign_discount(),
            7: admin_main_menu(),
        }

        switch_case.get(current_tab_index)


def admin_menu_tabs_init(gui):

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

    init_admin_menu(gui, admin_tab_8)


def init_admin_menu(gui, main_menu_tab):
    ttk.Button(
        main_menu_tab, text="Back to Main Menu", width=40,
        command=lambda: back_to_main_menu(gui)
    ).pack(pady=20)


def back_to_main_menu(gui):
    gui.remove_all_tabs()
    from view.MainMenu import init_main_menu
    init_main_menu(gui)
