from __future__ import annotations
from difflib import SequenceMatcher as sm
from wms.DbHandler import Category as CategoryTable
from wms.DbHandler import Deal as DealTable
from wms.DbHandler import MenuItem as MenuTable


from wms import Category, MenuItem, Deal, DbHandler
from .PersonalisedDeal import PersonalisedDeal
from sqlalchemy.orm import Session
from sqlalchemy import delete, select

class Menu():

    def __init__(self, db: DbHandler, categories: list[Category] = None, deals: list[Deal] = None):
        """ Constructor for the Menu class

        Args:
            db (DbHandler): Database handler to ensure database persistence
            categories (list[Category], optional): Different menu categories. 
            Defaults to None.
            deals (list[Deal], optional): Different menu deals. 
            Defaults to None.
        """
        self.__db = db
        self.__categories = [] if categories is None else categories
        self.__deals = [] if deals is None else deals
 
    @property
    def db(self) -> DbHandler:
        """Returns db handler"""
        return self.__db
    
    @property
    def categories(self) -> list[Category]:
        """ Returns a list of categories """
        return self.__categories
    
    @categories.setter
    def categories(self, categories: list[Category]):
        """ Sets the categories of the menu """
        if not isinstance(categories, list[Category]):
            return ValueError("Menu: menu.set_categories(categories): argument is not a list of categories")
        self.__categories = categories
    
    @property
    def deals(self) -> list[Deal]:
        """ Returns a list of deals """
        return self.__deals
    
    def get_category(self, name: str) -> (Category | None):
        """ Returns a category with a matching name attribute

        Args:
            name (str): Name of the category 

        Returns:
            Category: Category to be acquired. If no category is found returns
            None
        """
        return next((it for it in self.categories if it.name == name), None)

    def add_category(self, category: Category):
        """ Adds a new category to the menu

        Args:
            category (Category): Category to be added to the menu

        Raises:
            TypeError: Raised if category argument is not of type category
            ValueError: Raised if category already exists in the menu
        """
        if not isinstance(category, Category):
            raise TypeError("Menu: add_category(): Object is not of type Category")
        
        if self.get_category(category.name) is not None:
            raise ValueError("Menu: add_category(): Category already exists")
        
        self.__categories.append(category)
        with Session(self.db.engine) as session:
            session.add(CategoryTable(id=category.id, name=category.name))
            try: 
                session.commit()
            except:
                session.rollback()


    def remove_category(self, name: str) -> (Category | None):
        """ Removes a category, if that category exists, from the menu.

        Args:
            name (str): Name of the category to be removed

        Raises:
            TypeError: Raised if name argument is not a string
            ValueError: Raised if category does not exist in the menu

        Returns:
            Category: Returns the removed category if found, None otherwise
        """
        if not isinstance(name, str):
            raise TypeError("Menu: menu.remove_category(): not a string")
        for i in self.categories:
            if i.name == name:
                self.__categories.remove(i)
                with Session(self.db.engine) as session:
                    session.execute(delete(CategoryTable).where(
                        CategoryTable.name == name)
                    )
                    try: 
                        session.commit()
                    except:
                        session.rollback()
                return i
        
        raise ValueError("Menu: menu.remove_category(): not in categories")
    
    def add_deal(self, deal: Deal, menu_items: list[str]) -> None:
        """ Adds a new deal to the menu

        Args:
            deal (Deal): Deal to be added to the menu
            menu_items (list[str]): List of menu items that the deal applies to

        Raises:
            TypeError: Raised if deal object is not of type Deal
            ValueError: Raised if deal already exists in the menu
        """
        if not isinstance(deal, Deal):
            raise TypeError("Menu: add_deal(): Object is not of type Deal")
        
        if deal in self.__deals:
            raise ValueError("Menu: add_deal(): Deal already exists")
        self.__deals.append(deal)
        with Session(self.db.engine) as session:
            res = session.scalars(select(MenuTable).filter(MenuTable.name.in_(menu_items)))
            if session.get(DealTable, deal.id) is None:
                session.add(DealTable(
                    id=deal.id,
                    discount = deal.discount,
                    menu_items = res.fetchall(),
                    orders = []
                ))
            try: 
                session.commit()
            except:
                session.rollback()

    
    def remove_deal(self, deal: Deal) -> Deal:
        """ Removes a deal from the menu.

        Args:
            deal (Deal): Deal to be removed from the menu

        Raises:
            TypeError: Raised if deal object is not of type Deal
            ValueError: Raised if deal does not exist in the menu

        Returns:
            Deal: Returns removed deal if found
        """
        if not isinstance(deal, Deal):
            raise TypeError("Menu: menu.remove_deal(): Object is not of type Deal")
        
        if deal not in self.__deals:
            raise ValueError("Menu: menu.remove_deal(): not in deals")
        
        self.__deals.remove(deal)
        with Session(self.db.engine) as session:
            session.execute(delete(DealTable).where(
                DealTable.id == deal.id)
            )
            try: 
                session.commit()
            except:
                session.rollback()
        return deal
    
    def user_has_personalised(self, user: str) -> bool:
        """ A check for if a personalised deal applies to a particular user. 
        Also removes any expired personalised deals for that user.

        Args:
            user (str): ID string of the user

        Returns:
            bool: Returns true if a personalised deal was found, false otherwise
        """
        for i in self.deals:
            if isinstance(i, PersonalisedDeal):
                if i.user == user and i.is_expired():
                    self.remove_deal(i)

        for i in self.deals:
            if isinstance(i, PersonalisedDeal):
                if i.user == user and i.visible:
                    return True
                
        return False
    
    def menu_items(self) -> list[MenuItem]:
        """ Returns a list of menu items

        Returns:
            list[MenuItem]: List of menu items in menu
        """
        output = []
        for i in self.categories:
            output += i.menu_items
        return output
    
    def menu_item_lookup(self, id: int) -> (MenuItem | None):
        """ Performs a look up through the menu's menu items

        Args:
            id (int): ID of menu item to be searched for

        Returns:
            MenuItem: Menu item to be searched for if found. Returns None if 
            menu item cannot be found.
        """
        for i in self.menu_items():
            if i.id == id:
                return i
        return None
    
    def update_categories(self, new_order: list[str]):
        """ Updates the order of the categories given a list of category IDs

        Args:
            new_order (list[str]): List of category IDs that represent the 
            new order of categories in the menu

        Raises:
            TypeError: Raised if new_order argument is not a list of strings
            ValueError: Raised if IDs in new_order are not unique or new_order
            does not have the right number of ID strings or it contains an ID
            that does not correspond to a valid category ID
        """
        if not isinstance(new_order, list):
            raise TypeError("Menu: update_categories(): Object should be a list of strings")
        
        if len(new_order) != len(self.__categories):
            raise ValueError("Menu: update_categories(): Wrong number of list IDs provided")

        if len(new_order) > len(set(new_order)):
            raise ValueError("Menu: update_categories(): IDs in list are not unique")
        
        curr_category_ids = [i.id for i in self.__categories]
        new_categories = []

        for id in new_order:
            try:
                id_index = curr_category_ids.index(int(id))
                new_categories.append(self.__categories[id_index])
            except ValueError:
                raise ValueError(f"Menu: update_categories(): ID {id} is not a valid category ID")

        self.__categories = new_categories
        
    def search_items(self, query: str) -> dict:
        """ Searches the menu for menu_items that match a provided query

        Args:
            query (str): The name, or a close replicate, of the menu_item you're searching for

        Returns:
            dict: A dictionary similar to self.categories except with irrelevant menu_items omitted

        Note: 
            This function is only so needlessly complex because of how the menu items are stored,
            and also the desire to preserve category. We therefore conduct a number of reads of the 
            menu without forgetting where they are in the menu, adding complexity and reducing efficiency.
        """
        # The harshness of the similarity. 1.0 is max value and will only return 
        # exact matches. 0 returns everything. 0.5 is a pretty good midpoint
        STRENGTH_COEFFICIENT = 0.40
        # Generate levenschtein distances for each menu item in all categories against the query argument
        levenschtein = [[sm(None, j.name, query).ratio() 
                         for j in i.menu_items if j.visible == True] 
                         for i in self.categories if i.visible == True]

        # Get the normal dictionary of menu_items in self.categories
        normal = [[j 
                   for j in i.menu_items if j.visible == True] 
                   for i in self.categories if i.visible == True]
        # Sort the normal list by the levenschtein one, zipping them together and removing bad matches
        sorted_by_levenschtein = [
            sorted(
            list(zip(
                    (i for i in levenschtein[k]), 
                    (j.jsonify() for j in normal[k]))), 
                    key = lambda x: x[0], reverse=True) 
                    for k, _ in enumerate(normal)
        ]
        # Remove values with low ratios
        cropped_output = [[i 
                           for i in sublist if i[0] > STRENGTH_COEFFICIENT]
                           for sublist in sorted_by_levenschtein]

        # Add the categories back in and remove the levenschtein value from the output
        with_categories = {category.name: [i[1] for i in cropped_output[k]] 
                           for k, category in enumerate(i for i in self.categories if i.visible == True)}
        
        # Clean up the data and return. Automatically omits empty categories
        return {key: with_categories[key] 
                for key in with_categories.keys() if with_categories[key]}
    
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the categories and deals of the 
        menu

        Returns:
            dict: Dictionary containing the categories and deals of the menu
        """
        return {
            'categories': [i.jsonify() for i in self.categories], 
            'deals': [i.jsonify() for i in self.deals]
        }

        
