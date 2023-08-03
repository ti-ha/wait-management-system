from .Deal import Deal
from .MenuItem import MenuItem
from datetime import datetime, timedelta

# After how many hours does a Personalised Deal expire
EXPIRY_HOURS = 1

class PersonalisedDeal(Deal):
    def __init__(self, discount: float, menu_items, user: str):
        """ Constructor for the personalisedDeal class """
        super().__init__(discount, [menu_items])
        self.__user = user
        self.__expiry = datetime.now()+timedelta(hours=EXPIRY_HOURS)

    @property
    def user(self) -> str:
        """ The user associated with the deal

        Returns:
            str: The id of the user associated with the deal
        """
        return self.__user
    
    @property
    def expiry(self) -> str:
        """ The expiry date of the deal

        Returns:
            str: datestring of the expiry of the deal
        """
        return self.__expiry.strftime("%H:%M:%S %d/%m/%Y")
    
    def is_expired(self) -> bool:
        """ Checks if the deal is expired

        Returns:
            bool: True if expired, False if not expired
        """
        return datetime.now() >= self.__expiry

    def jsonify(self) -> dict:
        """ Returns the json-style dictionary representing all the data in the
        object for use in the API

        Returns:
            dict: json-style dictionary containing relevant data
        """
        return {
            "id": self.id, 
            "discount": self.discount, 
            "menu_items": [{"id": i.jsonify()["id"], 
                            "name": i.jsonify()["name"], 
                            "price": round(i.jsonify()["price"] - i.jsonify()["price"]*self.discount, 2),
                            "imageURL": i.jsonify()["imageURL"],
                            "visible": i.jsonify()["visible"]} for i in self.menu_items],
            "user": self.user,
            "expiry": self.expiry,
            "is_expired": self.is_expired()
            }