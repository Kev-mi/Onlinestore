from tkinter import ttk, messagebox
import view.CustomerMenu as CustomerMenu
import view.AdminMenu as AdminMenu
import sqlite3


def init_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu, go_to_main_menu):
    user_type_tab = ttk.Frame(gui.tabs)
    gui.add_tab(user_type_tab, text="User Type")

    #saving it user type tab as an attribute to later remove it
    gui.user_type_tab = user_type_tab

    ttk.Button(
        user_type_tab, text="Click here to get customer menu", width=40,
        command= switch_to_customer_menu
    ).pack(side="top", padx=0, pady=20)

    ttk.Button(
        user_type_tab, text="Click here to get admin menu", width=40,
        command= switch_to_admin_menu
    ).pack(side="top", padx=0, pady=30)

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


def handle_admin_login(gui, username, password):
    if check_admin_credentials(gui.cursor, username, password):
        gui.tabs.forget(gui.tabs.select())
        AdminMenu.admin_menu_tabs_init(gui)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


def check_admin_credentials(cursor, username, password):
    if not username or not password:
        return False
    try:
        cursor.execute('''
            SELECT user_type FROM User
            WHERE username = ? AND password = ?
        ''', (username, password))
        user_type = cursor.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error accessing the database: {e}")
        return False

    return user_type and user_type[0] == "admin"
