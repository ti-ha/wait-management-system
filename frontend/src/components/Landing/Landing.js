import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css'

export default function Landing() {
    return (
        <div className="container">
            <div className='appName'>
                Romantic Cheese Systems
            </div>
            <div className="linksContainer">
                <Link className="linkContainer" to="/staff"> 
                    Staff Page 
                </Link>
                <Link className="linkContainer" to="/select-table"> 
                    Customer Page 
                </Link>
                <Link className="linkContainer" to="/manager"> 
                    Manager Page 
                </Link>
            </div>
        </div>
    )
}

