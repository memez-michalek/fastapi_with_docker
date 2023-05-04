import json

import pytest

from .confest import test_app_with_db  # noqa: F401,F811


def test_create_summary(test_app_with_db):  # noqa: F401,F811
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    assert resp.status_code == 201
    assert resp.json()["url"] == "https://foo.bar"


def test_create_summary_invalid_json(test_app_with_db):  # noqa: F401,F811
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

    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "invalid://url"})
    )
    assert resp.status_code == 422
    assert resp.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_get_summary(test_app_with_db):  # noqa: F401,F811
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


def test_get_summary_incorrect_id(test_app_with_db):  # noqa: F401,F811
    resp = test_app_with_db.get("/summaries/999/")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Summary not found"

    resp = test_app_with_db.get("/summaries/0/")
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_remove_summary(test_app_with_db):  # noqa: F401,F811
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    resp_id = resp.json()["id"]

    resp = test_app_with_db.delete(f"/summaries/{resp_id}/")
    assert resp.status_code == 200
    assert resp.json() == {"id": resp_id, "url": "https://foo.bar"}


def test_remove_summary_incorrect_id(test_app_with_db): # noqa: F401,F811
    resp = test_app_with_db.delete("/summaries/999/")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Summary not found"

    resp = test_app_with_db.delete("/summaries/0/")
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_summary(test_app_with_db): # noqa: F401,F811
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    resp_id = resp.json()["id"]

    resp = test_app_with_db.put(
        f"/summaries/{resp_id}/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert resp.status_code == 200
    response_dict = resp.json()
    assert response_dict["id"] == resp_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "summary": "updated!"},
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "loc": ["body", "summary"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_app_with_db, summary_id, payload, status_code, detail # noqa: F401,F811
):
    resp = test_app_with_db.put(f"/summaries/{summary_id}", data=json.dumps(payload))
    assert resp.status_code == status_code
    assert resp.json()["detail"] == detail


def test_update_summary_invalid_url(test_app_with_db): # noqa: F401,F811
    resp = test_app_with_db.put(
        "/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert resp.status_code == 422
    assert resp.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_update_summary_incorrect_id(test_app_with_db): # noqa: F401,F811
    resp = test_app_with_db.put( 
        "/summaries/999/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Summary not found"

    resp = test_app_with_db.put(
        "/summaries/0/",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_summary_invalid_json(test_app_with_db): # noqa: F401,F811
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    resp_id = resp.json()["id"]

    resp = test_app_with_db.put(f"summaries/{resp_id}", data=json.dumps({}))
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_update_summaries_invalid_keys(test_app_with_db): # noqa: F401,F811
    resp = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    resp_id = resp.json()["id"]

    resp = test_app_with_db.put(
        f"/summaries/{resp_id}/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    resp = test_app_with_db.put(
        f"/summaries/{resp_id}",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert resp.status_code == 422
    assert resp.json()["detail"][0]["msg"] == "URL scheme not permitted"
