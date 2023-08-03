from wms import User, Customer, KitchenStaff, WaitStaff, Manager
from wms.DbHandler import DbHandler
from wms.DbHandler import User as UserTable
from sqlalchemy.orm import Session
from sqlalchemy import select, update

class UserHandler():
    def __init__(self, db: DbHandler) -> None:
        """ Constructor for the UserHandler Class 
        
        Args:
            db (DbHandler): Database handler to maintain database persistence
        """
        self.__users = []
        self.__db = db
    
    @property
    def users(self) -> list[User]:
        """ Returns list of users """
        return self.__users
    
    @property
    def db(self) -> DbHandler:
        """ Returns db handler """
        return self.__db
    
    def add_user(self, firstname: str, lastname: str, user_type: str, password: str, 
                 existing_hash: str = None):
        """ Adds a user to the system

        Args:
            firstname (str): First name of the user
            lastname (str): Last name of the user
            user_type (str): Class type of the user. Must be one of Customer,
            KitchenStaff, WaitStaff or Manager 
            password (str): Password of the user.
            existing_hash (str, optional): Already hashed password. Defaults to
            None

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
            new_user = Customer(firstname, lastname, password, existing_hash)
        elif user_type == "KitchenStaff":
            new_user = KitchenStaff(firstname, lastname, password, existing_hash)
        elif user_type == "WaitStaff":
            new_user = WaitStaff(firstname, lastname, password, existing_hash)
        elif user_type == "Manager":
            new_user = Manager(firstname, lastname, password, existing_hash)
        else: 
            return None
        
        self.__users.append(new_user)
        self.__users.append(new_user)
        with Session(self.db.engine) as session:
            session.add(UserTable(
                id=new_user.id,
                first_name = firstname,
                last_name = lastname,
                type = user_type,
                password_hash = new_user.password_hash,
                logged_in = 0
            ))
            try: 
                session.commit()
            except:
                session.rollback()

    def login(self, firstname: str, lastname: str, password: str) -> User:
        """ Attempts to log in the user

        Args:
            firstname (str): First name of the user
            lastname (str): Last name of the user
            password (str): Password of the user

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
        
    def logout(self, user: User) -> bool:
        """ Attempts to log out the user

        Args:
            user (User): User logging out of the system

        Returns:
            bool: Returns true if logout was successful, false otherwise
        """
        usermatch = next((i for i in self.users 
                     if i.firstname == user.firstname and i.lastname == user.lastname), None)
        
        if usermatch is not None:
            usermatch.status = False
            with Session(self.db.engine) as session:
                session.execute(update(UserTable).where(
                    UserTable.first_name == user.firstname).where(
                    UserTable.last_name == user.lastname).values(
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
        name, class type and hashed password. 

        Returns:
            dict: A dictionary of all the users and their first name, last name
        class type, and hashed password. 
        """
        
        user_dict = {}
        for user in self.users:
            user_dict[f"User_{str(user.id)}"] = {"first_name": user.firstname,
                                                 "last_name": user.lastname,
                                                 "type": user.__class__.__name__,
                                                 "password": user.password_hash}
        return user_dict
    
    def id_to_user(self, id: int) -> User:
        """ Finds a particular user by their ID value

        Args:
            id (int): ID value of the user

        Returns:
            User: User to be found by their ID value
        """
        return next((user for user in self.__users if user.id == id), None)
