from .ServiceRequest import ServiceRequest
from .Application import Base
from sqlalchemy import Column, Integer, Double, String, ForeignKey

class ServiceRequestManager:
    __tablename__ = 'request'
    requestId = Column(Integer, primary_key=True)
    tableId = Column(Integer, ForeignKey('table.tableId'))

    def __init__(self):
        self.__queue = []