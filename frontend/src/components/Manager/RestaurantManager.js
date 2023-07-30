import React, { useEffect, useState } from 'react';
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';
import { Box, Typography, Grid, Card, CardContent, Container, TableContainer, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';


export default function RestaurantManager() {

    const auth_token = localStorage.getItem('token'); 

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    const [tables, setTables] = useState([]);
    const [users, setUsers] = useState({});

    const fetchTables = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/table`);
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            setTables(data.tables);
        } catch (error) {
            console.error("Error fetching tables:", error);
        }
    }

    const fetchUsers = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/users`, {
                headers: { 'Authorization': `${auth_token}` }
            });
            if (!response.ok) { 
                const responseBody = await response.json();
                console.error('Server response:', responseBody); 
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            setUsers(data);
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    }

    useEffect(() => {
        fetchTables();
        fetchUsers();
    }, []);

    const kitchenStaff = Object.values(users).filter(user => user.type === 'KitchenStaff');
    const waitStaff = Object.values(users).filter(user => user.type === 'WaitStaff');

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied userType={userType}/>
    }

    return (
        <>
            <Header userType={userType} currentPage="restaurant-manager" />
            <Container maxWidth="lg"> 
                <Box py={4} px={2}> 
                <Grid container spacing={2} justify="center">
                    <Grid item xs={12} md={6} lg={4}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Kitchen Staff</Typography>
                                {kitchenStaff.map((staff, index) => (
                                    <Typography align="center" key={index}>{staff.first_name} {staff.last_name}</Typography>
                                ))}
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} md={6} lg={4}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Wait Staff</Typography>
                                {waitStaff.map((staff, index) => (
                                    <Typography align="center" key={index}>{staff.first_name} {staff.last_name}</Typography>
                                ))}
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} md={6} lg={4}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Available Tables</Typography>
                                <TableContainer>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell align="center">Table Number</TableCell>
                                                <TableCell align="center">Max Occupants</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {tables.map((table) => (
                                                <TableRow key={table.id}>
                                                    <TableCell align="center">{table.id + 1}</TableCell>
                                                    <TableCell align="center">{table.table_limit}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
                </Box>
            </Container>
        </>
    )
}