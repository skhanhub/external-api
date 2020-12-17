import axios from 'axios';

const API = {
  getMovieList: async () => {
    const result = await axios.get(`/api/movies`);
    return result.data;
  },
  getMovieDetails: async (movie: { [key: string]: string }) => {
    const result = await axios.post(`/api/movie`, movie);
    return result.data;
  },
};
export default API;
