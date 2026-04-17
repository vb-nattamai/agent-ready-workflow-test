"""Tests for the Order Service API."""
import json
import pytest
from src.app import app, store


@pytest.fixture(autouse=True)
def reset_store():
    """Clear in-memory store between tests."""
    store._orders.clear()
    yield
    store._orders.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_create_order(client):
    r = client.post("/orders", json={"customer_id": "c1", "items": [{"sku": "A", "qty": 2}]})
    assert r.status_code == 201
    data = r.get_json()
    assert data["customer_id"] == "c1"
    assert data["status"] == "pending"
    assert "id" in data


def test_create_order_missing_customer(client):
    r = client.post("/orders", json={"items": [{"sku": "A"}]})
    assert r.status_code == 400


def test_create_order_empty_items(client):
    r = client.post("/orders", json={"customer_id": "c1", "items": []})
    assert r.status_code == 400


def test_get_order(client):
    r = client.post("/orders", json={"customer_id": "c1", "items": [{"sku": "B"}]})
    order_id = r.get_json()["id"]
    r2 = client.get(f"/orders/{order_id}")
    assert r2.status_code == 200
    assert r2.get_json()["id"] == order_id


def test_get_order_not_found(client):
    assert client.get("/orders/does-not-exist").status_code == 404


def test_list_orders_by_customer(client):
    client.post("/orders", json={"customer_id": "c2", "items": [{"sku": "X"}]})
    client.post("/orders", json={"customer_id": "c2", "items": [{"sku": "Y"}]})
    client.post("/orders", json={"customer_id": "c3", "items": [{"sku": "Z"}]})
    r = client.get("/orders?customer=c2")
    assert r.status_code == 200
    assert len(r.get_json()) == 2


def test_list_orders_missing_customer(client):
    assert client.get("/orders").status_code == 400


def test_cancel_order(client):
    r = client.post("/orders", json={"customer_id": "c1", "items": [{"sku": "A"}]})
    order_id = r.get_json()["id"]
    r2 = client.patch(f"/orders/{order_id}/cancel")
    assert r2.status_code == 200
    assert r2.get_json()["status"] == "cancelled"


def test_cancel_already_cancelled(client):
    r = client.post("/orders", json={"customer_id": "c1", "items": [{"sku": "A"}]})
    order_id = r.get_json()["id"]
    client.patch(f"/orders/{order_id}/cancel")
    r2 = client.patch(f"/orders/{order_id}/cancel")
    assert r2.status_code == 409
