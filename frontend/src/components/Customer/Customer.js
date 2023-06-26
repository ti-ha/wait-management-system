import React, { useState, useEffect, useContext } from "react";
import { Link, useParams } from 'react-router-dom';
import ItemModal from "./ItemModal.js";
import { OrderContext } from "../../contexts/OrderContext.js";
import './Customer.css'
import { Button } from "@mui/material";

export default function Customer() {

    const [categories, setCategories] = useState([]);
    const [currentCategory, setCurrentCategory] = useState("");
    const [currentItems, setCurrentItems] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [currentOrder, setCurrentOrder] = useState([]);
    const { tableNumber } = useParams();
    const { setOrders } = useContext(OrderContext);
    

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const res = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories`);
                if (!res.ok) { throw res }
                const data = await res.json();
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
        const res = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`);
        const data = await res.json();
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

    const sendOrderToKitchen = () => {
        setOrders(prevOrders => [...prevOrders, ...currentOrder]);
        setCurrentOrder([]);
    }

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
                                {/* Image URL Pending to be added to menu item class*/}
                                {/* <img src={item.imageURL} alt={item.name}/> */} 
                                <p>{item.name}</p>
                                <p>${item.price}</p>
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
                            <h2>Current Order</h2>
                            {currentOrder.map((order, index) => (
                                <div key={index} className="orderItem">
                                    <p>{order.name}</p>
                                    <p>{order.quantity}</p>
                                    <p>${order.price}</p>
                                </div>
                            ))}
                        </div>
                        
                        <Button variant="contained" onClick={sendOrderToKitchen}>
                            Send Order
                        </Button>
                    </div>

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

        </div>
    )
}