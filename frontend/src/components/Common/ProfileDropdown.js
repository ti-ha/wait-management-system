import React from 'react';
import { Avatar, Menu, MenuItem } from "@mui/material";

export default function ProfileDropdown ({ user, handleLogout }) {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <Avatar alt="Profile Picture" onClick={handleClick} style={{cursor: 'pointer'}}>
                {user.first_name && user.first_name[0]}
            </Avatar>
            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                onClick={handleClose}
            >
                <MenuItem>
                    <Avatar /> Welcome, {user.first_name} {user.last_name}
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
        </>
    );
};
