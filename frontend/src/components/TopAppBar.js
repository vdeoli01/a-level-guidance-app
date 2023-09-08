import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import axios from 'axios';
import { BASE_API_ENDPOINT } from '../config';
import Logout from './Logout';
import HomeButton from './HomeButton';

function TopAppBar() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const checkLoginStatus = async () => {
            try {
                const response = await axios.get(`${BASE_API_ENDPOINT}/authenticated-route`, {
                    withCredentials: true
                });
                if(response.status === 200) {
                    setIsLoggedIn(true);
                }
            } catch (error) {
                console.error(error);
            }
        };

        checkLoginStatus();
    }, []);

    return (
        <AppBar position="static" style={{ backgroundColor: '#3f51b5', marginBottom: '20px' }}>
            <Toolbar>
                <HomeButton style={{marginRight: '20px'}}/>
                <Typography variant="h6" style={{ flex: 1 }}>
                    Quiz App - Enhance Your Knowledge
                </Typography>
                {isLoggedIn && (
                    <>
                        <Typography variant="subtitle1" style={{ marginRight: '20px' }}>
                            Logged in
                        </Typography>
                        <Logout />
                    </>
                )}
            </Toolbar>
        </AppBar>
    );
}

export default TopAppBar;
