import User

class WaitStaff(User):
    def __init__(self, firstname, lastname):
        super().__init__(self, firstname, lastname)
        self.__requests = []
