import React, { useState } from "react";
import { Button, TextField, Container } from "@mui/material";
import axios from "axios";
import { BASE_API_ENDPOINT } from "../config";
import HomeButton from '../components/HomeButton';

function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async () => {
        try {
            const response = await axios.post(`${BASE_API_ENDPOINT}/auth/jwt/login`, `username=${email}&password=${password}`, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });
            console.log(response.data);
            // Add your handling logic here e.g. redirecting to another page, storing token etc.
        } catch (error) {
            console.error(error);
            // Handle error accordingly
        }
    };

    return (
        <Container component="main" maxWidth="xs" style={{ marginTop: '8%' }}>
            <HomeButton />
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundColor: '#f7f7f7', padding: '20px', borderRadius: '10px' }}>
                <h1>Login</h1>
                <TextField label="Email" variant="outlined" margin="normal" fullWidth onChange={e => setEmail(e.target.value)} />
                <TextField label="Password" variant="outlined" margin="normal" fullWidth type="password" onChange={e => setPassword(e.target.value)} />
                <Button variant="contained" color="primary" onClick={handleLogin}>Login</Button>
            </div>
        </Container>
    );
}

export default LoginPage;
