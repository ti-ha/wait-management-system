import React, { useEffect, useState } from 'react';
import { Modal, Box, Button } from '@mui/material';
import './BillModal.css'

export default function BillModal({ orders, onClose }) {

    const [total, setTotal] = useState(0);

    function aggregateOrders(orders) {
        let itemsMap = {};
    
        orders.forEach(order => {
            // Create a mapping of deals for easy lookup
            let dealsMap = {};
            order.deals.forEach(deal => {
                deal.menu_items.forEach(item => {
                    dealsMap[item.id] = item;
                });
            });

            order.menu_items.forEach(item => {
                // Use the price from the deal if it exists, otherwise use the regular price
                const price = dealsMap[item.id] ? dealsMap[item.id].price : item.price;
                if (itemsMap[item.name]) {
                    itemsMap[item.name].quantity += 1;
                    itemsMap[item.name].price = price; 
                } else {
                    itemsMap[item.name] = {
                        ...item,
                        price: price, 
                        quantity: 1
                    };
                }
            });
        });
    
        return Object.values(itemsMap);
    }

    const aggregatedOrders = aggregateOrders(orders);

    useEffect(() => {
        let totalCost = 0;
        aggregatedOrders.forEach(item => {
            totalCost += item.price * item.quantity;
        });
        setTotal(totalCost);
    }, [aggregatedOrders]);

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
                        <p>${(item.price * item.quantity).toFixed(2)}</p>
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