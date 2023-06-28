import json

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

    # When bill is paid, set bool to true
    def pay(self):
        self.__paid = True

    def jsonify(self) -> str:
        output = {"price": self.__price, "paid": self.__paid}
        return output
