from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect a known activity to be present
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    test_email = "test_student@example.com"

    # Ensure test email not present initially
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    assert test_email not in resp.json()[activity]["participants"]

    # Sign up the test user
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {test_email} for {activity}"

    # Verify participant added
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    assert test_email in resp.json()[activity]["participants"]

    # Unregister the test user
    resp = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Unregistered {test_email} from {activity}"

    # Verify participant removed
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    assert test_email not in resp.json()[activity]["participants"]


def test_signup_already_registered():
    activity = "Programming Class"
    existing_email = activities[activity]["participants"][0]

    # Try to sign up an already registered user
    resp = client.post(f"/activities/{activity}/signup?email={existing_email}")
    assert resp.status_code == 400


def test_unregister_not_registered():
    activity = "Programming Class"
    fake_email = "i_do_not_exist@example.com"

    # Try to unregister someone not in the activity
    resp = client.delete(f"/activities/{activity}/unregister?email={fake_email}")
    assert resp.status_code == 404
