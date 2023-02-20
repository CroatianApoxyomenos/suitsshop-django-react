import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Row, Col, ListGroup, Image, Card } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { PayPalButton } from "react-paypal-button-v2";
import Message from "../components/Message";
import Loader from "../components/Loader";
import { getOrderDetails, payOrder } from "../actions/orderActions";
import { ORDER_PAY_RESET } from "../constants/orderConstants";

function OrderScreen() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const [sdkReady, setSdkReady] = useState(false);
  const orderDetails = useSelector((state) => state.orderDetails);
  const { order, error, loading } = orderDetails;

  const orderPay = useSelector((state) => state.orderPay);
  const { loading: loadingPay, success: successPay } = orderPay;

  if (!loading && !error) {
    order.itemsPrice = order.order_items
      .reduce((acc, item) => acc + item.total_price * item.quantity, 0)
      .toFixed(2);
  }

  // ATqcB184E_aBVfLiTGrUZgI88s5Dy_tsuGsIQi5Ws3WutHa0LjKo_EwS3OvCQCejQiaEEYadR8XoT-vD

  const addPayPalScript = () => {
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src =
      "https://www.paypal.com/sdk/js?client-id=ATqcB184E_aBVfLiTGrUZgI88s5Dy_tsuGsIQi5Ws3WutHa0LjKo_EwS3OvCQCejQiaEEYadR8XoT-vD";
    script.async = true;
    script.onload = () => {
      setSdkReady(true);
    };
    document.body.appendChild(script);
  };

  useEffect(() => {
    if (!order || successPay || order.id !== Number(id)) {
      dispatch({ type: ORDER_PAY_RESET });
      dispatch(getOrderDetails(id));
    } else if (!order.is_paid) {
      if (!window.paypal) {
        addPayPalScript();
      } else {
        setSdkReady(true);
      }
    }
  }, [dispatch, order, id, successPay]);

  const successPayHandler = (paymentResult) => {
    dispatch(payOrder(id, paymentResult));
  };

  console.log(order);
  return loading ? (
    <Loader />
  ) : error ? (
    <Message variant="danger">{error}</Message>
  ) : (
    <div>
      <h1>Order: {order.id}</h1>
      <Row>
        <Col md={8}>
          <ListGroup variant="flush">
            <ListGroup.Item>
              <h2>Shipping</h2>
              <p>
                <strong>Name: </strong> {order.user.first_name}{" "}
                {order.user.last_name}
              </p>
              <p>
                <strong>Email: </strong> {order.user.email}
              </p>
              <p>
                <strong>Shipping: </strong>
                {order.shipping_address.address}, {order.shipping_address.city},
                {"   "}
                {order.shipping_address.postal_code},{"   "}
                {order.shipping_address.country}
              </p>

              {order.is_delivered ? (
                <Message variant="success">
                  Delivered on {order.delivered_at}
                </Message>
              ) : (
                <Message variant="warning">Not delivered!</Message>
              )}
            </ListGroup.Item>

            <ListGroup.Item>
              <h2>Payment Method</h2>
              <p>
                <strong>Method: </strong>
                {order.payment_method}
              </p>
              {order.is_paid ? (
                <Message variant="success">Paid on {order.paid_at}</Message>
              ) : (
                <Message variant="warning">Not paid!</Message>
              )}
            </ListGroup.Item>

            <ListGroup.Item>
              <h2>Order Items</h2>
              {order.order_items.length === 0 ? (
                <Message variant="info"> Your order is empty!</Message>
              ) : (
                <ListGroup variant="flush">
                  {order.order_items.map((item, index) => (
                    <ListGroup.Item key={index}>
                      <Row>
                        <Col md={1}>
                          <Image
                            src={item.image}
                            alt={item.product.name}
                            fluid
                            rounded
                          />
                        </Col>

                        <Col>
                          <Link
                            to={`/products/${item.product}`}
                            className="link-color-inherit"
                          >
                            {item.name}
                          </Link>
                        </Col>

                        <Col md={4}>
                          {item.quantity} X {item.total_price} RON ={" "}
                          {(item.quantity * item.total_price).toFixed(2)} RON
                        </Col>
                      </Row>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </ListGroup.Item>
          </ListGroup>
        </Col>
        <Col md={4}>
          <Card>
            <ListGroup variant="flush">
              <ListGroup.Item>
                <h2>ORDER SUMMARY</h2>
              </ListGroup.Item>

              <ListGroup.Item>
                <Row>
                  <Col>Items:</Col>
                  <Col>{order.itemsPrice} RON</Col>
                </Row>
              </ListGroup.Item>

              <ListGroup.Item>
                <Row>
                  <Col>Shipping:</Col>
                  <Col>{order.shipping_price} RON</Col>
                </Row>
              </ListGroup.Item>

              <ListGroup.Item>
                <Row>
                  <Col>Total Price:</Col>
                  <Col>{order.total_price} RON</Col>
                </Row>
              </ListGroup.Item>

              {!order.is_paid && (
                <ListGroup.Item>
                  {loadingPay && <Loader />}
                  {!sdkReady ? (
                    <Loader />
                  ) : (
                    <PayPalButton
                      amount={order.total_price}
                      onSuccess={successPayHandler}
                    />
                  )}
                </ListGroup.Item>
              )}
            </ListGroup>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default OrderScreen;
