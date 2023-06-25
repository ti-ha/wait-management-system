from wms import *


# A decorator class for managing the app
class Application():
    def __init__(self):
        self.__menu = Menu()
        self.__tables = []
        self.__order_manager = OrderManager()
        self.__service_request_manager = ServiceRequestManager()
        self.__users = []
        self.__restaurant_manager = RestaurantManager(self.__menu)

    def menu_json(self):
        return self.__menu.jsonify()
    
    def add_menu_category(self, category):
        self.__menu.add_category(Category(category))

    def get_menu_category(self, category):
        return self.__menu.get_category(category)

    def remove_menu_category(self, category):
        self.__menu.remove_category(category)

    def jsonify_menu_category(self, category):
        return self.__menu.get_category(category).jsonify()

    def jsonify_menu_categories(self):
        categories = self.__menu.categories()
        output = [i.jsonify() for i in categories]
        return output
    
    def add_menu_item(self, category, name, price, imageurl):
        self.__menu.get_category(category).add_menu_item(name, price, imageurl)

    def get_menu_item(self, category, name):
        return self.__menu.get_category(category).menu_item(name)
    
    def remove_menu_item(self, category, name):
        self.__menu.get_category(category).remove_menu_item(name)
    
    def menu_item_json(self, category, name):
        return self.__menu.get_category(category).menu_item(name).jsonify()
    
    def get_deals_json(self):
        return [i.jsonify() for i in self.__menu.deals()]
    
    def add_deal(self, discount, menu_items):
        deal_items = []
        for i in self.__menu.categories():
            for j in i.menu_items():
                if j.name() in menu_items:
                    deal_items.append(j)

        if len(menu_items) != len(deal_items):
                return None
        
        deal = Deal(discount, deal_items)
        self.__menu.add_deal(deal)
        return deal.id()
        

    