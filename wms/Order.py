import itertools
import Bill
import Deal
import MenuItem

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()
    
    def __init__(self):
        self.__id = next(Order.__id_iter)
        self.__menu_items = []
        self.__deals = []
        self.__bill = Bill(0)
        #self.__status: State (NOT YET IMPLEMENTED)
    
    def __init__(self, menu_items):
        self.__id: next(Order.__id_iter)
        self.__menu_items =  menu_items
        self.__deals = []

    def __init__(self, menu_items, deals):
        self.__id = next(Order.__id_iter)
        self.__menu_items = menu_items
        self.__deals = deals

    # Getters
    def get_bill(self):
        return self.__bill
    
    def get_deals(self):
        return self.__deals
    
    def get_menu_items(self):
        return self.__menu_items
    
    # Adding and removing deal items to the order
    def add_deal(self, deal):
        self.__deals.append(deal)
        # self.get_bill().add_price(deal.get_discount())

    def remove_deal(self, deal):
        self.__deals.remove(deal)
    
    # Adding and removing menu items to the order
    def add_menu_item(self, menuItem):
        self.__menu_items.append(menuItem)
        # self.get_bill().add_price(menuItem.get_price())

    def remove_menu_item(self, menuItem):
        self.__menu_items.remove(menuItem)
    
    # def change_state():