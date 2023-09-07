import React from "react";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";
import HomeIcon from "@mui/icons-material/Home";

function HomePage() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <h1>Welcome to the A-Level Recommendation Quiz</h1>
            <div style={{ marginBottom: '20px' }}>
                <Button variant="contained" color="primary" style={{ marginRight: '10px' }}>
                    <Link to="/login" style={{ textDecoration: 'none', color: '#fff' }}>Login</Link>
                </Button>
                <Button variant="contained" color="secondary" style={{ marginLeft: '10px' }}>
                    <Link to="/register" style={{ textDecoration: 'none', color: '#fff' }}>Register</Link>
                </Button>
            </div>
            <Button variant="contained" startIcon={<HomeIcon />}>
                <Link to="/quiz" style={{ textDecoration: 'none', color: '#000' }}>Take the Quiz</Link>
            </Button>
        </div>
    );
}

export default HomePage;
