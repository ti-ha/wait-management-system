import Category, MenuItem, Deal

class Menu:

    def __init__(self):
        self.__categories = []
        self.__deals      = []
    
    def __init__(self, categories, deals):
        self.__categories = categories
        self.__deals = deals

