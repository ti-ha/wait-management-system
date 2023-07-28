from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)

# Create database session
Session = sessionmaker(db_engine)
session = Session()
