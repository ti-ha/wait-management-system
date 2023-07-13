import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Landing.css'

export default function Landing() {

    const navigate = useNavigate();

    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('user_type');
    
    const handleStaffPageNavigation = () => {
        if (token) {
            switch(userType) {
                case 'KitchenStaff':
                    navigate('/kitchen');
                    break;
                case 'WaitStaff':
                    navigate('/wait-staff');
                    break;
                case 'Manager':
                    navigate('/staff-landing');
                    break;
                default:
                    navigate('/staff-login');
                    break;
            }
        } else {
            navigate('/staff-login');
        }
    }

    const handleCustomerPageNavigation = () => {
        navigate('/select-table');
    };

    const handleManagerPageNavigation = () => {
        navigate('/manager');
    };


    return (
        <div className="container">
            <div className='appName'>
                Romantic Cheese Systems
            </div>
            <div className="linksContainer">
                <div className="linkContainer" onClick={handleStaffPageNavigation}> 
                    Staff Page 
                </div>
                <div className="linkContainer" onClick={handleCustomerPageNavigation}> 
                    Customer Page 
                </div>
                <div className="linkContainer" onClick={handleManagerPageNavigation}> 
                    Manager Page 
                </div>
            </div>
        </div>
    )
}

