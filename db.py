from sqlalchemy import create_engine, Column, Integer, String, Double, ForeignKey, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

db_engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)
Session = sessionmaker(db_engine)
session = Session()
Base = declarative_base()
metadata_obj = MetaData()

category = Table(
    "category",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(40), nullable=False)
)

menu = Table(
    "menu_item",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("name", String(40), nullable=False),
    Column("price", Double(2), nullable=False),
    Column("category", Integer, ForeignKey('category.id')),
    Column("image_url", String(256))
)

metadata_obj.create_all(db_engine)


