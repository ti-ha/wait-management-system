import itertools
from .Table import Table
from datetime import datetime
from wms import User

class ServiceRequest:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, table: Table, subject: str, summary: str):
        self.__id = next(ServiceRequest.__id_iter)
        self.__table = table
        self.__subject = subject
        self.__summary = summary
        self.__timestamp = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        self.__completed = False
        self.__assignee = None

    @property
    def id(self):
        return self.__id
    
    @property
    def table(self):
        return self.__table
    
    @property
    def subject(self):
        return self.__subject
    
    @property
    def summary(self):
        return self.__summary
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def completed(self):
        return self.__completed
    
    @property
    def assignee(self) -> User:
        return self.__assignee
    
    @table.setter
    def table(self, table: Table):
        self.__table = table

    @subject.setter
    def subject(self, subject: str):
        self.__subject = subject

    @summary.setter
    def summary(self, string: str):
        self.__summary = string
    
    @completed.setter
    def completed(self, value: bool):
        self.__completed = value

    @assignee.setter
    def assignee(self, assignee: User):
        self.__assignee = assignee

    def jsonify(self):
        return {
            "id": self.id,
            "table": self.table.id,
            "summary": self.summary,
            "subject": self.subject,
            "timestamp": self.timestamp,
            "completed": self.completed,
            "assignee": f"{self.assignee.firstname}, {self.assignee.lastname}" if self.assignee else None 
        }