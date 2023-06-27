import React from 'react';
import { Modal, Box } from '@mui/material';

export default function BillModal({ orders, onClose }) {

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
                <h2>Bill</h2>
                {/* {orders.map((order, index) => (
                    <div key={index} className="billOrder">
                        <p>{order.name}</p>
                        <p>{order.quantity}</p>
                        <p>${order.price}</p>
                    </div>
                ))} */}
                <button onClick={onClose}>Close</button>
            </Box>
        </Modal>
    );
};