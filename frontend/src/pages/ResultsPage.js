import React from 'react';
import {Link, useLocation} from 'react-router-dom';
import {Button, Typography} from '@mui/material';
import TopAppBar from "../components/TopAppBar";

function ResultsPage() {
    const location = useLocation();
    const subjects = location.state ? location.state.subjects : [];

    return (
        <>
            <TopAppBar/>
            <div style={{padding: '20px'}}>
                <Typography variant="h4" gutterBottom>Recommended Subjects</Typography>
                {subjects.length ? (
                    subjects.map((subject, index) => (
                        <Typography variant="h6" key={index}>
                            {subject}
                        </Typography>
                    ))
                ) : (
                    <Typography variant="subtitle1" color="textSecondary">No recommendations available</Typography>
                )}
            </div>
        </>

    );
}

export default ResultsPage;
