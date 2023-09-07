import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import HomePage from "./components/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import QuizPage from "./pages/QuizPage";

const BASE_API_ENDPOINT = process.env.REACT_APP_BASE_API_ENDPOINT;
function App() {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={HomePage} />
                <Route path="/login" component={LoginPage} />
                <Route path="/register" component={RegisterPage} />
                <Route path="/quiz" component={QuizPage} />
            </Switch>
        </Router>
    );
}

export default App;
