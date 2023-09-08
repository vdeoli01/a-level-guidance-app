import React from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

function HomeButton(props) {
    const navigate = useNavigate();

    const handleHomeClick = () => {
        navigate('/');
    };

    return (
        <Button variant="outlined" style={{ margin: '10px 0' }} onClick={handleHomeClick} {...props}>
            Home
        </Button>
    );
}

export default HomeButton;
