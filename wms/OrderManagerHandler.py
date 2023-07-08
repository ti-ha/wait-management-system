from wms import OrderManager, TableHandler, MenuHandler, Order

class OrderManagerHandler():
    def __init__(self, order_manager: OrderManager, 
                 table_handler: TableHandler,
                 menu_handler: MenuHandler) -> None:
        """ Constructor for the OrderManagerHandler Class """
        self.__order_manager = order_manager
        self.__table_handler = table_handler
        self.__menu_handler = menu_handler

    def get_table_orders(self, table_id) -> dict:
        """ Acquires the table orders of a particular table

        Args:
            table_id (Integer): ID of a table

        Raises:
            ValueError: Raised if table ID does not correspond to any table

        Returns:
            Dict: A dictionary of all the table orders of a particular table
        """
        tID = int(table_id)
        try:
            orders = self.__order_manager.get_table_orders(tID)
        except ValueError:
            raise ValueError("table_id does not exist in map")
        
        return {
            "orders": [i.jsonify() for i in orders]
            }
    
    def get_order_by_id(self, order_id) -> dict:
        """ Gets an order by its ID value

        Args:
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            Dict: A dictionary of the order to be found
        """
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        
        return order.jsonify()
    
    def get_order_state(self, order_id) -> dict:
        """ Gets the current state of an order 

        Args:
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            Dict: A dictionary of the order's state
        """
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        
        return {
            "state": order.state
            }
    
    def get_menu_item_state(self, order_id, menu_item_id) -> dict:
        oID = int(order_id)
        mID = int(menu_item_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        
        return {
            "state": order.get_menu_item_state_by_id(mID).state
        }
    
    def get_order_bill(self, order_id) -> dict:
        """ Gets the current bill of an order 

        Args:
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            Dict: A dictionary of the order's bill price and whether it is paid
            or not
        """
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        if order.bill == None:
            order.calculate_bill()

        return {
            "price": order.bill.price, 
            "paid": order.bill.paid
            }

    def add_order(self, table_id, menu_items_ids, deals_ids):
        """ Adds an order to the list of orders

        Args:
            table_id (Integer): ID value of a table
            menu_items_ids (List[Integer]): List of ID values corresponding to
            individual menu item objects
            deals_ids (List[Integer]): List of ID values corresponding to
            individual deal objects

        Raises:
            ValueError: Raised if table_id does not correspond to any table
            ValueError: Raised if a menu_item_id does not correspond to any
            menu item
            ValueError: Raised if a deal_id does not correspond to any deal
        """
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
        """ Changes the state of an order

        Args:
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            State: New state of the order
        """
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        self.__order_manager.change_state(oID)
        return order.state
    
    def change_menu_item_state(self, order_id, menu_item_id):
        """ Changes the state of a menu_item within an order

        Args:
            order_id (int): the order id of the menu_item to be changed
            menu_item_id (int): the order-specific menu_item id to be changed

        Raises:
            ValueError: Order id provided does not exist
        """
        oID = int(order_id)
        mID = int(menu_item_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        order.get_menu_item_state_by_id(mID).transition_state()

    def remove_order(self, table_id, order_id):
        """ Remove an order from the list of orders

        Args:
            table_id (Integer): ID value of the table
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if either the table_id or order_id do not 
            correspond to a table or order object respectively
            ValueError: Raised if the order is not assigned to the table
        """
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
        """ Removed an order by it's ID value

        Args:
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders
            ValueError: Raised if the order does not apart of any table
        """
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        
        tID = -1

        tID = next((i for i in self.__order_manager.map if oID in self.__order_manager.map[i]), None)
        
        if tID == None:
            raise ValueError("Order is not in a table. How did you manage that?")
        
        self.__order_manager.remove_order(order, self.__table_handler.id_to_table(tID))

    def calculate_and_return_bill(self, table_id) -> dict:
        """ Calculates and returns the current bill

        Args:
            table_id (Integer): ID value of the table

        Raises:
            e: Raised when either there is an invalid table_id or the table
            has no orders to calculate a bill out of

        Returns:
            Dict: A dictionary of the bill's price and whether or not it has
            been paid
        """
        tID = int(table_id)
        try: 
            bill = self.__order_manager.calculate_table_bill(tID)
        except Exception as e:
            raise e
        
        self.__table_handler.id_to_table(tID).bill = bill
        return {"price": bill.price, "is_paid": bill.paid}
    
    def pay_table_bill(self, table_id):
        """ A function to simulate the payment of the table bill

        Args:
            table_id (Integer): ID value of the table

        Raises:
            ValueError: Raised if table_id does not match any of the tables
            ValueError: Raised if the table's bill has not been created yet
            ValueError: Raised if an order of the table has not been served yet
        """
        tID = int(table_id)
        table = self.__table_handler.id_to_table(tID)
        if table == None:
            raise ValueError("Not a valid table_id")
        
        bill = table.bill
        if bill == None:
            raise ValueError("Bill not created yet. Try calculating it with a GET")
        
        payable = len([False for i in table.orders if i.state not in ["served", "completed"]]) == 0

        if not payable:
            raise ValueError("One or more orders hasn't been served yet")
        
        bill.pay()

    def pay_order_bill(self, order_id):
        """ A function to simulate the payment of an order's bill

        Args:
            order_id (Integer): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders 
            ValueError: Raised if the order's bill has not been created yet
            e: Raised if the order has not been served yet
        """
        oID = int(order_id)
        order = self.__order_manager.get_order(oID)
        if order == None:
            raise ValueError("Not a valid order_id")
        if order.bill == None:
            raise ValueError("Order does not have a bill. Try calculating it first")
        
        try:
            order.mark_as_paid()
        except Exception as e:
            raise e
    
    #jsons
    def jsonify(self) -> dict:
        """ Creates a dictionary with a list containing all of the orders of 
        each individual table

        Returns:
            dict: Dictionary containing a list of all of the orders of 
        each individual table
        """
        return self.__order_manager.jsonify()
    
    def jsonify_orders(self) -> dict:
        """ Creates a dictionary with a list containing all of the current orders

        Returns:
            dict: Dictionary containing a list of all the current orders
        """
        return self.__order_manager.orders_json()
