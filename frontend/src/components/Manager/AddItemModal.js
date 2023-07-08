import React, { useState } from "react";
import { Modal, Fade, Box, TextField, Button, Select, InputLabel, MenuItem, FormControl } from "@mui/material";

export default function AddItemModal({ open, onClose, onAdd, categories }) {
    const [itemName, setItemName] = useState("");
    const [itemCost, setItemCost] = useState("");
    const [itemImageURL, setItemImageURL] = useState("");
    const [selectedCategory, setSelectedCategory] = useState("");

    const handleItemNameChange = (event) => {
        setItemName(event.target.value);
    };
    
    const handleItemCostChange = (event) => {
        setItemCost(event.target.value);
    };

    const handleItemImageURL = (event) => {
        setItemImageURL(event.target.value);
    };

    const handleCategoryChange = (event) => {
        setSelectedCategory(event.target.value);
    };

    const handleAddItem = () => {
        onAdd(itemName, itemCost, selectedCategory, itemImageURL);
        setItemName("");
        setItemCost("");
        setSelectedCategory("");
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
                    <h2>New Menu Item</h2>
                    <TextField 
                        label="Item Name" 
                        variant="outlined" 
                        value={itemName} 
                        onChange={handleItemNameChange} 
                        fullWidth
                    />
                    <TextField 
                        label="Cost" 
                        variant="outlined" 
                        value={itemCost} 
                        onChange={handleItemCostChange} 
                        fullWidth
                        style={{marginTop: '10px'}}
                    />
                    <TextField 
                        label="Image URL" 
                        variant="outlined" 
                        value={itemImageURL} 
                        onChange={handleItemImageURL} 
                        fullWidth
                        style={{marginTop: '10px'}}
                    />
                    <FormControl fullWidth style={{marginTop: '10px'}}>
                        <InputLabel id="category-label">Category</InputLabel>
                        <Select
                            labelId="category-label"
                            value={selectedCategory}
                            onChange={handleCategoryChange}
                        >
                            {categories.map((category, index) => (
                                <MenuItem key={index} value={category.name}>{category.name}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <div style={{marginTop: '20px', display: 'flex', justifyContent: 'flex-end'}}>
                        <Button variant="contained" onClick={handleAddItem} style={{marginRight: '10px'}}>Add to Menu</Button>
                        <Button variant="contained" onClick={onClose}>Cancel</Button>
                    </div>
                </Box>
            </Fade>
        </Modal>
    );
}
