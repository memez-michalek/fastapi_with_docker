

from .confest import test_app # noqa: F401


def test_ping(test_app): # noqa: F401
    resp = test_app.get("/test")
    assert resp.status_code == 200
    assert resp.json() == {"env": "dev", "message": "pong", "testing": True}
