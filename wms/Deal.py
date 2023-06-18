class Deal:
    def __init__(self, discount):
        self.__discount = discount
        self.__menu_items = []
    
    def __init__(self, discount, menu_items):
        self.__discount = discount
        self.__menu_items = menu_items