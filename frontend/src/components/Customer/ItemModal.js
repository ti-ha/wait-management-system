import React from "react";
import { Modal, Fade, Box } from "@mui/material"

export default function ItemModal({ item, onClose, onAddToOrder, quantity, setQuantity }) {

    const handleIncreaseQuantity = () => {
        setQuantity(quantity + 1)
    }

    const handleDecreaseQuantity = () => {
        setQuantity(quantity - 1)
    }

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
            open={true}
            onClose={onClose} 
            closeAfterTransition
        >
            <Fade in={true}>
                <Box sx={style}>
                    <div className="modalContent">
                        <h2>{item.name}</h2>
                        <img src={item.imageURL} alt={item.name} />
                        <div>
                            <p>Quantity</p>
                            <button onClick={handleDecreaseQuantity}>-</button>
                            <span>{quantity}</span>
                            <button onClick={handleIncreaseQuantity}>+</button>
                        </div>
                        <button onClick={onAddToOrder}>Add to Order</button>
                        <button onClick={onClose}>Cancel</button>
                    </div>
                </Box>
            </Fade>
        </Modal>
    );
}