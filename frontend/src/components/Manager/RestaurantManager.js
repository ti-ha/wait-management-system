import React, { useEffect, useState } from 'react';
import './RestaurantManager.css'
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';

export default function RestaurantManager() {

    const [tables, setTables] = useState([]);

    const fetchTables = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/table`);
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            setTables(data.tables);
        } catch (error) {
            console.error("Error fetching tables:", error);
        }
    }

    useEffect(() => {
        fetchTables();
    }, []);

    const occupiedTables = tables.filter(table => table["is occupied"]);
    const availableTables = tables.filter(table => !table["is occupied"]);

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied userType={userType}/>
    }

    return (
        <>
            <Header userType={userType} currentPage="restaurant-manager" />
            <div className="restaurantManagerContainer">
                <div className="restaurantManagerColumn">
                    <h2>Kitchen Staff</h2>
                </div>
                <div className="restaurantManagerColumn">
                    <h2>Wait Staff</h2>
                </div>
                <div className="restaurantManagerColumn">
                    <h2>Occupied Tables</h2>
                    {occupiedTables.map(table => (
                        <p key={table.id}>Table {table.id + 1}</p>
                    ))}
                </div>
                <div className="restaurantManagerColumn">
                    <h2>Available Tables</h2>
                    {availableTables.map(table => (
                        <p key={table.id}>Table {table.id + 1}</p>
                    ))}
                </div>
            </div>

        </>

    )
}