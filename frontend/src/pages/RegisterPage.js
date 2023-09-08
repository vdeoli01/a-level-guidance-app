import React, { useState } from "react";
import { Button, TextField, FormControl, InputLabel, Select, MenuItem, Container } from "@mui/material";

import axios from "axios";
import { BASE_API_ENDPOINT } from "../config";
import HomeButton from "../components/HomeButton";

function RegisterPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [role, setRole] = useState("normal");

    const handleRegister = async () => {
        try {
            const response = await axios.post(`${BASE_API_ENDPOINT}/auth/register`, {
                email,
                password,
                is_active: true,
                is_superuser: false,
                is_verified: false,
                name,
                role
            }, {
                headers: {
                    "Content-Type": "application/json"
                }
            });
            console.log(response.data);
            // Add your handling logic here e.g. redirecting to another page
        } catch (error) {
            console.error(error);
            // Handle error accordingly
        }
    };

    return (
        <Container component="main" maxWidth="xs" style={{ marginTop: '8%' }}>
            <HomeButton />
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundColor: '#f7f7f7', padding: '20px', borderRadius: '10px' }}>
                <h1>Register</h1>
                <TextField label="Name" variant="outlined" margin="normal" fullWidth onChange={e => setName(e.target.value)} />
                <TextField label="Email" variant="outlined" margin="normal" fullWidth onChange={e => setEmail(e.target.value)} />
                <TextField label="Password" variant="outlined" margin="normal" fullWidth type="password" onChange={e => setPassword(e.target.value)} />
                <FormControl variant="outlined" margin="normal" fullWidth>
                    <InputLabel>Role</InputLabel>
                    <Select value={role} label="Role" onChange={e => setRole(e.target.value === "Student" ? "normal" : "advisor")}>
                        <MenuItem value="normal">Student</MenuItem>
                        <MenuItem value="advisor">Advisor</MenuItem>
                    </Select>
                </FormControl>
                <Button variant="contained" color="primary" onClick={handleRegister}>Register</Button>
            </div>
        </Container>
    );
}

export default RegisterPage;
