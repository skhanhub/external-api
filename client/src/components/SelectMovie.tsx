// Import necessary libraries
import React from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
// Functional component for dispaying the movie names
const SelectMovie = (props: any) => {
  return (
    <form>
      <Form.Row className="justify-content-md-center">
        <Col md="auto">
          <Form.Group>
            <Form.Label>Movies</Form.Label>
            <Form.Control as="select" onChange={props.newMovieSelected}>
              {Object.keys(props.movies).map((movie: string, i: number) => (
                <option key={i} value={movie}>
                  {movie}
                </option>
              ))}
            </Form.Control>
          </Form.Group>
        </Col>
      </Form.Row>
    </form>
  );
};
// Export the component as the default object
export default SelectMovie;
