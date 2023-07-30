from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData

engine = create_engine("sqlite+pysqlite:///wms_db.db")
def create_engine():
    session = sessionmaker(engine)
    metadata_obj = MetaData()

    category_table = Table(
        "category",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(40), nullable=False)
    )
    menu_table = Table(
        "menu_item",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(40), nullable=False),
        Column("price", Float(2), nullable=False),
        Column("category", Integer, ForeignKey('category.id')),
        Column("image_url", String(256))
    )

    create_tables(metadata_obj)

def create_tables(metadata_obj):
    metadata_obj.create_all(engine)

def load_engine():
    return engine
