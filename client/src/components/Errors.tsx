import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
// Functional component for displaying errors
const Errors = (props: any) => {
  return (
    <Col>
      <Row className="justify-content-md-center">
        <p style={{ color: 'red' }}>{props.errorMessage}</p>
      </Row>
      <Row className="justify-content-md-center">
        {props.errorCode === 1 || props.errorCode === 2 ? ( // Display 'Try Again' button if errorCode is 1 or 2
          <button
            style={{ color: 'purple' }}
            onClick={props.tryAgain}
            className="close"
            aria-label="Close"
          >
            Try Again
          </button>
        ) : null}
        <button onClick={props.clearError} className="close" aria-label="Close">
          <span
            aria-hidden="true"
            style={{ color: 'red', margin: '0 0 0 3em ' }}
          >
            ×
          </span>
        </button>
      </Row>
    </Col>
  );
};

export default Errors;
