import React, { useState, useEffect } from "react";
import { Modal, Fade, Box, TextField, Button } from "@mui/material";

export default function EditItemModal({ open, onClose, onSave, oldItem }) {
    const [itemName, setItemName] = useState(oldItem.name);
    const [itemPrice, setItemPrice] = useState(oldItem.price);
    const [itemPriceError, setItemPriceError] = useState("");
    const [itemImageUrl, setItemImageUrl] = useState(oldItem.imageURL);

    useEffect(() => {
        setItemName(oldItem.name);
        setItemPrice(oldItem.price);
        setItemImageUrl(oldItem.imageURL);
    }, [oldItem]);

    const handleItemNameChange = (event) => {
        setItemName(event.target.value);
    };

    const handleItemPriceChange = (event) => {
        const newPrice = event.target.value;
        setItemPrice(newPrice);

        if (!/^\d*\.?\d{0,2}$/.test(newPrice)) { 
            setItemPriceError("Please enter a number with up to 2 decimal places");
        } else {
            setItemPriceError("");
        }
    };

    const handleItemImageUrlChange = (event) => {
        setItemImageUrl(event.target.value);
    };

    const handleSaveItem = () => {
        if (itemPriceError) {
            return;
        }

        const updatedItem = {
            name: itemName !== oldItem.name ? itemName : null,
            price: itemPrice !== oldItem.price ? itemPrice : null,
            imageUrl: itemImageUrl !== oldItem.imageURL ? itemImageUrl : null,
            visibility: true, 
        };

        onSave(updatedItem);
        setItemName("");
        setItemPrice("");
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
                        label="Item Price" 
                        variant="outlined" 
                        value={itemPrice} 
                        onChange={handleItemPriceChange} 
                        fullWidth
                        style={{marginTop: '20px'}}
                        error={Boolean(itemPriceError)}
                        helperText={itemPriceError}
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
