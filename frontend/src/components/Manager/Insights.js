import React, { useState, useEffect } from 'react';
import { useIsManager } from '../Hooks/useIsAuthorised.js';
import AccessDenied from '../Common/AccessDenied.js';
import Header from '../Common/Header.js';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from "@mui/material";
import styled from 'styled-components';


const StyledBox = styled(Box)`
    display: flex;
    justify-content: space-between;
    margin: 30px auto;
    max-width: 1600px;
`;

const StyledTableContainer = styled(TableContainer)`
    flex: 1;
    margin: 0 30px;
`;

export default function Insights() {

    const auth_token = localStorage.getItem('token'); 
    const [menuStats, setMenuStats] = useState({});
    const [pairStats, setPairStats] = useState({});

    // Ensure the user is authorised to access this page
    const { isAuthorised, isLoading } = useIsManager();
    const userType = localStorage.getItem('user_type');

    useEffect(() => {
        const fetchMenuStats = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/restaurant/menu/stats`, {
                    headers: { 'Authorization': `${auth_token}` }
                });
                if (!response.ok) { 
                    const responseBody = await response.json();
                    console.error('Server response:', responseBody); 
                    throw new Error(`HTTP Error with status: ${response.status}`);
                }
                const data = await response.json();
                setMenuStats(data);
            } catch (error) {
                console.error("Error fetching menu stats:", error);
            }
        }
        fetchMenuStats();
    }, []);

    useEffect(() => {
        const fetchPairStats = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/restaurant/menu/stats/pairs`, {
                    headers: { 'Authorization': `${auth_token}` }
                });
                if (!response.ok) { 
                    const responseBody = await response.json();
                    console.error('Server response:', responseBody); 
                    throw new Error(`HTTP Error with status: ${response.status}`);
                }
                const data = await response.json();
                setPairStats(data);
            } catch (error) {
                console.error("Error fetching pair stats:", error);
            }
        }
        fetchPairStats();
    }, []);
    

    if (isLoading) {
        return null;
    }

    if (!isAuthorised) {
        return <AccessDenied userType={userType}/>
    }
    
    return (
        <>
            <Header userType={userType} currentPage="insights" />
            <StyledBox>
                <StyledTableContainer component={Paper}>
                    <Typography variant="h5" align="center" gutterBottom>Menu Item Popularity</Typography>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell component="th">
                                    <Typography variant="h6" align="center">
                                        Item Name
                                    </Typography>
                                </TableCell>
                                <TableCell component="th" align="center">
                                    <Typography variant="h6" align="center">
                                        No. Orders
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.entries(menuStats).map(([item, orders]) => (
                                <TableRow key={item}>
                                    <TableCell component="th" scope="row" align="center">{item}</TableCell>
                                    <TableCell align="center">{orders}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </StyledTableContainer>
                <StyledTableContainer component={Paper}>
                    <Typography variant="h5" align="center" gutterBottom>Popular Item Pairings</Typography>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell component="th" align="center">
                                    <Typography variant="h6" align="center">
                                        Item Name
                                    </Typography>
                                </TableCell>
                                <TableCell component="th" align="center">
                                    <Typography variant="h6" align="center">
                                        Most Paired With
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.entries(pairStats).map(([item, pair]) => (
                                <TableRow key={item}>
                                    <TableCell component="th" scope="row" align="center">{item}</TableCell>
                                    <TableCell align="center">{pair}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </StyledTableContainer>
            </StyledBox>
        </>
    );
};
