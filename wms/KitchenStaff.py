from .Order import Order
from .User import User
from sqlalchemy import Column, Integer, Double, String, ForeignKey

class KitchenStaff(User):

    __tablename__ = 'kitchen_staff'
    __mapper_args__ = {'polymorphic_identity': 'kitchen_staff'}

    orderId = Column(Integer, ForeignKey('order.orderId'))
    id = Column(Integer, ForeignKey('user.userId'), primary_key=True)

    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        self.__orders = []

    # Add to list of orders
    def assign_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("KitchenStaff: assign_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("KitchenStaff: assign_order(): Order already exists")
        self.__orders.append(order)

    # Remove order once complete
    def remove_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("KitchenStaff: remove_order(): Object is not of type Order")
        
        if order not in self.__orders:
            raise ValueError("KitchenStaff: remove_order(): Order does not exist")
        orderNum = self.__orders.index(order)
        self.__orders[orderNum].change_state()
        # Move order to wait staff
        self.__orders.remove(order) 
