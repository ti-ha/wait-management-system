import fetch from 'node-fetch';
import { config } from 'dotenv';

config();

const categories = [
    "Drinks",
    "Mains",
    "Snacks"
];

const menuItems = [
    {
        category: "Drinks",
        items: [
            { name: "Orange Juice", price: 3 },
            { name: "Apple Juice", price: 3 },
            { name: "Happy Dad", price: 6.5 },
            { name: "Prime Hydration", price: 8.5 }
        ]
    },
    {
        category: "Mains",
        items: [
            { name: "Burger", price: 12 },
            { name: "Item 2", price: 12 },
            { name: "Item 3", price: 12 },
            { name: "Item 4", price: 12 },
            { name: "Item 5", price: 12 },
            { name: "Item 6", price: 12 }
        ]
    },
    {
        category: "Snacks",
        items: [
            { name: "Item 7", price: 10 },
            { name: "Item 8", price: 10 },
            { name: "Item 9", price: 10 },
            { name: "Item 10", price: 10 },
            { name: "Item 11", price: 10 }
        ]
    }
]

categories.forEach((category) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ name: category })
    }

    fetch(`${process.env.REACT_APP_API_URL}/menu/categories`, requestOptions)
        .then(response => response.text())
        .then(data => console.log('Response from server:', data))
        .catch(error => console.error('Error:', error))
});

menuItems.forEach(({category, items}) => {
    items.forEach((item) => {
        console.log(`Creating item: ${item.name} in category: ${category}`);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(item)
        };
    
        fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`, requestOptions)
            .then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.log('Error:', error));
    });
});