from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Engine
import enum
from sqlalchemy import MetaData, ARRAY, Enum
from typing import List, Set

from sqlalchemy.orm import relationship, DeclarativeBase, declarative_base
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column, configure_mappers, registry

class OrderStates(enum.Enum):
    DELETED = -1
    ORDERED = 0
    COOKING = 1
    READY = 2
    SERVED = 3
    COMPLETED = 4


class Base(DeclarativeBase):
    pass

class DbHandler():
    """A class to handle database functions"""
    def __init__(self):
        self.__engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)
        self.__session = sessionmaker(self.engine)
    
    @property
    def engine(self) -> Engine:
        """Returns the db engine"""
        return self.__engine

    @property
    def session(self) -> Session:
        """Returns the db session"""
        return self.__session

    def initialise(self):
        Base.metadata.create_all(self.engine)

class DealMenu(Base):
    __tablename__ = 'deal_menu'
    deal_id = mapped_column(ForeignKey('deal.id'), primary_key=True)
    menu_item_id = mapped_column(ForeignKey('menu_item.id'), primary_key=True)
    
class OrderMenu(Base):
    __tablename__ = 'order_menu'
    order_id = mapped_column(ForeignKey('order.id'), primary_key=True)
    menu_item_id = mapped_column(ForeignKey('menu_item.id'), primary_key=True)

class OrderDeal(Base):
    __tablename__ = 'order_deal'
    order_id = mapped_column(ForeignKey('order.id'), primary_key=True)
    deal_id = mapped_column(ForeignKey('deal.id'), primary_key=True)

class Category(Base):
    __tablename__ = 'category'
    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    name = mapped_column(String(40), nullable=False)
    menu_items: Mapped[Set[MenuItem]] = relationship(back_populates="category")

class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    name = mapped_column(String(40), nullable=False)
    price = mapped_column(Float(2), nullable=False)
    category_id = mapped_column(Integer, ForeignKey('category.id'))
    image_url = mapped_column(String(256))
    category: Mapped[Category] = relationship(back_populates="menu_items")
    deals: Mapped[List[Deal]] = relationship(secondary='deal_menu', back_populates='menu_items')
    orders: Mapped[List[Order]] = relationship(secondary='order_menu', back_populates='menu_items')

class Deal(Base):
    __tablename__ = 'deal'
    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    discount = mapped_column(Float(2), nullable=False)
    menu_items: Mapped[List[MenuItem]] = relationship(secondary='deal_menu', back_populates='deals')
    orders: Mapped[List[Order]] = relationship(secondary='order_deal',back_populates= 'deals')

class Order(Base):
    __tablename__ = 'order'
    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    state = mapped_column(Enum(OrderStates), nullable=False)
    customer = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    menu_items: Mapped[List[MenuItem]] = relationship(secondary='order_menu', back_populates='orders')
    deals: Mapped[List[Deal]] = relationship(secondary='order_deal',back_populates='orders')

class User(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    first_name = mapped_column(String(40), nullable=False)
    last_name = mapped_column(String(40), nullable=False)
    password_hash = mapped_column(String(64), nullable=False)
    logged_in = mapped_column(Integer, nullable=False)