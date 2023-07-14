import React, { useState } from "react";
import { Modal, Fade, Box, TextField, Button } from "@mui/material";

export default function AddCategoryModal({ open, onClose, onAdd }) {
    const [categoryName, setCategoryName] = useState("");

    const handleCategoryNameChange = (event) => {
        setCategoryName(event.target.value);
    };

    const handleAddCategory = () => {
        onAdd(categoryName);
        setCategoryName("");
    };

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
    };

    return (
        <Modal
            open={open}
            onClose={onClose}
            closeAfterTransition
        >
            <Fade in={open}>
                <Box sx={style}>
                    <h2>New Category</h2>
                    <TextField 
                        label="Category Name" 
                        variant="outlined" 
                        value={categoryName} 
                        onChange={handleCategoryNameChange} 
                        fullWidth
                    />
                    <div style={{marginTop: '20px', display: 'flex', justifyContent: 'flex-end'}}>
                        <Button variant="contained" onClick={handleAddCategory} style={{marginRight: '10px'}}>Add to Menu</Button>
                        <Button variant="contained" onClick={onClose}>Cancel</Button>
                    </div>
                </Box>
            </Fade>
        </Modal>
    );
}
