from tkinter import ttk, messagebox
import view.CustomerMenu as CustomerMenu
import view.AdminMenu as AdminMenu
import sqlite3


def init_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu):
    user_type_tab = ttk.Frame(gui.tabs)
    gui.add_tab(user_type_tab, text="User Type")

    #saving it user type tab as an attribute to later remove it
    gui.user_type_tab = user_type_tab

    user_type_tab.grid_columnconfigure(0, weight=1)

    ttk.Button(
        user_type_tab, text="Click here to get customer menu", width=40,
        command=switch_to_customer_menu
    ).place(relx=0.4, rely=0.04)

    ttk.Button(
        user_type_tab, text="Click here to get admin menu", width=40,
        command=switch_to_admin_menu
    ).place(relx=0.4, rely=0.09)

    gui.tabs.select(user_type_tab)


def open_admin_login(gui):
    # checking if user type tab is in tab list and deletes it
    if gui.user_type_tab in gui.tabs_list:
        gui.remove_tab(gui.user_type_tab)

    admin_login_tab = ttk.Frame(gui.tabs)
    gui.add_tab(admin_login_tab, text="Admin Login")
    gui.tabs.select(admin_login_tab)

    ttk.Label(admin_login_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    username_input = ttk.Entry(admin_login_tab, width=30)
    username_input.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(admin_login_tab, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_input = ttk.Entry(admin_login_tab, width=30, show='*')
    password_input.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(admin_login_tab, text="Username: user123, Password: pass123").grid(row=0, column=2, padx=10, pady=10)

    ttk.Button(
        admin_login_tab, text="Login", width=40,
        command=lambda: handle_admin_login(gui, username_input.get(), password_input.get())
    ).grid(row=2, column=1, padx=10, pady=20)


def verifyAdminLogin(gui, AdminMenu, admin_manager):

    selected_tab = gui.tabs.select()
    if selected_tab:
        gui.remove_tab(gui.root.nametowidget(selected_tab))

    admin_login_tab = ttk.Frame(gui.tabs)

    gui.add_tab(admin_login_tab, text="Admin Login")

    username_label = ttk.Label(admin_login_tab, text="username:")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    username_input = ttk.Entry(admin_login_tab, width=30)
    username_input.grid(row=0, column=1, padx=10, pady=10)

    password_label = ttk.Label(admin_login_tab, text="password:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    password_input = ttk.Entry(admin_login_tab, width=30)
    password_input.grid(row=1, column=1, padx=10, pady=10)

    admin_login_hint = ttk.Label(admin_login_tab, text="username: user123, password: pass123")
    admin_login_hint.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # this is querying admin, it is checking if the admin username and password combination exists
    def admin_checker(username, password, gui, AdminMenu, admin_manager):
        print("it works")
        # this is to prevent query of empty field

        if not username or not password:
            return False

        try:
            gui.cursor.execute('''
                    SELECT user_type FROM User
                    WHERE username = ? AND password = ?
                ''', (username, password))
            user_type = gui.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"here is the error type: {e}")
            return False

        if user_type and user_type[0] == "admin":
            selected_tab = gui.tabs.select()
            if selected_tab:
                tab_widget = gui.root.nametowidget(selected_tab)
                if tab_widget in gui.tabs_list:
                    gui.remove_tab(tab_widget)
            AdminMenu.admin_menu_tabs_init(gui, admin_manager)

        return False

    login_label = ttk.Button(admin_login_tab, text="login", width=40, command=lambda: admin_checker(username_input.get(), password_input.get(), gui, AdminMenu, admin_manager))
    login_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")





