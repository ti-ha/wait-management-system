import itertools
from enum import Enum
from .Bill import Bill
from .Deal import Deal
from .MenuItem import MenuItem

class State(Enum):
    ORDERED = 0
    COOKED = 1
    SERVED = 2

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, menu_items=[], deals=[]):
        self.__id = next(Order.__id_iter)
        self.__menu_items = menu_items
        self.__deals = deals
        self.__bill = Bill(0)
        self.__state = State.ORDERED

    # Getters
    def get_bill(self):
        return self.__bill
    
    def get_deals(self):
        return self.__deals
    
    def get_menu_items(self):
        return self.__menu_items
    
    def get_state(self):
        return self.__state
    
    def get_id(self):
        return self.__id
    
    # Adding and removing deal items to the order
    def add_deal(self, deal):
        if not isinstance(deal, Deal):
            raise TypeError("Order: add_deal(): Object is not of type Deal")
        
        if deal in self.__deals:
            raise ValueError("Order: add_deal(): Deal already exists")
        # TODO: Unsure how deals work

    def remove_deal(self, deal):
        if not isinstance(deal, Deal):
            raise TypeError("Order: remove_deal(): Object is not of type Deal")
        
        if deal not in self.__deals:
            raise ValueError("Order: remove_deal(): Deal does not exist")
        # TODO: Unsure how deals work
    
    # Adding and removing menu items to the order
    def add_menu_item(self, menuItem):
        if not isinstance(menuItem, MenuItem):
            raise TypeError("Order: add_menu_item(): Object is not of type MenuItem")
        
        if menuItem in self.__menu_items:
            raise ValueError("Order: add_menu_item(): MenuItem already exists")
        self.__menu_items.append(menuItem)
        self.__bill.add_price(menuItem.price())

    def remove_menu_item(self, menuItem):
        if not isinstance(menuItem, MenuItem):
            raise TypeError("Order: remove_menu_item(): Object is not of type MenuItem")
        
        if menuItem not in self.__menu_items:
            raise ValueError("Order: remove_menu_item(): MenuItem does not exist")
        self.__menu_items.remove(menuItem)
        self.__bill.reduce_price(menuItem.price())
    
    # Progress through states
    def change_state(self):
        if (self.__state == State.SERVED):
            raise ValueError("Order: change_state(): Already at the final state")
        elif (self.__state == State.COOKED):
            self.__state = State.SERVED
        elif (self.__state == State.ORDERED):
            self.__state = State.COOKED

    # Return final bill and set boolean to paid
    def calculate_bill(self):
        # This needs work -> Do we need to check the state before paying the bill?
        # Should we prohibit adding/removing items when bill is paid?
        if not (self.__state == State.SERVED):
            raise ValueError("Order: calculate_bill(): Order has not been served yet")
        self.__bill.pay()
        return self.__bill.get_price()