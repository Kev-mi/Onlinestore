import view.MainMenu as MainMenu

def go_to_main_menu(gui, switch_to_customer_menu, switch_to_admin_menu):

    gui.remove_all_tabs()

    MainMenu.init_main_menu(
        gui,
        switch_to_customer_menu,
        switch_to_admin_menu
    )
