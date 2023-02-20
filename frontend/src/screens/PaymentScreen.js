import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Row, Col, Form, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import FormContainer from "../components/FormContainer";
import CheckOut from "../components/CheckOut";
import { savePaymentMethod } from "../actions/cartActions";

function PaymentScreen() {
  const cart = useSelector((state) => state.cart);
  const { shippingAddress } = cart;
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [paymentMethod, setPaymentMethod] = useState("");

  if (!shippingAddress.address) {
    navigate("/shipping");
  }
  const submitHandler = (e) => {
    e.preventDefault();
    dispatch(savePaymentMethod(paymentMethod));
    navigate("/placeorder");
  };

  return (
    <FormContainer>
      <CheckOut step1 step2 step3 />

      <Form onSubmit={submitHandler}>
        <Form.Group>
          <Form.Label as="legend">Select Method</Form.Label>
          <Col>
            <Form.Check
              type="radio"
              label="PayPal"
              id="paypal"
              name="paymentMethod"
              value="PAYPAL"
              onChange={(e) => setPaymentMethod(e.target.value)}
            ></Form.Check>
          </Col>

          <Col>
            <Form.Check
              type="radio"
              label="Credit Card"
              id="creditCard"
              name="paymentMethod"
              value="CREDIT CARD"
              onChange={(e) => setPaymentMethod(e.target.value)}
            ></Form.Check>
          </Col>

          <Col>
            <Form.Check
              type="radio"
              label="Cash"
              id="cash"
              name="paymentMethod"
              value="CASH"
              onChange={(e) => setPaymentMethod(e.target.value)}
            ></Form.Check>
          </Col>
        </Form.Group>
        <Row className="py-3">
          <Col>
            <Button type="submit" variant="primary">
              Continue
            </Button>
          </Col>
        </Row>
      </Form>
    </FormContainer>
  );
}

export default PaymentScreen;
