// SeatList.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './style.css';
import SeatComponent from './SeatComponents';
import { useParams } from 'react-router-dom';

const SeatList = ({ onSeatClick }) => {
  const [seats, setSeats] = useState([]);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const { id: theaterId } = useParams();
  console.log('Theater ID:', theaterId);

  useEffect(() => {
    const fetchSeats = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/theater-seat/${theaterId}/`);
        setSeats(response.data);
        setLoading(false);
        console.log('Data received from API:', response.data);
      } catch (error) {
        console.error(`Error fetching seats for theater ID ${theaterId}. Endpoint: http://127.0.0.1:8000/api/theater-seat/${theaterId}/`, error);
        setLoading(false);
      }
    };
  
    fetchSeats();
  }, [theaterId]);

  const handleSeatClick = (seatId) => {
    console.log(`Seat ${seatId} selected`);
    onSeatClick(seatId);
    setSelectedSeats((prevSelectedSeats) =>
      prevSelectedSeats.includes(seatId)
        ? prevSelectedSeats.filter((id) => id !== seatId)
        : [...prevSelectedSeats, seatId]
    );
  };

  const handleSeatSelection = async () => {
    try {
      await axios.post(`http://127.0.0.1:8000/api/seat/`, { selectedSeats }); // Assuming you want to send selectedSeats
      console.log('Seats booked successfully!');
    } catch (error) {
      console.error('Error booking seats:', error);
    }
  };

  return (
    <div>
      {loading ? <div>Loading...</div> : <SeatComponent seats={seats} onSeatClick={handleSeatClick} />}
      <button onClick={handleSeatSelection}>Book Selected Seats</button>
    </div>
  );
};

export default SeatList;
