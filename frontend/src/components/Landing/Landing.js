import React from 'react';
import { Button } from '@mui/material';
import { Settings } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import './Landing.css'

export default function Landing() {

    const navigate = useNavigate();

    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('user_type');
    
    const handleAdminNavigation = () => {
        if (token) {
            switch(userType) {
                case 'KitchenStaff':
                case 'WaitStaff':
                    navigate('/staff');
                    break;
                case 'Manager':
                    navigate('/manager');
                    break;
                default:
                    navigate('/login');
                    break;
            }
        } else {
            navigate('/login');
        }
    }

    return (
        <div className="container">
            <div className="headertext">
                Savour the Flavour of Cheesy Bliss!
            </div>
            <div>
                <div className='welcomeBox'>
                    Welcome to Romantic Cheese Dining
                </div>
                <div className="middleSection">
                    <div className="introText">
                        We know you're hungry. Start ordering now...
                    </div>
                    <Button variant="contained" onClick={() => navigate('/select-table')}>
                        Start Ordering
                    </Button>
                </div>
            </div>
            <div className="bottomSection">
                <Button 
                    variant="contained"
                    onClick={handleAdminNavigation}
                    startIcon={<Settings />}>
                    Admin Only
                </Button>
            </div>
        </div>
    )
}
