import React from 'react';

const SeatComponent = ({ seats, onSeatClick }) => {
  return (
    <div>
      <h2>Select Your Seat</h2>
      <div className="seat-container">
        {seats.map((seat) => (
          <div
            key={seat.id}
            className={`seat ${seat.is_reserved ? 'booked' : ''}`}
            onClick={() => onSeatClick(seat.id)}
          >
            {seat.seat_number}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SeatComponent;
