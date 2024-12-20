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
    # Initialize the database
    db_manager = DatabaseManager('online_store.db')
    init_tables(db_manager.cursor)
    init_admin(db_manager.cursor)

    # Initialize the GUI
    gui = Gui(db_manager.cursor)

    customer_manager = CustomerManager(db_manager.cursor)
    admin_manager = AdminManager(db_manager.cursor)

    admin_manager.set_current_date(datetime.date.today().strftime("%Y-%m-%d"))

    def switch_to_customer_menu():
        CustomerMenu.customer_menu_tabs_init(gui, customer_manager)

    def switch_to_admin_menu():
        AdminMenu.admin_menu_tabs_init(gui, admin_manager)


    gui.switch_to_customer_menu = switch_to_customer_menu
    gui.switch_to_admin_menu = switch_to_admin_menu

    # init main menu method
    MainMenu.init_main_menu(
        gui,
        switch_to_customer_menu,
        switch_to_admin_menu,
        lambda: go_to_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu, customer_manager)
    )


    # Run the application
    gui.run()


def go_to_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu, customer_manager):

    gui.remove_all_tabs()

    MainMenu.init_main_menu(
        gui,
        switch_to_customer_menu,
        switch_to_admin_menu,
        lambda: go_to_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu, customer_manager)
    )
