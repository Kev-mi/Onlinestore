import view.CustomerMenu as CustomerMenu

class AdminManager:

    def __init__(self, cursor):
        self.cursor = cursor

        self.product_id_search_input = None
        self.product_name_search_input = None
        self.product_base_search_price_input = None
        self.product_supplier_search_input = None
        self.product_supplier_search_input = None
        self.product_code_input_2 = None

        self._current_date = None

    def get_current_date(self):
        return self._current_date

    def set_current_date(self, date):
        self._current_date = date
