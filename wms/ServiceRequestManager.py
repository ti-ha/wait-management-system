from wms import ServiceRequest

class ServiceRequestManager:
    def __init__(self):
        self.__queue = []
        # Once a Service Request is removed from the queue it cannot be changed.
        self.__history = []

    @property
    def queue(self) -> list[ServiceRequest]:
        return self.__queue
    
    @property
    def history(self) -> list[ServiceRequest]:
        return self.__history
    
    def add_request(self, table, subject, summary):
        self.queue.append(ServiceRequest(table, subject, summary))
        self.history.append(self.queue[-1])

    def get_request(self, id) -> ServiceRequest:
        return next((i for i in self.queue if i.id == id), None)
    
    def update_request(self, id, subject, summary):
        sr = self.get_request(id)
        if sr:
            sr.subject = sr.subject if subject == None else subject
            sr.summary = sr.summary if summary == None else summary
        else:
            raise ValueError("ServiceRequestManager: update_request(): Invalid id")
    
    def remove_request(self, id):
        request = self.get_request(id)
        request.set_as_deleted()
        self.queue.remove(request)
    
    def transition_request_state(self, id):
        request = self.get_request(id)
        if not request:
            raise ValueError("ServiceRequestManager: transition_request_state(): Request does not exist or has been archived")
        
        request.transition_state()
        if request.status == "completed":
            self.queue.remove(request)

    def jsonify(self):
        return {"queue": [i.jsonify() for i in 
                          sorted(self.queue, key = lambda x: x.timestamp)]}
    
    def jsonify_history(self):
        return {"requests": [i.jsonify() for i in
                             sorted(self.history, key = lambda x: x.timestamp)]}
    
    def get_staffmember_requests_json(self, id):
        return {"requests": [i.jsonify() for i in 
                             sorted([i for i in self.queue if i.assignee is not None and i.assignee.id == id],
                                     key= lambda x: x.timestamp, )]}
    
    def get_request_json(self, id):
        request = self.get_request(id)

        if not request:
            raise ValueError("ServiceRequestManager: get_request_json(): Request does not exist")
        
        return request.jsonify()
        