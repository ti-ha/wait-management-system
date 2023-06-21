from User import User

class WaitStaff(User):
    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        self.__requests = []

    # Get list of requests
    def get_requests(self):
        return self.__requests