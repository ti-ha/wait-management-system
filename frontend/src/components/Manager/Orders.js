import React, { useState, useEffect } from 'react';
import { useIsStaffMember } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from "../Common/Header.js";
import BillModal from '../Customer/BillModal.js';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, IconButton, Tooltip, Grid} from '@mui/material';
import { Refresh } from "@mui/icons-material"

export default function Orders() {

    const auth_token = localStorage.getItem('token'); 

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsStaffMember();
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

            // Initialise bill for every table in orders
            const tableIds = [...new Set(data.history.map(order => order.table_id))];
            for(let tableId of tableIds) {
                await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/tables/${tableId}/bill`)
            }

            setOrders(data.history);
        } catch (error) {
            console.error("Error fetching orders:", error);
        }
    }

    const payBill = async (table_id) => {
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

            // Fetch all orders again to update the page state
            await fetchAllOrders();
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

    const currentOrders = orders.filter(order => order.state !== "completed");
    const completedOrders = orders.filter(order => order.state === "completed");

    return (
        <>
            <Header userType={userType} currentPage="orders" />

            <h1 style={{textAlign: 'center'}}>Current Orders</h1>
            <div style={{maxWidth: '1600px', margin: 'auto'}}>
                <div style={{display: 'flex', justifyContent: 'flex-end'}}>
                    <Tooltip title="Refresh Orders">
                        <IconButton onClick={fetchAllOrders}>
                            <Refresh />
                        </IconButton>
                    </Tooltip>
                </div>

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
                            <TableCell sx={{ width: '25%' }}>{order.table_id + 1}</TableCell>
                            <TableCell sx={{ width: '25%' }}>${order.bill?.price.toFixed(2)}</TableCell>
                            <TableCell sx={{ width: '25%' }} align="right">
                                <Grid container spacing={2}>
                                    <Grid item xs={6}>
                                        <Button variant="contained" color="secondary" fullWidth onClick={() => handleViewBill(order)}>View Bill</Button>
                                    </Grid>
                                    <Grid item xs={6}>
                                        {order.state === 'served' ? (
                                            <Button variant="contained" color="primary" fullWidth onClick={() => payBill(order.table_id)}>Mark as Paid</Button>
                                        ) : (
                                            <Button variant="contained" disabled fullWidth>Order Pending</Button>
                                        )}
                                    </Grid>
                                </Grid>
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
                                    <TableCell sx={{ width: '25%' }}>Order Id</TableCell>
                                    <TableCell sx={{ width: '25%' }}>Table Number</TableCell>
                                    <TableCell sx={{ width: '25%' }}>Total</TableCell>
                                    <TableCell sx={{ width: '25%' }} align="right">Actions</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                            {completedOrders.map((order) => (
                                <TableRow
                                key={order.id}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell>{order.id}</TableCell>
                                    <TableCell>{order.table_id + 1}</TableCell>
                                    <TableCell>${order.bill.price.toFixed(2)}</TableCell>
                                    <TableCell align="right">
                                        <Button variant="contained" color="secondary" onClick={() => handleViewBill(order)}>View Bill</Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </Box>
            {currentOrder && <BillModal orders={[currentOrder]} onClose={handleCloseModal} table_id={currentOrder.table_id}/>}
        </>
    )
}