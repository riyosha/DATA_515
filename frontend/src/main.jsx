import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import Landing from './Landing.jsx';
import MovieInfo from './MovieReview/MovieInfo.jsx';
import Roast from './Roast/Roast.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/movie-info" element={<MovieInfo />} />
        <Route path="/roast" element={<Roast />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
