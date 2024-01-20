import React from 'react';
import './style.css';
import { Link } from 'react-router-dom';

const MovieCard = ({ movie }) => {
  if (!movie) {
    return null;
  }

  const { title, genre, rating, movie_length, language, image, id } = movie;

  return (
    <div className='card-container'>
      <div className="card-img-container">
       <Link to ={"/movies/details/" +id}> <img className="card-img" src={image} alt="movie-card" /></Link>
      </div>
      <div className='card-details'>
        <div>
          <span className='title'>{title}</span>
        </div>
        <div>
          <span className='genre'>{genre}</span>
          <span className='genre'>{language}</span>
        </div>
        <div className='rating'>
          <span>{rating}</span>
          <span>{movie_length}</span>
          <span>{id}</span>
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
