import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"ShopWave" in r.data

def test_products_listed(client):
    r = client.get("/")
    assert b"Wireless Headphones" in r.data
    assert b"Smart Watch" in r.data

def test_cart_empty(client):
    r = client.get("/cart")
    assert r.status_code == 200
    assert b"empty" in r.data.lower()

def test_add_to_cart(client):
    r = client.get("/add/1", follow_redirects=True)
    assert r.status_code == 200
    assert b"Cart (1)" in r.data

def test_remove_from_cart(client):
    client.get("/add/1")
    r = client.get("/remove/1", follow_redirects=True)
    assert r.status_code == 200