from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Engine
import enum
from sqlalchemy import MetaData, ARRAY, Enum


from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column

class OrderStates(enum.Enum):
    DELETED = -1
    ORDERED = 0
    COOKING = 1
    READY = 2
    SERVED = 3
    COMPLETED = 4

class DbHandler():
    """
    A class to handle database functions
    """

    class Base(DeclarativeBase):
        pass

    class DealMenu(Base):
        __tablename__ = 'deal_menu'
        deal_id = mapped_column('deal', ForeignKey('deal.id'), primary_key=True)
        menu_item_id = mapped_column('menu_item', ForeignKey('menu_item.id'), primary_key=True),
    
    class OrderMenu(Base):
        __tablename__ = 'order_menu'
        order_id = mapped_column('order', ForeignKey('order.id'), primary_key=True)
        menu_item_id = mapped_column('menu_item', ForeignKey('menu_item.id'), primary_key=True),

    class OrderDeal(Base):
        __tablename__ = 'order_deal'
        order_id = mapped_column('order', ForeignKey('order.id'), primary_key=True)
        deal_id = mapped_column('deal', ForeignKey('deal.id'), primary_key=True),
    
    class Category(Base):
        __tablename__ = 'category'
        id = mapped_column(Integer, primary_key=True, autoincrement='auto')
        name = mapped_column(String(40), nullable=False)
    
    class MenuItem(Base):
        __tablename__ = 'menu_item'
        id = mapped_column(Integer, primary_key=True, autoincrement='auto')
        name = mapped_column(String(40), nullable=False)
        price = mapped_column(Float(2), nullable=False)
        category = mapped_column(Integer, ForeignKey('category.id'))
        image_url = mapped_column(String(256))

    class Deal(Base):
        __tablename__ = 'deal'
        id = mapped_column('id', Integer, primary_key=True, autoincrement='auto')
        discount = mapped_column('discount', Float(2), nullable=False) 
        menu_items: Mapped[self.MenuItem] = relationship(secondary='deal_menu', back_populates='menu_item')

    class Order(Base):
        __tablename__ = 'order'
        id = mapped_column(Integer, primary_key=True, autoincrement='auto')
        state = mapped_column(Enum(OrderStates), nullable=False)
        customer = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
        menu_items: Mapped[self.MenuItem] = relationship(secondary='order_menu', back_populates='menu_item')
        deals: Mapped[self.Deal] = relationship(secondary='order_deal', back_populates='deal'),

    class User(Base):
        __tablename__ = 'user'
        id = mapped_column(Integer, primary_key=True, autoincrement='auto')
        first_name = mapped_column(String(40), nullable=False)
        last_name = mapped_column(String(40), nullable=False)
        password_hash = mapped_column(String(64), nullable=False)
        logged_in = mapped_column(Integer, nullable=False)

    def __init__(self):
        self.__engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)
        self.__session = sessionmaker(self.engine)
        # self.__metadata_obj = self.Base.metadata
        self.Base.metadata.create_all(self.engine)
        # self.__category_table = Table(
        #     "category",
        #     self.metadata_obj,
        #     Column("id", Integer, primary_key=True, autoincrement='auto'),
        #     Column("name", String(40), nullable=False)
        # )
        # self.__menu_table = Table(
        #     "menu_item",
        #     self.metadata_obj,
        #     Column("id", Integer, primary_key=True, autoincrement='auto'),
        #     Column("name", String(40), nullable=False),
        #     Column("price", Float(2), nullable=False),
        #     Column("category", Integer, ForeignKey('category.id')),
        #     Column("image_url", String(256))
        # )
        # self.__deals_table = Table(
        #     "deals",
        #     self.metadata_obj,
        #     Column("id", Integer, primary_key=True, autoincrement='auto'),
        #     Column("discount", Float(2), nullable=False),
        #     Column("menu_items", ARRAY(Integer), ForeignKey('menu_item.id'))
        # )
        # self.__order_table = Table(
        #     "orders",
        #     self.metadata_obj,
        #     Column("id", Integer, primary_key=True, autoincrement='auto'),
        #     Column("state", Enum(OrderStates), nullable=False),
        #     Column("customer", Integer, ForeignKey('users.id'), nullable=False),
        #     Column("menu_items", ARRAY(Integer), ForeignKey('menu_item.id')),
        #     Column("deals", ARRAY(Integer), ForeignKey('deals.id'))
        # )
        # self.__user_table = Table(
        #     "users",
        #     self.metadata_obj,
        #     Column("id", Integer, primary_key=True, autoincrement='auto'),
        #     Column("first_name", String(40), nullable=False),
        #     Column("last_name", String(40), nullable=False),
        #     Column("password_hash", String(64), nullable=False),
        #     Column("logged_in", Integer, nullable=False)
        # )

        # self.__order_menu_items = Table(
        #     "order_menu_items",
        #     Column("order_id", Integer, ForeignKey('menu_item.id')),
        #     Column("menu_item_id", Integer, ForeignKey('menu_item.id')),
        # )

        # self.create_tables()

    @property
    def engine(self) -> Engine:
        """Returns the db engine"""
        return self.__engine

    @property
    def session(self) -> Session:
        """Returns the db session"""
        return self.__session

    # @property
    # def metadata_obj(self) -> MetaData:
    #     """Returns the metadata object"""
    #     return self.__metadata_obj

    # @property
    # def menu_table(self) -> Table:
    #     """Returns menu_table"""
    #     return self.__menu_table

    # @property
    # def category_table(self) -> Table:
    #     """Returns category_table"""
    #     return self.__category_table

    # @property
    # def deals_table(self) -> Table:
    #     """Returns deals_table"""
    #     return self.__deals_table

    # @property
    # def order_table(self) -> Table:
    #     """Returns order_table"""
    #     return self.__order_table

    # @property
    # def user_table(self) -> Table:
    #     """Returns user_table"""
    #     return self.__user_table

    # def create_tables(self):
    #     """Initialises all database tables"""
    #     self.metadata_obj.create_all(self.engine)

