from __future__ import annotations
import itertools
from enum import Enum
from .Bill import Bill
from .Deal import Deal
from .MenuItem import MenuItem
import json

class States(Enum):
    ORDERED = 0
    COOKING = 1
    READY = 2
    SERVED = 3
    COMPLETED = 4

    def successor(self):
        v = self.value + 1
        if v > 4:
            raise ValueError("Enumeration ended")
        return States(v)
    
    @staticmethod
    def list():
        return States._member_names_

class State:

    def __init__(self):
        self.__state = States(0)

    def transition_state(self):
        self.__state = self.__state.successor()

    def state(self) -> str:
        if self.__state == States(0):
            return "ordered"
        elif self.__state == States(1):
            return "cooking"
        elif self.__state == States(2):
            return "ready"
        elif self.__state == States(3):
            return "served"
        elif self.__state == States(4):
            return "completed"

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, menu_items=None, deals=None):
        self.__id = next(Order.__id_iter)
        self.__bill = None
        self.__state = State()

        if isinstance(deals, Deal):
            self.__deals = [deals]
        else:
            self.__deals = deals

        if isinstance(menu_items, MenuItem):
            self.__menu_items = [menu_items]
        else:
            self.__menu_items = menu_items

        if self.__menu_items == None:
            self.__menu_items = []

        if self.__deals == None:
            self.__deals = []

    # Getters
    def bill(self) -> Bill | None:
        return self.__bill
    
    def deals(self) -> list[Deal]:
        return self.__deals
    
    def menu_items(self) -> list[MenuItem]:
        return self.__menu_items
    
    def state(self) -> str:
        return self.__state.state()

    def change_state(self):
        self.__state.transition_state()
    
    def id(self) -> int:
        return self.__id
    
    # Adding and removing deal items to the order
    def add_deal(self, deal):
        if not isinstance(deal, Deal):
            raise TypeError("Order: add_deal(): Object is not of type Deal")
        
        if deal in self.__deals:
            raise ValueError("Order: add_deal(): Deal already exists")
        
        self.deals().append(deal)

    def remove_deal(self, deal):
        if not isinstance(deal, Deal):
            raise TypeError("Order: remove_deal(): Object is not of type Deal")
        
        if deal not in self.__deals:
            raise ValueError("Order: remove_deal(): Deal does not exist")
        
        self.deals().remove(deal)
    
    # Adding and removing menu items to the order
    def add_menu_item(self, menuItem):
        if not isinstance(menuItem, MenuItem):
            raise TypeError("Order: add_menu_item(): Object is not of type MenuItem")
        
        if menuItem in self.__menu_items:
            raise ValueError("Order: add_menu_item(): MenuItem already exists")
        self.__menu_items.append(menuItem)

    def remove_menu_item(self, menuItem):
        if not isinstance(menuItem, MenuItem):
            raise TypeError("Order: remove_menu_item(): Object is not of type MenuItem")
        
        if menuItem not in self.__menu_items:
            raise ValueError("Order: remove_menu_item(): MenuItem does not exist")
        self.__menu_items.remove(menuItem)

    # Applies a deal to a dictionary of menuitem: price
    def apply_deal(self, pricedict: dict, deal: Deal):
        for i in deal.menu_items():
            item = i.name()
            if item in pricedict.keys():
                pricedict[item] = pricedict[item] - (deal.discount()*pricedict[item])
        return pricedict

    # Return final bill
    def calculate_bill(self) -> Bill:
        # This needs work -> Do we need to check the state before paying the bill?
        # Should we prohibit adding/removing items when bill is paid?
        # Yes, but just make it so they can't pay the bill until order has been served
                
        # Create a NEW dictionary of {menuitem: price, ... , menuitem: price}. We do not want to modify the existing objects
        pricedict = {}
        for i in self.menu_items():
            pricedict[i.name()] = i.price()

        # For each deal in the order, apply it to the price dictionary
        for i in self.deals():
            pricedict = self.apply_deal(pricedict, i)

        # Add the prices in pricedict together
        finalcost = sum([pricedict[i] for i in pricedict.keys()])
        self.__bill = Bill(finalcost)

        return Bill(finalcost)
    
    def mark_as_paid(self):
        if not self.state() == "served":
            raise ValueError("Order: mark_as_paid(): Order "+self.id()+" has not been served yet")
        
        if self.bill() == None:
            raise ValueError("Order: bill has not been calculated yet. (Try order.calculate_bill())")
        
        if self.bill().is_paid():
            return "Bill already paid"
        
        else:
            self.bill().pay()
            self.change_state()
    
    def bill_paid(self):
        return self.bill().is_paid()
    
    def jsonify(self):
        if self.__bill != None:
            bill = self.__bill.jsonify()
        else:
            bill = None
        output = {"id": self.__id, 
                  "bill": bill,
                  "state": self.state(),
                  "menu_items": [],
                  "deals": []}
        for i in self.menu_items():
            output["menu_items"].append(i.jsonify())
        for i in self.deals():
            output["deals"].append(i.jsonify())
        
        return output
        
        

        


        


        

