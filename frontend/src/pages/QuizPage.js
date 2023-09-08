import React, { useState } from 'react';
import { Button, Typography, Radio, RadioGroup, FormControlLabel, FormControl } from '@mui/material';
import axios from 'axios';
import { BASE_API_ENDPOINT } from '../config';
import { useNavigate } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage';

function QuizPage() {
    const [quizId, setQuizId] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState({});
    const [started, setStarted] = useState(false);
    const [error, setError] = useState(null);
    const history = useNavigate();

    const startQuiz = async () => {
        setError(null)
        try {
            const { data } = await axios.get(`${BASE_API_ENDPOINT}/quizzes/?skip=0&limit=1`);
            const latestQuizId = data[0].quiz_id;
            setQuizId(latestQuizId);

            const quizData = await axios.get(`${BASE_API_ENDPOINT}/quizzes/${latestQuizId}`);
            setQuestions(quizData.data.questions);
            setStarted(true);
        } catch (error) {
            setError(error.message || 'An error occurred while fetching quiz data');
            console.error('Error fetching quiz data', error);
        }
    };

    const handleSubmit = async () => {
        setError(null)
        try {
            const questionResponses = Object.keys(responses).map(key => ({
                question_id: parseInt(key),
                response_id: responses[key]
            }));
            const { data } = await axios.post(`${BASE_API_ENDPOINT}/users/me/quiz_attempts`, {
                quiz_id: quizId,
                question_responses: questionResponses
            });
            history('/results', { state: { subjects: data.subjects } });
        } catch (error) {
            setError(error.message || 'An error occurred while submitting quiz responses');
            console.error('Error submitting quiz responses', error);
        }
    };

    const handleChange = (questionId, value) => {
        setResponses(prev => ({
            ...prev,
            [questionId]: value
        }));
    };

    return (
        <div style={{ padding: '20px' }}>
            {!started ? (
                <Button variant="contained" color="primary" onClick={startQuiz}>Start Quiz</Button>
            ) : (
                <div>
                    <Typography variant="h6" gutterBottom>
                        Please answer the questions on a scale of 1 (Strongly Agree) to 5 (Strongly Disagree)
                    </Typography>
                    {questions.map(question => (
                        <FormControl component="fieldset" key={question.question_id}>
                            <Typography variant="subtitle1" gutterBottom>{question.question}</Typography>
                            <RadioGroup row onChange={(e) => handleChange(question.question_id, parseInt(e.target.value))}>
                                {[1, 2, 3, 4, 5].map(val => (
                                    <FormControlLabel key={val} value={val} control={<Radio />} label={val} />
                                ))}
                            </RadioGroup>
                        </FormControl>
                    ))}
                    <Button variant="contained" color="primary" onClick={handleSubmit}>Submit</Button>
                </div>
            )}
            {error && <ErrorMessage message={error} />}
        </div>
    );
}

export default QuizPage;
