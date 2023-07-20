from wms import ServiceRequest

class ServiceRequestManager:
    def __init__(self):
        self.__queue = []

    @property
    def queue(self) -> list[ServiceRequest]:
        return self.__queue
    
    def add_request(self, table, summary):
        self.queue.append(ServiceRequest(table, summary))

    def get_request(self, id) -> ServiceRequest:
        return next((i for i in self.queue if i.id == id), None)
    
    def remove_request(self, id):
        request = self.get_request(id)
        self.queue.remove(request)

    def jsonify(self):
        return {"queue": [i.jsonify() for i in self.queue]}