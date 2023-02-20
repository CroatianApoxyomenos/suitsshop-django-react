import React from "react";
import { Container, Row, Col } from "react-bootstrap";

function FormContainer({ children }) {
  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col xs={12} md={6}>
          <div className="text-center">
            <img
              src="https://static.thenounproject.com/png/4953788-200.png"
              alt="Login"
            />
          </div>
          {children}
        </Col>
      </Row>
    </Container>
  );
}

export default FormContainer;
