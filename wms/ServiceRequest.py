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
        if self.__state   == States.DELETED:
            return "deleted"
        elif self.__state == States.READY: 
            return "ready"
        elif self.__state == States.INPROGRESS:
            return "in_progress"
        elif self.__state == States.COMPLETED:
            return "completed"
        else:
            raise ValueError("State outside bounds")
            
    @property
    def value(self) -> int:
        """ Converts state to int

        Raises:
            ValueError: Current state out of bounds somehow

        Returns:
            int: The state value
        """
        if self.__state   == States.DELETED:
            return -1
        elif self.__state == States.READY: 
            return 0
        elif self.__state == States.INPROGRESS:
            return 1
        elif self.__state == States.COMPLETED:
            return 2
        else:
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
        """ The id of the service request."""
        return self.__id
    
    @property
    def table(self):
        """ The table at which the service request is being called from.  """
        return self.__table
    
    @property
    def subject(self):
        """ The subject field of the service request. """
        return self.__subject
    
    @property
    def summary(self):
        """ The summary field of the service request. """
        return self.__summary
    
    @property
    def timestamp(self):
        """ The time when the service request was created. """
        return self.__timestamp
    
    @property
    def status(self) -> str:
        """ The status of the service request. """
        return self.__status.state
    
    @property
    def assignee(self) -> User:
        """ The WaitStaff assigned to the request. Defaults to None. """
        return self.__assignee
    
    @property
    def assignee_id(self) -> int:
        """ WaitStaff id if exist, else None """
        return self.assignee.id if self.assignee is not None else None
    
    def transition_state(self):
        """ Move the state of the order one pace forward. """
        self.__status.transition_state()

    def set_as_deleted(self):
        """ Marks the request as deleted. """
        self.__status = State(-1)
    
    @table.setter
    def table(self, table: Table):
        """ Sets the table of the request. """
        self.__table = table

    @subject.setter
    def subject(self, subject: str):
        """ Sets the subject of the request. """
        self.__subject = subject

    @summary.setter
    def summary(self, string: str):
        """ Sets the summary of the request. """
        self.__summary = string

    @assignee.setter
    def assignee(self, assignee: User):
        """ Sets the assignee of the request. """
        self.__assignee = assignee

    def jsonify(self):
        """Generates a JSON-style dictionary containing all the relevant
        attributes of the Service Request.

        Returns:
            dict: the JSON-style object containing all attribute info
        """
        return {
            "id": self.id,
            "table": self.table.id,
            "summary": self.summary,
            "subject": self.subject,
            "timestamp": self.timestamp,
            "status": self.status,
            "assignee": f"{self.assignee.firstname} {self.assignee.lastname}" if self.assignee else None 
        }