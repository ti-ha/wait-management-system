import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import './Customer.css'

// Temporary mock data
import { categories, menuItems } from '../../mocks/menu_items.js'

export default function Customer() {

    const [currentCategory, setCurrentCategory] = useState("");
    const [currentItems, setCurrentItems] = useState([]);

    // First category is rendered by default
    useEffect(() => {
        setCurrentCategory(categories[0]);
        setCurrentItems(menuItems.filter(item => item.category === categories[0]))
    }, [])

    const handleCategoryClick = (category) => {
        setCurrentCategory(category);
        setCurrentItems(menuItems.filter(item => item.category === category))
    };

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
                    <h2>{currentCategory}</h2>
                    <div className="itemContainer">
                        {currentItems.map((item, index) => (
                            <div className="itemBox" key={index}>
                                <img src={item.imageURL} alt={item.name}/>
                                <p>{item.name}</p>
                                <p>{item.cost}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}