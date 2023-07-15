import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function useLogin() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (event, allowedUserTypes) => {
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
        
        if (!allowedUserTypes.includes(userData.usertype)) {
            throw new Error('Unauthorized user type');
        }
        
        switch (userData.usertype) {
            case 'KitchenStaff':
                navigate('/kitchen');
                break;
            case 'WaitStaff':
                navigate('/wait-staff');
                break;
            case 'Manager':
                navigate('/manager');
                break;
            default:    
                throw new Error('Invalid user type');
        }
        
        } catch (error) {
        setError('The details you have entered are invalid. Please try again.');
        }
  };

  return {
    firstName,
    lastName,
    password,
    error,
    setFirstName,
    setLastName,
    setPassword,
    handleLogin,
  };
}
