from app import main

from .confest import test_app


def test_ping(test_app):
    resp = test_app.get("/test")
    assert resp.status_code == 200
    assert resp.json() == {"env": "dev", "message": "pong", "testing": True}
