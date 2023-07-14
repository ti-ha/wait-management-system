import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Box } from "@mui/material";
import './AccessDenied.css';

export default function AccessDenied() {
    return (
        <Box className="access-denied-container">
            <Box className="access-denied-content">
                <h1>Oops! This isn't the menu!</h1>
                <p>Don't worry. Just click here to get right back to ordering delicious meals.</p>
                <Button variant="contained" color="primary" component={Link} to="/select-table">
                    Back to Ordering
                </Button>
            </Box>
            <Box className="access-denied-footer">
                <p>Are you a staff member? <Link to="/staff-login">Login here</Link></p>
            </Box>
        </Box>
    );
}
