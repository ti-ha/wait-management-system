import itertools

class ServiceRequest:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, table, summary):
        self.__id = next(ServiceRequest.__id_iter)
        self.__table = table
        self.__summary = summary
    