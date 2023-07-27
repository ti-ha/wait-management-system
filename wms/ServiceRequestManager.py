from wms import ServiceRequest

class ServiceRequestManager:
    def __init__(self):
        self.__queue = []
        # Once a Service Request is removed from the queue it cannot be changed.
        self.__history = []

    @property
    def queue(self) -> list[ServiceRequest]:
        """ The list of active service requests in the queue.

        Returns:
            list[ServiceRequest]: List of service requests
        """
        return self.__queue
    
    @property
    def history(self) -> list[ServiceRequest]:
        """ The list of all service requests including those that have been archived.

        Returns:
            list[ServiceRequest]: List of service requests
        """
        return self.__history
    
    def add_request(self, table, subject, summary):
        """Adds a request to the queue.

        Args:
            table (Table): The table at which the request originates
            subject (string): The subject field of the request
            summary (string): The summary field of the request
        """
        request_active = next((i for i in self.queue if i.table == table), None)
        
        if not request_active:
            self.queue.append(ServiceRequest(table, subject, summary))
            self.history.append(self.queue[-1])
        else:
            raise Exception("ServiceRequestManager: add_request(): A request is already active at this table")

    def get_request(self, id) -> ServiceRequest:
        """Gets a request from the queue that matches the id.

        Args:
            id (int): The id to be searched for

        Returns:
            ServiceRequest: The service request with matching id.
        """
        return next((i for i in self.queue if i.id == id), None)
    
    def update_request(self, id, subject, summary):
        """Updates a request with matching id, based on a provided subject or
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
    
    def remove_request(self, id):
        """Removes a request with matching id from the queue. It will persist in
        the history.

        Args:
            id (int): The id of the request to be deleted
        """
        request = self.get_request(id)
        request.set_as_deleted()
        self.queue.remove(request)
    
    def transition_request_state(self, id):
        """Moves the request that corresponds to id forward one state. If the
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

    def jsonify(self):
        """ Returns a JSON-style dictionary object with all the service requests
        in the queue, sorted by timestamp.

        Returns:
            dict: The dictionary containing all service requests in queue
        """
        return {"queue": [i.jsonify() for i in 
                          sorted(self.queue, key = lambda x: x.timestamp)]}
    
    def jsonify_history(self):
        """ Returns a JSON-style dictionary object with all the service requests
        in the request history, sorted by timestamp.

        Returns:
            dict: The dictionary containing all service requests in history
        """
        return {"requests": [i.jsonify() for i in
                             sorted(self.history, key = lambda x: x.timestamp)]}
    
    def get_staffmember_requests_json(self, id):
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
    
    def get_request_json(self, id):
        """Returns a JSON-style dictionary with all the relevant information
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
        