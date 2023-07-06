from wms import User, Customer, KitchenStaff, WaitStaff, Manager

class UserHandler():
    def __init__(self) -> None:
        self.__users = []
    
    
    def add_user(self, firstname, lastname, user_type):
        match user_type:
            case "Customer":      new_user = Customer(firstname, lastname)
            case "Kitchen Staff": new_user = KitchenStaff(firstname, lastname)
            case "Wait Staff":    new_user = WaitStaff(firstname, lastname)
            case "Manager":       new_user = Manager(firstname, lastname)
            case _:               return None
        
        self.__users.append(new_user)
        return new_user.id
    
    def jsonify(self):
        user_dict = {}
        for user in self.__users:
            user_dict[f"User_{str(user.get_id())}"] = {"first_name": user.get_firstname(),
                                                       "last name": user.get_lastname(),
                                                       "type": user.__class__.__name__}
        return user_dict
    
    def id_to_user(self, id):
        return next([user for user in self.__users if user.get_id() == id], None)
