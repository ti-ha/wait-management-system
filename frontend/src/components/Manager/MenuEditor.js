import React, { useState, useEffect } from "react";
import './MenuEditor.css'
import { Button } from "@mui/material";
import { Add, Edit, Delete, Visibility, VisibilityOff } from "@mui/icons-material";
import AddCategoryModal from './AddCategoryModal.js';
import AddItemModal from './AddItemModal.js'
import EditCategoryModal from './EditCategoryModal.js';
import DeleteConfirmationModal from "./DeleteConfirmationModal.js";
import EditItemModal from "./EditItemModal.js";
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from "../Common/Header.js";

export default function MenuEditor() {
    const [categories, setCategories] = useState([]);
    const [currentCategory, setCurrentCategory] = useState("");
    const [currentItems, setCurrentItems] = useState([]);
    const [showAddCategoryModal, setShowAddCategoryModal] = useState(false);
    const [showAddItemModal, setShowAddItemModal] = useState(false);
    const [deleteCategory, setDeleteCategory] = useState({active: false, category: ""});
    const [editCategory, setEditCategory] = useState({active: false, category: ""});
    const [editItem, setEditItem] = useState({active: false, item: null});
    const [deleteItem, setDeleteItem] = useState({active: false, item: null, categoryName: null});

    const auth_token = localStorage.getItem('token'); 

    const fetchCategories = async (updatedCategoryName) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories`);
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            setCategories(data);

            const categoryName = updatedCategoryName || currentCategory;
            const currentCategoryExists = data.some(category => category.name === categoryName);
            if (currentCategoryExists) {
                fetchItems(categoryName);
            } else {
                setCurrentCategory(data[0].name);
                fetchItems(data[0].name);
            }
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
                    'Authorization': `${auth_token}`
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

    const handleAddItem = async (itemName, itemPrice, itemCategory, itemImageURL) => {
        console.log(itemName, itemPrice, itemImageURL);
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${itemCategory}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${auth_token}`
                },
                body: JSON.stringify({ name: itemName, price: parseFloat(itemPrice), image_url: itemImageURL }),
            });
    
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data.message);
    
            // Fetch items again to update the page state
            fetchItems(currentCategory);
        } catch (error) {
            console.error("Error adding item:", error);
        }
        setShowAddItemModal(false);
    };

    const handleDeleteCategory = async (category) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `${auth_token}`
                }
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
            console.error("Error deleting category:", error);
        }
        setDeleteCategory({active: false, category: ""});
    };

    const handleEditCategory = async (newCategoryName) => {
        const oldCategoryName = editCategory.category;
    
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${oldCategoryName}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${auth_token}`
                },
                body: JSON.stringify({
                    new_name: newCategoryName,
                }),
            });
    
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data.message);

            if (oldCategoryName === currentCategory) {
                setCurrentCategory(newCategoryName);
                fetchCategories(newCategoryName);
            } else {
                // Fetch categories again to update the page state
                fetchCategories();
            }
        } catch (error) {
            console.error(`Error editing category '${oldCategoryName}':`, error);
        }
    
        setEditCategory({active: false, category: ""});
    };

    const handleEditItem = async (newItem) => {
        const oldItemName = editItem.item.name;
        const categoryName = currentCategory;
    
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${categoryName}/${oldItemName}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${auth_token}`
                },
                body: JSON.stringify({
                    new_name: newItem.name,
                    price: newItem.price,
                    image_url: newItem.imageUrl,
                    visible: newItem.visibility,
                }),
            });
    
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data.message);
    
            // Fetch items again to update the page state
            fetchItems(categoryName);
        } catch (error) {
            console.error(`Error editing item '${oldItemName}':`, error);
        }
    
        setEditItem({active: false, item: null});
    };

    const handleDeleteItem = async (item, categoryName) => {
        const itemName = item.name;
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${categoryName}/${itemName}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `${auth_token}`
                }
            });
    
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data.message);
    
            // Fetch items again to update the page state
            fetchItems(categoryName);
        } catch (error) {
            console.error(`Error deleting item '${itemName}':`, error);
        }
        setDeleteItem({active: false, item: null, categoryName: null});
    };

    const handleVisibilityCategory = async (categoryName, visible) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${categoryName}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${auth_token}`
                },
                body: JSON.stringify({
                    visible: String(visible),
                }),
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
            console.error(`Error changing visibility of category '${categoryName}':`, error);
        }
    };
    
    
    
    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied userType={userType}/>
    }


    return (
        <div className="customerPage">
            <Header userType={userType} currentPage="menu-editor" />
            <div className="editorContainer">
                <div className="categories">
                    <Button 
                        variant="contained" 
                        onClick={() => setShowAddCategoryModal(true)} 
                        sx={{marginBottom: '10px'}}
                        startIcon={<Add />}
                    >
                        Add New Category
                    </Button>
                    <Button 
                        variant="contained" 
                        onClick={() => setShowAddItemModal(true)}
                        startIcon={<Add />}
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
                            <div className="editFunctionality">
                            {category.visible ? 
                                <Visibility onClick={(e) => {e.stopPropagation(); handleVisibilityCategory(category.name, "False")}}/> 
                                : 
                                <VisibilityOff onClick={(e) => {e.stopPropagation(); handleVisibilityCategory(category.name, "True")}}/>
                            }
                                <p style={category.visible ? {} : {textDecoration: 'line-through'}}>{category.name}</p>
                                <div>
                                    <Edit onClick={(e) => {e.stopPropagation(); setEditCategory({active: true, category: category.name})}}/>
                                    <Delete onClick={(e) => {e.stopPropagation(); setDeleteCategory({active: true, category: category.name})}}/>
                                </div>
                            </div>
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
                                <div className="editDeleteIcons">
                                    <Edit onClick={(e) => {e.stopPropagation(); setEditItem({active: true, item})}}/>
                                    <Delete onClick={(e) => {e.stopPropagation(); setDeleteItem({active: true, item: item, categoryName: currentCategory})}}/>
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

            {editCategory.active && 
                <EditCategoryModal 
                    open={editCategory.active} 
                    onClose={() => setEditCategory({active: false, category: ""})} 
                    onSave={handleEditCategory}
                    oldCategoryName={editCategory.category}
                />
            }   

            {deleteCategory.active && 
                <DeleteConfirmationModal 
                    open={deleteCategory.active} 
                    onClose={() => setDeleteCategory({active: false, category: ""})} 
                    onConfirm={() => handleDeleteCategory(deleteCategory.category)}
                    objectName={deleteCategory.category}
                />
            }       

            {editItem.active && 
                <EditItemModal 
                    open={editItem.active} 
                    onClose={() => setEditItem({active: false, item: null})} 
                    onSave={handleEditItem}
                    oldItem={editItem.item}
                />
            }   

            {deleteItem.active && 
                <DeleteConfirmationModal 
                    open={deleteItem.active} 
                    onClose={() => setDeleteItem({active: false, item: null})} 
                    onConfirm={() => handleDeleteItem(deleteItem.item, deleteItem.categoryName)}
                    objectName={deleteItem.item.name}
                />
            }
        </div>
    )
};
