import React, { useState, useEffect, useContext } from "react";
import { Link, useParams } from 'react-router-dom';
import ItemModal from "./ItemModal.js";
import BillModal from "./BillModal.js";
import './Customer.css'
import { Button, Icon, IconButton } from "@mui/material";
import { Add, Remove } from "@mui/icons-material"


export default function Customer() {

    const [categories, setCategories] = useState([]);
    const [currentCategory, setCurrentCategory] = useState("");
    const [currentItems, setCurrentItems] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [currentOrder, setCurrentOrder] = useState([]);
    const { tableNumber } = useParams();
    const [orders, setOrders] = useState([]);
    const [billOrders, setBillOrders] = useState([]);
    const [isBillOpen, setIsBillOpen] = useState(false);

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories`);
                if (!response.ok) { 
                    const responseBody = await response.json();
                    console.error('Server response:', responseBody); 
                    throw new Error(`HTTP Error with status: ${response.status}`);
                }
                const data = await response.json();
                setCategories(data);
                setCurrentCategory(data[0].name);
                fetchItems(data[0].name);
            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        }
        fetchCategories();
    }, []);

    const fetchItems = async (category) => {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`);
        const data = await response.json();
        setCurrentItems(data.menu_items);
    }

    const handleCategoryClick = (category) => {
        setCurrentCategory(category);
        fetchItems(category);
    };

    const handleOpenModal = (item) => {
        console.log('The selected item is', item)
        setSelectedItem(item);
    }

    const handleCloseModal = () => {
        setSelectedItem(null);
    }

    const handleAddToOrder = () => {
        const newOrder = { tableNumber, ...selectedItem, quantity };
        setCurrentOrder(prevOrder => [...prevOrder, newOrder])
        handleCloseModal();
    }

    const sendOrderToKitchen = async () => {
        const menu_items = currentOrder.flatMap(order => Array(order.quantity).fill({ id: order.id }));
        const deals = []

        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/orders/add/${tableNumber - 1}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ menu_items: menu_items, deals: deals })
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            setOrders(prevOrders => [...prevOrders, ...currentOrder]);
            setCurrentOrder([]);            
        } catch (error) {
            console.error('Error sending order to kitchen:', error);
        }
    }

    const fetchBill = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/tables/${tableNumber - 1}`);
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            setBillOrders(data.orders);
            console.log('The bill orders are:', billOrders);
            setIsBillOpen(true);
        } catch (error) {
            console.error("Error fetching bill orders:", error);
        }
    };

    const updateQuantity = (itemID, amount) => {
        setCurrentOrder(prevOrder => prevOrder.map(order => {
            if (order.id === itemID) {
                return { ...order, quantity: Math.max(0, order.quantity + amount) };
            } else {
                return order;
            }
        }).filter(order => order.quantity > 0));
    };

    return (
        <div className="customerPage">
            <header className="customerPageHeader">
                <div></div>
                <Link to="/">
                        <Button variant="contained">
                            Landing Page
                        </Button>
                </Link>
            </header>

            <div className="customerContainer">
                <div className="categories">
                    <h2>Menu</h2>
                    {categories.map((category, index) => (
                        <div 
                            key={index} 
                            className={`${category.name === currentCategory ? "selectedCategoryBox" : "categoryBox"}`}
                            onClick={() => handleCategoryClick(category.name)}
                        >
                            <p>{category.name}</p>   
                        </div>
                    ))}
                </div>

                <div className="items">
                    <h2 className="itemsTitle">{currentCategory}</h2>
                    <div className="itemContainer">
                        {currentItems.map((item, index) => (
                            <div className="itemBox" key={index} onClick={() => handleOpenModal(item)}>
                                <div className="imageContainer">
                                    <img src={item.imageURL} alt={item.name}/> 
                                </div>
                                <div className="itemInfo">
                                    <p>{item.name}</p>
                                    <p>${item.price}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="orderContainer">
                    <div>
                        <h2 className="tableNumber">
                            Table Number: {tableNumber}
                        </h2>
                    </div>

                    <div className="orders">
                        <div className="ordersList">
                            <h2 className="ordersHeader">Current Order</h2>
                            {currentOrder.map((order, index) => (
                                <div key={index} className="orderItem">
                                    <p>{order.name}</p>
                                    <div style={{display: 'flex', alignItems: 'center'}}>
                                        <IconButton onClick={() => updateQuantity(order.id, -1)}>
                                            <Remove />
                                        </IconButton>
                                            {order.quantity}
                                        <IconButton onClick={() => updateQuantity(order.id, 1)}>
                                            <Add />
                                        </IconButton>
                                    </div>
                                    <p>${order.price}</p>
                                </div>
                            ))}
                        </div>
                        
                        <Button variant="contained" onClick={sendOrderToKitchen}>
                            Send Order
                        </Button>
                    </div>

                    <Button variant="contained" onClick={fetchBill}>
                        View Bill
                    </Button>
                </div>
            </div>

            {selectedItem && 
                <ItemModal 
                    item={selectedItem}
                    onClose={handleCloseModal}
                    onAddToOrder={handleAddToOrder}
                    quantity={quantity}
                    setQuantity={setQuantity}
                />
            }

            {isBillOpen && 
                <BillModal 
                    orders={billOrders}
                    onClose={() => setIsBillOpen(false)}
                />
            }

        </div>
    )
};