from wms import User, Customer, KitchenStaff, WaitStaff, Manager

class UserHandler():
    def __init__(self) -> None:
        """ Constructor for the UserHandler Class """
        self.__users = []
    
    @property
    def users(self) -> list[User]:
        """ Returns list of users"""
        return self.__users
    
    def add_user(self, firstname, lastname, user_type, password):
        """ Adds a user to the system

        Args:
            firstname (String): First name of the user
            lastname (String): Last name of the user
            user_type (String): Class type of the user. Must be one of Customer,
            KitchenStaff, WaitStaff or Manager 

        Returns:
            None: Returns None if an invalid user_type was provided
        """
        user_lookup = next((i for i in self.users if 
                       i.firstname == firstname and 
                       i.lastname == lastname and 
                       i.__class__.__name__ == user_type and 
                       i.check_password(password) == True), None)
        
        if user_lookup:
            raise ValueError("UserHandler: add_user(): User with exact credentials already exists")
        
        if user_type == "Customer": 
            new_user = Customer(firstname, lastname, password)
        elif user_type == "KitchenStaff":
            new_user = KitchenStaff(firstname, lastname, password)
        elif user_type == "WaitStaff":
            new_user = WaitStaff(firstname, lastname, password)
        elif user_type == "Manager":
            new_user = Manager(firstname, lastname, password)
        else: 
            return None
        
        self.__users.append(new_user)

    def login(self, firstname, lastname, password) -> User:
        """ Attempts to log in the user

        Args:
            firstname (String): First name of the user
            lastname (String): Last name of the user
            password (String): Password of the user

        Returns:
            User: Returns the user if log in was successful, otherwise 
            returns None
        """
        usermatch = next((i for i in self.users 
                     if i.firstname == firstname and i.lastname == lastname), None)
        
        if usermatch is not None:
            success = usermatch.check_password(password)
        else:
            return None
    
        usermatch.status = True
        return usermatch if success else None
        
    def logout(self, user: User) -> bool:
        """ Attempts to log out the user

        Args:
            firstname (String): First name of the user
            lastname (String): Last name of the user

        Returns:
            Bool: Returns true if logout was successful, false otherwise
        """
        if not isinstance(user, User):
            raise TypeError("UserHandler: logout(): argument is of invalid type (expected User)")
        elif user is not None:
            user.status = False
            return None
        raise ValueError("UserHandler: logout(): token did not match a user")

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
                                                 "last_name": user.lastname,
                                                 "type": user.__class__.__name__,
                                                 "password": user.password_hash}
        return user_dict
    
    
    def id_to_user(self, id) -> User:
        """ Finds a particular user by their ID value

        Args:
            id (Integer): ID value of the user

        Returns:
            User: User to be found by their ID value
        """
        return next((user for user in self.__users if user.id == id), None)
