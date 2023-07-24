from wms import OrderManagerHandler, UserHandler,  MenuHandler
import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans

class PersonalisedDealEngine():
    def __init__(self, user_handler, order_manager_handler):
        self.__user_handler = user_handler
        self.__order_manager_handler = order_manager_handler

    @property
    def user_handler(self) -> UserHandler:
        return self.__user_handler
    
    @property
    def order_manager_handler(self) -> OrderManagerHandler:
        return self.__order_manager_handler
    
    @property
    def menu_handler(self) -> MenuHandler:
        return self.order_manager_handler.menu_handler
    
    def load_data(self):
        ratings_dict = {
            "item": [],
            "user": [],
            "rating": []
        }


        # Generate the unique list of all users in the system currently
        users = []
        for order in self.order_manager_handler.order_manager.history:
            if order.customer not in users:
                users.append(order.customer)
        
        # Generate a list of how many times each user has ordered each menu_item
        user_frequencies = { user: {} for user in users }
        for user in users:
            for order in self.order_manager_handler.order_manager.history:
                if order.customer == user:
                    for menu_item in order.menu_items:
                        if menu_item.id not in user_frequencies[user].keys():
                            user_frequencies[user][menu_item.id] = 1
                        else:
                            user_frequencies[user][menu_item.id] += 1

        # flatten user_frequencies into three arrays for the surprise library
        for user in user_frequencies.keys():
            for item in user_frequencies[user].keys():
                ratings_dict["item"].append(item)
                ratings_dict["user"].append(user)
                ratings_dict["rating"].append(user_frequencies[user][item])

        # Normalise the ratings between 0 and 5
        ratings_dict["rating"] = [(i/max(ratings_dict["rating"])*5) for i in ratings_dict["rating"]]

        return ratings_dict
    
    def dataset(self):
        # creates a Panda dataframe from the data in load_data()
        dataframe = pd.DataFrame(self.load_data())
        reader = Reader(rating_scale=(0,5))
        data = Dataset.load_from_df(dataframe[["user", "item", "rating"]], reader)

        return data
    
    def algorithm(self) -> KNNWithMeans:
        # Initialises the algorithm
        options = {
            "name": "cosine",
            "user_based": False
        }

        algo = KNNWithMeans(sim_options=options)
        return algo
    
    def generate_prediction(self, user, id):
        # Feeds the dataset into the algorithm
        training_set = self.dataset().build_full_trainset()
        algorithm = self.algorithm()

        algorithm.fit(training_set)
        prediction = algorithm.predict(user, id)
        
        return prediction.est




