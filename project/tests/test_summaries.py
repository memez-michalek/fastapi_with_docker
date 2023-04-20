import json

import pytest

from .confest import test_app_with_db


def test_create_summary(test_app_with_db):
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    assert resp.status_code == 201
    assert resp.json()["url"] == "https://foo.bar"


def test_create_summary_invalid_json(test_app_with_db):
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"link": "https://foo.bar"})
    )
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_get_summary(test_app_with_db):
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    resp_id = resp.json()["id"]

    resp = test_app_with_db.get(f"/summaries/{resp_id}/")
    assert resp.status_code == 200

    resp_dict = resp.json()

    assert resp_dict["id"] == resp_id
    assert resp_dict["url"] == "https://foo.bar"
    assert resp_dict["summary"]
    assert resp_dict["created_at"]


def test_get_summary_incorrect_id(test_app_with_db):
    resp = test_app_with_db.get(f"/summaries/999/")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Summary not found"
