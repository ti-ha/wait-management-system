import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from "@mui/material";
import ProfileDropdown from './ProfileDropdown.js';
import './Header.css'

export default function Header ({ userType, currentPage }) {

    const navigate = useNavigate();

    const isManager = userType === 'Manager';

    const auth_token = localStorage.getItem('token'); 
    const [user, setUser] = useState({});

    useEffect(() => {
        const me = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/me`, {
                    headers: { 'Authorization': `${auth_token}` }
                });
                if (!response.ok) { 
                    const responseBody = await response.json();
                    console.error('Server response:', responseBody); 
                    throw new Error(`HTTP Error with status: ${response.status}`);
                }    
                const data = await response.json();
                setUser(data);
            } catch (error) {
                console.error("Error fetching my profile:", error);
            }
        }
        me()
    }, []);

    const handleLogout = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/logout`, {
                method: 'POST',
                headers: { 'Authorization': `${auth_token}` }
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }    
        } catch (error) {
            console.error("Error logging out:", error);
        }

        localStorage.clear();
        navigate("/login");
    };

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
                <ProfileDropdown user={user} handleLogout={handleLogout} />
            </div>
        </header>
    );
}
