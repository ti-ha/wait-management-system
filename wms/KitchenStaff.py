from .User import User

class KitchenStaff(User):
    def __init__(self, firstname, lastname):
        super().__init__(self, firstname, lastname)
        self.__orders = []
