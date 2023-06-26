from wms import *

menu = Menu()
burger = MenuItem("burger", 20.0)
snack = MenuItem("snack",  20.0)
drink = MenuItem("drink", 5.0)
deal = Deal(0.4, [burger, snack])
deal2 = Deal(0.2, drink)
table = Table(5)

def test1():
    order1 = Order()
    order1.add_menu_item(burger)
    order1.add_menu_item(snack)
    order1.add_menu_item(drink)
    assert(len(order1.menu_items()) == 3)
    order1.remove_menu_item(snack)
    order1.remove_menu_item(drink)
    order1.remove_menu_item(burger)
    assert(len(order1.menu_items()) == 0)
    print("Test1 pass")

def test2():
    order2 = Order()  
    assert(order2.state() == "ordered")
    order2.change_state()
    assert(order2.state() == "cooking")
    order2.change_state()
    assert(order2.state() == "ready")
    order2.change_state()
    assert(order2.state() == "served")
    order2.change_state()
    assert(order2.state() == "completed")
    try:
        order2.change_state()
        print("Test2 fail")
    except:
        pass
    print("Test2 pass")

def test3():
    order3 = Order()
    orderMan = OrderManager()
    table1 = Table(4)
    orderMan.add_order(order3, table1)
    assert(len(orderMan.orders()) == 1)
    order3_ID = order3.id()
    assert(order3 == orderMan.get_order(order3_ID))
    orderMan.change_state(order3_ID)
    assert(order3.state() == "cooking")
    print("Test3 pass")

def test4():
    order4 = Order([burger, snack, drink], [deal, deal2])
    assert(order4.state() == "ordered")
    # kitchen staff starts cooking order
    order4.change_state()
    assert(order4.state() == "cooking")
    # kitchen staff finishes cooking order
    order4.change_state()
    assert(order4.state() == "ready")
    # wait staff serves order to customer
    order4.change_state()
    assert(order4.state() == "served")
    assert(order4.bill() == None)
    # customer asks for the bill
    bill = order4.calculate_bill()
    assert(bill != None)
    assert(bill.get_price() == 28.0)
    order4.mark_as_paid()
    assert(order4.bill_paid() == True)
    assert(order4.state() == "completed")
    print("Test4 pass")

def test5():
    orderman = OrderManager()
    table1 = Table(4)
    orderA = Order([burger, snack, drink], [deal, deal2])
    orderB = Order(snack)
    orderman.add_order(orderA, table1)
    orderman.add_order(orderB, table1)
    try:
        orderman.calculate_table_bill(table1.get_id())
    except ValueError:
        pass
    orderman.change_to_state(orderA, "served")
    orderman.change_to_state(orderB, "served")
    bill = orderman.calculate_table_bill(table1.get_id())
    assert(bill.get_price() == 48.0)
    print(orderman.map())
    assert(len(orderman.orders()) == 2)
    orderman.remove_order(orderA, table1)
    assert(len(orderman.orders()) == 1)






if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()