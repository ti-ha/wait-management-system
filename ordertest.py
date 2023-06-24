from wms import Menu, Category, MenuItem, Order, Bill, OrderManager
from wms.Order import State

menu = Menu()
burger = MenuItem("burger", 20.0)
snack = MenuItem("snack",  20.0)
drink = MenuItem("drink", 5.0)

def test1():
    order1 = Order()
    assert(order1.get_bill().get_price() == 0)
    order1.add_menu_item(burger)
    assert(order1.get_bill().get_price() == 20.0)
    order1.add_menu_item(snack)
    assert(order1.get_bill().get_price() == 40.0)
    order1.add_menu_item(drink)
    assert(order1.get_bill().get_price() == 45.0)

    order1.remove_menu_item(snack)
    assert(order1.get_bill().get_price() == 25.0)
    order1.remove_menu_item(drink)
    assert(order1.get_bill().get_price() == 20.0)
    order1.remove_menu_item(burger)
    assert(order1.get_bill().get_price() == 0)

def test2():
    order2 = Order()  
    assert(order2.get_state() == State.ORDERED)
    order2.change_state()
    assert(order2.get_state() == State.COOKED)
    order2.change_state()
    assert(order2.get_state() == State.SERVED)

def test3():
    order3 = Order()
    orderMan = OrderManager()
    orderMan.add_order(order3)
    assert(len(orderMan.get_orders()) == 1)
    order3_ID = order3.get_id()
    assert(order3 == orderMan.get_order(order3_ID))
    orderMan.mark_as_complete(order3_ID)
    assert(order3.get_state() == State.COOKED)
