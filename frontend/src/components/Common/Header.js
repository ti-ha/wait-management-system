import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@mui/material";
import './Header.css'

export default function Header ({ userType, currentPage }) {

    const isManager = userType === 'Manager';

    return (
        <header className="headerContainer">
            <div className="headerButtonsLeft">
                {isManager &&
                    <>
                        <Link to="/menu-editor">
                            <Button variant="contained" disabled={currentPage === 'menu-editor'}>
                                Menu Editor
                            </Button>
                        </Link>
                        <Link to="/restaurant-manager">
                            <Button variant="contained" disabled={currentPage === 'restaurant-manager'}>
                                Restaurant Manager
                            </Button>
                        </Link>
                    </>
                }
                <Link to="/kitchen">
                    <Button variant="contained" disabled={currentPage === 'kitchen'}>
                        Kitchen View
                    </Button>
                </Link>
                <Link to="/wait-staff">
                    <Button variant="contained" disabled={currentPage === 'wait-staff'}>
                        Wait Staff View
                    </Button>
                </Link>
                <Link to="/orders">
                    <Button variant="contained" disabled={currentPage === 'orders'}>
                        Orders
                    </Button>
                </Link>
            </div>
            <div className="headerButtonsRight">
                <Link to="/">
                    <Button variant="contained" disabled={currentPage === '/'}>
                        Landing Page
                    </Button>
                </Link>
            </div>
        </header>
    );
}
