import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@mui/material";
import './StaffLanding.css'
import { useIsStaffMember } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';

export default function StaffLanding() {

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsStaffMember();

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied />
    }

    return (
        <div className="staffLandingContainer">
            <Link to="/kitchen">
                <Button variant="contained" className="staffButton" style={{fontSize: "2em"}}>
                    Kitchen Staff
                </Button>
            </Link>
            <Link to="/wait-staff">
                <Button variant="contained" className="staffButton" style={{fontSize: "2em"}}>
                    Wait Staff
                </Button>
            </Link>


        </div>
    )
}
