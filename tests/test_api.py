import sys
from pathlib import Path
from fastapi.testclient import TestClient

# --- Ensure project root is in Python path for imports ---
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.main import app

client = TestClient(app)


def test_frontend_root_serves_html():
    """Check that the frontend index loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.text.lower()  # basic sanity check


def test_create_note_and_fetch_it():
    """Create a new note and verify it exists."""
    payload = {"title": "Test Note", "body": "This is a test entry"}

    # Create
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201

    created_note = response.json()
    assert created_note["title"] == payload["title"]
    assert created_note["body"] == payload["body"]
    assert "id" in created_note

    # Fetch list to confirm presence
    list_response = client.get("/api/items")
    notes = list_response.json()

    assert any(note["id"] == created_note["id"] for note in notes)


def test_delete_note():
    """Create a note, delete it, and verify it is gone."""
    payload = {"title": "Delete Me", "body": "To be removed"}

    # Create note first
    create_response = client.post("/api/items", json=payload)
    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    # Delete note
    delete_response = client.delete(f"/api/items/{note_id}")
    assert delete_response.status_code == 204

    # Check that it no longer exists
    list_response = client.get("/api/items")
    notes = list_response.json()

    assert all(note["id"] != note_id for note in notes)
