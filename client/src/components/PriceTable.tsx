// Import necessary libraries
import React from 'react';
import Table from 'react-bootstrap/Table';

// Functional component for dispaying the movie price
const PriceTable = (props: any) => {
  // Get all the cinema names
  const cinemas = Object.keys(props.movieDetails);
  const movieDetails = props.movieDetails;
  return (
    <div>
      <Table striped bordered hover variant="dark">
        <tbody>
          <tr>
            <th colSpan={2}>
              <b>Price</b>
            </th>
          </tr>
          {cinemas.map((cinema, i) => (
            <tr key={i}>
              <td>{cinema.toUpperCase()}</td>
              <td>${movieDetails[cinema]['Price']}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};
// Export the component as the default object
export default PriceTable;
