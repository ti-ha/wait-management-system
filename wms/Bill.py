class Bill:
    # Constructor for the final bill
    def __init__(self, price):
        self.__price = price
        self.__paid = False

    # Getters for price and paid status
    def get_price(self):
        return self.__price
    
    def is_paid(self):
        return self.__paid
    
    # Method to accumulate bill from menu items
    def add_price(self, price):
        if (self.__paid == True):
            raise ValueError("Bill: add_price(): Bill has already been paid")
        self.__price += price

    # Method to reduce bill from menu items
    def reduce_price(self, price):
        if (self.__paid == True):
            raise ValueError("Bill: reduce_price(): Bill has already been paid")
        self.__price -= price

    # When bill is paid, set bool to true
    def pay(self):
        self.__paid = True