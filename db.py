from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

class db():
    def __init__(self):
        self.db_engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)
        Session = sessionmaker(self.db_engine)
        self.session = Session()
        self.metadata_obj = MetaData()
        # self.Base = declarative_base()

    @property
    def session(self):
        """ Returns the session"""
        return self.session
    
    @property
    def metadata_obj(self):
        """ Returns the metadata object"""
        return self.metadata_obj
    
    def create_db(self):
        category = Table(
            "category",
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("name", String(40), nullable=False)
        )

        menu = Table(
            "menu_item",
            self.metadata_obj,
            Column("id", Integer, primary_key=True, autoincrement='auto'),
            Column("name", String(40), nullable=False),
            Column("price", Float(2), nullable=False),
            Column("category", Integer, ForeignKey('category.id')),
            Column("image_url", String(256))
        )

        self.metadata_obj.create_all(self.db_engine)


