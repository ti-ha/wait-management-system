from .Deal import Deal
from .MenuItem import MenuItem
from datetime import datetime, timedelta

# After how many hours does a Personalised Deal expire
EXPIRY_HOURS = 1

class PersonalisedDeal(Deal):
    def __init__(self, discount, menu_items, user):
        super().__init__(discount, [menu_items])
        self.__user = user
        self.__expiry = datetime.now()+timedelta(hours=EXPIRY_HOURS)


    @property
    def user(self):
        """ The user associated with the deal

        Returns:
            string: The id of the user associated with the deal
        """
        return self.__user
    
    @property
    def expiry(self):
        """ The expiry date of the deal

        Returns:
            string: datestring of the expiry of the deal
        """
        return self.__expiry.strftime("%H:%M:%S %d/%m/%Y")
    
    def is_expired(self):
        """ Checks if the deal is expired

        Returns:
            bool: True if expired, False if not expired
        """
        return datetime.now() >= self.__expiry

    def jsonify(self):
        """ Returns the json-style dictionary representing all the data in the
        object for use in the API

        Returns:
            dict: json-style dictionary containing relevant data
        """
        return {
            "id": self.id, 
            "discount": self.discount, 
            "menu_items": [i.jsonify() for i in self.menu_items],
            "user": self.user,
            "expiry": self.expiry,
            "is_expired": self.is_expired()
            }