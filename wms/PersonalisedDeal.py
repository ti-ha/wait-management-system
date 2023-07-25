from .Deal import Deal
from .MenuItem import MenuItem
from datetime import datetime, timedelta

EXPIRY_HOURS = 1

class PersonalisedDeal(Deal):
    def __init__(self, discount, menu_items, user):
        super().__init__(discount, [menu_items])
        self.__user = user
        self.__expiry = datetime.now()+timedelta(hours=EXPIRY_HOURS)


    @property
    def user(self):
        return self.__user
    
    @property
    def expiry(self):
        return self.__expiry.strftime("%H:%M:%S %d/%m/%Y")
    
    def is_expired(self):
        return datetime.now() >= self.__expiry

    def jsonify(self):
        return {
            "id": self.id, 
            "discount": self.discount, 
            "menu_items": [i.jsonify() for i in self.menu_items],
            "user": self.user,
            "expiry": self.expiry,
            "is_expired": self.is_expired()
            }