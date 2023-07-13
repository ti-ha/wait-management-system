import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Container, Col } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';


export default function StaffLogin() {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (event) => {
        event.preventDefault()

        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/user/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ first_name: firstName, last_name: lastName, password })
            });
            
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
    
            const data = await response.json();
            const { auth_token } = data;
            localStorage.setItem('token', auth_token);
            
            // Get the user type
            const userResponse = await fetch(`${process.env.REACT_APP_API_URL}/me`, {
                method: 'GET',
                headers: { 'Authorization': `${auth_token}` },
            });
            
            if (!userResponse.ok) { 
                const userResponseBody = await userResponse.json();
                console.error('Server response:', userResponseBody); 
                throw new Error(`HTTP Error with status: ${userResponse.status}`);
            }
            
            const userData = await userResponse.json();
            localStorage.setItem('user_type', userData.usertype);
    
            switch (userData.usertype) {
                case 'KitchenStaff':
                    navigate('/kitchen');
                    break;
                case 'WaitStaff':
                    navigate('/wait-staff');
                    break;
                case 'Manager':
                    navigate('/staff-landing');
                    break;
                default:
                    throw new Error('Invalid user type');
            }
    
        } catch (error) {
            setError('The details you have entered are invalid. Please try again.');
        }
    };

    
    
    return (
        <Container>
            <h1>Login</h1>
            <Form onSubmit={handleLogin}>
                <Form.Group className="mb-3">
                    <Form.Label>First Name</Form.Label>
                    <Form.Control style={{width: "80vw", maxWidth: "500px"}} type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Last Name</Form.Label>
                    <Form.Control type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Login
                </Button>
                {error && <p className="text-danger">{error}</p>}
            </Form>
        </Container>
    )
}