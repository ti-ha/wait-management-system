import React from 'react';
import { Modal, Box, Button } from '@mui/material';
import './BillModal.css'

export default function BillModal({ orders, onClose }) {

    console.log(orders)

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

    // const total = orders.reduce((sum, order) => {
    //     return sum + order.menu_items.reduce((itemSum, item) => itemSum + item.price, 0);
    // }, 0);

    const total = aggregatedOrders.reduce((sum, item) => {
        return sum + (item.quantity * item.price);
    }, 0);

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