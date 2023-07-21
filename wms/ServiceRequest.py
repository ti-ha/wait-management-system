import itertools
from .Table import Table
from datetime import datetime
from wms import User
from enum import Enum

class States(Enum):
    DELETED = -1
    READY = 0
    INPROGRESS = 1
    COMPLETED = 2

    def successor(self):
        """ Acquires the next state

        Raises:
            ValueError: Raised if final state has been reached

        Returns:
            State: Next state to be transitioned to
        """
        v = self.value + 1
        if v > 2:
            raise ValueError("Enumeration ended")
        return States(v)

    @staticmethod
    def list():
        """ Returns names of all the states """
        return [i.lower() for i in States._member_names_]

class State:

    def __init__(self, value=0):
        """ Constructor for the State class """
        self.__state = States(value)

    def transition_state(self):
        """ Moves state to the next one """
        self.__state = self.__state.successor()

    @property
    def state(self) -> str:
        """ Converts State to string

        Returns:
            str: Current state as a string
        """
        match self.__state:
            case States.DELETED:
                return "deleted"
            case States.READY:
                return "ready"
            case States.INPROGRESS:
                return "in_progress"
            case States.COMPLETED:
                return "completed"
            case _:
                raise ValueError("State outside bounds")
            
    @property
    def value(self) -> int:
        """ Converts state to int

        Raises:
            ValueError: Current state out of bounds somehow

        Returns:
            int: The state value
        """
        match self.__state:
            case States.DELETED:
                return -1
            case States.READY:
                return 0
            case States.INPROGRESS:
                return 1
            case States.COMPLETED:
                return 2
            case _:
                raise ValueError("State outside bounds")


class ServiceRequest:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, table: Table, subject: str, summary: str):
        self.__id = next(ServiceRequest.__id_iter)
        self.__table = table
        self.__subject = subject
        self.__summary = summary
        self.__timestamp = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        self.__status = State()
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
    def status(self) -> str:
        return self.__status.state
    
    @property
    def assignee(self) -> User:
        return self.__assignee
    
    def transition_state(self):
        self.__status.transition_state()

    def set_as_deleted(self):
        self.__status = State(-1)
    
    @table.setter
    def table(self, table: Table):
        self.__table = table

    @subject.setter
    def subject(self, subject: str):
        self.__subject = subject

    @summary.setter
    def summary(self, string: str):
        self.__summary = string

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
            "status": self.status,
            "assignee": f"{self.assignee.firstname} {self.assignee.lastname}" if self.assignee else None 
        }