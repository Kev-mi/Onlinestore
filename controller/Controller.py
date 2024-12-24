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

    # init the GUI with the connection
    gui = Gui(db_manager.conn)

    customer_manager = CustomerManager()
    admin_manager = AdminManager()

    admin_manager.set_current_date(datetime.date.today().strftime("%Y-%m-%d"))

    def switch_to_customer_menu():
        CustomerMenu.customer_menu_tabs_init(gui, customer_manager)

    def switch_to_admin_menu():
        MainMenu.verifyAdminLogin(gui, AdminMenu, admin_manager)


    gui.switch_to_customer_menu = switch_to_customer_menu
    gui.switch_to_admin_menu = switch_to_admin_menu

    # init main menu method
    MainMenu.init_main_menu(
        gui,
        switch_to_customer_menu,
        switch_to_admin_menu
    )


    # Run the application
    gui.run()
