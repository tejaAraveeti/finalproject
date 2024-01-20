// MovieList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MovieCard from './MovieCard';
import MovieFilter from '../MovieFilter';
import "./style.css";
const MovieList = () => {
  const [movies, setMovies] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true);
        const { data } = await axios.get(`http://127.0.0.1:8000/api/movies/?page=${currentPage}`);
        
        setMovies((prevMovies) => {
          // Filter out movies with duplicate IDs before appending
          const uniqueMovies = data.data.filter((newMovie) => {
            return !prevMovies.find((prevMovie) => prevMovie.id === newMovie.id);
          });
          return [...prevMovies, ...uniqueMovies];
        });

        setLoading(false);
      } catch (error) {
        console.error("Error fetching movies:", error);
        setLoading(false);
      }
    };

    fetchMovies();
  }, [currentPage, filters]);

  const handleNextPage = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };

  const handleFilterChange = (newFilters) => {
    // Update filters and reset page to 1 when filters change
    setFilters(newFilters);
    setCurrentPage(1);
  };

  return (
    <div className="App">
      <h1 className="text-center">Movies</h1>
      <MovieFilter onFilterChange={handleFilterChange} />

      <main className="main">
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </main>
      {loading && <p>Loading...</p>}
      {!loading && (
        <button onClick={handleNextPage} disabled={loading}>
          Load More
        </button>
      )}
    </div>
  );
};

export default MovieList;
