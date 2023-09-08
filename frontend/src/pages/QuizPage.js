import React, {useState} from 'react';
import {Button, Container, FormControl, FormControlLabel, Radio, RadioGroup, Typography} from '@mui/material';
import axios from 'axios';
import {BASE_API_ENDPOINT} from '../config';
import {useNavigate} from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage';
import TopAppBar from "../components/TopAppBar";
import ResponseMapBar from "../components/ResponseMapBar";

function QuizPage() {
    const [quizId, setQuizId] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState({});
    const [started, setStarted] = useState(false);
    const [error, setError] = useState(null);
    const history = useNavigate();

    const startQuiz = async () => {
        setError(null);
        try {
            const {data} = await axios.get(`${BASE_API_ENDPOINT}/quizzes/?skip=0&limit=1`);
            const latestQuizId = data[0].quiz_id;
            setQuizId(latestQuizId);

            const quizData = await axios.get(`${BASE_API_ENDPOINT}/quizzes/${latestQuizId}`);
            setQuestions(quizData.data.questions);
            setStarted(true);
        } catch (error) {
            setError(error.message || 'An error occurred while fetching quiz data');
        }
    };

    const handleSubmit = async () => {
        setError(null);
        try {
            const questionResponses = Object.keys(responses).map(key => ({
                question_id: parseInt(key),
                response_id: responses[key]
            }));
            const {data} = await axios.post(`${BASE_API_ENDPOINT}/users/me/quiz_attempts`, {
                quiz_id: quizId,
                question_responses: questionResponses
            });
            history('/results', {state: {subjects: data.subjects}});
        } catch (error) {
            setError(error.message || 'An error occurred while submitting quiz responses');
        }
    };

    const handleChange = (questionId, value) => {
        setResponses(prev => ({
            ...prev,
            [questionId]: value
        }));
    };

    const resetForm = () => {
        setResponses({});
        setError(null);
    };

    return (
        <>
            <TopAppBar/>
            <Container component="main" maxWidth="xs" style={{marginTop: '8%', textAlign: 'center'}}>
                {!started ? (
                    <Button variant="contained" color="primary" onClick={startQuiz}
                            style={{fontSize: 'large', padding: '10px 20px'}}>Start Quiz</Button>
                ) : (
                    <div>
                        <Typography variant="h4" gutterBottom style={{marginBottom: '20px'}}>
                            Quiz Time!
                        </Typography>
                        <Typography variant="h6" gutterBottom>
                            Please answer the questions on using the scale below:
                        </Typography>
                        <ResponseMapBar/>
                        {questions.map(question => (
                            <FormControl component="fieldset" key={question.question_id} style={{marginBottom: '20px'}}>
                                <Typography variant="subtitle1" gutterBottom>{question.question}</Typography>
                                <RadioGroup row
                                            onChange={(e) => handleChange(question.question_id, parseInt(e.target.value))}>
                                    {[1, 2, 3, 4, 5].map(val => (
                                        <FormControlLabel key={val} value={val} control={<Radio/>} label={val}/>
                                    ))}
                                </RadioGroup>
                            </FormControl>
                        ))}
                        <br/>
                        <div style={{display: 'flex', justifyContent: 'space-between'}}>
                            <Button variant="contained" onClick={resetForm}
                                    style={{backgroundColor: '#f0ad4e', marginTop: '20px'}}>Reset</Button>
                            <Button variant="contained" color="primary" onClick={handleSubmit}
                                    style={{marginTop: '20px'}}>Submit</Button>
                        </div>
                    </div>
                )}
                {error && <ErrorMessage message={error} style={{marginTop: '20px'}}/>}
            </Container>
        </>
    );
}

export default QuizPage;
