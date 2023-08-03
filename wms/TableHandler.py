from .Table import Table
from .Customer import Customer
from .Order import Order

class TableHandler():
    def __init__(self):
        """ Constructor for the TableHandler Class """
        self.__tables = []

    @property
    def tables(self) -> list[Table]:
        """ Returns the list of tables """
        return self.__tables
    
    def add_table(self, table_limit: int, orders: list[Order]):
        """ Adds a table to the restaurant

        Args:
            table_limit (int): Maximum number of customers at the table
            orders (list[Order]): Orders to be predefined with the table 
        """
        table = Table(table_limit, orders)
        self.__tables.append(table)
    
    def add_customer(self, table_id: int, customer: Customer) -> bool:
        """ Adds a customer to the table

        Args:
            table_id (int): ID of the table that customer is being added to
            customer (Customer): Customer to be added to the table
        """
        table = self.id_to_table(table_id)
        table.add_customers(customer)

    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id, availability string, table
        limit and occupied boolean of the table  

        Returns:
            dict: A dictionary containing the id, availability string, table
        limit and occupied boolean of the table  
        """
        return {"tables": [table.jsonify() for table in self.tables]}

    def id_to_table(self, id: int) -> Table:
        """ Converts a given id to a table object

        Args:
            id (int): ID value of the table

        Returns:
            Table: Table object that matches the provided ID value
        """
        return next((table for table in self.tables if table.id == id), None)