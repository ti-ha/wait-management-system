from __future__ import annotations
from .Order import Order, States
from .User import User
from .Table import Table
from .Bill import Bill
import json

class OrderManager:
    # Constructor for the Order Manager class
    def __init__(self):
        self.__orders = []
        self.__observers = []
        # maps table: [orders]
        self.__map = {}
        
    # Getter
    def orders(self) -> list[Order]:
        return self.__orders
    
    def observer_attach(self, observer):
        self.__observers.append(observer)

    def observer_update(self):
        for observer in self.__observers:
            observer.order_manager_update(self.__orders)

    # Adding orders to list of orders
    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("OrderManager: add_order(): Object is not of type Order")
    def map(self) -> dict:
        return self.__map
    
    # Returns a specific order based off provided order ID
    def get_order(self, order_ID) -> Order:
        for order in self.orders():
            if (order.id() == order_ID):
                return order
        return None
    
    # Returns a list of orders at a specific table
    def get_table_orders(self, table_id: int) -> list[Order]:
        if table_id not in self.map().keys():
            raise ValueError("OrderManager: get_table_orders(): table_id does not exist in map")
        
        order_ids = self.map()[table_id]
        order_list = []
        for i in self.orders():
            if i.id() in order_ids:
                order_list.append(i)

        return order_list
    
    # Adding orders to list of orders and relational map
    def add_order(self, order: Order, table: Table):
        if order in self.__orders:
            raise ValueError("OrderManager: add_order(): Order already exists")
        self.__orders.append(order)
        if table.get_id() in self.__map.keys():
            self.__map[table.get_id()] += [order.id()]
        else:
            self.__map[table.get_id()] = [order.id()]
        table.add_order(order)
        self.observer_update()

    # Removing orders from list of orders and relational map
    def remove_order(self, order: Order, table: Table):
        if order not in self.__orders:
            raise ValueError("OrderManager: remove_order(): Order does not exist")

        if table.get_id() in self.map().keys():
            self.__map[table.get_id()].remove(order.id())
            table.remove_order(order)
            self.__orders.remove(order)
        else:
            raise ValueError("OrderManager: remove_order(): Table does not have supplied order")
        
    # Move item along to the next stage        
    def change_state(self, order: int | Order):
        if isinstance(order, int):
            order = self.get_order(order)
        elif isinstance(order, Order):
            pass
        else:
            raise TypeError("OrderManager: change_state(): Not a valid Order obj or order_id")
        order.change_state()
        self.observer_update()

    def change_to_state(self, order: int | Order, string: str):
        if isinstance(order, int):
            order = self.get_order(order)
        elif isinstance(order, Order):
            pass
        else:
            raise TypeError("OrderManager: change_to_state(): Not a valid Order obj or order_id")
        if string.upper() in States.list():
            while order.state() != string:
                order.change_state()
            return True
        
        return False
    

    def calculate_table_bill(self, table_id: int) -> Bill:
        if isinstance(table_id, int):
            pass
        else:
            raise TypeError("OrderManager: calculate_table_bill(): Not a valid id")
        
        orderlist = self.get_table_orders(table_id)
        bills = []
        for i in orderlist:
            bills.append(i.calculate_bill())
        
        if None in bills:
            raise ValueError("OrderManager: calculate_table_bill(): One or more orders have not been served yet")
        subtotal = sum([(i.get_price(),0)[i.is_paid()] for i in bills])
        
        return Bill(subtotal)
    
    def orders_json(self):
        output = {"orders": []}
        for i in self.orders():
            output["orders"].append(i.jsonify())
        
        return json.dumps(output, indent = 8)
    
    def jsonify(self):
        output = {"orders": [],
                  "table_order_map": self.map()}
        for i in self.orders():
            output["orders"].append(i.jsonify())
        
        return json.dumps(output, indent = 8)



