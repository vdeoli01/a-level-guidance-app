import React from "react";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";
import QuizIcon from '@mui/icons-material/Quiz';
import TopAppBar from "./TopAppBar";

function HomePage() {
    return (
        <>
            <TopAppBar />
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
                <h1>Welcome to the A-Level Recommendation Quiz</h1>
                <div style={{ marginBottom: '20px' }}>
                    <Button variant="contained" color="primary" style={{ marginRight: '10px' }} component={Link} to="/login">
                        Login
                    </Button>
                    <Button variant="contained" color="secondary" style={{ marginLeft: '10px' }} component={Link} to="/register">
                        Register
                    </Button>
                </div>
                <Button variant="contained" startIcon={<QuizIcon />} component={Link} to="/quiz">
                    Take the Quiz
                </Button>
            </div>
        </>
    );
}

export default HomePage;
