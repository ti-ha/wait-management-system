class Bill:
    def __init__(self, price):
        """Constructor for the bill class

        Args:
            price (float): Starting price value of the bill
        """
        self.__price = price
        self.__paid = False

    # Getters for price and paid status
    @property
    def price(self) -> float:
        """Returns bill price"""
        return self.__price
    
    @property
    def paid(self) -> bool:
        """Returns if it is paid or not"""
        return self.__paid

    def pay(self):
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
        output = {"price": self.__price, "paid": self.__paid}
        return output
