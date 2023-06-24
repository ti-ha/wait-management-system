import React, { useState, useEffect } from "react";
import { Link, useParams } from 'react-router-dom';
import ItemModal from "./ItemModal";
import './Customer.css'

// Temporary mock data
import { categories, menuItems } from '../../mocks/menu_items.js'
import { Button } from "@mui/material";

export default function Customer() {

    const [currentCategory, setCurrentCategory] = useState("");
    const [currentItems, setCurrentItems] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [currentOrder, setCurrentOrder] = useState([]);
    const { tableNumber } = useParams();

    // First category is rendered by default
    useEffect(() => {
        setCurrentCategory(categories[0]);
        setCurrentItems(menuItems.filter(item => item.category === categories[0]))
    }, [])

    const handleCategoryClick = (category) => {
        setCurrentCategory(category);
        setCurrentItems(menuItems.filter(item => item.category === category))
    };

    const handleOpenModal = (item) => {
        setSelectedItem(item);
    }

    const handleCloseModal = () => {
        setSelectedItem(null);
    }

    const handleAddToOrder = () => {
        setCurrentOrder(prevOrder => [...prevOrder, {...selectedItem, quantity }])
        handleCloseModal();
    }

    return (
        <div className="customerPage">
            <Link to="/" className="landingPageButton">Landing Page</Link>

            <div className="customerContainer">
                <div className="categories">
                    <h2>Menu</h2>
                    {categories.map((category, index) => (
                        <div 
                            key={index} 
                            className={`${category === currentCategory ? "selectedCategoryBox" : "categoryBox"}`}
                            onClick={() => handleCategoryClick(category)}
                        >
                            <p>{category}</p>   
                        </div>
                    ))}
                </div>

                <div className="items">
                    <h2 className="itemsTitle">{currentCategory}</h2>
                    <div className="itemContainer">
                        {currentItems.map((item, index) => (
                            <div className="itemBox" key={index} onClick={() => handleOpenModal(item)}>
                                <img src={item.imageURL} alt={item.name}/>
                                <p>{item.name}</p>
                                <p>{item.cost}</p>
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
                                    <p>{order.cost}</p>
                                </div>
                            ))}
                        </div>
                        
                        <Button variant="contained">
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