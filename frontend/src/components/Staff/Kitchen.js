import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Kitchen.css';
import { Button } from '@mui/material';
import { Check } from '@mui/icons-material';
import { useIsStaffMember } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';

export default function Kitchen() {

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsStaffMember();

    const [orders, setOrders] = useState([]);

    const auth_token = localStorage.getItem('token'); 

    const fetchOrders = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager`, {
                headers: { 'Authorization': `${auth_token}` }
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            console.log(`The data being returned is ${data.orders}`);
            setOrders(data.orders || []);
        } catch (error) {
            console.error("Error fetching orders:", error);
            setOrders([]);
        }
    }

    useEffect(() => {
        fetchOrders()
    }, []);

    const receivedOrders = orders.filter(order => order.state === 'ordered');
    const preparingOrders = orders.filter(order => order.state === 'cooking');

    const updateOrderState = async (orderId) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/orders/${orderId}/state`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${auth_token}`
                }
            });

            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }

            // Refetch orders to ensure page is updated with the latest order states.
            fetchOrders();

        } catch (error) {
            console.error("Error updating order state:", error);
        }
    }

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied />
    }


    return (
        <div className="kitchenContainer">
            <header className="kitchenHeader">
                <h1>Kitchen View</h1>
                <div className='headerButtons'>
                    <Link to="/wait-staff">
                        <Button variant="contained">
                            Switch to Wait Staff View
                        </Button>
                    </Link>
                    <Link to="/">
                        <Button variant="contained">
                            Landing Page
                        </Button>
                    </Link>
                </div>
            </header>

            <main className="kitchenBody">
                <section className='ordersReceived'>
                    <h2>Orders Received</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Item</h3>
                        <h3>Ready to Prepare</h3>
                    </div>
                    {receivedOrders && receivedOrders.flatMap((order, index) =>
                        order.menu_items.map((item, itemIndex) => (
                            <div key={`${index}-${itemIndex}`} className='orderBox'>
                                <p>Table {order.table_id + 1}</p>
                                <p>{item.name}</p>
                                <Button 
                                    variant="contained" 
                                    startIcon={<Check />}
                                    onClick={() => updateOrderState(order.id)}>Ready</Button>
                            </div>
                        ))
                    )}
                </section>
                <section className='preparing'>
                    <h2>Preparing</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Item</h3>
                        <h3>Ready to Serve</h3>
                    </div>
                    {preparingOrders && preparingOrders.flatMap((order, index) =>
                        order.menu_items.map((item, itemIndex) => (
                            <div key={`${index}-${itemIndex}`} className='orderBox'>
                                <p>Table {order.table_id + 1}</p>
                                <p>{item.name}</p>
                                <Button 
                                    variant="contained" 
                                    startIcon={<Check />}
                                    onClick={() => updateOrderState(order.id)}>Ready</Button>
                            </div>
                        ))
                    )}
                </section>
            </main>
        </div>
    )
}