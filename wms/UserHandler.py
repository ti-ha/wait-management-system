from wms import User, Customer, KitchenStaff, WaitStaff, Manager
from wms.DbHandler import DbHandler
from wms.DbHandler import User as UserTable
from sqlalchemy.orm import Session
from sqlalchemy import select, update

class UserHandler():
    def __init__(self, db: DbHandler) -> None:
        """ Constructor for the UserHandler Class """
        self.__users = []
        self.__db = db
    
    @property
    def users(self) -> list[User]:
        """ Returns list of users"""
        return self.__users
    
    @property
    def db(self) -> DbHandler:
        """Returns db"""
        return self.__db
    
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
        self.__users.append(new_user)
        with Session(self.db.engine) as session:
            session.add(UserTable(
                id=new_user.id,
                first_name = firstname,
                last_name = lastname,
                password_hash = new_user.password_hash,
                logged_in = 0
            ))
            try: 
                session.commit()
            except:
                session.rollback()

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
        with Session(self.db.engine) as session:
            session.execute(update(UserTable).where(
                UserTable.first_name == firstname).where(
                UserTable.last_name == lastname).values(
                logged_in=1
            ))
            try: 
                session.commit()
            except:
                session.rollback()
        return usermatch if success else None
        
    def logout(self, firstname, lastname) -> bool:
        """ Attempts to log out the user

        Args:
            firstname (String): First name of the user
            lastname (String): Last name of the user

        Returns:
            Bool: Returns true if logout was successful, false otherwise
        """
        usermatch = next((i for i in self.users 
                     if i.firstname == firstname and i.lastname == lastname), None)
        
        if usermatch is not None:
            usermatch.status = False
            with Session(self.db.engine) as session:
                session.execute(update(UserTable).where(
                    UserTable.first_name == firstname).where(
                    UserTable.last_name == lastname).values(
                    logged_in=0
                ))
                try: 
                    session.commit()
                except:
                    session.rollback()
            return True
        return False

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
