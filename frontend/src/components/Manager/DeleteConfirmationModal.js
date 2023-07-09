import React from "react";
import { Modal, Fade, Box, Button, Typography } from "@mui/material";

export default function DeleteConfirmationModal({ open, onClose, onConfirm, objectName }) {
    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'space-between'
    };

    return (
        <Modal
            open={open}
            onClose={onClose}
            closeAfterTransition
        >
            <Fade in={open}>
                <Box sx={style}>
                    <Typography variant="h6" component="h2" align="center">
                        Are you sure you want to delete {objectName}?
                    </Typography>
                    <div style={{display: 'flex', justifyContent: 'center'}}>
                        <Button variant="contained" onClick={onConfirm} style={{marginRight: '10px'}}>Yes</Button>
                        <Button variant="contained" onClick={onClose}>No</Button>
                    </div>
                </Box>
            </Fade>
        </Modal>
    );
}
