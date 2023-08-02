import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Select, MenuItem, InputLabel, FormControl, InputAdornment, IconButton } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useForm } from "react-hook-form";
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';
import { useIsManager } from '../Hooks/useIsAuthorised.js';

export default function StaffRegistration() {

    const auth_token = localStorage.getItem('token'); 
    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    const [userTypeState, setUserTypeState] = useState('');

    const handleSelectChange = (event) => {
        setUserTypeState(event.target.value);
    };

    const { register, handleSubmit, formState: { errors }, reset } = useForm();
    const onSubmit = async (data) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/user/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `${auth_token}` },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                const responseBody = await response.json();
                console.error('Server response:', responseBody);
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const responseData = await response.json();
            console.log(responseData);

            reset();
            setUserTypeState();
        } catch (error) {
            console.error("Error fetching menu stats:", error);
        }
    };

    const [showPassword, setShowPassword] = useState(false);

    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };


    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied userType={userType}/>
    }

    return (
        <>
            <Header userType={userType} currentPage="register-staff" />
            <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
                <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: '300px', border: '1px solid', borderRadius: 1, padding: 2 }}>
                    <Typography variant="h5" align="center" mb={2}>Register New Staff</Typography>
                    <TextField {...register("first_name", { required: "This field is required" })} label="First Name" error={!!errors.first_name} helperText={errors.first_name && errors.first_name.message} />
                    <TextField {...register("last_name", { required: "This field is required" })} label="Last Name" error={!!errors.last_name} helperText={errors.last_name && errors.last_name.message} />

                    <FormControl>
                        <InputLabel id="user_type_label">Staff Type</InputLabel>
                        <Select
                            labelId="user_type_label"
                            {...register("user_type", { required: "This field is required" })}
                            label="Staff Type"
                            value={userTypeState} 
                            onChange={handleSelectChange} 
                            error={!!errors.user_type}
                        >
                            <MenuItem value={"KitchenStaff"}>Kitchen Staff</MenuItem>
                            <MenuItem value={"WaitStaff"}>Wait Staff</MenuItem>
                            <MenuItem value={"Manager"}>Manager</MenuItem>
                        </Select>
                        {errors.user_type && <Typography variant="caption" color="error">{errors.user_type.message}</Typography>}
                    </FormControl>

                    <TextField 
                        {...register("password", { required: "This field is required" })} 
                        label="Password" 
                        type={showPassword ? 'text' : 'password'}
                        error={!!errors.password}
                        helperText={errors.password && errors.password.message}
                        InputProps={{
                            endAdornment:
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle password visibility"
                                    onClick={handleClickShowPassword}
                                    edge="end"
                                >
                                    {showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                            </InputAdornment>
                        }}
                    />
                    
                    <Button type="submit" variant="contained" color="primary">Register</Button>
                </Box>
            </Box>
        </>
    )
};