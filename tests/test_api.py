from fastapi.testclient import TestClient

from ecommerce.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_existing_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_get_missing_product():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_create_order():
    response = client.post("/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "created"
    assert data["product_id"] == 1
    assert data["quantity"] == 2
    assert data["unit_price"] == 899.99
    assert data["total"] == 1799.98


def test_create_order_unknown_product():
    response = client.post("/orders", json={"product_id": 999, "quantity": 2})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_create_order_invalid_quantities():
    for quantity in [0, -1, 101]:
        response = client.post(
            "/orders",
            json={"product_id": 1, "quantity": quantity},
        )
        assert response.status_code == 422


def test_create_order_missing_fields():
    assert client.post("/orders", json={"quantity": 2}).status_code == 422
    assert client.post("/orders", json={"product_id": 1}).status_code == 422


def test_create_order_invalid_product_id():
    response = client.post(
        "/orders",
        json={"product_id": "not-an-id", "quantity": 2},
    )
    assert response.status_code == 422


def test_create_order_invalid_quantity_type():
    response = client.post(
        "/orders",
        json={"product_id": 1, "quantity": "not-a-number"},
    )
    assert response.status_code == 422


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    expected = {"/", "/health", "/products", "/products/{product_id}", "/orders"}
    assert expected.issubset(paths)
