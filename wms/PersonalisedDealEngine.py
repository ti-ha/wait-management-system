from wms import OrderManagerHandler, UserHandler,  MenuHandler
from .PersonalisedDeal import PersonalisedDeal
import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans
import warnings
from random import choice
from contextlib import redirect_stdout
from io import StringIO


# A user-controlled variable to allow the user to control how many deals get
# returned to the user.
MAX_DEALS = 3

# Discounts are not determined algorithmically so you have to set bounds for
# this yourself. The reason being that it is completely arbitrary and up to the
# store to decide how much of a discount they wish to offer.
MIN_DISCOUNT = 0.1
MAX_DISCOUNT = 0.3

class PersonalisedDealEngine():
    '''
    A class for generating personalised deals for the user using item-based
    collaborative filtering. Gets better the more the system is used.
    '''

    def __init__(self, user_handler: UserHandler, order_manager_handler: OrderManagerHandler):
        """ Constructor for the PersonalisedDealEngine Class. Class loads the 
        data initially on creation

        Args:
            user_handler (UserHandler): UserHandler object utilised with the engine
            order_manager_handler (OrderManagerHandler): OrderManagerHandler object 
            utilised with the engine
        """
        self.__user_handler = user_handler
        self.__order_manager_handler = order_manager_handler
        self.__data = self.load_data()
        self.__algorithm = None
        self.gen_algorithm()

    @property
    def user_handler(self) -> UserHandler:
        """ Returns the user_handler of the application """
        return self.__user_handler
    
    @property
    def order_manager_handler(self) -> OrderManagerHandler:
        """ Returns the OrderManagerHandler of the application """
        return self.__order_manager_handler
    
    @property
    def menu_handler(self) -> MenuHandler:
        """ Returns the MenuHandler of the application """
        return self.order_manager_handler.menu_handler
    
    @property
    def data(self) -> dict:
        """ Returns the data generated in load_data() """
        return self.__data
    
    @data.setter
    def data(self, data: dict):
        """ Setter for the trainset data """
        self.__data = data

    @property
    def algorithm(self) -> KNNWithMeans:
        """ Gets the algorithm used for personalised deals """
        return self.__algorithm
    
    @algorithm.setter
    def algorithm(self, algo: KNNWithMeans):
        """ Sets the algorithm used for personalised deals """
        self.__algorithm = algo
    
    def reload_data(self):
        """ Reloads the data so the algorithm has the most recent data. Try to
        minimise the number of calls to this, as the data generation algorithm
        is pretty slow as it scrapes all of the order history to generate """
        self.data = self.load_data()
        self.gen_algorithm()
    
    def load_data(self) -> dict:
        """ Generates the dataset to be used by the collaborative filtering algorithm

        Returns:
            dict: The dictionary containing all the data
        """
        ratings_dict = {
            "item": [],
            "user": [],
            "rating": []
        }

        # Generate data structure for counting menu_items by frequency in order
        user_frequencies = {}
        for order in self.order_manager_handler.order_manager.history:
            if order.customer not in user_frequencies.keys():
                user_frequencies[order.customer] = { menu_item.id: 1 
                                                    for menu_item in order.menu_items 
                                                    if menu_item.visible }
            else:
                for menu_item in order.menu_items:
                    if menu_item.visible:
                        user_frequencies[order.customer][menu_item.id] += 1

        # flatten user_frequencies into three arrays for the surprise library
        for user in user_frequencies.keys():
            for item in user_frequencies[user].keys():
                ratings_dict["item"].append(item)
                ratings_dict["user"].append(user)
                ratings_dict["rating"].append(user_frequencies[user][item])

        # Normalise the ratings between 0 and 5
        ratings_dict["rating"] = [(i/max(ratings_dict["rating"])*5) for i in ratings_dict["rating"]]

        return ratings_dict
    
    def dataset(self) -> Dataset:
        """ Creates a Pandas Dataset for use with the Surprise library

        Returns:
            DatasetAutoFolds: The Pandas dataset
        """
        dataframe = pd.DataFrame(self.data)
        reader = Reader(rating_scale=(0,5))
        data = Dataset.load_from_df(dataframe[["user", "item", "rating"]], reader)

        return data
    
    def gen_algorithm(self) -> KNNWithMeans:
        """ Initialises the algorithm

        Returns:
            KNNWithMeans: The Algorithm, from the Surprise library, that takes
            in a Dataset to be trained with
        """

        # Options for the algorithm if you ever want to change them
        options = {
            "name": "cosine",
            "user_based": False
        }

        # We redirect stdout because algo.fit() generates some unavoidable
        # output which provides absolutely zero benefit to anyone
        with redirect_stdout(StringIO()):
            algo = KNNWithMeans(sim_options=options)
            training_set = self.dataset().build_full_trainset()

            algo.fit(training_set)
            self.algorithm = algo
    
    def generate_prediction(self, user: str, id: int) -> int:
        """ Generate a prediction for a user of their rating of an item with id <id>

        Args:
            user (str): The user whose prediction is to be generated
            id (int): The id of the item whose rating is being predicted

        Returns:
            int: The estimate from the prediction
        """

        # Wrapper to catch warnings, as predict() can raise some warnings if it
        # has never been ordered before. Functionally, if this happens we just want
        # it to give a rating of 0 cause nobody must like that item. This way,
        # if there are no orders in the system all ratings are predicted as 0
        # and the user gets random personalised deals, which fixes the cold
        # start problem
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            prediction = self.algorithm.predict(user, id)
            if w and issubclass(w[0].category, RuntimeWarning):
                return 0
        
        return prediction.est
    
    def generate_top_predictions(self, user: str, coeff: int) -> list[int]:
        """ Generates the top menu item predictions for a user.

        Args:
            user (string): The id of the user whose predictions are being generated
            coeff (int): This number is passed in from another function and
            facilitates the possiblity of less than MAX_DEALS predictions
            needing to be made

        Returns:
            list[int]: A list of menu item ids 
        """
        self.reload_data()

        # sort by top n
        if len(self.menu_handler.menu.menu_items()) >= MAX_DEALS:
            n = MAX_DEALS - coeff
        else:
            n = len(self.menu_handler.menu.menu_items()) - coeff

        if n == 0: return []

        # Generates predictions, sorts them by most relevant, then crops the
        # data to n values
        predictions = sorted([(i.id, self.generate_prediction(user, i.id)) 
                       for i in self.menu_handler.menu.menu_items() if i.visible], 
                       reverse=True,
                       key = lambda x: x[1])[:n]
        
        return predictions
    
    def make_deals(self, user: str) -> list[dict]:
        """ Parses the output from generate_predictions, performing necessary
        checks for item visibility and whether the user already has valid deals.
        Adds the generated deals to the system if all goes well so they can be
        added from the relevant menu endpoints. This method is called directly
        by the API and is the entrypoint of the class

        Args:
            user (str): The id of the user whose personalised deals are being added

        Returns:
            list[dict]: The list of jsonified personalised deals of the user. 
        """

        # Check if the user already has personalised deals, making a list out of them
        if self.menu_handler.menu.user_has_personalised(user):
            preexisting = [i for i in self.menu_handler.menu.deals 
                           if isinstance(i, PersonalisedDeal) and i.user == user]
        else:
            preexisting = []

        # If the preexisting menu_items exactly match the visible menu items,
        # return the preexisting list
        if len(preexisting) == len([i for i in self.menu_handler.menu.menu_items() if i.visible]):
            return [i.jsonify() for i in preexisting if i.visible]


        # Otherwise, generate new ones to fill the gaps
        deals = [
            PersonalisedDeal(
                choice(range(int(MIN_DISCOUNT*100), int(MAX_DISCOUNT*100), 5))/100,
                self.menu_handler.menu.menu_item_lookup(i[0]),
                user
                )
                for i in self.generate_top_predictions(user, len(preexisting))
        ]

        # Add the new deals to the menu
        for i in deals:
            self.menu_handler.menu.add_deal(i)

        # Combine the two lists
        deals += preexisting

        # Return the jsonified list
        return [i.jsonify() for i in deals if i.visible]
    







