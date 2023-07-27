class Bill:
    def __init__(self, price):
        """ Constructor for the bill class

        Args:
            price (float): Starting price value of the bill
        """
        self.__price = price
        self.__paid = False

    def __eq__(self, bill):
        """ Checks if the price of another bill object is the same, if so
        returns True. if the other non-boolean attribute is not equal, or its
        the wrong class type, return false.
        """
        if not isinstance(bill, Bill):      return False
        if self.price is not bill.price:    return False
        
        return True


    # Getters for price and paid status
    @property
    def price(self) -> float:
        """ Returns bill price """
        return self.__price
    
    @property
    def paid(self) -> bool:
        """ Returns if it is paid or not """
        return self.__paid

    def pay(self) -> None:
        """ When the bill is paid, set bool to true
        """
        self.__paid = True

    def jsonify(self) -> dict:
        """ Creates a dictionary containing the price and paid status of the 
        bill

        Returns:
            dict: Dictionary containing the price and paid status of the 
        bill
        """
        return {"price": self.__price, "paid": self.__paid}
    
