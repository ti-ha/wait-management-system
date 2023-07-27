import React from "react";
import { Grid, Typography } from "@mui/material";
import './StaffLanding.css'
import { useIsStaffMember } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';

export default function StaffLanding() {

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsStaffMember();
    const userType = localStorage.getItem('user_type');

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied />
    }

    return (
        <>
            <Header userType={userType} currentPage="" />
                <Grid container direction="column" justifyContent="center" alignItems="center">
                    <Typography variant="h4" gutterBottom>
                        Welcome to the Staff Dashboard
                    </Typography>
                    <Typography variant="body1" gutterBottom>
                    <br />Use the navigation bar at the top of the page to switch between the different staff views.
                    </Typography>
                    <Typography variant="body1">
                        The <strong>Kitchen View</strong> shows current orders being prepared. <br /> 
                        The <strong>Wait Staff View</strong> shows orders served and tables requiring assistance.
                    </Typography>
                </Grid>

        </>
    )
}
