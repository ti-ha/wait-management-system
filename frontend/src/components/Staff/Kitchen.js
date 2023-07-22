import React, { useState, useEffect } from 'react';
import './Kitchen.css';
import { Button } from '@mui/material';
import { Check } from '@mui/icons-material';
import { useIsStaffMember } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';

export default function Kitchen() {

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsStaffMember();
    const userType = localStorage.getItem('user_type');

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
            setOrders(data.orders || []);
        } catch (error) {
            console.error("Error fetching orders:", error);
            setOrders([]);
        }
    }

    useEffect(() => {
        fetchOrders()
    }, []);

    const allMenuItems = orders.flatMap((order) =>
        order.menu_items.map((item) => ({ ...item, order_id: order.id, table_id: order.table_id }))
    );
    const receivedItems = allMenuItems.filter((item) => item.state === 'ordered');
    const preparingItems = allMenuItems.filter((item) => item.state === 'cooking');


    const updateOrderState = async (orderId, menuItemId) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/orders/${orderId}/${menuItemId}/state`, {
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
            <Header userType={userType} currentPage="kitchen" />

            <main className="kitchenBody">
                <section className='ordersReceived'>
                    <h2>Orders Received</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Item</h3>
                        <h3>Ready to Prepare</h3>
                    </div>
                    {receivedItems.map((item, index) => (
                        <div key={index} className='orderBox'>
                            <p>Table {item.table_id + 1}</p>
                            <p>{item.name}</p>
                            <Button 
                                variant="contained" 
                                startIcon={<Check />}
                                onClick={() => updateOrderState(item.order_id, item.order_specific_id)}>Ready</Button>
                        </div>
                    ))}
                </section>
                <section className='preparing'>
                    <h2>Preparing</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Item</h3>
                        <h3>Ready to Serve</h3>
                    </div>
                    {preparingItems.map((item, index) => (
                        <div key={index} className='orderBox'>
                            <p>Table {item.table_id + 1}</p>
                            <p>{item.name}</p>
                            <Button 
                                variant="contained" 
                                startIcon={<Check />}
                                onClick={() => updateOrderState(item.order_id, item.order_specific_id)}>Ready</Button>
                        </div>
                    ))}
                </section>
            </main>
        </div>
    )
}