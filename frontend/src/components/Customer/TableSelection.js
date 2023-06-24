import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { Button, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import './TableSelection.css'


export default function TableSelection() {

    const navigate = useNavigate();

    const [tableNo, setTableNo] = useState("");

    const handleChange = (event) => {
        setTableNo(event.target.value);
    }

    const handleConfirm = () => {
        console.log(`Table ${tableNo} selected`);
        navigate(`/customer/${tableNo}`)
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
                            <MenuItem value={1}>Table 1</MenuItem>
                            <MenuItem value={2}>Table 2</MenuItem>
                            <MenuItem value={3}>Table 3</MenuItem>
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