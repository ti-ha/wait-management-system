import React, { useState, useEffect, useContext } from "react";
import { Link, useParams } from 'react-router-dom';
import ItemModal from "./ItemModal.js";
import BillModal from "./BillModal.js";
import './Customer.css'
import { Button, IconButton, TextField } from "@mui/material";
import { Add, Remove } from "@mui/icons-material"
import useDebounce from "../Hooks/useDebounce.js";


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
    const [personalisedDeals, setPersonalisedDeals] = useState([]);


    const [searchInput, setSearchInput] = useState("");
    const [searchResults, setSearchResults] = useState(null);
    const debouncedSearchTerm = useDebounce(searchInput, 500);

    useEffect(() => {
        if (debouncedSearchTerm) {
            fetchSearchResults(debouncedSearchTerm);
        } else {
            setSearchResults(null);
        }
    }, [debouncedSearchTerm]);

    const fetchSearchResults = async (query) => {
        console.log(`The query is ${query}`)
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/search?query=${query}`);
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            console.log(`The search results are`, data)
            setSearchResults(data);
        } catch (error) {
            console.error("Error searching menu:", error);
        }
    }

    const handleSearchChange = (event) => {
        setSearchInput(event.target.value);
    }


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
                
                // Find the first visible category
                const firstVisibleCategory = data.find(category => category.visible);
                if (firstVisibleCategory) {
                    setCurrentCategory(firstVisibleCategory.name);
                    fetchItems(firstVisibleCategory.name);
                }

            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        }
        fetchCategories();
    }, []);

    useEffect(() => {
        const fetchPersonalisedDeals = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/personalised/deals`);
                if (!response.ok) { 
                    const responseBody = await response.json();
                    console.error('Server response:', responseBody); 
                    throw new Error(`HTTP Error with status: ${response.status}`);
                }
                const data = await response.json();
                setPersonalisedDeals(data);
            } catch (error) {
                console.error("Error fetching personalised deals:", error);
            }
        }
        fetchPersonalisedDeals();
    }, []);
    

    const fetchItems = async (category) => {
        let data;
        if (category === 'Personalised Deals') {
            data = personalisedDeals;
            
            // Extract all menu items from each deal
            let allMenuItems = data.flatMap(deal => deal.menu_items);
            console.log(`the personalised deals are:`, allMenuItems)
            setCurrentItems(allMenuItems);
        } else {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`);
            data = await response.json();
            console.log(' the normal items are: ', data)
            setCurrentItems(data.menu_items);
        }
    }

    const handleCategoryClick = (category) => {
        setSearchResults(null);
        setSearchInput("");
        setCurrentCategory(category);
        fetchItems(category);
    };

    const handleOpenModal = (item) => {
        console.log('The selected item is', item)
        setSelectedItem(item);
    }

    const handleCloseModal = () => {
        setSelectedItem(null);
        setQuantity(1);
    }

    const handleAddToOrder = () => {
        setCurrentOrder(prevOrder => {
            // Check if the item already exists in the order
            const existingOrderItem = prevOrder.find(order => order.id === selectedItem.id);
            
            // If the item exists, increment its quantity
            if (existingOrderItem) {
                return prevOrder.map(order => {
                    if (order.id === selectedItem.id) {
                        return { ...order, quantity: order.quantity + quantity };
                    }
                    return order;
                });
            }
            
            // If the item does not exist, add a new order item
            const newOrder = { tableNumber, ...selectedItem, quantity };
            return [...prevOrder, newOrder];
        });
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

    const sendAssistanceRequest = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/servicerequests/queue`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    subject: "",
                    summary: "",
                    table_id: tableNumber - 1 
                })
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            console.log('Assistance request sent successfully');
        } catch (error) {
            console.error('Error sending assistance request:', error);
        }
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
                    <TextField
                        value={searchInput}
                        onChange={handleSearchChange}
                        label="Search"
                        variant="outlined"
                        sx={{marginBottom: '50px'}}
                    />
                    <h2>Menu</h2>
                    {categories
                        .filter(category => category.visible)
                        .map((category, index) => (
                        <div 
                            key={index} 
                            className={`${category.name === currentCategory ? "selectedCategoryBox" : "categoryBox"}`}
                            onClick={() => handleCategoryClick(category.name)}
                        >
                            <p>{category.name}</p>   
                        </div>
                    ))}
                    <div 
                        className={`${'Personalised Deals' === currentCategory ? "selectedPersonalisedDealBox" : "personalisedDealBox"}`}
                        onClick={() => handleCategoryClick('Personalised Deals')}
                    >
                        <p>Personalised Deals</p>
                    </div>
                </div>

                <div className="items">
                    {(currentItems.length > 0 && (!searchResults)) &&
                        <h2 className="itemsTitle">{currentCategory}</h2>
                    }
                    {(searchResults && Object.keys(searchResults).length !== 0) &&
                        <h2 className="itemsTitle">Search Results</h2>
                    }
                        <div className="itemContainer">
                            {searchResults ? 
                                (
                                Object.keys(searchResults).length !== 0 ? 
                                <>
                                    {Object.values(searchResults).flat().map((item, index) => (
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
                                </>
                                :
                           
                                <h2>No Results Found</h2>
                         
                            )   
                            :
                                currentItems.map((item, index) => (
                                    <div className="itemBox" key={index} onClick={() => handleOpenModal(item)}>
                                        <div className="imageContainer">
                                            <img src={item.imageURL} alt={item.name}/> 
                                        </div>
                                        <div className="itemInfo">
                                            <p>{item.name}</p>
                                            <p>${item.price}</p>
                                        </div>
                                    </div>
                                ))
                            }
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

                    <Button style={{ marginTop: "10px" }} variant="contained" onClick={fetchBill}>
                        View Bill
                    </Button>

                    <Button style={{ marginTop: "10px" }} variant="contained" onClick={sendAssistanceRequest}>
                        Request Assistance
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