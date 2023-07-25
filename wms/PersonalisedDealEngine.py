from wms import OrderManagerHandler, UserHandler,  MenuHandler
from .PersonalisedDeal import PersonalisedDeal
import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans
import warnings
from random import choice


# A user-controlled variable to allow the user to control how many deals get
# returned to the user.
MAX_DEALS = 3

# Discounts are not determined algorithmically so you have to set bounds for
# this yourself. The reason being that it is completely arbitrary and up to the
# store to decide how much of a discount they wish to offer.
MIN_DISCOUNT = 0.1
MAX_DISCOUNT = 0.3

class PersonalisedDealEngine():

    def __init__(self, user_handler, order_manager_handler):
        self.__user_handler = user_handler
        self.__order_manager_handler = order_manager_handler
        self.__data = self.load_data()

    @property
    def user_handler(self) -> UserHandler:
        return self.__user_handler
    
    @property
    def order_manager_handler(self) -> OrderManagerHandler:
        return self.__order_manager_handler
    
    @property
    def menu_handler(self) -> MenuHandler:
        return self.order_manager_handler.menu_handler
    
    @property
    def data(self) -> dict:
        return self.__data
    
    @data.setter
    def data(self, data: dict):
        self.__data = data
    
    def reload_data(self):
        self.data = self.load_data()
    
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
        dataframe = pd.DataFrame(self.data)
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

        # This function prints a thing because of the library being used. I have
        # tried EVERYTHING to stop it from printing but I can't. We just have to
        # live with the consequences. It's someone else's bug, the arg for
        # turning it off just doesn't work.
        training_set = self.dataset().build_full_trainset()
        algorithm = self.algorithm()

        algorithm.fit(training_set)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            prediction = algorithm.predict(user, id)
            if w and issubclass(w[0].category, RuntimeWarning):
                return 0
        
        return prediction.est
    
    def generate_top_predictions(self, user):
        # make sure the data is up to date
        self.reload_data()

        # sort by top N
        if len(self.menu_handler.menu.menu_items()) >= MAX_DEALS + 1:
            n = MAX_DEALS
        else:
            n = len(self.menu_handler.menu.menu_items()) + 1

        predictions = sorted([(i.id, self.generate_prediction(user, i.id)) 
                       for i in self.menu_handler.menu.menu_items()], 
                       reverse=True,
                       key = lambda x: x[1])[:n]
        
        return predictions
    
    def make_deals(self, user):
        if self.menu_handler.menu.user_has_personalised(user):
            return [i.jsonify() for i in self.menu_handler.menu.deals 
                    if isinstance(i, PersonalisedDeal) and i.user == user]

        deals = [
            PersonalisedDeal(
                choice(range(int(MIN_DISCOUNT*100), int(MAX_DISCOUNT*100), 5))/100,
                self.menu_handler.menu.menu_item_lookup(i[0]),
                user
                )
                for i in self.generate_top_predictions(user)
        ]

        for i in deals:
            self.menu_handler.menu.add_deal(i)

        return [i.jsonify() for i in deals]
    







