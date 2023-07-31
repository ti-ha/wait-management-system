from __future__ import annotations
import itertools
from enum import Enum
from .Bill import Bill
from .Deal import Deal
from .PersonalisedDeal import PersonalisedDeal
from .MenuItem import MenuItem

class States(Enum):
    DELETED = -1
    ORDERED = 0
    COOKING = 1
    READY = 2
    SERVED = 3
    COMPLETED = 4

    def successor(self):
        """ Acquires the next state

        Raises:
            ValueError: Raised if final state has been reached

        Returns:
            State: Next state to be transitioned to
        """
        v = self.value + 1
        if v > 4:
            raise ValueError("Enumeration ended")
        return States(v)

    @staticmethod
    def list():
        """ Returns names of all the states """
        return [i.lower() for i in States._member_names_]

class State:

    def __init__(self):
        """ Constructor for the State class """
        self.__state = States(0)

    def transition_state(self):
        """ Moves state to the next one """
        self.__state = self.__state.successor()

    @property
    def state(self) -> str:
        """ Converts State to string

        Returns:
            str: Current state as a string
        """
        if self.__state   == States.DELETED:
            return "deleted"
        elif self.__state == States.ORDERED:
            return "ordered"
        elif self.__state == States.COOKING:
            return "cooking"
        elif self.__state == States.READY:
            return "ready"
        elif self.__state == States.SERVED:
            return "served"
        elif self.__state == States.COMPLETED:
            return "completed"
        else:
            raise ValueError("State outside bounds")
            
    @property
    def value(self) -> int:
        """ Converts state to int

        Raises:
            ValueError: Current state out of bounds somehow

        Returns:
            int: The state value
        """
        if self.__state   == States.DELETED:
            return -1
        elif self.__state == States.ORDERED:
            return 0
        elif self.__state == States.COOKING:
            return 1
        elif self.__state == States.READY:
            return 2
        elif self.__state == States.SERVED:
            return 3
        elif self.__state == States.COMPLETED:
            return 4
        else:
            raise ValueError("State outside bounds")

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, menu_items=None, deals=None, customer=None):
        """ Constructor for the Order class

        Args:
            menu_items (List[MenuItem], optional): Menu items to be added to the
            order. Defaults to None.
            deals (List[Deal], optional): Deals to be added to the order.
            Defaults to None.
            customer (User, optional): The customer to be assigned to the order.
        """
        self.__id = next(Order.__id_iter)
        self.__bill = None
        self.__state = State()
        self.__deals = [deals] if isinstance(deals, Deal) else deals
        self.__menu_items_ids = itertools.count()
        self.__customer = customer if customer else None

        # Perhaps there is a more pythonic way to do this
        if menu_items == None:
            self.__menu_items = []
        elif isinstance(menu_items, MenuItem):
            if menu_items.visible == False:
                raise ValueError("Order(): One or more menu_items is currently hidden")
            self.__menu_items = [{"menu_item": menu_items,
                                  "state": State(),
                                  "order_specific_id": next(self.__menu_items_ids)}]
        else:
            if next((i for i in menu_items if i.visible == False), None) != None:
                raise ValueError("Order(): One or more menu_items is currently hidden")
            self.__menu_items = [{"menu_item": m,
                                  "state": State(),
                                  "order_specific_id": next(self.__menu_items_ids)}
                                  for m in menu_items]
        #self.__menu_items = [menu_items] if isinstance(menu_items, MenuItem) else menu_items


        #self.__menu_items = [] if menu_items is None else menu_items
        self.__deals = [] if deals is None else deals

    # Getters
    @property
    def id(self) -> itertools.count:
        """ Returns order ID """
        return self.__id

    @property
    def bill(self) -> Bill:
        """ Returns order bill """
        return self.__bill

    @property
    def deals(self) -> list[Deal]:
        """ Returns list of deals in the order """
        return self.__deals
    
    @property
    def customer(self) -> int:
        """ Returns the customer id assigned to the order"""
        return self.__customer
    
    @property
    def menu_items(self) -> list[MenuItem]:
        """ Returns list of menu items in the order """
        return [i["menu_item"] for i in self.__menu_items]

    @property
    def menu_item_states(self) -> list[dict]:
        return self.__menu_items

    @property
    def state(self) -> str:
        """ Returns current state of the order """
        return self.__state.state
    
    @property
    def state_value(self) -> int:
        return self.__state.value

    def get_menu_item_state_obj(self, id: int) -> State:
        """Gets the state of a menu_item within the order

        Args:
            id (int): The order_specific_id of the menu_item whose state is to be fetched

        Raises:
            ValueError: Raised if the menu_item does not exist in the order

        Returns:
            string: The state of the menu_item
        """
        menu_item_state = next((i["state"] for i in self.menu_item_states if i["order_specific_id"] == id), None)
        if menu_item_state == None:
            raise ValueError("Order: get_menu_item_state(): menu_item does not exist in order")
        
        return menu_item_state


    def change_menu_item_state_by_id(self, id):
        """Transitions the state of a menu item to the next state, looking up by order_specific_id

        Args:
            id (int): The id of the menu_item in the order
        """
        self.get_menu_item_state_obj(id).transition_state()

        while min([i["state"].value for i in self.menu_item_states]) > self.state_value:
            self.change_state()

    def change_state(self):
        """ Transitions state to the next one """
        self.__state.transition_state()

    def add_deal(self, deal):
        """ Adding a deal item to the order

        Args:
            deal (Deal): Deal to be added to the order

        Raises:
            TypeError: Raised when deal argument is not of type deal
            ValueError: Raised when deal already exists in the order
        """
        if not isinstance(deal, Deal):
            raise TypeError("Order: add_deal(): Object is not of type Deal")

        if deal in self.__deals:
            raise ValueError("Order: add_deal(): Deal already exists")
        
        if isinstance(deal, PersonalisedDeal):
            if deal.is_expired():
                raise ValueError("Order: add_deal(): Deal has expired")
            elif deal.user != self.customer:
                raise ValueError("Order: add_deal(): That is not your deal")
            elif next((i for i in deal.menu_items if i.visible == False) != None):
                raise ValueError("Order: add_deal(): One or more menu_items is hidden")

        self.deals.append(deal)

    def remove_deal(self, deal):
        """ Removing a deal item from the order

        Args:
            deal (Deal): Deal to be removed from the order

        Raises:
            TypeError: Raised when deal argument is not of type deal
            ValueError: Raised when deal does not exist in the order
        """
        if not isinstance(deal, Deal):
            raise TypeError("Order: remove_deal(): Object is not of type Deal")

        if deal not in self.__deals:
            raise ValueError("Order: remove_deal(): Deal does not exist")

        self.deals.remove(deal)

    def add_menu_item(self, menu_item):
        """ Adding a menu item to the order

        Args:
            menuItem (MenuItem): Menu item to be added to the order

        Raises:
            TypeError: Raised when menu_item argument is not of type MenuItem
            ValueError: Raised when menu_item already exists in the order
        """
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Order: add_menu_item(): Object is not of type MenuItem")

        if menu_item in self.__menu_items:
            raise ValueError("Order: add_menu_item(): MenuItem already exists")
        
        if menu_item.visible == False:
            raise ValueError("Order: add_menu_item(): MenuItem is not visible")
        
        self.__menu_items.append(menu_item)

    def get_menu_item_by_id(self, id) -> MenuItem:
        return next((i["menu_item"] for i in self.menu_item_states if i["order_specific_id"] == id), None)

    def remove_menu_item(self, menu_item):
        """ Removing a menu item from the order

        Args:
            menuItem (MenuItem): Menu item to be removed from the order

        Raises:
            TypeError: Raised when menu_item argument is not of type MenuItem
            ValueError: Raised when menu_item does not exist in the order
        """
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Order: remove_menu_item(): Object is not of type MenuItem")

        if menu_item not in self.__menu_items:
            raise ValueError("Order: remove_menu_item(): MenuItem does not exist")
        self.__menu_items.remove(menu_item)

    def apply_deal(self, pricedict: dict, deal: Deal) -> dict:
        """ Applies a deal to a dictionary of menuitem: price

        Args:
            pricedict (dict): Dictionary linking prices to menu items
            deal (Deal): Deal to be applied to the menu item

        Returns:
            Dict: New dictionary after deal discount is applied to menu items
        """
        if deal.visible == False:
            discount = 0
        else:
            discount = deal.discount
        for i in deal.menu_items:
            item = i.name
            if item in pricedict.keys():
                pricedict[item] = round(pricedict[item] - (discount*pricedict[item]), 2)
        return pricedict

    def calculate_bill(self) -> Bill:
        """ Return current bill of the order

        Returns:
            Bill: Returns the current bill. Create a NEW dictionary of
            {menuitem: price, ... , menuitem: price}.
            We do not want to modify the existing objects
        """
        if self.bill != None:
            return self.bill
        
        pricedict = {}
        for i in self.menu_items:
            pricedict[i.name] = i.price

        # For each deal in the order, apply it to the price dictionary
        for i in self.deals:
            pricedict = self.apply_deal(pricedict, i)

        # Add the prices in pricedict together
        finalcost = sum([float(pricedict[i]) for i in pricedict])
        self.__bill = Bill(finalcost)

        return self.__bill

    def mark_as_paid(self):
        """ Mark order bill as paid once all conditions are satisfied

        Raises:
            ValueError: Raised when order state is not at served yet or if the
            bill has not been calculated yet. Check error description for more
            information

        Returns:
            String: Only returns if the bill is already paid. Otherwise returns
            nothing
        """
        if self.state != "served":
            raise ValueError(f"Order: mark_as_paid(): Order {self.id} has not been served yet")

        if self.__bill is None:
            raise ValueError("Order: bill has not been calculated yet. (Try order.calculate_bill())")

        if self.__bill.paid:
            return "Bill already paid"

        self.__bill.pay()
        self.change_state()

    def bill_paid(self) -> bool:
        """ Returns status of bill

        Returns:
            bool: Returns whether the bill is paid or not
        """
        return self.__bill.paid

    def jsonify_menu_item_states(self) -> dict:
        """ Generates a dictionary for each menu_item in the order that also contains its state

        Returns:
            dict: Dictionary containing all properties of each menu_item with an accompanying state
        """
        output = []
        for i in self.menu_item_states:
            states = i["menu_item"].jsonify()
            states["state"] = i["state"].state
            states["order_specific_id"] = i["order_specific_id"]
            output.append(states)

        return output


    def jsonify(self, table_id=None) -> dict:
        """ Creates a dictionary containing the id, bill, state, list of menu
        items and deals of the order

        Returns:
            dict: Dictionary containing the id, bill, state, list of menu items
            and deals of the order
        """
        bill = self.__bill.jsonify() if self.__bill is not None else None
        # if self.__bill is not None:
        #     bill = self.__bill.jsonify()
        # else:
        #     bill = None
        output = {
            "id": self.__id,
            "bill": bill,
            "state": self.state,
            "menu_items": self.jsonify_menu_item_states(),
            "deals": [i.jsonify() for i in self.deals],
            "user": self.customer
        }

        if table_id is not None:
            output["table_id"] = table_id

        return output