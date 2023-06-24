import React from 'react'
import { Link } from 'react-router-dom'
import './WaitStaff.css'
import { Button } from '@mui/material'

export default function WaitStaff() {
    return (
        <div className="waitStaffContainer">
            <header className="waitStaffHeader">
                <h1>Wait Staff View</h1>
                <div className='headerButtons'>
                    <Link to="/kitchen">
                        <Button variant="contained">
                            Switch to Kitchen View
                        </Button>
                    </Link>
                    <Link to="/">
                        <Button variant="contained">
                            Landing Page
                        </Button>
                    </Link>
                </div>
            </header>

            <main className="waitStaffBody">
                <section className='toBeServed'>
                    <h2>To Be Served</h2>
                </section>
                <section className='assistanceRequired'>
                    <h2>Assistance Required</h2>
                </section>
            </main>
        </div>
    )
}