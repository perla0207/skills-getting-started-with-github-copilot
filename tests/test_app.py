import copy
import pathlib
import importlib.util
import urllib.parse

import pytest
from fastapi.testclient import TestClient

# Load app module by path (works even if src isn't a package)
ROOT = pathlib.Path(__file__).resolve().parent.parent
app_path = ROOT / "src" / "app.py"
spec = importlib.util.spec_from_file_location("app_module", str(app_path))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    # Arrange: keep original state
    original = copy.deepcopy(app_module.activities)
    yield
    # Assert/Teardown: restore original state after each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


def _encode(name: str) -> str:
    return urllib.parse.quote(name, safe="")


def test_get_activities_contains_chess_club(client=client):
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_delete_participant(client=client):
    # Arrange
    activity = "Chess Club"
    email = "test.user@example.com"
    encoded = _encode(activity)

    # Act: signup
    post_resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert signup succeeded and in-memory updated
    assert post_resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Act: delete
    del_resp = client.delete(f"/activities/{encoded}/participants", params={"email": email})

    # Assert deletion succeeded and removed
    assert del_resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_duplicate_signup_returns_400(client=client):
    # Arrange
    activity = "Programming Class"
    email = "emma@mergington.edu"
    encoded = _encode(activity)

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400