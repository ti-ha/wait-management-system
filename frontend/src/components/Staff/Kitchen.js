import React from 'react'
import { Link } from 'react-router-dom'
import './Kitchen.css'
import { Button } from '@mui/material'

export default function Kitchen() {
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
                </section>
                <section className='preparing'>
                    <h2>Preparing</h2>
                </section>
            </main>
        </div>
    )
}