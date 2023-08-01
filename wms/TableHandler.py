from .Table import Table
from .Customer import Customer
from wms import DbHandler
from wms.DbHandler import Table as TableTable
from sqlalchemy.orm import Session

class TableHandler():
    def __init__(self, db: DbHandler) -> None:
        """ Constructor for the TableHandler Class """
        self.__tables = []
        self.__db = db

    @property
    def tables(self) -> list[Table]:
        return self.__tables

    @property
    def db(self) -> DbHandler:
        return self.__db
    
    def add_table(self, table_limit, orders):
        """ Adds a table to the restaurant

        Args:
            table_limit (Integer): Maximum number of customers at the table
            orders (List[Order]): Orders to be predefined with the table 
        """
        table = Table(table_limit, orders)
        self.__tables.append(table)
        with Session(self.db.engine) as session:
            try:
                session.add(TableTable(
                    id=table.id,
                    limit=table.table_limit
                ))
                session.commit()
            except:
                session.rollback()
    
    def add_customer(self, table_id, customer: Customer) -> bool:
        """ Adds a customer to the table

        Args:
            table_id (Integer): ID of the table that customer is being added to
            customer (Customer): Customer to be added to the table
        """
        table = self.id_to_table(table_id)
        table.add_customers(customer)

    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id, availability string, table
        limit and occupied boolean of the table  

        Returns:
            Dict: A dictionary containing the id, availability string, table
        limit and occupied boolean of the table  
        """
        return {"tables": [table.jsonify() for table in self.tables]}

    def id_to_table(self, id) -> Table:
        """ Converts a given id to a table object

        Args:
            id (Integer): ID value of the table

        Returns:
            Table: Table object that matches the provided ID value
        """
        return next((table for table in self.tables if table.id == id), None)