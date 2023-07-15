import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './WaitStaff.css';
import { Button } from '@mui/material';
import { Check } from '@mui/icons-material';
import { useIsStaffMember } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';


export default function WaitStaff() {

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsStaffMember();
    const userType = localStorage.getItem('user_type');

    const [orders, setOrders] = useState([]);

    const fetchOrders = async () => {
        try {
            const auth_token = localStorage.getItem('token'); 
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

    const toBeServedOrders = orders.filter(order => order.state === 'ready');

    const updateOrderState = async (orderId) => {
        try {
            const auth_token = localStorage.getItem('token');
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
        <div className="waitStaffContainer">
            <Header userType={userType} currentPage="wait-staff" />

            <main className="waitStaffBody">
                <section className='toBeServed'>
                    <h2>To Be Served</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Item</h3>
                        <h3>Served</h3>
                    </div>
                    {toBeServedOrders && toBeServedOrders.flatMap((order, index) =>
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
                <section className='assistanceRequired'>
                    <h2>Assistance Required</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Done</h3>
                    </div>
                </section>
            </main>
        </div>
    )
}