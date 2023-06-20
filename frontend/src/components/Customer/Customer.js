import React from "react";
import { Link } from 'react-router-dom';
import './Customer.css'

export default function Customer() {

    // Mock Data - Temporary
    const categories = ['Category 1', 'Category 2', 'Category 3'];
    const menuItems = [
        { name: 'Item 1', cost: '$10'},
        { name: 'Item 2', cost: '$20'},
        { name: 'Item 3', cost: '$30'},
    ];

    return (
        <div className="customerPage">
            <Link to="/" className="landingPageButton">Landing Page</Link>

            <div className="customerContainer">
                <div className="categories">
                    <h2>Menu</h2>
                    {categories.map((category, index) => (
                        <p key={index}>{category}</p>
                    ))}
                </div>

                <div className="items">
                    <h2>Category X</h2>
                    {menuItems.map((item, index) => (
                        <div className="itemBox" key={index}>
                            <p>{item.name}</p>
                            <p>{item.cost}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}