import React from 'react';
import { Form, Container } from 'react-bootstrap'
import { Link } from 'react-router-dom';
import { Button } from '@mui/material';
import { useLogin } from '../Hooks/useLogin.js';
import './Login.css'
import 'bootstrap/dist/css/bootstrap.min.css';


export default function Login() {
    const { firstName, lastName, password, error, setFirstName, setLastName, setPassword, handleLogin } = useLogin();

    return (
        <>
            <header className="login-header">
                <div className='header-buttons'>
                    <Link to="/">
                        <Button variant="contained">
                            Landing Page
                        </Button>
                    </Link>
                </div>
            </header>
            <Container style={{maxHeight: "90vh"}}>
                <h1>Login</h1>
                <Form onSubmit={(e) => handleLogin(e, ['KitchenStaff', 'WaitStaff', 'Manager'])}>
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
                    <Button variant="contained" type="submit">
                        Login
                    </Button>
                    {error && <p className="text-danger">{error}</p>}
                </Form>
                <div className="diner-message">
                    <p>Oops! Are you a diner and just in search of delicious meals? Click here:</p>
                    <Link to="/select-table">
                        <Button variant="contained" >
                            Dine In
                        </Button>
                    </Link>
                </div>
            </Container>
        </>
    )
}