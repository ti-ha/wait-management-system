import React, { useEffect, useState } from 'react';

import './RestaurantManager.css'
import { Link } from 'react-router-dom';
import { Button } from "@mui/material";

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

    return (
        <>
            <header className="restaurantManagerPageHeader">
                    <div>
                        <Link to="/menu-editor">
                            <Button variant="contained">
                                Menu Editor
                            </Button>
                        </Link>
                        <Link to="/restaurant-manager">
                            <Button variant="contained" disabled>
                                Restaurant Manager
                            </Button>
                        </Link>
                    </div>
                    <div>
                        <Link to="/staff">
                            <Button variant="contained">
                                Staff View
                            </Button>
                        </Link>
                        <Link to="/">
                            <Button variant="contained">
                                Landing Page
                            </Button>
                        </Link>
                    </div>
            </header>

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