from wms import Menu, Category, MenuItem, Deal

menu = Menu()
burgers = Category("burgers")
snacks = Category("snacks")
burger = MenuItem("burger", 20.0)
snack = MenuItem("snack",  20.0)
drink = MenuItem("drink", 5.0)
burgers.add_menu_item(burger)
snacks.add_menu_item(snack)
snacks.add_menu_item(drink)
deal = Deal(0.50)
deal.add_menu_item(snack)
deal.add_menu_item(drink)
menu.add_category(burgers)
menu.add_category(snacks)
menu.add_deal(deal)

def test1(menu):
    if len(menu.categories()) != 2:
        print("test1 FAIL")
        print(menu.categories())
        return False
    
    print("test1 PASS")
    return True

def test2(menu):
    if len(menu.deals()) != 1:
        print("test2 FAIL")
        print(menu.deals())
        return False
    
    print("test2 PASS")
    return True

def test3(menu):
    c = menu.get_category("burgers")
    if c == None:
        print("test3 FAIL")
        return False
    
    print("test3 PASS")
    return True

def test4(menu):
    c = menu.get_category("burgers")
    if c != burgers:
        print("test4 FAIL")
        print(c)
        return False
    
    print("test4 PASS")
    return True

def test5(menu):
    c = Category("sides")
    menu.add_category(c)
    i = menu.get_category("sides")
    if c != i:
        print("test5 FAIL")
        print(menu.categories())
        return False
    
    print("test5 PASS")
    return True

def test6(menu):
    try:
        menu.add_category(burgers)
    except ValueError:
        print("test6 PASS")
        return True
    
    print("test6 FAIL")
    return False

def test7(menu):
    menu.remove_category("sides")
    c = menu.get_category("sides")
    if c != None:
        print("test7 FAIL")
        return False
    
    print("test7 PASS")
    return True

def test8(menu):
    try:
        menu.add_deal(deal)
    except ValueError:
        print("test8 PASS")
        return True
    
    print("test8 FAIL")
    return False

def test9(menu):
    newdeal = Deal(0.1)
    menu.add_deal(newdeal)
    if len(menu.deals()) != 2:
        print("test9 FAIL")
        return False
    
    print("test9 PASS")
    return True

def test10(menu):
    newdeal = menu.deals()[1]
    menu.remove_deal(newdeal)
    if len(menu.deals()) != 1:
        print("test10 FAIL")
        return False
    
    print("test10 PASS")
    return newdeal

def test11(menu, out):
    try:
        menu.remove_deal(out)
    except ValueError:
        print("test11 PASS")
        return True
    
    print("test11 FAIL")
    return False

def test12(menu):
    try:
        menu.remove_category(24)
    except TypeError:
        print("test12 PASS")
        return True
    
    print("test12 FAIL")
    return False

def test13(menu):
    try:
        menu.remove_deal(69)
    except TypeError:
        print("test13 PASS")
        return True
    
    print("test13 FAIL")
    return False

def test14():
    if burgers.id() != 0 or snacks.id() != 1:
        print("test14 FAIL")
        return False
    
    newcat = Category("newcategory")
    if newcat.id() != 3:
        print("test14 FAIL")
        return False
    
    print("test14 PASS")
    return True

def test15():
    if burgers.name() != "burgers":
        print("test15 FAIL")
        return False
    
    print("test15 PASS")
    return True

def test16():
    if len(burgers.menu_items()) != 1 or len(snacks.menu_items()) != 2:
        print("test16 FAIL")
        return False
    
    print("test16 PASS")
    return True

def test17():
    o = burgers.menu_item("burger")
    if o != burger:
        print("test17 FAIL")
        return False
    
    print("test17 PASS")
    return True

def test18():
    o = burgers.menu_item("foo")
    if o != None:
        print("test18 FAIL")
        return False
    
    print("test18 PASS")
    return True

def test19():
    shoestring_fries = MenuItem("Shoestring Fries", 1000000)
    burgers.add_menu_item(shoestring_fries)
    if burgers.menu_item("Shoestring Fries") != None:
        print("test19 PASS")
        return shoestring_fries
    
    print("test19 FAIL")
    return False

def test20(out):
    burgers.remove_menu_item(out)
    if burgers.menu_item("Shoestring Fries") == None:
        print("test20 PASS")
        return True
    
    print("test20 FAIL")
    return False

def test21():
    try:
        burgers.add_menu_item(burger)
    except ValueError:
        print("test21 PASS")
        return True
    
    print("test21 FAIL")
    return False

def test22():
    try: 
        burgers.add_menu_item(24)
    except TypeError:
        print("test22 PASS")
        return True
    
    print("test22 FAIL")
    return False

def test23(out):
    try:
        burgers.remove_menu_item(out)
    except ValueError:
        print("test23 PASS")
        return True
    
    print("test23 FAIL")
    return False

def test24():
    try:
        burgers.remove_menu_item(24)
    except TypeError:
        print("test24 PASS")
        return True
    
    print("test24 FAIL")
    return False

    

if __name__ == '__main__':
    test1(menu)
    test2(menu)
    test3(menu)
    test4(menu)
    test5(menu)
    test6(menu)
    test7(menu)
    test8(menu)
    test9(menu)
    out = test10(menu)
    test11(menu, out)
    test12(menu)
    test13(menu)
    test14()
    test15()
    test16()
    test17()
    test18()
    out1 = test19()
    test20(out1)
    test21()
    test22()
    test23(out1)
    test24()