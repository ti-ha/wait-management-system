from __future__ import annotations

from sqlalchemy import UniqueConstraint, create_engine, Integer, String, Float, ForeignKey, Engine
import enum
from sqlalchemy import select
from typing import List, Set

from sqlalchemy.orm import relationship, DeclarativeBase, sessionmaker, Session, Mapped, mapped_column
from sqlalchemy.types import DateTime
from sqlalchemy.schema import Sequence

class Base(DeclarativeBase):
    """Base class of database tables"""

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
        """Create all tables"""
        # Base.metadata.reflect(self.engine)
        Base.metadata.create_all(self.engine, checkfirst=True)
                
class DealMenu(Base):
    """Association table for deal and menu items"""
    __tablename__ = 'deal_menu'
    deal_id = mapped_column(ForeignKey('deal.id'), primary_key=True)
    menu_item_id = mapped_column(ForeignKey('menu_item.id'), primary_key=True)

class OrderMenu(Base):
    """Association table for order and menu items"""
    __tablename__ = 'order_menu'
    order_id = mapped_column(ForeignKey('order.id'), primary_key=True)
    menu_item_id = mapped_column(ForeignKey('menu_item.id'), primary_key=True)

class OrderDeal(Base):
    """"Association table for order and deal"""
    __tablename__ = 'order_deal'
    order_id = mapped_column(ForeignKey('order.id'), primary_key=True)
    deal_id = mapped_column(ForeignKey('deal.id'), primary_key=True)

class Deal(Base):
    """Table for deal"""
    __tablename__ = 'deal'
    id = mapped_column(Integer, primary_key=True)
    discount = mapped_column(Float(2), nullable=False)
    menu_items: Mapped[List[MenuItem]] = relationship(secondary='deal_menu', back_populates='deals')
    orders: Mapped[List[Order]] = relationship(secondary='order_deal',back_populates='deals')

class Category(Base):
    """Table for category"""
    __tablename__ = 'category'
    __table_args__ = (UniqueConstraint('name'), )
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(40), nullable=False)
    menu_items: Mapped[Set[MenuItem]] = relationship(back_populates="category")

class MenuItem(Base):
    """Table for menu item"""
    __tablename__ = 'menu_item'
    __table_args__ = (UniqueConstraint('name'), )
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(40), nullable=False)
    price = mapped_column(Float(2), nullable=False)
    category_id = mapped_column(Integer, ForeignKey('category.id'))
    image_url = mapped_column(String(256))
    category: Mapped[Category] = relationship(back_populates="menu_items")
    deals: Mapped[List[Deal]] = relationship(secondary='deal_menu', back_populates='menu_items')
    orders: Mapped[List[Order]] = relationship(secondary='order_menu', back_populates='menu_items')

class Table(Base):
    """Table for table"""
    __tablename__ = 'table'
    id = mapped_column(Integer, primary_key=True)
    limit = mapped_column(Integer, nullable=False)
    orders: Mapped[List[Order]] = relationship(back_populates='table')

class Order(Base):
    """Table for order"""
    __tablename__ = 'order'
    id = mapped_column(Integer, primary_key=True)
    state = mapped_column(Integer, nullable=False)
    customer = mapped_column(Integer, ForeignKey('user.id'))
    table: Mapped[Table] = relationship(back_populates='orders')
    table_id = mapped_column(Integer, ForeignKey('table.id'))
    menu_items: Mapped[List[MenuItem]] = relationship(secondary='order_menu', back_populates='orders')
    deals: Mapped[List[Deal]] = relationship(secondary='order_deal',back_populates='orders')
    datetime = mapped_column(DateTime, nullable=False)

class User(Base):
    """Table for user"""
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(40), nullable=False)
    last_name = mapped_column(String(40), nullable=False)
    type = mapped_column(String(20), nullable=False)
    password_hash = mapped_column(String(64), nullable=False)
    logged_in = mapped_column(Integer, nullable=False)

class ServiceRequest(Base):
    """Table for service requests"""
    __tablename__ = 'service_request'
    id = mapped_column(Integer, primary_key=True)
    table = mapped_column(Integer)
    subject = mapped_column(String(64))
    summary = mapped_column(String(128))
    timestamp = mapped_column(String(512), nullable=False)
    status = mapped_column(Integer)
    assignee = mapped_column(Integer, ForeignKey('user.id'))
