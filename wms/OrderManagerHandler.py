from wms import OrderManager, TableHandler, MenuHandler, Order

class OrderManagerHandler():
    def __init__(self, order_manager: OrderManager, 
                 table_handler: TableHandler,
                 menu_handler: MenuHandler) -> None:
        self.__order_manager = order_manager
        self.__table_handler = table_handler
        self.__menu_handler = menu_handler

    #getters
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
    
    def get_order_by_id(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        
        return order.jsonify()
    
    def get_order_state(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        output = {"state": order.state()}
        return output
    
    def get_order_bill(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        if order.bill() == None:
            order.calculate_bill()
        output = {"price": order.bill().price, "paid": order.bill().paid}
        return output

    #setters
    def add_order(self, table_id, menu_items_ids, deals_ids):
        table = self.__table_handler.id_to_table(int(table_id))

        if table == None:
            raise ValueError("OrderManagerHandler: add_order(): Table does not exist")
        
        menu_items = []
        for i in menu_items_ids:
            item = self.__menu_handler.get_menu_item_by_id(i)
            if item == None:
                raise ValueError("OrderManagerHandler: add_order(): MenuItem does not exist")
            else:
                menu_items.append(item)
        
        deals = []
        for i in deals_ids:
            deal = self.__menu_handler.get_deals_by_id(i)
            if deal == None:
                raise ValueError("OrderManagerHandler: add_order(): Deal does not exist")
            else:
                deals.append(deal)
        order = Order(menu_items, deals)
        self.__order_manager.add_order(order, table)

    def change_order_state(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        self.__order_manager.change_state(oID)
        return order.state()

    #deleters
    def remove_order(self, table_id, order_id):
        tID = int(table_id)
        oID = int(order_id)
        table = self.__table_handler.id_to_table(tID)
        order = self.__order_manager.get_order(oID)
        if table == None or order == None:
            raise ValueError("OrderManagerHandler: remove_order(): either table or order do not exist")
        try: 
            self.__order_manager.remove_order(order, table)
        except:
            raise ValueError("OrderManagerHandler: remove_order(): Order either doesn't exist or is not assigned to a table")
        
    def delete_order_by_id(self, order_id):
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        tID = -1
        for i in self.__order_manager.get_map():
            if oID in self.__order_manager.get_map()[i]:
                tID = i
        
        if tID == -1:
            raise ValueError("Order is not in a table. How did you manage that?")
        
        self.__order_manager.remove_order(order, self.__table_handler.id_to_table(tID))

    #logic
    def calculate_and_return_bill(self, table_id):
        tID = int(table_id)
        try: 
            bill = self.__order_manager.calculate_table_bill(tID)
        except Exception as e:
            raise e
        
        self.__table_handler.id_to_table(tID).bill = bill
        return {"price": bill.price, "is_paid": bill.paid}
    
    def pay_table_bill(self, table_id):
        tID = int(table_id)
        table = self.__table_handler.id_to_table(tID)
        if table == None:
            raise ValueError("Not a valid table_id")
        
        bill = table.bill
        if bill == None:
            raise ValueError("Bill not created yet. Try calculating it with a GET")
        
        payable = True
        for i in table.orders:
            if i.state() not in ["served", "completed"]:
                payable == False
                raise ValueError("One or more orders hasn't been served yet")
        bill.pay()

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
    
    #jsons
    def jsonify(self):
        return self.__order_manager.jsonify()
    
    def jsonify_orders(self):
        return self.__order_manager.orders_json()

    #helpers
