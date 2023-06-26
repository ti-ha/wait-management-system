import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import './Kitchen.css'
import { Button } from '@mui/material'
import { Check } from '@mui/icons-material';
import { OrderContext } from '../../contexts/OrderContext.js'

export default function Kitchen() {

    const { orders } = useContext(OrderContext)

    return (
        <div className="kitchenContainer">
            <header className="kitchenHeader">
                <h1>Kitchen View</h1>
                <div className='headerButtons'>
                    <Link to="/wait-staff">
                        <Button variant="contained">
                            Switch to Wait Staff View
                        </Button>
                    </Link>
                    <Link to="/">
                        <Button variant="contained">
                            Landing Page
                        </Button>
                    </Link>
                </div>
            </header>

            <main className="kitchenBody">
                <section className='ordersReceived'>
                    <h2>Orders Received</h2>
                    <div className="subheadings">
                        <h3>Table No</h3>
                        <h3>Item</h3>
                        <h3>Ready to Prepare</h3>
                    </div>
                    {orders.map((order, index) => (
                        <div key={index} className='orderBox'>
                            <p>{order.tableNumber}</p>
                            <p>{order.name}</p>
                            <Button variant="contained" startIcon={<Check />}>Ready</Button>
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
                </section>
            </main>
        </div>
    )
}