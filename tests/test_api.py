import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Damit pytest die backend-App findet (Project Root in den Python-Pfad aufnehmen)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.main import app

client = TestClient(app)


def test_frontend_index_loads():
    """Testet, ob die Startseite erreichbar ist."""

    response = client.get("/")
    assert response.status_code == 200

    # Es muss kein exakter Text geprüft werden – nur ob HTML zurückkommt.
    assert "<!DOCTYPE" in response.text or "html" in response.text.lower()


def test_create_and_read_note():
    """Legt einen Eintrag an und prüft, ob dieser wieder abrufbar ist."""

    new_note = {"title": "Notiz zum Test", "body": "Eintrag für Testzwecke"}

    # POST-Request zum Anlegen
    create_response = client.post("/api/items", json=new_note)
    assert create_response.status_code == 201

    created = create_response.json()

    # Überprüfung der Inhalte
    assert created["title"] == new_note["title"]
    assert created["body"] == new_note["body"]
    assert "id" in created  # muss eine ID bekommen

    # Die Liste der Notizen abrufen und prüfen, ob der Eintrag enthalten ist
    list_response = client.get("/api/items")
    notes = list_response.json()

    assert any(note["id"] == created["id"] for note in notes)


def test_delete_note_and_verify():
    """Erstellt eine Notiz, löscht sie und prüft anschließend, ob sie verschwunden ist."""

    temp_note = {"title": "Zum Löschen", "body": "Soll später nicht mehr existieren"}

    # Anlegen einer Notiz
    create_response = client.post("/api/items", json=temp_note)
    assert create_response.status_code == 201

    note_id = create_response.json()["id"]

    # Löschen des Eintrags
    delete_response = client.delete(f"/api/items/{note_id}")
    assert delete_response.status_code == 204

    # Liste erneut abrufen und sicherstellen, dass die ID nicht mehr existiert
    updated_list = client.get("/api/items").json()

    assert all(entry["id"] != note_id for entry in updated_list)
