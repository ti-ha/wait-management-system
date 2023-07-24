import React, { useState, useEffect } from 'react';
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
    const [serviceRequests, setServiceRequests] = useState([]);

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

    const fetchServiceRequests = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/servicerequests/queue`, {
                headers: { 'Authorization': `${auth_token}` }
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            console.log(`The service requests being returned are ${data.serviceRequests}`);
            setServiceRequests(data.queue || []);
        } catch (error) {
            console.error("Error fetching service requests:", error);
            setServiceRequests([]);
        }
    }

    useEffect(() => {
        fetchOrders()
        fetchServiceRequests();
        const intervalId = setInterval(() => {
            fetchOrders();
            fetchServiceRequests();
        }, 10000);
        return () => clearInterval(intervalId);
    }, []);

    


    const allMenuItems = orders.flatMap((order) =>
        order.menu_items.map((item) => ({ ...item, order_id: order.id, table_id: order.table_id }))
    );

    const toBeServedOrders = allMenuItems.filter((item) => item.state === 'ready');

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

    const updateServiceRequest = async (serviceRequestId) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/servicerequests/${serviceRequestId}/state`, {
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

            // Refetch service requests to ensure page is updated with the latest request states.
            fetchServiceRequests();

        } catch (error) {
            console.error("Error completing service request:", error);
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
                    {toBeServedOrders.map((item, index) => (
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
                <section className='assistanceRequired'>
                <h2>Assistance Required</h2>
                <div className="subheadings">
                    <h3>Table No</h3>
                    <h3>Pending</h3>
                    <h3>In Progress</h3>
                </div>
                {serviceRequests.map((request, index) => (
                    <div key={index} className='requestBox'>
                        <p>Table {request.table + 1}</p>
                        <Button 
                            className={request.status === 'ready' ? 'visible' : 'hidden'}
                            variant="contained"
                            onClick={() => updateServiceRequest(request.id)}>Mark In Progress</Button>
                        <Button 
                            className={request.status === 'in_progress' ? 'visible' : 'hidden'}
                            variant="contained" 
                            onClick={() => updateServiceRequest(request.id)}>Mark as Done</Button>
                    </div>
                ))}
            </section>
            </main>
        </div>
    )
}