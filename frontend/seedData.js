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
            { name: "Orange Juice", price: 3, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Apple Juice", price: 3, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Happy Dad", price: 6.5, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Prime Hydration", price: 8.5, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" }
        ]
    },
    {
        category: "Mains",
        items: [
            { name: "Burger", price: 12, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 2", price: 12, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 3", price: 12, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 4", price: 12, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 5", price: 12, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 6", price: 12, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" }
        ]
    },
    {
        category: "Snacks",
        items: [
            { name: "Item 7", price: 10, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 8", price: 10, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 9", price: 10, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 10", price: 10, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" },
            { name: "Item 11", price: 10, image_url: "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg" }
        ]
    }
]

let categoryPromises = categories.map((category) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ name: category })
    }

    return fetch(`${process.env.REACT_APP_API_URL}/menu/categories`, requestOptions)
        .then(response => response.text())
        .then(data => console.log('Response from server:', data))
        .catch(error => console.error('Error:', error))
});

Promise.all(categoryPromises).then(() => {
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
});


const tables = [1, 2, 3];

tables.forEach(async () => {
    try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/table/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ table_limit: 3, orders: [] })
        });

        if (!response.ok) { 
            const responseBody = await response.json();
            console.error('Server response:', responseBody); 
            throw new Error(`HTTP Error with status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Successfully added table", data);
    } catch (error) {
        console.error("Error adding table:", error);
    }
});