from wms import *
import json

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
    
    def get_menu_item_by_id(self, id):
        return self.__menu.menu_item_lookup(id)

    def remove_menu_item(self, category, name):
        self.__menu.get_category(category).remove_menu_item(name)
    
    def menu_item_json(self, category, name):
        return self.__menu.get_category(category).menu_item(name).jsonify()
    
    def get_deals_json(self):
        return [i.jsonify() for i in self.__menu.deals()]
    
    def get_deal_by_id(self, id):
        for i in self.__menu.deals():
            if i.id() == id:
                return i
        return None
    
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
        
    def get_tables_json(self):
        tableDict = {}
        for table in self.__tables:
            table_num = "Table_" + str(table.get_id())
            tableDict[table_num] = {"availability": table.get_open_seats(),
                                    "table limit": table.get_tablelimit(), 
                                    "is occupied": table.is_occupied()}
        return json.dumps(tableDict)
    
    def add_table(self, table_limit, orders):
        table = Table(table_limit, orders)
        self.__tables.append(table)
        return table.get_id()
    
    def get_users_json(self):
        userDict = {}
        for user in self.__users:
            user_num = "User_" + str(user.get_id())
            userDict[user_num] = {"first name": user.get_firstname(),
                                  "last name": user.get_lastname(),
                                  "type": user.__class__.__name__}
        return json.dumps(userDict)
    
    def add_user(self, firstname, lastname, user_type):
        new_user = None
        if user_type == "Customer":
            new_user = Customer(firstname, lastname)
        elif user_type == "Kitchen Staff":
            new_user = KitchenStaff(firstname, lastname, self.__order_manager)
        elif user_type == "Wait Staff":
            new_user = WaitStaff(firstname, lastname, self.__order_manager)
        elif user_type == "Manager":
            new_user = Manager(firstname, lastname, self.__order_manager)
        else:
            return None
        self.__users.append(new_user)
        return new_user.get_id()
        
    def add_table_customer(self, table_id, customer_id):
        table = self.id_to_table(table_id)
        customer = self.id_to_user(customer_id)
        try:
            table.add_customers(customer)
        except:
            return False
        return True
    
    # Might need to move these to a helper file 
    def id_to_user(self, id):
        for user in self.__users:
            if user.get_id() == id:
                return user
        return None
    
    def id_to_table(self, id) -> Table:
        for table in self.__tables:
            if table.get_id() == id:
                return table
        return None