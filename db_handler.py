from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData

class DatabaseHandler():
    def __init__(self):
        self.__engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)
        self.__session = sessionmaker(self.engine)
        self.__metadata_obj = MetaData()

        self.category_table = Table(
            "category",
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("name", String(40), nullable=False)
        )
        self.menu_table = Table(
            "menu_item",
            self.metadata_obj,
            Column("id", Integer, primary_key=True, autoincrement='auto'),
            Column("name", String(40), nullable=False),
            Column("price", Float(2), nullable=False),
            Column("category", Integer, ForeignKey('category.id')),
            Column("image_url", String(256))
        )

        self.create_tables()

    @property
    def engine(self) -> engine:
        """ Returns the engine"""
        return self.__engine
    
    @property
    def session(self) -> Session:
        """ Returns the session"""
        return self.__session
    
    @property
    def metadata_obj(self) -> MetaData:
        """ Returns the metadata object"""
        return self.__metadata_obj

    
    def create_tables(self):
        self.metadata_obj.create_all(self.engine)


    def load_db(self):
        pass
