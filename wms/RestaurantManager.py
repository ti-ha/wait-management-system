from wms import Menu

class RestaurantManager:
    def __init__(self):
        """ Constructor for the RestaurantManager Class """
        self.__statistics = {}

    @property
    def statistics(self) -> dict:
        """ Returns statistics list """
        return self.__statistics

    def add_menu_item(self, menu_item: str):
        if menu_item not in self.statistics:
            self.statistics[menu_item] = 0
        else:
            raise ValueError("RestaurantManager: add_menu_item(): Menu Item is already in the statistics")
        
    def increase_count(self, menu_items: list[str]):
        for item in menu_items:
            if item not in self.statistics:
                raise ValueError("RestaurantManager: increase_count(): Menu Item is not in the statistics")
            self.statistics[item] += 1

    def jsonify(self) -> dict:
        return dict(sorted(self.statistics.items(), key=lambda item:item[1], reverse=True))