import React from 'react';

export default function BillModal({ orders, onClose }) {
    return (
        <div className="billModal">
            <h2>Bill</h2>
            {orders.map((order, index) => (
                <div key={index} className="billOrder">
                    <p>{order.name}</p>
                    <p>{order.quantity}</p>
                    <p>${order.price}</p>
                </div>
            ))}
            <button onClick={onClose}>Close</button>
        </div>
    );
};