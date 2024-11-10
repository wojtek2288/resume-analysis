import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import JobPostingPage from './Pages/JobPostingPage';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/job-posting/:id" element={<JobPostingPage />} />
      </Routes>
    </Router>
  );
};

export default App;
