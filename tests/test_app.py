import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app

client = TestClient(app)


def test_get_activities():
    """Test that we can fetch all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) > 0
    assert "Chess Club" in activities


def test_signup_for_activity():
    """Test signing up for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]


def test_signup_duplicate_fails():
    """Test that signing up twice for the same activity fails"""
    email = "duplicate@mergington.edu"
    # First signup should succeed
    response1 = client.post(
        f"/activities/Chess%20Club/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(
        f"/activities/Chess%20Club/signup?email={email}"
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_unregister_from_activity():
    """Test unregistering from an activity"""
    email = "unregister@mergington.edu"
    # First signup
    signup_response = client.post(
        f"/activities/Programming%20Class/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Then unregister
    unregister_response = client.delete(
        f"/activities/Programming%20Class/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    assert "Unregistered" in unregister_response.json()["message"]


def test_activity_not_found():
    """Test that accessing a non-existent activity returns 404"""
    response = client.post(
        "/activities/Fake%20Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_not_registered():
    """Test that unregistering a non-registered student fails"""
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=never@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
