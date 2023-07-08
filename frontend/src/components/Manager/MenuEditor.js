import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import './MenuEditor.css'
import { Button } from "@mui/material";
import AddCategoryModal from './AddCategoryModal.js';
import AddItemModal from './AddItemModal.js'


export default function MenuEditor() {

    const [categories, setCategories] = useState([]);
    const [currentCategory, setCurrentCategory] = useState("");
    const [currentItems, setCurrentItems] = useState([]);
    const [showAddCategoryModal, setShowAddCategoryModal] = useState(false);
    const [showAddItemModal, setShowAddItemModal] = useState(false);

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

    useEffect(() => {
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

    const handleAddCategory = async (categoryName) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: categoryName }),
            });
    
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data.message);
    
            // Fetch categories again to update the page state
            fetchCategories();
        } catch (error) {
            console.error("Error adding category:", error);
        }
        setShowAddCategoryModal(false);
    };

    const handleAddItem = async (itemName, itemCost, itemCategory, itemImageURL) => {
        console.log(itemName, itemCost, itemImageURL);
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${itemCategory}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: itemName, price: parseFloat(itemCost), image_url: itemImageURL }),
            });
    
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data.message);
    
            // Fetch items again to update the page state
            fetchItems(itemCategory);
        } catch (error) {
            console.error("Error adding item:", error);
        }
        setShowAddItemModal(false);
    };



    return (
        <div className="customerPage">
            <header className="editorPageHeader">
                <div>
                    <Link to="/menu-editor">
                        <Button variant="contained" disabled>
                            Menu Editor
                        </Button>
                    </Link>
                    <Link to="/restaurant-manager">
                        <Button variant="contained">
                            Restaurant Manager
                        </Button>
                    </Link>
                </div>
                <Link to="/">
                    <Button variant="contained">
                        Landing Page
                    </Button>
                </Link>
            </header>

            

            <div className="editorContainer">
                <div className="categories">
                    <Button 
                        variant="contained" 
                        onClick={() => setShowAddCategoryModal(true)} 
                        sx={{marginBottom: '10px'}}
                    >
                        Add New Category
                    </Button>
                    <Button 
                        variant="contained" 
                        onClick={() => setShowAddItemModal(true)}
                    >
                        Add New Menu Item
                    </Button>
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
                            <div className="itemBox" key={index}>
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
            </div>

            {showAddCategoryModal && 
                <AddCategoryModal 
                    open={showAddCategoryModal} 
                    onClose={() => setShowAddCategoryModal(false)} 
                    onAdd={handleAddCategory} 
                />
            }

            {showAddItemModal && 
                <AddItemModal
                    open={showAddItemModal}
                    onClose={() => setShowAddItemModal(false)}
                    onAdd={handleAddItem}
                    categories={categories}
                />
            }
        </div>
    )
};
