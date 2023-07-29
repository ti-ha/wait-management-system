from db_handler import DatabaseHandler

def initialise():
    db = DatabaseHandler()
    db.create_tables()
    return db