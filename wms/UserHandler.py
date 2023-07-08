from wms import User, Customer, KitchenStaff, WaitStaff, Manager

class UserHandler():
    def __init__(self) -> None:
        """ Constructor for the UserHandler Class """
        self.__users = []
    
    @property
    def users(self) -> list[User]:
        """ Returns list of users"""
        return self.__users
    
    def add_user(self, firstname, lastname, user_type):
        """ Adds a user to the system

        Args:
            firstname (String): First name of the user
            lastname (String): Last name of the user
            user_type (String): Class type of the user. Must be one of Customer,
            Kitchen Staff, Wait Staff or Manager 

        Returns:
            None: Returns None if an invalid user_type was provided
        """
        match user_type:
            case "Customer":      new_user = Customer(firstname, lastname)
            case "Kitchen Staff": new_user = KitchenStaff(firstname, lastname)
            case "Wait Staff":    new_user = WaitStaff(firstname, lastname)
            case "Manager":       new_user = Manager(firstname, lastname)
            case _:               return None
        
        self.__users.append(new_user)
    
    def jsonify(self) -> dict:
        """ Creates a dictionary of all the users and their first name, last 
        name and class type. 

        Returns:
            Dic: A dictionary of all the users and their first name, last name
        and class type. 
        """
        
        user_dict = {}
        for user in self.users:
            user_dict[f"User_{str(user.id)}"] = {"first_name": user.firstname,
                                                 "last name": user.lastname,
                                                 "type": user.__class__.__name__}
        return user_dict
    
    def id_to_user(self, id) -> User:
        """ Finds a particular user by their ID value

        Args:
            id (Integer): ID value of the user

        Returns:
            User: User to be found by their ID value
        """
        return next((user for user in self.__users if user.id == id), None)
