from wms import RestaurantManager

class RestaurantManagerHandler():
    def __init__(self, restaurant_manager, menu_handler):
        self.__rm = restaurant_manager
        self.__menu_handler = menu_handler