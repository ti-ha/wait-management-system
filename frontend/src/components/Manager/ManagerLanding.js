import React from "react";
import { Grid, Typography } from "@mui/material";
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';

export default function ManagerLanding() {

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
        <Header userType={userType} currentPage="" />
            <Grid container direction="column" justifyContent="center" alignItems="center">
                <Typography variant="h4" gutterBottom>
                    Welcome to the Manager Dashboard
                </Typography>
                <Typography variant="body1" gutterBottom>
                    Use the navigation bar at the top of the page to switch between the different management views.
                </Typography>
                <Typography variant="body1">
                    The <strong>Manager</strong> button gives you access to the Menu Editor, Insights, Restaurant Manager and Staff Registration page.<br /> 
                    The <strong>Kitchen View</strong> shows current orders being prepared. <br /> 
                    The <strong>Wait Staff View</strong> shows orders served and tables requiring assistance.<br />
                    The <strong>Orders</strong> page gives you access to all the current and past orders.<br /> 
                </Typography>
            </Grid>
        </>
    )
}
