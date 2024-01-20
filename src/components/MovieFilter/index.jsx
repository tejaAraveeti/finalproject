// MovieFilter.js
import React, { useState } from 'react';
import "./style.css"
const MovieFilter = ({ onFilterChange }) => {
  const [genre, setGenre] = useState('');
  const [language, setLanguage] = useState('');

  const handleFilterChange = () => {
    onFilterChange({ genre, language });
  };

  return (
    <div>
      <label>Genre:</label>
      <input type="text" value={genre} onChange={(e) => setGenre(e.target.value)} />

      <label>Language:</label>
      <input type="text" value={language} onChange={(e) => setLanguage(e.target.value)} />

      <button onClick={handleFilterChange}>Apply Filters</button>
    </div>
  );
};

export default MovieFilter;
