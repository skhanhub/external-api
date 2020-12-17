import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import SelectMovie from './components/SelectMovie';
import PriceTable from './components/PriceTable';
import Errors from './components/Errors';
import API from './utils/API';
import './App.css';

function App() {
  const [movies, setMovies] = useState<any>({});
  const [movieDetails, setMovieDetails] = useState({});
  const [movieSelected, setMovieSelected] = useState('');
  const [error, setError] = useState('');
  const [errorCode, setErrorCode] = useState(0);
  const [loadingMovies, setLoadingMovies] = useState(true);
  const [loadingPrice, setLoadingPrice] = useState(true);

  // Get the movie names after the component mounts
  useEffect(() => {
    getMovies();
  }, []);

  useEffect(() => {
    getMovieDetails();
  }, [movieSelected]);
  // Function for getting movie names
  // This function does not take any arguments
  const getMovies = async () => {
    let data: any = {};
    // Try at most three times to get the data from the backend
    for (let i = 0; i < 3; i++) {
      data = await API.getMovieList();
      if (data['code'] !== 2) {
        break;
      }
    }
    // If unsuccessful then show error
    if (data['code'] === 2) {
      setErrorCode(1);
      setError('Could not retrive Movies');
    }
    // If successfull then then change the state and get movie details
    else {
      setErrorCode(0);
      setError('');
      setMovies(data['movies']);
      setMovieSelected(Object.keys(data['movies'])[0]);
    }
    setLoadingMovies(false);
  };

  // Function for getting movie price
  // This function does not take any arguments
  const getMovieDetails = async () => {
    // Set loading to true
    setLoadingPrice(true);
    let data;
    // Try at most three times to get the data from the backend
    for (let i = 0; i < 3; i++) {
      data = await API.getMovieDetails({
        ...movies[movieSelected], // body data type must match "Content-Type" header
      });

      if (data['code'] !== 2) {
        break;
      }
    }
    // If unsuccessful then show error
    if (data['code'] === 2) {
      setErrorCode(2);
      setError('Could not retrive price');
    }
    // If successfull then then change the state
    else {
      setError('');
      setMovieDetails(data['cinemas']);
    }
    setLoadingPrice(false);
  };

  // Function for updating the state with the selected movie
  const newMovieSelected = async (e: any) => {
    console.log(e.target.value);
    setMovieSelected(e.target.value);
  };
  // Function for clearing errors
  const clearError = (e: any) => {
    setError('');
  };
  // Function for trying to fetch data from the client again
  const tryAgain = async (e: any) => {
    if (errorCode === 1) await getMovies();
    else if (errorCode === 2) await getMovieDetails();
  };

  return (
    <div className="App">
      <header className="App-header">
        <Container>
          {error ? ( // If showErrors is true then render only the error component
            <Errors
              errorMessage={error}
              errorCode={errorCode}
              clearError={clearError}
              tryAgain={tryAgain}
            /> // If showErrors is false then diplay the other components
          ) : loadingMovies ? (
            <p>Loading</p> // Show loading message while fetching movies
          ) : (
            <React.Fragment>
              <Container>
                <h1 style={{ margin: '50px' }}>Compare Movie Price</h1>
              </Container>
              <Container>
                <SelectMovie
                  newMovieSelected={newMovieSelected}
                  movies={movies}
                />
              </Container>
              <Container>
                {loadingPrice ? (
                  <p>Getting Price</p> // Show 'Getting Price' message while fetching price
                ) : (
                  <PriceTable movieDetails={movieDetails} />
                )}
              </Container>
            </React.Fragment>
          )}
        </Container>
      </header>
    </div>
  );
}

export default App;
