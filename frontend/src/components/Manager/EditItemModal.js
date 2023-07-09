import React, { useState, useEffect } from "react";
import { Modal, Fade, Box, TextField, Button } from "@mui/material";

export default function EditItemModal({ open, onClose, onSave, oldItem }) {
    const [itemName, setItemName] = useState(oldItem.name);
    const [itemCost, setItemCost] = useState(oldItem.price);
    const [itemImageUrl, setItemImageUrl] = useState(oldItem.imageURL);

    useEffect(() => {
        setItemName(oldItem.name);
        setItemCost(oldItem.price);
        setItemImageUrl(oldItem.imageURL);
    }, [oldItem]);

    const handleItemNameChange = (event) => {
        setItemName(event.target.value);
    };

    const handleItemCostChange = (event) => {
        setItemCost(event.target.value);
    };

    const handleItemImageUrlChange = (event) => {
        setItemImageUrl(event.target.value);
    };

    const handleSaveItem = () => {
        onSave({name: itemName, cost: itemCost, imageUrl: itemImageUrl});
        setItemName("");
        setItemCost("");
        setItemImageUrl("");
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
                    <h2>Edit Item</h2>
                    <TextField 
                        label="Item Name" 
                        variant="outlined" 
                        value={itemName} 
                        onChange={handleItemNameChange} 
                        fullWidth
                    />
                    <TextField 
                        label="Item Cost" 
                        variant="outlined" 
                        value={itemCost} 
                        onChange={handleItemCostChange} 
                        fullWidth
                        style={{marginTop: '20px'}}
                    />
                    <TextField 
                        label="Image URL" 
                        variant="outlined" 
                        value={itemImageUrl} 
                        onChange={handleItemImageUrlChange} 
                        fullWidth
                        style={{marginTop: '20px'}}
                    />
                    <div style={{marginTop: '20px', display: 'flex', justifyContent: 'flex-end'}}>
                        <Button variant="contained" onClick={handleSaveItem} style={{marginRight: '10px'}}>Save</Button>
                        <Button variant="contained" onClick={onClose}>Cancel</Button>
                    </div>
                </Box>
            </Fade>
        </Modal>
    );
}
