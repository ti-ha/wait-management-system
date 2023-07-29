import React, { useState, useEffect } from 'react';
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from "../Common/Header.js";
import BillModal from '../Customer/BillModal.js';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box } from '@mui/material';



export default function Orders() {

    const auth_token = localStorage.getItem('token'); 

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    const [orders, setOrders] = useState([]);
    const [currentOrder, setCurrentOrder] = useState(null);

    const handleViewBill = (order) => {
        setCurrentOrder(order);
    }

    const handleCloseModal = () => {
        setCurrentOrder(null);
    }


    const fetchAllOrders = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/history`, {
                headers: { 'Authorization': `${auth_token}` }
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            setOrders(data.history);
        } catch (error) {
            console.error("Error fetching orders:", error);
        }
    }

    const payBill = async (table_id) => {
        table_id = 0
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/tables/${table_id}/bill`, {
                method: 'POST'
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            console.log(data.message);
        } catch (error) {
            console.error("Error paying bill:", error);
        }
    }
    
    useEffect(() => {
        fetchAllOrders()
        const intervalId = setInterval(fetchAllOrders, 10000);
        return () => clearInterval(intervalId);
    }, []);

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied userType={userType}/>
    }

    const currentOrders = orders.filter(order => order.bill.paid === false);
    const completedOrders = orders.filter(order => order.bill.paid === true);



    return (
        <>
            <Header userType={userType} currentPage="order-history" />

            <h1 style={{textAlign: 'center'}}>Current Orders</h1>
            <div style={{maxWidth: '1600px', margin: 'auto'}}>

                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                        <TableRow>
                            <TableCell>Order Id</TableCell>
                            <TableCell>Table Number</TableCell>
                            <TableCell>Total</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                        </TableHead>
                        <TableBody>
                        {currentOrders.map((order) => (
                            <TableRow
                            key={order.id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                            <TableCell sx={{ width: '25%' }}>{order.id}</TableCell>
                            <TableCell sx={{ width: '25%' }}>{order.table_number}</TableCell>
                            <TableCell sx={{ width: '25%' }}>${order.bill.price.toFixed(2)}</TableCell>
                            <TableCell sx={{ width: '25%' }} align="right">
                            <Button variant="contained" color="secondary" onClick={() => handleViewBill(order)}>View Bill</Button>
                            <Button variant="contained" color="primary" onClick={() => payBill(order.table_id)}>Mark as Paid</Button>
                            </TableCell>
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>

            <Box mt={10}>
                <h1 style={{textAlign: 'center'}}>Completed Orders</h1>
                <div style={{maxWidth: '1600px', margin: 'auto'}}>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 650 }} aria-label="simple table">
                            <TableHead>
                            <TableRow>
                                <TableCell>Order Id</TableCell>
                                <TableCell>Table Number</TableCell>
                                <TableCell>Total</TableCell>
                                <TableCell align="right">Actions</TableCell>
                            </TableRow>
                            </TableHead>
                            <TableBody>
                            {completedOrders.map((order) => (
                                <TableRow
                                key={order.id}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                <TableCell>{order.id}</TableCell>
                                <TableCell>{order.table_number}</TableCell>
                                <TableCell>${order.bill.price.toFixed(2)}</TableCell>
                                <TableCell align="right">
                                    <Button variant="contained" color="secondary">View Bill</Button>
                                </TableCell>
                                </TableRow>
                            ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </Box>
            {currentOrder && <BillModal orders={[currentOrder]} onClose={handleCloseModal} table_id={currentOrder.id}/>}
        </>
    )
}