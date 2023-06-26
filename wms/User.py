import itertools
from .Application import Base
from sqlalchemy import Column, Integer, Double, String, ForeignKey

class User(Base):
    # Unique identifier starting from 0
    __id_iter = itertools.count()
    __tablename__ = "user"
    userId = Column(Integer, primary_key=True)
    firstname = Column(String(40), nullable=False)
    lastname = Column(String(40), nullable=False)
    userType = Column(String(40), nullable=False)
    
    def __init__(self, firstname, lastname):
        self.__id = next(User.__id_iter)
        self.__firstname = firstname
        self.__lastname = lastname

    # Getters
    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname
    
    def get_id(self):
        return self.__id