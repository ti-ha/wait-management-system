import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@mui/material";
import './ManagerLanding.css'

export default function ManagerLanding() {
    return (
        <div className="managerLandingContainer">
            <Link to="/menu-editor">
                <Button variant="contained" className="managerButton" style={{fontSize: "2em"}}>
                    Menu Editor
                </Button>
            </Link>
            <Link to="/restaurant-manager">
                <Button variant="contained" className="managerButton" style={{fontSize: "2em"}}>
                    Restaurant Manager
                </Button>
            </Link>
        </div>
    )
}
