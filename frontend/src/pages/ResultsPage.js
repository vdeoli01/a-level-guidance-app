import React from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Typography, Card, CardContent } from '@mui/material';
import TopAppBar from "../components/TopAppBar";

function ResultsPage() {
    const location = useLocation();
    const subjects = location.state ? location.state.subjects : [];

    const materialColors = [
        'primary.main',
        'secondary.main',
        'error.main',
        'warning.main',
        'info.main',
        'success.main'
    ];

    const getRandomMaterialColor = () => {
        return materialColors[Math.floor(Math.random() * materialColors.length)];
    };

    return (
        <>
            <TopAppBar/>
            <Container component="main" maxWidth="xs" style={{ marginTop: '8%', textAlign: 'center' }}>
                <Typography variant="h4" gutterBottom style={{ marginBottom: '20px' }}>
                    Recommended Subjects
                </Typography>
                {subjects.length ? (
                    subjects.map((subject, index) => (
                        <Card key={index} sx={{ bgcolor: getRandomMaterialColor(), mb: 2, borderRadius: 2 }}>
                            <CardContent>
                                <Typography variant="h6" style={{ color: '#fff' }}>
                                    {subject}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <Typography variant="subtitle1" color="textSecondary">
                        No recommendations available
                    </Typography>
                )}
            </Container>
        </>
    );
}

export default ResultsPage;
