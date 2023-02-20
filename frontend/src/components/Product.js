import React from "react";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

function Product({ product }) {
  return (
    <Card className="my-3 p-3 rounded">
      <Link to={`/products/${product.id}`}>
        <Card.Img src={product.image}></Card.Img>
      </Link>

      <Card.Body>
        <Link to={`/products/${product.id}`} className="link-color-inherit">
          <Card.Title as="div">
            <strong>{product.name}</strong>
          </Card.Title>
        </Link>
        <Card.Text as="h3">{product.price} RON</Card.Text>
      </Card.Body>
    </Card>
  );
}

export default Product;
