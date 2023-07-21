from wms import ServiceRequestManager, UserHandler, WaitStaff

# SRM stands for "Service Request Manager"
class SRMHandler():
    def __init__(self, service_request_manager: ServiceRequestManager, user_handler: UserHandler) -> None:
        """ Constructor for the SRMHandler Class """
        self.__srm = service_request_manager
        self.__user_handler = user_handler

    @property
    def srm(self) -> ServiceRequestManager:
        return self.__srm
    
    @property
    def user_handler(self) -> UserHandler:
        return self.__user_handler
    
    def id_to_waitstaff(self, user_id) -> WaitStaff:
        user = self.user_handler.id_to_user(user_id)
        return user if user.__class__ == WaitStaff else None
    
    def assign_request_to_user(self, request_id, user_id):
        request = self.srm.get_request(request_id)
        if not request:
            raise ValueError("SRMHandler: assign_request_to_user: No request found")
        
        if request.assignee is not None:
            raise ValueError("SRMHandler: assign_request_to_user(): Someone else is already managing that request")
        
        assignee = self.id_to_waitstaff(user_id)
        if not assignee:
            raise ValueError("SRMHandler: assign_request_to_user(): No waitstaff found")
        
        assignee.assign_requests(request)
        request.assignee = assignee

    def unassign_request_from_user(self, request_id, user_id):
        request = self.srm.get_request(request_id)
        if not request:
            raise ValueError("SRMHandler: unassign_request_from_user: No request found")
        
        if request.assignee is None:
            raise ValueError("SRMHandler: unassign_request_from_user(): That is not your request")
        
        assignee = self.id_to_waitstaff(user_id)
        if not assignee:
            raise ValueError("SRMHandler: unassign_request_from_user(): No waitstaff found")
        
        assignee.remove_requests(request)
        request.assignee = None

    def get_requests_of_user(self, user_id):
        assignee = self.id_to_waitstaff(user_id)
        if not assignee:
            raise ValueError("SRMHandler: get_requests_of_user(): No waitstaff found")
        
        return self.srm.get_staffmember_requests_json(user_id)

        

    def jsonify(self):
        return self.srm.jsonify()