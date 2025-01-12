import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.Tables import init_tables, init_admin
from model.DatabaseManager import DatabaseManager
from view.Gui import Gui
import view.MainMenu as MainMenu
import view.AdminMenu as AdminMenu
import view.CustomerMenu as CustomerMenu
from model.CustomerManager import CustomerManager
from model.AdminManager import AdminManager
import datetime

if __name__ == '__main__':
    db_manager = DatabaseManager('online_store.db')
    init_tables(db_manager.cursor)
    init_admin(db_manager.cursor)

    gui = Gui(db_manager.conn)

    customer_manager = CustomerManager()
    admin_manager = AdminManager()

    gui.set_current_date(datetime.date.today().strftime("%Y-%m-%d"))

    try:

        db_manager.execute_query('''
            INSERT INTO Product (
                product_code,
                quantity_in_stock,
                number_of_sales,
                base_price,
                product_revenue,
                supplier_name,
                product_name,
                maximum_orders_per_month
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (100, 1000, 0, 10, 10, "supplier", "product100", 10000))

        db_manager.commit_transaction()
        print("Product inserted successfully!")

    except Exception as e:
        db_manager.rollback_transaction()
        print("Failed to insert product:", e)
        raise

    def switch_to_customer_menu():
        CustomerMenu.customer_menu_tabs_init(gui, customer_manager)

    def switch_to_admin_menu():
        MainMenu.verifyAdminLogin(gui, AdminMenu, admin_manager)

    gui.switch_to_customer_menu = switch_to_customer_menu
    gui.switch_to_admin_menu = switch_to_admin_menu

    MainMenu.init_main_menu(
        gui,
        switch_to_customer_menu,
        switch_to_admin_menu
    )

    gui.run()
