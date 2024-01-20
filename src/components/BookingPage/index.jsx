import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import SeatList from '../SeatList';
import Theater from '../Theaters';
import "./style.css"


const BookingPage = () => {
  const { id } = useParams(); // Use useParams to get movieId from the route
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [seats, setSeats] = useState([]);  // Ensure this line is present

  const [numTickets, setNumTickets] = useState();
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [movieDetails, setMovieDetails] = useState(null);
  const [selectedTheater, setSelectedTheater] = useState(null);

  useEffect(() => {
    const fetchMovieDetails = async () => {
      try {
        const { data } = await axios.get(`http://127.0.0.1:8000/api/movies/` + id);
        console.log("Movie Details:", data);
        setMovieDetails(data);
      } catch (error) {
        console.error("Error fetching movie details:", error);
      }
    };

    fetchMovieDetails();
  }, [id]);
  const handleTheaterSelect = (theater) => {
    setSelectedTheater(theater);
    console.log('Selected Theater:', theater);
  }
  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const handleTimeChange = (e) => {
    console.log("Time changed:", e.target.value);
    setSelectedTime(e.target.value);
  };

  const handleNumTicketsChange = (e) => {
    const value = parseInt(e.target.value, 10);
  console.log('Handling numTickets change. New value:', value);
  setNumTickets((prevNumTickets) => isNaN(value) ? prevNumTickets : Math.max(1, value));
  };

  const handleSeatSelection = (seatId) => {
    console.log(`Seat ${seatId} selected`);
    setSelectedSeats((prevSeats) =>
      prevSeats.includes(seatId)
        ? prevSeats.filter((selectedSeat) => selectedSeat !== seatId)
        : [...prevSeats, seatId]
    );
  };
  

  const handleBookingSubmit = async () => {
    console.log('Booking details:', {
      movieId: id,
      selectedDate,
      selectedTime,
      numTickets,
      selectedSeats,
      selectedTheater,
    });
    const access_token = localStorage.getItem('access_token');
    console.log('Access Token:', access_token);
  
    const bookingData = {
      movieId: id,
      date: selectedDate,
      time: selectedTime,
      numTickets: numTickets,
      seats: selectedSeats,
      theater: selectedTheater.id,
    };
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/bookings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${access_token}`,
        },
        body: JSON.stringify(bookingData),
      });
  
      if (!response.ok) {
        console.error('Booking request failed:', response.status, response.statusText);
        const errorDetails = await response.json();
        console.error('Error details:', errorDetails);
        throw new Error('Booking failed. Please try again.');
      }
  
      // Handle successful booking response here...
    } catch (error) {
      console.error('Booking error:', error.message);
      // Handle additional error handling or display error to the user if needed
    }
  };
  
// Handle successful booking response here...

  
  
  
  return (
    <div className="booking-container">
      {!selectedTheater ? (
        <Theater onSelectTheater={handleTheaterSelect} />
      ) : (
        <>
          <h2>Book Tickets</h2>
          <label>
            Date:
            <input type="date" value={selectedDate} onChange={handleDateChange} />
          </label>
          <label>
            Time:
            <input type="time" value={selectedTime} onChange={handleTimeChange} />
          </label>
          <label>
            Number of Tickets:
            <input
              key={numTickets}
              type="number"
              value={numTickets}
              onChange={handleNumTicketsChange}
            />
          </label>
          <SeatList seats={seats} onSeatClick={handleSeatSelection} />
          <button onClick={handleBookingSubmit}>Book Now</button>
        </>
      )}
    </div>
  );
};

export default BookingPage;