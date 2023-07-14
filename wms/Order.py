from __future__ import annotations
import itertools
from enum import Enum
from .Bill import Bill
from .Deal import Deal
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
        match self.__state:
            case States.DELETED:
                return "deleted"
            case States.ORDERED:
                return "ordered"
            case States.COOKING:
                return "cooking"
            case States.READY:
                return "ready"
            case States.SERVED:
                return "served"
            case States.COMPLETED:
                return "completed"
            case _:
                raise ValueError("State outside bounds")

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, menu_items=None, deals=None):
        """ Constructor for the Order class

        Args:
            menu_items (List[MenuItem], optional): Menu items to be added to the
            order. Defaults to None.
            deals (List[Deal], optional): Deals to be added to the order.
            Defaults to None.
        """
        self.__id = next(Order.__id_iter)
        self.__bill = None
        self.__state = State()
        self.__deals = [deals] if isinstance(deals, Deal) else deals
        self.__menu_items_ids = itertools.count()

        # Perhaps there is a more pythonic way to do this
        if menu_items == None:
            self.__menu_items = []
        elif isinstance(menu_items, MenuItem):
            self.__menu_items = [{"menu_item": menu_items,
                                  "state": State(),
                                  "order_specific_id": next(self.__menu_items_ids)}]
        else:
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

    def get_menu_item_state_obj(self, menu_item: MenuItem) -> State:
        """Gets the state of a menu_item within the order

        Args:
            menu_item (MenuItem): The menu_item whose state is to be fetched

        Raises:
            ValueError: Raised if the menu_item does not exist in the order

        Returns:
            string: The state of the menu_item
        """
        if menu_item == None:
            raise ValueError("Order: get_menu_item_state(): menu_item does not exist in order")

        return next((i["state"] for i in self.menu_item_states if i["menu_item"] == menu_item))

    def get_menu_item_state_by_id(self, id):
        """Gets the state of a menu_item within the order, searching by order-native id

        Args:
            id (int): The id of the menu_item whose state is to be fetched

        Returns:
            string: The state of the menu_item
        """
        menu_item = next((i["menu_item"] for i in self.menu_item_states if i["order_specific_id"] == id), None)
        return self.get_menu_item_state_obj(menu_item)

    def change_menu_item_state(self, menu_item: MenuItem):
        """Transitions the state of a menu item based upon the menu_item itself

        Args:
            menu_item (MenuItem): the menu item whose state is to be transitioned

        Raises:
            ValueError: Raised if the menu_item does not exist in the order
        """
        if menu_item is None:
            raise ValueError("Order: change_menu_item_state(): menu_item does not exist in order")

        self.get_menu_item_state_obj(menu_item).transition_state()

    def change_menu_item_state_by_id(self, id):
        """Transitions the state of a menu item to the next state, looking up by id

        Args:
            id (int): The id of the menu_item in the order
        """
        menu_item = self.get_menu_item_state_by_id(id)
        self.change_menu_item_state(menu_item)

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
        self.__menu_items.append(menu_item)

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
        for i in deal.menu_items:
            item = i.name
            if item in pricedict.keys():
                pricedict[item] = pricedict[item] - (deal.discount*pricedict[item])
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
            "deals": [i.jsonify() for i in self.deals]
        }

        if table_id is not None:
            output["table_id"] = table_id

        return output