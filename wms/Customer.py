from .User import User
from .Application import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Customer(User):

    __tablename__ = 'customer'
    tableId = Column(Integer, ForeignKey('table.id'))
    id = Column(Integer, ForeignKey('user.userId'), primary_key=True)

    def __init__(self, firstname="Guest", lastname="Customer"):
        super().__init__(firstname, lastname)
        self.__table = None
    
    # Getters and Setters
    def get_table(self):
        return self.__table
    
    def set_table(self, table):
        self.__table = table