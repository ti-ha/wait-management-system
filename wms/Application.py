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
    
    def add_menu_item(self, category, name, price, imageURL):
        self.__menu.get_category(category).add_menu_item(MenuItem(name, price, imageURL))

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
        tableDict = {"tables": []}
        for table in self.__tables:
            tableDict["tables"].append({ "id":table.get_id(),
                                    "availability": table.get_open_seats(),
                                    "table limit": table.get_tablelimit(), 
                                    "is occupied": table.is_occupied()})
        return tableDict
    
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
        return userDict
    
    def add_user(self, firstname, lastname, user_type):
        new_user = None
        if user_type == "Customer":
            new_user = Customer(firstname, lastname)
        elif user_type == "Kitchen Staff":
            new_user = KitchenStaff(firstname, lastname)
        elif user_type == "Wait Staff":
            new_user = WaitStaff(firstname, lastname)
        elif user_type == "Manager":
            new_user = Manager(firstname, lastname)
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
    
    def jsonify_order_manager(self):
        return self.__order_manager.jsonify()
    
    def jsonify_order_manager_orders(self):
        return self.__order_manager.orders_json()
    
    
    def add_order_to_order_manager(self, table_id, menu_items_ids, deals_ids):
        table = self.id_to_table(int(table_id))
        if table == None:
            raise ValueError("Application(OrderManager): add_order_to_order_manager(): Table does not exist")
        
        menu_items = []
        for i in menu_items_ids:
            item = self.get_menu_item_by_id(i)
            if item == None:
                raise ValueError("Application(OrderManager): add_order_to_order_manager(): MenuItem does not exist")
            else:
                menu_items.append(item)
            
        deals = []
        for i in deals_ids:
            deal = self.get_deal_by_id(i)
            if deal == None:
                raise ValueError("Application(OrderManager): add_order_to_order_manager(): Deal does not exist")
            else:
                deals.append(deal)
        
        order = Order(menu_items, deals)
        self.__order_manager.add_order(order, table)

    def remove_order_from_order_manager(self, table_id, order_id):
        tID = int(table_id)
        oID = int(order_id)
        table = self.id_to_table(tID)
        order = self.__order_manager.get_order(oID)
        if table == None or order == None:
            raise ValueError("Application(OrderManager): remove_order_from_order_manager(): either table or order do not exist")
        
        try: 
            self.__order_manager.remove_order(order, table)
        except:
            raise ValueError("Application(OrderManager): remove_order_from_order_manager(): Order either doesn't exist or is not assigned to a table")
        
    def get_table_orders(self, table_id):
        tID = int(table_id)
        try:
            orders = self.__order_manager.get_table_orders(tID)
        except ValueError:
            raise ValueError("table_id does not exist in map")
        
        output = {"orders": []}
        for i in orders:
            output["orders"].append(i.jsonify())
        return output
    
    def calculate_and_return_bill(self, table_id):
        tID = int(table_id)
        try: 
            bill = self.__order_manager.calculate_table_bill(tID)
        except Exception as e:
            raise e
        
        self.id_to_table(tID).set_bill(bill)
        return {"price": bill.get_price(), "is_paid": bill.is_paid()}
    
    def pay_table_bill(self, table_id):
        tID = int(table_id)
        table = self.id_to_table(tID)
        if table == None:
            raise ValueError("Not a valid table_id")
        
        bill = table.get_bill()
        if bill == None:
            raise ValueError("Bill not created yet. Try calculating it with a GET")
        
        payable = True
        for i in table.get_orders():
            if i.state() not in ["served", "completed"]:
                payable == False
                raise ValueError("One or more orders hasn't been served yet")
        bill.pay()

    def get_order_by_id(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        
        return order.jsonify()
    
    def delete_order_by_id(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        tID = -1
        for i in self.__order_manager.map():
            if oID in self.__order_manager.map()[i]:
                tID = i
        
        if tID == -1:
            raise ValueError("Order is not in a table. How did you manage that?")
        
        self.__order_manager.remove_order(order, self.id_to_table(tID))

    def get_order_state(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        output = {"state": order.state()}
        return output
    
    def change_order_state(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        self.__order_manager.change_state(oID)
        return order.state()

    def get_order_bill(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        if order.bill() == None:
            order.calculate_bill()
        output = {"price": order.bill().get_price(), "paid": order.bill().is_paid()}
        return output
    
    def pay_order_bill(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        if order.bill() == None:
            raise ValueError("Order does not have a bill. Try calculating it first")
        try:
            order.mark_as_paid()
        except Exception as e:
            raise e
        
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