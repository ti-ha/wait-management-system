import React, { useState, useEffect } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { Button, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import './TableSelection.css'


export default function TableSelection() {

    const navigate = useNavigate();

    const [tables, setTables] = useState([]);
    const [tableNo, setTableNo] = useState("");

    useEffect(() => {
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
        fetchTables();
    }, []);
    

    const handleChange = (event) => {
        setTableNo(event.target.value);
    }

    const handleConfirm = () => {
        console.log(`Table ${tableNo} selected`);
        navigate(`/customer/${tableNo}`);
    }

    return (
        <div className="container">
            <Button 
                variant="contained"
                color="primary"
                component={Link}
                to="/"
                sx={{ position: "fixed", top: 20, right: 20, zIndex: 2000 }}
            >
                    Landing Page
            </Button>
            <div className="boxContainer">
                <Box className="dropdownBox">
                    <h2 className="formHeading">
                        Select Table Number:
                    </h2>
                    <FormControl variant="outlined" fullWidth>
                        <InputLabel id="select-table-label">Table Number</InputLabel>
                        <Select
                            labelId="select-table-label"
                            id="select-table"
                            value={tableNo}
                            onChange={handleChange}
                            label="Table Number"
                        >
                            {tables.map((table) => (
                                <MenuItem key={table.id + 1} value={table.id + 1}>
                                    {`Table ${table.id + 1}`}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <Button 
                        variant="contained"
                        color="secondary"
                        className="confirmButton"
                        disabled={!tableNo}
                        onClick={handleConfirm}
                    >
                        Confirm
                    </Button>
                </Box>
            </div>
        </div>
    )
}