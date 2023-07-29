import React, { useEffect, useState } from 'react';
import { Modal, Box, Button } from '@mui/material';
import './BillModal.css'

export default function BillModal({ orders, onClose, table_id }) {

    const [total, setTotal] = useState(0);

    function aggregateOrders(orders) {
        let itemsMap = {};
    
        orders.forEach(order => {
            order.menu_items.forEach(item => {
                if (itemsMap[item.name]) {
                    itemsMap[item.name].quantity += 1;
                } else {
                    itemsMap[item.name] = {
                        ...item,
                        quantity: 1
                    };
                }
            });
        });
    
        return Object.values(itemsMap);
    }

    const aggregatedOrders = aggregateOrders(orders);

    useEffect(() => {
        const fetchTotalBill = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/ordermanager/tables/${table_id}/bill`);
                if (!response.ok) { 
                    const responseBody = await response.json();
                    console.error('Server response:', responseBody); 
                    throw new Error(`HTTP Error with status: ${response.status}`);
                }
                const data = await response.json();
                setTotal(data.price);
            } catch (error) {
                console.error("Error fetching total bill:", error);
            }
        };
        fetchTotalBill();
    }, [orders]);


    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
    };

    return (
        <Modal
            open={true}
            onClose={onClose}
        >
            <Box sx={style}>
                <h2 >Bill</h2>
                <div className="billOrder">
                    <strong>Item Name</strong>
                    <strong>Quantity</strong>
                    <strong>Price</strong>
                </div>
                {aggregatedOrders.map((item, index) => (
                    <div key={index} className="billOrder">
                        <p>{item.name}</p>
                        <p>{item.quantity}</p>
                        <p>${item.price.toFixed(2)}</p>
                    </div>
                ))}
                <div className="billOrder">
                    <strong>Total:</strong>
                    <strong>${total.toFixed(2)}</strong>
                </div>
                <Button variant="contained" onClick={onClose}>Close</Button>
            </Box>
        </Modal>
    );
};