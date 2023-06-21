from .User import User

# Has no other attributes differentiating itself from a user
# only important difference is type. Also can see OrderManager
class Manager(User):
    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        pass