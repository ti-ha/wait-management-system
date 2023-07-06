from wms import Table, Customer

class TableHandler():
    def __init__(self) -> None:
        self.__tables = []
    
    def add_table(self, table_limit, orders):
        table = Table(table_limit, orders)
        self.__tables.append(table)
        return table.id()
    
    def add_customer(self, table_id, customer: Customer):
        table = self.id_to_table(table_id)
        try:
            table.add_customers(customer)
        except:
            return False
        return True

    def jsonify(self):
        return {"tables": [{"id": table.id(),
                            "availability": table.get_open_seats(),
                            "table limit": table.get_table_limit(),
                            "is occupied": table.is_occupied()}
                            for table in self.__tables]}

    def id_to_table(self, id) -> Table:
        for table in self.__tables:
            if table.id() == id:
                return table
        return None