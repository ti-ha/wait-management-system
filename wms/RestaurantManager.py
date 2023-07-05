from .Menu import Menu

class RestaurantManager:
    def __init__(self, menuhandler):
        self.__menuhandler = menuhandler
        self.__statistics = []