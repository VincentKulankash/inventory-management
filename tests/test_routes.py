"""Tests for the Flask REST API routes."""
import pytest

from app import app


@pytest.fixture
def client():
    """Flask test client — no real server needed."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


#GET all
def test_get_all_returns_list(client):
    r = client.get("/inventory")
    assert r.status_code == 200
    assert isinstance(r.json, list)
    assert len(r.json) == 2   # the two seed items


#GET one

def test_get_one_existing(client):
    r = client.get("/inventory/1")
    assert r.status_code == 200
    assert r.json["id"] == 1
    assert r.json["product_name"] == "Organic Almond Milk"


def test_get_one_missing(client):
    r = client.get("/inventory/9999")
    assert r.status_code == 404
    assert "not found" in r.json["error"].lower()


#POST

def test_create_item_success(client):
    r = client.post("/inventory", json={
        "product_name": "Test Yogurt",
        "brands": "Chobani",
        "price": 1.99,
        "stock": 8,
    })
    assert r.status_code == 201
    assert r.json["id"] == 3   # next id after the two seeds
    assert r.json["product_name"] == "Test Yogurt"
    assert r.json["price"] == 1.99
    assert r.json["stock"] == 8


def test_create_item_missing_name(client):
    r = client.post("/inventory", json={"price": 1.99})
    assert r.status_code == 400
    assert "required" in r.json["error"].lower()


def test_create_item_no_body(client):
    r = client.post("/inventory")
    assert r.status_code == 400


#PATCH

def test_update_price(client):
    r = client.patch("/inventory/1", json={"price": 9.99})
    assert r.status_code == 200
    assert r.json["price"] == 9.99


def test_update_stock(client):
    r = client.patch("/inventory/1", json={"stock": 100})
    assert r.status_code == 200
    assert r.json["stock"] == 100


def test_update_missing_item(client):
    r = client.patch("/inventory/9999", json={"price": 1.0})
    assert r.status_code == 404


#DELETE

def test_delete_existing(client):
    r = client.delete("/inventory/1")
    assert r.status_code == 200
    assert "deleted" in r.json["message"].lower()

    # Confirm it's actually gone
    r2 = client.get("/inventory/1")
    assert r2.status_code == 404


def test_delete_missing(client):
    r = client.delete("/inventory/9999")
    assert r.status_code == 404