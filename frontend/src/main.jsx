import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import Landing from './Landing.jsx';
import Movie from './MovieReview/Movie.jsx';
import Roast from './Roast/Roast.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/movie" element={<Movie />} />
        <Route path="/roast" element={<Roast />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
