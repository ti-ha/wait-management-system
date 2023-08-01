import React, { useEffect, useState } from 'react';
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';
import { Box, IconButton, Typography, Grid, Card, CardContent, Container, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Button } from '@mui/material';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, DialogContentText } from '@mui/material';
import { Add, ArrowUpward, ArrowDownward } from '@mui/icons-material'
import { Link } from 'react-router-dom'

export default function RestaurantManager() {

    const auth_token = localStorage.getItem('token'); 

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    const [tables, setTables] = useState([]);
    const [users, setUsers] = useState({});
    const [openModal, setOpenModal] = useState(false);
    const [tableLimit, setTableLimit] = useState(1);
    const [sortOrder, setSortOrder] = useState('asc');


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
    const managers = Object.values(users).filter(user => user.type === 'Manager');


    const handleClickOpenModal = () => {
        setOpenModal(true);
    };
    
    const handleCloseModal = () => {
        setOpenModal(false);
    };
    
    const handleAddTable = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/table/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${auth_token}`
                },
                body: JSON.stringify({ table_limit: Number(tableLimit), orders: [] })
            });
            if (!response.ok) {
                const responseBody = await response.json();
                console.error('Server response:', responseBody);
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Successfully added table", data);
            fetchTables(); 
            setOpenModal(false);
        } catch (error) {
            console.error("Error adding table:", error);
        }
    };
    
    const fetchSortedTables = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/restaurant/table/size`, {
                headers: { 'Authorization': `${auth_token}` }
            });
            if (!response.ok) {
                const responseBody = await response.json();
                console.error('Server response:', responseBody);
                throw new Error(`HTTP Error with status: ${response.status}`);
            }
            const data = await response.json();
            if (sortOrder === 'asc') {
                setTables(data.tables);
                setSortOrder('desc');
            } else {
                setTables(data.tables.reverse());
                setSortOrder('asc');
            }
        } catch (error) {
            console.error("Error fetching sorted tables:", error);
        }
    };
    

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
                    <Grid item xs={12} md={3} lg={2.6}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Managers</Typography>
                                {managers.map((manager, index) => (
                                    <Typography align="center" key={index}>{manager.first_name} {manager.last_name}</Typography>
                                ))}
                                <Button 
                                    component={Link} 
                                    to="/register-staff" 
                                    variant="contained"
                                    color="secondary" 
                                    style={{
                                        marginTop: '20px', 
                                        width: '200px', 
                                        marginLeft: 'auto', 
                                        marginRight: 'auto',
                                        display: 'flex'
                                    }}
                                    startIcon={<Add />}
                                >
                                    New Staff
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} md={3} lg={2.6}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Kitchen Staff</Typography>
                                {kitchenStaff.map((staff, index) => (
                                    <Typography align="center" key={index}>{staff.first_name} {staff.last_name}</Typography>
                                ))}
                                <Button 
                                    component={Link} 
                                    to="/register-staff" 
                                    variant="contained"
                                    color="secondary" 
                                    style={{
                                        marginTop: '20px', 
                                        width: '200px', 
                                        marginLeft: 'auto', 
                                        marginRight: 'auto',
                                        display: 'flex'
                                    }}
                                    startIcon={<Add />}
                                >
                                    New Staff
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} md={3} lg={2.6}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Wait Staff</Typography>
                                {waitStaff.map((staff, index) => (
                                    <Typography align="center" key={index}>{staff.first_name} {staff.last_name}</Typography>
                                ))}
                                <Button 
                                    component={Link} 
                                    to="/register-staff" 
                                    variant="contained"
                                    color="secondary" 
                                    style={{
                                        marginTop: '20px', 
                                        width: '200px', 
                                        marginLeft: 'auto', 
                                        marginRight: 'auto',
                                        display: 'flex'
                                    }}
                                    startIcon={<Add />}
                                >
                                    New Staff
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} md={3} lg={4}>
                        <Card>
                            <CardContent>
                                <Typography variant="h5" align="center">Tables</Typography>
                                <TableContainer>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell align="center">Table Number</TableCell>
                                                <TableCell align="center">
                                                    Max Occupants
                                                    <IconButton onClick={fetchSortedTables}>
                                                        {sortOrder === 'asc' ? <ArrowUpward /> : <ArrowDownward />}
                                                    </IconButton>
                                                </TableCell>
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
                                <Button 
                                    variant="contained"
                                    color="secondary" 
                                    style={{
                                        marginTop: '20px', 
                                        width: '200px', 
                                        marginLeft: 'auto', 
                                        marginRight: 'auto',
                                        display: 'flex'
                                    }}
                                    startIcon={<Add />}
                                    onClick={handleClickOpenModal}
                                >
                                    New Table
                                </Button>
                            </CardContent>
                        </Card>

                        <Dialog open={openModal} onClose={handleCloseModal}>
                            <DialogTitle>Add New Table</DialogTitle>
                            <DialogContent>
                                <DialogContentText>
                                    Enter the table limit.
                                </DialogContentText>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    id="table_limit"
                                    label="Table Limit"
                                    type="number"
                                    fullWidth
                                    value={tableLimit}
                                    onChange={event => setTableLimit(event.target.value)}
                                />
                            </DialogContent>
                            <DialogActions>
                                <Button onClick={handleCloseModal} color="primary">
                                    Cancel
                                </Button>
                                <Button onClick={handleAddTable} color="primary">
                                    Add
                                </Button>
                            </DialogActions>
                        </Dialog>

                    </Grid>
                </Grid>
                </Box>
            </Container>
        </>
    )
}