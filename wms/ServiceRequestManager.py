from wms import ServiceRequest, Table

class ServiceRequestManager:
    def __init__(self):
        """ Constructor for the ServiceRequestManager class """
        self.__queue = []
        # Once a Service Request is removed from the queue it cannot be changed.
        self.__history = []

    @property
    def queue(self) -> list[ServiceRequest]:
        """ Gets the list of active service requests in the queue """
        return self.__queue
    
    @property
    def history(self) -> list[ServiceRequest]:
        """ Gets the list of all service requests including those that have been 
        archived """
        return self.__history
    
    def add_request(self, table: Table, subject: str, summary: str):
        """ Adds a request to the queue.

        Args:
            table (Table): The table at which the request originates
            subject (str): The subject field of the request
            summary (str): The summary field of the request
        """
        request_active = next((i for i in self.queue if i.table == table), None)
        
        if not request_active:
            self.queue.append(ServiceRequest(table, subject, summary))
            self.history.append(self.queue[-1])
        else:
            raise Exception("ServiceRequestManager: add_request(): A request is already active at this table")

    def get_request(self, id: int) -> ServiceRequest:
        """ Gets a request from the queue that matches the id.

        Args:
            id (int): The id to be searched for

        Returns:
            ServiceRequest: The service request with matching id.
        """
        return next((i for i in self.queue if i.id == id), None)
    
    def update_request(self, id: int, subject: str, summary: str):
        """ Updates a request with matching id, based on a provided subject or
        summary.

        Args:
            id (int): The id to be searched for
            subject (str): The subject to replace the current subject (Can be None)
            summary (str): The summary to replace the current summary (Can be None)

        Raises:
            ValueError: Raised if no request with id exists
        """
        sr = self.get_request(id)
        if sr:
            sr.subject = sr.subject if subject == None else subject
            sr.summary = sr.summary if summary == None else summary
        else:
            raise ValueError("ServiceRequestManager: update_request(): Invalid id")
    
    def remove_request(self, id: int):
        """ Removes a request with matching id from the queue. It will persist in
        the history.

        Args:
            id (int): The id of the request to be deleted
        """
        request = self.get_request(id)
        request.set_as_deleted()
        self.queue.remove(request)
    
    def transition_request_state(self, id: int):
        """ Moves the request that corresponds to id forward one state. If the
        state reaches "completed", the request is removed from the queue.

        Args:
            id (int): The id of the request to be advanced

        Raises:
            ValueError: Raised if the request is not in the queue either due to
            not existing or having been archived.
        """
        request = self.get_request(id)
        if not request:
            raise ValueError("ServiceRequestManager: transition_request_state(): Request does not exist or has been archived")
        
        request.transition_state()
        if request.status == "completed":
            self.queue.remove(request)

    def jsonify(self) -> dict:
        """ Returns a JSON-style dictionary object with all the service requests
        in the queue, sorted by timestamp.

        Returns:
            dict: The dictionary containing all service requests in queue
        """
        return {"queue": [i.jsonify() for i in 
                          sorted(self.queue, key = lambda x: x.timestamp)]}
    
    def jsonify_history(self) -> dict:
        """ Returns a JSON-style dictionary object with all the service requests
        in the request history, sorted by timestamp.

        Returns:
            dict: The dictionary containing all service requests in history
        """
        return {"requests": [i.jsonify() for i in
                             sorted(self.history, key = lambda x: x.timestamp)]}
    
    def get_staffmember_requests_json(self, id: int) -> dict:
        """ Returns a JSON-style dictionary object with all the service requests
        assigned to a user matching id, sorted by timestamp.

        Args:
            id (int): The id of the user whose assigned requests are being fetched

        Returns:
            dict: The dictionary containing all service requests of the user
            matching the id
        """
        return {"requests": [i.jsonify() for i in 
                             sorted([i for i in self.queue if i.assignee is not None and i.assignee.id == id],
                                     key= lambda x: x.timestamp, )]}
    
    def get_request_json(self, id: int) -> dict:
        """ Returns a JSON-style dictionary with all the relevant information
        pertaining to a single request matching the request id.

        Args:
            id (int): The id of the request to be returned

        Raises:
            ValueError: The request does not exist

        Returns:
            dict: The dictionary containing all the attribute info of the request
        """
        request = self.get_request(id)

        if not request:
            raise ValueError("ServiceRequestManager: get_request_json(): Request does not exist")
        
        return request.jsonify()
        