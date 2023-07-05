from wms import ServiceRequestManager

# SRM stands for "Service Request Manager"
class SRMHandler():
    def __init__(self, service_request_manager) -> None:
        self.__srm = service_request_manager