import React, { useState, useEffect, useContext } from "react";
import { Link, useParams } from 'react-router-dom';
import ItemModal from "./ItemModal.js";
import BillModal from "./BillModal.js";
import { IconButton, TextField, Button, Grid, Card, CardContent, Typography, Box, CardMedia, CardActions, Modal } from '@mui/material';
import { Add, Remove } from "@mui/icons-material"
import useDebounce from "../Hooks/useDebounce.js";
import Header from "../Common/Header.js";


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

    const [assistanceModalOpen, setAssistanceModalOpen] = useState(false);



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
    useEffect(() => {
        fetchPersonalisedDeals();
    }, []);
    

    const fetchItems = async (category) => {
        let data;
        if (category === 'Personalised Deals') {
            data = personalisedDeals;
            
            // Extract all menu items from each deal and apply discount
            let allMenuItems = data.flatMap(deal => {
                return deal.menu_items.map(item => ({
                    ...item, 
                    price: (item.price * (1 - deal.discount)).toFixed(2) // Apply the discount
                }));
            });
            setCurrentItems(allMenuItems);
        } else {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`);
            data = await response.json();
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
        const deals = personalisedDeals.map(deal => ({ id: deal.id }));

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
            fetchPersonalisedDeals();
            fetchItems(currentCategory);
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

            // Don't include order in bill if it is paid
            const filteredOrders = data.orders.filter(order => order.bill === null || order.bill.paid === false);
            setBillOrders(filteredOrders);
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
        setAssistanceModalOpen(true);
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

    useEffect(() => {
        let timer;
        if (assistanceModalOpen) {
            timer = setTimeout(() => {
                setAssistanceModalOpen(false);
            }, 3000);
        }
        return () => clearTimeout(timer);
    }, [assistanceModalOpen]);

    return (
        <>
            <Header userType='customer' currentPage="/customer" />
            <Box 
                sx={{ 
                    display: 'flex', 
                    flexDirection: 'column', 
                    justifyContent: 'flex-start', 
                    alignItems: 'center',
                    minHeight: '100vh',
                    maxWidth: '1600px', 
                    margin: 'auto',
                    pt: 10
                }}
            >


                <Grid container spacing={3}>
                    <Grid item xs={12} md={3}>
                        <Box sx={{ marginLeft: '20px', marginRight: '20px' }}>
                            <TextField
                                value={searchInput}
                                onChange={handleSearchChange}
                                label="Search"
                                variant="outlined"
                                sx={{marginBottom: '50px', display: 'flex', marginLeft: 'auto', marginRight: 'auto'}}
                            />

                            {categories
                                .filter(category => category.visible)
                                .map((category, index) => (
                                <Card 
                                    key={index} 
                                    onClick={() => handleCategoryClick(category.name)}
                                    sx={{ marginBottom: '10px', cursor: 'pointer', background: category.name === currentCategory ? '#808080' : '#f0f0f0' }}
                                >
                                    <CardContent>
                                        <Typography align="center">{category.name}</Typography>
                                    </CardContent>
                                </Card>
                            ))}
                            {personalisedDeals.length > 0 && (
                                <Card 
                                    onClick={() => handleCategoryClick('Personalised Deals')}
                                    sx={{ marginBottom: '10px', cursor: 'pointer', background: 'Personalised Deals' === currentCategory ? '#808080' : '#ffcc00' }}
                                >
                                    <CardContent>
                                        <Typography align="center">Personalised Deals</Typography>
                                    </CardContent>
                                </Card>
                            )}
                        </Box>
                    </Grid>

                    <Grid item xs={12} md={5}>
                        {(currentItems.length > 0 && (!searchResults)) &&
                            <Typography variant="h4" align="center" gutterBottom>{currentCategory}</Typography>
                        }
                        {(searchResults && Object.keys(searchResults).length !== 0) &&
                            <Typography variant="h4" align="center" gutterBottom>Search Results</Typography>
                        }
                        <Grid container spacing={3}>
                            {searchResults ? 
                                (
                                Object.keys(searchResults).length !== 0 ? 
                                    Object.values(searchResults).flat().map((item, index) => (
                                        <Grid item xs={12} sm={6} key={index}>
                                            <Card onClick={() => handleOpenModal(item)}>
                                                <CardMedia
                                                    component="img"
                                                    alt={item.name}
                                                    height="140"
                                                    image={item.imageURL}
                                                    title={item.name}
                                                />
                                                <CardContent>
                                                    <Typography gutterBottom variant="h5" component="div">
                                                        {item.name}
                                                    </Typography>
                                                    <Typography variant="body2" color="text.secondary">
                                                        ${item.price}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                    ))
                                :
                                    <Typography variant="h5" align="center" gutterBottom>No Results Found</Typography>
                                )   
                                :
                                    currentItems.map((item, index) => (
                                        <Grid item xs={12} sm={6} key={index}>
                                            <Card onClick={() => handleOpenModal(item)}>
                                                <CardMedia
                                                    component="img"
                                                    alt={item.name}
                                                    height="140"
                                                    image={item.imageURL}
                                                    title={item.name}
                                                />
                                                <CardContent>
                                                    <Typography gutterBottom variant="h5" component="div">
                                                        {item.name}
                                                    </Typography>
                                                    <Typography variant="body2" color="text.secondary">
                                                        ${item.price}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                    ))
                            }
                        </Grid>
                    </Grid>

                    <Grid item xs={12} md={4}>
                        <Typography variant="h4" align="center" gutterBottom>
                            Table {tableNumber}
                        </Typography>
                        <Card sx={{ mb: 3, minHeight: '500px' }}>
                            <CardContent>
                                <Typography variant="h5" textAlign="center" gutterBottom>
                                    Current Order
                                </Typography>
                                {currentOrder.map((order, index) => (
                                    <Card key={index} sx={{ mb: 1 }}>
                                        <CardContent sx={{ py: 1 }}>
                                            <Grid container justifyContent="space-between" alignItems="center">
                                                <Grid item>
                                                    <Typography variant="body1">{order.name}</Typography>
                                                </Grid>
                                                <Grid item>
                                                    <Grid container alignItems="center" spacing={1}>
                                                        <Grid item>
                                                            <IconButton size="small" onClick={() => updateQuantity(order.id, -1)}>
                                                                <Remove />
                                                            </IconButton>
                                                        </Grid>
                                                        <Grid item>
                                                            <Typography variant="body1">{order.quantity}</Typography>
                                                        </Grid>
                                                        <Grid item>
                                                            <IconButton size="small" onClick={() => updateQuantity(order.id, 1)}>
                                                                <Add />
                                                            </IconButton>
                                                        </Grid>
                                                    </Grid>
                                                </Grid>
                                                <Grid item>
                                                    <Typography variant="body1">${order.price}</Typography>
                                                </Grid>
                                            </Grid>
                                        </CardContent>
                                    </Card>
                                ))}
                            </CardContent>
                            <CardActions sx={{ display: 'flex', justifyContent: 'center' }}>
                                {currentOrder.length >0 &&
                                    <Button variant="contained" sx={{ width: 200 }} onClick={sendOrderToKitchen}>
                                        Send Order
                                    </Button> 
                                }
                            </CardActions>
                        </Card>
                        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <Button variant="contained" sx={{ mb: 1, width: 200 }} onClick={fetchBill}>
                                View Bill
                            </Button>
                            <Button variant="contained" sx={{ width: 200 }} onClick={sendAssistanceRequest}>
                                Request Assistance
                            </Button>
                            <Modal
                                open={assistanceModalOpen}
                                onClose={() => setAssistanceModalOpen(false)} 
                            >
                                <Box
                                    sx={{
                                        position: 'absolute',
                                        top: '50%',
                                        left: '50%',
                                        transform: 'translate(-50%, -50%)',
                                        width: 200,
                                        bgcolor: 'background.paper',
                                        border: '2px solid #000',
                                        boxShadow: 24,
                                        p: 4,
                                        textAlign: 'center'
                                    }}
                                >
                                    <p>Assistance Requested!</p>
                                </Box>
                            </Modal>
                        </Box>
                    </Grid>


                </Grid>
            </Box>

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
        </>
    )
};