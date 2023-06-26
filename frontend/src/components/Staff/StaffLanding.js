import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@mui/material";
import './StaffLanding.css'

export default function StaffLanding() {
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
