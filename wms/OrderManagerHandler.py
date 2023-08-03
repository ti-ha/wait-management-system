from wms import OrderManager, TableHandler, MenuHandler, Order, RestaurantManagerHandler
from .PersonalisedDeal import PersonalisedDeal

class OrderManagerHandler():
    def __init__(self, order_manager: OrderManager,
                 table_handler: TableHandler,
                 menu_handler: MenuHandler):
        """ Constructor for the OrderManagerHandler Class

        Args:
            order_manager (OrderManager): OrderManager object utilised with the handler
            table_handler (TableHandler): TableHandler object utilised with the handler
            menu_handler (MenuHandler): MenuHandler object utilised with the handler
        """
        self.__order_manager = order_manager
        self.__table_handler = table_handler
        self.__menu_handler = menu_handler
        self.__observers = []

    def attach(self, observer: RestaurantManagerHandler):
        """ Attach observer to order manager handler """
        self.__observers.append(observer)

    def notify(self, menu_items: list[int]):
        """ Notify observers of a new order """
        for observer in self.__observers:
            observer.order_update(menu_items)

    @property
    def order_manager(self) -> OrderManager:
        """ Returns order manager handler object """
        return self.__order_manager
    
    @property
    def table_handler(self) -> TableHandler:
        """ Returns table handler object """
        return self.__table_handler
    
    @property
    def menu_handler(self) -> MenuHandler:
        """ Returns menu handler object """
        return self.__menu_handler

    def get_table_orders(self, table_id: int) -> dict:
        """ Acquires the table orders of a particular table

        Args:
            table_id (int): ID of a table

        Raises:
            ValueError: Raised if table ID does not correspond to any table

        Returns:
            dict: A dictionary of all the table orders of a particular table
        """
        try:
            orders = self.order_manager.get_table_orders(table_id)
        except ValueError as exc:
            raise ValueError("table_id does not exist in map") from exc

        return {
            "orders": [i.jsonify() for i in orders]
        }

    def get_order_by_id(self, order_id: int) -> dict:
        """ Gets an order by its ID value

        Args:
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            dict: A dictionary of the order to be found
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")

        return order.jsonify()

    def get_order_state(self, order_id: int) -> dict:
        """ Gets the current state of an order

        Args:
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            dict: A dictionary of the order's state
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")

        return { 
            "state": order.state 
        }

    def get_menu_item_state(self, order_id: int, menu_item_id: int) -> dict:
        """ Creates a dictionary of the menu item's current state

        Args:
            order_id (int): Id of the menu order
            menu_item_id (int): Id of the menu item within the specified order

        Raises:
            ValueError: Raised if the order_id does not correspond to an actual 
            order

        Returns:
            dict: Dictionary containing information about the menu item's 
            current state
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")

        return {
            "state": order.get_menu_item_state_obj(menu_item_id).state
        }

    def get_order_bill(self, order_id: int) -> dict:
        """ Gets the current bill of an order

        Args:
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders

        Returns:
            dict: A dictionary of the order's bill price and whether it is paid
            or not
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")
        if order.bill is None:
            order.calculate_bill()

        return {
            "price": order.bill.price,
            "paid": order.bill.paid
        }

    def add_order(self, table_id: int, menu_items_ids: list[int], deals_ids: list[int], 
                  user: str = None):
        """ Adds an order to the list of orders. Notifies restaurant manager to
        update menu item statistics. 

        Args:
            table_id (int): ID value of a table
            menu_items_ids (list[int]): List of ID values corresponding to
            individual menu item objects
            deals_ids (list[int]): List of ID values corresponding to
            individual deal objects
            user (str, optional): User that sent in the order. Defaults to None.

        Raises:
            ValueError: Raised if table_id does not correspond to any table
            ValueError: Raised if a menu_item_id does not correspond to any
            menu item
            ValueError: Raised if a deal_id does not correspond to any deal
        """
        table = self.table_handler.id_to_table(table_id)

        if table is None:
            raise ValueError("OrderManagerHandler: add_order(): Table does not exist")

        menu_items = []
        for i in menu_items_ids:
            item = self.menu_handler.get_menu_item_by_id(i)
            if item is None:
                raise ValueError("OrderManagerHandler: add_order(): MenuItem does not exist")
            menu_items.append(item)

        deals = []
        for i in deals_ids:
            deal = self.menu_handler.get_deals_by_id(i)
            if deal is None:
                raise ValueError("OrderManagerHandler: add_order(): Deal does not exist")
            deals.append(deal)
            if isinstance(deal, PersonalisedDeal):
                self.menu_handler.menu.remove_deal(deal)

        self.order_manager.add_order(Order(menu_items, deals, user), table)
        self.notify(menu_items_ids)

    def change_order_state(self, order_id: int):
        """ Changes the state of an order

        Args:
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")
        self.order_manager.change_state(order_id)
        if self.order_manager.get_order(order_id).state == "completed":
            self.order_manager.orders.remove(self.order_manager.get_order(order_id))

    def change_menu_item_state(self, order_id: int, menu_item_id: int):
        """ Changes the state of a menu_item within an order

        Args:
            order_id (int): the order id of the menu_item to be changed
            menu_item_id (int): the order-specific menu_item id to be changed

        Raises:
            ValueError: Order id provided does not exist
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")
        order.change_menu_item_state_by_id(menu_item_id)

    def remove_order(self, table_id: int, order_id: int):
        """ Remove an order from the list of orders

        Args:
            table_id (int): ID value of the table
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if either the table_id or order_id do not
            correspond to a table or order object respectively
            ValueError: Raised if the order is not assigned to the table
        """
        table = self.table_handler.id_to_table(table_id)
        order = self.order_manager.get_order(order_id)
        if table is None or order is None:
            raise ValueError("OrderManagerHandler: remove_order(): either table or order do not exist")
        try:
            self.order_manager.remove_order(order, table)
        except ValueError as exc:
            raise ValueError(
                "OrderManagerHandler: remove_order(): Order either doesn't exist or is not assigned to a table"
            ) from exc

    def delete_order_by_id(self, order_id: int):
        """ Removed an order by it's ID value

        Args:
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders
            ValueError: Raised if the order does not apart of any table
        """
        order = self.order_manager.get_order(int(order_id))
        if order is None:
            raise ValueError("Not a valid order_id")

        # tID = -1

        t_id = next(
            (i for i in self.order_manager.map if int(order_id) in self.order_manager.map[i]), 
            None
        )

        if t_id is None:
            raise ValueError("Order is not in a table. How did you manage that?")

        self.order_manager.remove_order(order, self.table_handler.id_to_table(t_id))

    def calculate_and_return_bill(self, table_id: int) -> dict:
        """ Calculates and returns the current bill

        Args:
            table_id (int): ID value of the table

        Raises:
            e: Raised when either there is an invalid table_id or the table
            has no orders to calculate a bill out of

        Returns:
            dict: A dictionary of the bill's price and whether or not it has
            been paid
        """

        try:
            bill = self.order_manager.calculate_table_bill(table_id)
        except Exception as e:
            raise e
        
        table = self.table_handler.id_to_table(table_id)

        if table.bill == None or table.bill != bill:
            table.bill = bill
            return bill.jsonify()
        else:
            return self.table_handler.id_to_table(table_id).bill.jsonify()

    def pay_table_bill(self, table_id: int):
        """ A function to simulate the payment of the table bill

        Args:
            table_id (int): ID value of the table

        Raises:
            ValueError: Raised if table_id does not match any of the tables
            ValueError: Raised if the table's bill has not been created yet
            ValueError: Raised if an order of the table has not been served yet
        """
        table = self.table_handler.id_to_table(table_id)
        if table is None:
            raise ValueError("Not a valid table_id")

        bill = table.bill
        if bill is None:
            raise ValueError("Bill not created yet. Try calculating it with a GET")

        payable = len([False for i in table.orders if i.state not in ["served", "completed"]]) == 0

        if not payable:
            raise ValueError("One or more orders hasn't been served yet")
        
        [i.bill.pay() for i in table.orders]
        
        bill.pay()

    def pay_order_bill(self, order_id: int):
        """ A function to simulate the payment of an order's bill

        Args:
            order_id (int): ID value of the order

        Raises:
            ValueError: Raised if order_id does not match any of the orders
            ValueError: Raised if the order's bill has not been created yet
            e: Raised if the order has not been served yet
        """
        order = self.order_manager.get_order(order_id)
        if order is None:
            raise ValueError("Not a valid order_id")
        if order.bill is None:
            raise ValueError("Order does not have a bill. Try calculating it first")
        
        order.mark_as_paid()

    def jsonify(self) -> dict:
        """ Creates a dictionary with a list containing all of the orders of
        each individual table

        Returns:
            dict: Dictionary containing a list of all of the orders of
        each individual table
        """
        return self.order_manager.jsonify()

    def jsonify_orders(self) -> dict:
        """ Creates a dictionary with a list containing all of the current orders

        Returns:
            dict: Dictionary containing a list of all the current orders
        """
        return self.order_manager.orders_json()
    
    def jsonify_history(self) -> dict:
        """ Creates a dictionary with a list containing all orders in the
        history

        Returns:
            dict: Dictionary containing a list of all orders in the history
        """
        return self.order_manager.history_json()
    
    def get_order_json_from_history(self, order_id: str) -> dict:
        """ Creates a dictionary of a specific order from the order history

        Args:
            order_id (str): Id of the order in the order history

        Raises:
            ValueError: Raised if no order in the order history has that id

        Returns:
            dict: A dictionary of a specific order from the order history
        """
        json = self.order_manager.get_order_from_history(order_id).jsonify()
        if json:
            return json
        else:
            raise ValueError("OrderManagerHandler(): Order does not exist in history")
