import view.CustomerMenu as CustomerMenu

class AdminManager:

    def __init__(self):

        self.product_id_search_input = None
        self.product_name_search_input = None
        self.product_base_search_price_input = None
        self.product_supplier_search_input = None
        self.product_supplier_search_input = None
        self.product_code_input_2 = None

        self.id_discount_input = None
        self.name_discount_input = None
        self.discount_input = None
        self.lower_date_input = None
        self.upper_date_input = None
        self.product_code_input = None
        self.discount_id_2 = None

        self.name_input = None
        self.street_input = None
        self.zip_code_input = None
        self.city_input = None
        self.country_input = None
        self.phone_number_input = None

        self.id_input_product = None
        self.product_name_input = None
        self.product_base_price_input = None
        self.product_supplier_input = None
        self.product_quantity_input = None
        self.product_id_input_2 = None
        self.product_quantity_input_2 = None

        self.selected_product_id = None
        self.selected_discount_id = None

        self._current_date = None

    def get_current_date(self):
        return self._current_date

    def set_current_date(self, date):
        self._current_date = date
