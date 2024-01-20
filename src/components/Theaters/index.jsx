// TheaterSelectionPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './style.css';
import { useParams } from 'react-router-dom';

const Theater = ({ onSelectTheater }) => {
  const [theaters, setTheaters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchTheaters = async () => {
      try {
        const { data } = await axios.get(`http://127.0.0.1:8000/api/movie-theater/`+id);
        console.log('Data received from API:', data);
  
        if (Array.isArray(data.theaters)) {
          setTheaters(data.theaters);
        } else {
          console.error('Invalid data structure. Expected an array.');
          setError('Invalid data structure from the API.');
        }
      } catch (error) {
        console.error('Error fetching theaters:', error);
        setError('An error occurred while fetching theaters.');
      } finally {
        setLoading(false);
      }
    };
  
    // Immediately-invoked async function expression (IIFE)
    (async () => {
      await fetchTheaters();
    })();
  }, [id]);

  const handleTheaterSelect = (selectedTheater) => {
    onSelectTheater(selectedTheater);
  };

  if (loading) {
    return <div>Loading theaters...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="theater-selection-container">
      <h2>Select a Theater</h2>
      <ul>
        {theaters.map((theater) => (
          <li key={theater.id} onClick={() => handleTheaterSelect(theater)}>
            {theater.name} - {theater.location}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Theater;
