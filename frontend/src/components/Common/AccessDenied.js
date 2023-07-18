import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Box } from "@mui/material";
import './AccessDenied.css';

export default function AccessDenied({ userType }) {
    let backLink, deniedHeading, deniedMessage;
    if (userType === 'KitchenStaff' || userType === 'WaitStaff') {
        backLink = "/staff";
        deniedHeading = "Access Denied"
        deniedMessage = "This page is for managers only.";
    } else {
        backLink = "/select-table";
        deniedHeading = "Oops! This isn't the menu!"
        deniedMessage = "Don't worry. Just click here to get right back to ordering delicious meals.";
    }

    return (
        <Box className="access-denied-container">
            <Box className="access-denied-content">
                <h1>{deniedHeading}</h1>
                <p>{deniedMessage}</p>
                <Button variant="contained" color="primary" component={Link} to={backLink}>
                    {userType === 'KitchenStaff' || userType === 'WaitStaff' ? "Back to Staff Page" : "Back to Ordering"}
                </Button>
            </Box>
            {(userType !== 'KitchenStaff' && userType !== 'WaitStaff') &&
                <Box className="access-denied-footer">
                    <p>Are you a staff member? <Link to="/login">Login here</Link></p>
                </Box>
            }
        </Box>
    );
}
