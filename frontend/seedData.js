import fetch from 'node-fetch';
import { config } from 'dotenv';

config();

/*                              MOCK DATA DEFINITIONS               */

// Create mock users
// Define your users
const users = [
    {
        first_name: "WaitStaff",
        last_name: "One",
        user_type: "WaitStaff",
        password: "waitstaff"
    },
    {
        first_name: "KitchenStaff",
        last_name: "One",
        user_type: "KitchenStaff",
        password: "kitchenstaff"
    },
    {
        first_name: "Manager",
        last_name: "One",
        user_type: "Manager",
        password: "manager"
    }
]

const imageLinks = {
    "Meatloaf": "https://www.spendwithpennies.com/wp-content/uploads/2022/12/1200-The-Best-Meatloaf-Recipe-SpendWithPennies.jpg",
    "Arancini Balls": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/arancini_balls-db2b1df.jpg?quality=90&webp=true&resize=440,400",
    "Greek Salad": "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/08/Greek-Salad-main.jpg",
    "Salt and Pepper Squid": "https://redhousespice.com/wp-content/uploads/2022/02/squid-with-salt-and-pepper-seasoning-scaled.jpg",
    "Steak": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Steak_with_shitaki_mushrooms.jpg/300px-Steak_with_shitaki_mushrooms.jpg",
    "Pizza": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Pizza-3007395.jpg/220px-Pizza-3007395.jpg",
    "Prawn Chips": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Fried_Krupuk_Udang.JPG/250px-Fried_Krupuk_Udang.JPG",
    "Buffalo Wings": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Buffalo_wings-01.jpg/220px-Buffalo_wings-01.jpg",
    "Burger": "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg"
}

const categories = [
    "Entrees",
    "Mains",
    "Snacks"
];

const menuItems = [
    {
        category: "Entrees",
        items: [
            { name: "Meatloaf", price: 3, image_url: imageLinks["Meatloaf"] },
            { name: "Arancini Balls", price: 9, image_url: imageLinks["Arancini Balls"] },
            { name: "Greek Salad", price: 6.5, image_url: imageLinks["Greek Salad"] },
            { name: "Squid", price: 8.5, image_url: imageLinks["Salt and Pepper Squid"] }
        ]
    },
    {
        category: "Mains",
        items: [
            { name: "Burger", price: 12, image_url: imageLinks["Burger"] },
            { name: "Steak", price: 25, image_url: imageLinks["Steak"] },
            { name: "Pizza", price: 18, image_url: imageLinks["Pizza"] },
        ]
    },
    {
        category: "Snacks",
        items: [
            { name: "Prawn Chips", price: 7, image_url: imageLinks["Prawn Chips"] },
            { name: "Buffalo Wings", price: 10, image_url: imageLinks["Buffalo Wings"] },
        ]
    }
]





/*                              API CALLS TO CREATE DUMMY DATA              */

let authToken;

const loginAsManager = async () => {
    // your code here
    try {
        const manager = users.find(user => user.user_type === "Manager");
        const response = await fetch(`${process.env.REACT_APP_API_URL}/user/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(manager)
        });
  
        if (!response.ok) { 
            const responseBody = await response.json();
            console.error('Server response:', responseBody); 
            throw new Error(`HTTP Error with status: ${response.status}`);
        }
  
        const data = await response.json();
        authToken = data.auth_token;
        console.log(`Logged in as Manager: ${data.message}`);
    } catch (error) {
        console.error("Error logging in as Manager:", error);
    }
};

const main = async () => {
    // Create users using the API endpoint
    const userPromises = users.map(user => fetch(`${process.env.REACT_APP_API_URL}/user/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    }));

    try {
        const responses = await Promise.all(userPromises);
        const jsonResponses = await Promise.all(responses.map(response => {
            if (!response.ok) {
                console.error('Server response:', response); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            return response.json();
        }));
        jsonResponses.forEach((data, index) => console.log(`Successfully added user ${users[index].first_name} ${users[index].last_name}`, data));
    } catch (error) {
        console.error("Error adding user:", error);
    }

    await loginAsManager();

    
    let categoryPromises = categories.map((category) => {
        const requestOptions = {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `${authToken}`
            },
            body: JSON.stringify({ name: category })
        }
    
        return fetch(`${process.env.REACT_APP_API_URL}/menu/categories`, requestOptions)
            .then(response => response.text())
            .then(data => console.log('Response from server:', data))
            .catch(error => console.error('Error:', error))
    });
    
    await Promise.all(categoryPromises);
    
    for (const {category, items} of menuItems) {
        for (const item of items) {
            console.log(`Creating item: ${item.name} in category: ${category}`);
            const requestOptions = {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `${authToken}`
                },
                body: JSON.stringify(item)
            };
            
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/menu/categories/${category}`, requestOptions);
                const data = await response.text();
                console.log(data);
            } catch (error) {
                console.log('Error:', error);
            }
        }
    }

    
    const tables = [1, 2, 3];
    
    tables.forEach(async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/table/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${authToken}`
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

};





main().catch(error => console.error(error));


