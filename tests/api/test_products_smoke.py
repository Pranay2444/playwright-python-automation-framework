"""A small live contract check: no hard-coded product ID or catalogue count."""

import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.api
@pytest.mark.smoke
def test_products_api_returns_catalog(api_context: APIRequestContext) -> None:
    response = api_context.get("/products")

    assert response.status == 200, f"Unexpected HTTP status: {response.status}"
    body = response.json()
    assert isinstance(body, dict), "Expected a JSON object"
    products = body.get("data")
    assert isinstance(products, list), "Expected a 'data' list"
    assert products, "The product catalogue must not be empty"

    product = products[0]
    assert isinstance(product, dict)
    assert isinstance(product.get("id"), str) and product["id"]
    assert isinstance(product.get("name"), str) and product["name"].strip()
    assert type(product.get("price")) in (int, float), "Price must be numeric"
    assert product["price"] >= 0
