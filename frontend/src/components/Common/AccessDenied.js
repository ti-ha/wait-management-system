import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Box, Typography } from "@mui/material";

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
        <Box display="flex" flexDirection="column" justifyContent="space-between" minHeight="100vh" p={2} boxSizing="border-box">
            <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" flexGrow={1} textAlign="center">
                <Typography variant="h2">{deniedHeading}</Typography>
                <Typography variant="body1">{deniedMessage}</Typography>
                <Button variant="contained" color="primary" component={Link} to={backLink}>
                    {userType === 'KitchenStaff' || userType === 'WaitStaff' ? "Back to Staff Page" : "Back to Ordering"}
                </Button>
            </Box>
            {(userType !== 'KitchenStaff' && userType !== 'WaitStaff') &&
                <Box display="flex" alignItems="center" justifyContent="center" height="100px">
                    <Typography variant="body1">Are you a staff member? <Link to="/login">Login here</Link></Typography>
                </Box>
            }
        </Box>
    );
}
