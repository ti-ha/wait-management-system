from __future__ import annotations
from wms import MenuItem
import itertools
from sqlalchemy import engine, Table, MetaData, Column, Integer, Double, String, ForeignKey, text
from sqlalchemy.orm import Session


class Category():

    __id_iter = itertools.count()

    def __init__(self, db_engine, name, menu_items=None):
        """ Constructor (no menu items by default)

        Args:
            name (String): Name of the category
            menu_items (List[MenuItem], optional): List of menu items to be 
            predefined with the new category. Defaults to None.
        """
        self.__id = next(Category.__id_iter)
        self.__name = name
        self.__menu_items = [] if menu_items is None else menu_items
        self.__visible = True
        self.__db_engine = db_engine

    @property
    def id(self) -> int:
        """ Returns id """
        return self.__id
    
    @property
    def name(self) -> str:
        """ Returns name """
        return self.__name
    
    @name.setter
    def name(self, name):
        """ Sets the category name """
        if not isinstance(name, str):
            raise TypeError("Category: category.set_name(name): argument is not string")
        self.__name = name

    @property
    def menu_items(self) -> list[MenuItem]:
        """ Returns a list of menu items """
        return self.__menu_items
    
    @property
    def visible(self) -> bool: 
        """ Returns category visiblity """
        return self.__visible

    @visible.setter
    def visible(self, visible):
        """ Sets the category visiblity as well as its menu items """
        self.__visible = visible
        for item in self.menu_items:
            item.visible = visible

    def update(self, name, visible):
        """ Updates the name and/or visibility of the category

        Args:
            name (String): Name of the category
            visible (String): Visibility of the category
        """
        if name is not None: self.name = name 
        if visible is not None: self.visible = (visible == "True")

    def update_menu_items(self, new_order):
        """ Updates the order of the menu items given a list of menu item IDs

        Args:
            new_order (List[String]): List of menu item IDs that represent the 
            new order of menu items in the category

        Raises:
            TypeError: Raised if new_order argument is not a list of strings
            ValueError: Raised if IDs in new_order are not unique or new_order
            does not have the right number of ID strings or it contains an ID
            that does not correspond to a valid menu item ID
        """
        if not isinstance(new_order, list):
            raise TypeError("Category: update_menu_items(): Object should be a list of strings")
        
        if len(set(new_order)) != len(self.__menu_items):
            raise ValueError("Category: update_menu_items(): Wrong number of list IDs provided")
        
        if len(new_order) > len(set(new_order)):
            raise ValueError("Category: update_menu_items(): IDs in list are not unique")
        
        curr_menu_item_ids = [i.id for i in self.__menu_items]
        new_menu_items = []

        for id in new_order:
            try:
                id_index = curr_menu_item_ids.index(int(id))
                new_menu_items.append(self.__menu_items[id_index])
            except ValueError:
                raise ValueError(f"Category: update_menu_items(): ID {id} is not a valid menu item ID")

        self.__menu_items = new_menu_items

    def menu_item(self, menu_item) -> (MenuItem | None):
        """ Returns a specific menu item from category

        Args:
            menu_item (MenuItem): Menu item to be searched for

        Returns:
            MenuItem: The specific menu item from the category. None if no menu 
            item exists
        """
        # for i in self.__menu_items:
        #     if i.is_equal(menu_item):
        #         return i
        # return None
        return next((it for it in self.menu_items if it.is_equal(menu_item)), None)

    def menu_item_by_name(self, name) -> (MenuItem | None):
        """ Returns menu item by name

        Args:
            name (str): name of item

        Returns:
            MenuItem if present, else None 
        """
        return next((it for it in self.menu_items if it.name == name), None)

    def add_menu_item(self, menu_item: MenuItem) -> None:
        """ Adds a menu_item to the category

        Args:
            menu_item (Menu_Item): Menu item to be added to the category

        Raises:
            ValueError: Raised if menu item is already in the category
        """
        if self.menu_item_by_name(menu_item.name) is not None:
            raise ValueError("Category: add_menu_item(): MenuItem already in category")
        
        self.menu_items.append(menu_item)
        self.add_to_db(menu_item)

    def add_to_db(self, menu_item: MenuItem):
        add_menu_item = text(
            f"""INSERT INTO menu_item (_id, _name, _price, _category, _image_url) 
            VALUES ({menu_item.id}, '{menu_item.name}', {menu_item.price}, {self.id}, '{menu_item.image_url}')"""
        )

        with Session(self.__db_engine) as session:
            session.execute(add_menu_item)
            session.commit()

    def remove_menu_item(self, name) -> int:
        """ Removes a menu_item from the category

        Args:
            menu_item (MenuItem): Menu item to be removed from the category

        Raises:
            ValueError: Raised if menu item does not exist in the category

        Returns:
            Integer: Id of the menu item that was removed
        """
        removed_item = self.menu_item_by_name(name)
        if removed_item is None:
            raise ValueError("Category: category.remove_menu_item(): not an existing menu item")
        
        self.menu_items.remove(removed_item)
        self.remove_from_db(name)

        return removed_item.id
        
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id, name and list of menu items 
        of the category

        Returns:
            dict: Dictionary containing the id, name and list of menu items 
        of the category
        """

        return {
            "id": self.id, 
            "name": self.name, 
            "menu_items": [it.jsonify() for it in self.menu_items],
            "visible": self.visible
        }
    