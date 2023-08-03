import React from "react";
import { Modal, Fade, Box, IconButton, Button, Typography } from "@mui/material";
import { Add, Remove } from "@mui/icons-material";

export default function ItemModal({ item, onClose, onAddToOrder, quantity, setQuantity }) {

    const handleIncreaseQuantity = () => {
        setQuantity(quantity + 1);
    }

    const handleDecreaseQuantity = () => {
        if (quantity > 0) {
            setQuantity(quantity - 1);
        }
    }

    return (
        <Modal
            open={true}
            onClose={onClose}
            closeAfterTransition
        >
            <Fade in={true}>
                <Box
                    sx={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        width: '50%',
                        maxWidth: '500px', // Note: corrected "maxwidth" to "maxWidth"
                        bgcolor: 'background.paper',
                        border: '2px solid #000',
                        boxShadow: 24,
                        p: 4,
                        borderRadius: '10px',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <h2>{item.name}</h2>
                    <Box
                        component="img"
                        src={item.imageURL}
                        alt={item.name}
                        sx={{
                            width: '100%',
                            maxHeight: '200px',
                            objectFit: 'cover',
                        }}
                    />
                    <Box display="flex" alignItems="center" mt={2}>
                        <Typography variant="h6">Quantity</Typography>
                        <IconButton onClick={handleDecreaseQuantity} disabled={quantity === 0}>
                            <Remove />
                        </IconButton>
                        <span>{quantity}</span>
                        <IconButton onClick={handleIncreaseQuantity}>
                            <Add />
                        </IconButton>
                    </Box>
                    <Box display="flex" justifyContent="center" mt={2} gap={2}>
                        <Button variant="contained" color="primary" onClick={onAddToOrder}>
                            Add to Order
                        </Button>
                        <Button variant="contained" color="secondary" onClick={onClose}>
                            Cancel
                        </Button>
                    </Box>
                </Box>
            </Fade>
        </Modal>
    );
}
