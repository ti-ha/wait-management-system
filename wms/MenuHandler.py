from wms import Menu, Category, MenuItem, Deal

class MenuHandler():
    def __init__(self, menu: Menu):
        self.__menu = menu
    
    
    def get_category(self, category):
        return self.__menu.get_category(category)
    
    def get_menu_item(self, category, name):
        return self.__menu.get_category(category).get_menu_item_by_name(name)
    
    def get_menu_item_by_id(self, id):
        return self.__menu.menu_item_lookup(id)
    
    def get_deals_by_id(self, id):
        for i in self.__menu.deals():
            if i.id() == id:
                return i
        return None
    
    def add_category(self, category):
        self.__menu.add_category(Category(category))

    def add_menu_item(self, category, name, price, imageurl):
        item = MenuItem(name, price, imageurl)
        self.__menu.get_category(category).add_menu_item(item)

    def add_deal(self, discount, menu_items):

        deal_items = [j for i in self.__menu.categories() 
                      for j in i.menu_items() 
                      if j.name() in menu_items]
        
        if len(menu_items) != len(deal_items):
            return None
        
        deal = Deal(discount, deal_items)
        self.__menu.add_deal(deal)
        return deal.id()
     
    def remove_category(self, category):
        self.__menu.remove_category(category)
    
    def remove_menu_item(self, category, name):
        self.__menu.get_category(category).remove_menu_item(name)

    def jsonify(self):
        return self.__menu.jsonify()
    
    def jsonify_category(self, category):
        return self.__menu.get_category(category).jsonify()
    
    def jsonify_categories(self):
        return [i.jsonify() for i in self.__menu.categories()]
    
    def jsonify_menu_item(self, category, name):
        return self.__menu.get_category(category).menu_item(name).jsonify()
    
    def jsonify_deals(self):
        return [i.jsonify() for i in self.__menu.deals()]


