import React, { useState, useEffect } from "react";
import { Modal, Fade, Box, TextField, Button } from "@mui/material";

export default function EditCategoryModal({ open, onClose, onSave, oldCategoryName }) {
    const [categoryName, setCategoryName] = useState(oldCategoryName);

    useEffect(() => {
        setCategoryName(oldCategoryName);
    }, [oldCategoryName]);

    const handleCategoryNameChange = (event) => {
        setCategoryName(event.target.value);
    };

    const handleSaveCategory = () => {
        onSave(categoryName);
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
                    <h2>Edit Category</h2>
                    <TextField 
                        label="Category Name" 
                        variant="outlined" 
                        value={categoryName} 
                        onChange={handleCategoryNameChange} 
                        fullWidth
                    />
                    <div style={{marginTop: '20px', display: 'flex', justifyContent: 'flex-end'}}>
                        <Button variant="contained" onClick={handleSaveCategory} style={{marginRight: '10px'}}>Save</Button>
                        <Button variant="contained" onClick={onClose}>Cancel</Button>
                    </div>
                </Box>
            </Fade>
        </Modal>
    );
}
