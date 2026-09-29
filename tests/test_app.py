import pytest

from hello_web.app import create_app
from hello_web.greeting import greeting


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize("name,expected", [
    ("", "Hello, World!"),
    ("  ", "Hello, World!"),
    (" Balaji ", "Hello, Balaji!"),
    ("உலகம்", "Hello, உலகம்!"),
])
def test_greeting(name, expected):
    assert greeting(name) == expected


def test_name_length_boundary():
    assert greeting("a" * 80) == "Hello, " + "a" * 80 + "!"
    with pytest.raises(ValueError, match="80 characters"):
        greeting("a" * 81)


def test_website_and_assets(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert b"Hello from Python" in response.data
    for path in ["/style.css", "/app.js"]:
        assert client.get(path).status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "stack": "python"}


def test_greeting_endpoint(client):
    assert client.get("/api/greet").text == "Hello, World!"
    response = client.get("/api/greet?name=Ada%20Lovelace")
    assert response.status_code == 200
    assert response.text == "Hello, Ada Lovelace!"
    assert response.mimetype == "text/plain"


def test_long_name_is_bad_request(client):
    response = client.get("/api/greet", query_string={"name": "a" * 81})
    assert response.status_code == 400
    assert "80 characters" in response.text


def test_unknown_route_and_unsupported_method(client):
    assert client.get("/missing").status_code == 404
    assert client.get("/health/extra").status_code == 404
    assert client.post("/api/greet").status_code == 405
