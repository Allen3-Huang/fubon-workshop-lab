from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_products(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 6
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["items"][0]["name"] == "Zenbook 14 OLED"


def test_get_product(client: TestClient) -> None:
    response = client.get("/products/2")

    assert response.status_code == 200
    assert response.json()["name"] == "ROG Zephyrus G14"


def test_get_missing_product(client: TestClient) -> None:
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_list_products_max_price_filters(client: TestClient) -> None:
    response = client.get("/products?max_price=40000")

    assert response.status_code == 200
    body = response.json()
    assert all(item["price"] <= 40000 for item in body["items"])
    assert body["total"] == len(body["items"])


def test_list_products_max_price_zero_is_invalid(client: TestClient) -> None:
    response = client.get("/products?max_price=0")

    assert response.status_code == 422


def test_list_products_max_price_negative_is_invalid(client: TestClient) -> None:
    response = client.get("/products?max_price=-1")

    assert response.status_code == 422


def test_list_products_max_price_absent_returns_all(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()["total"] == 6
