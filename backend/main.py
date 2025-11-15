from datetime import datetime
from typing import Optional, List

# --- FastAPI & Hilfsklassen importieren ---
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Validierungs- und Datenmodelle ---
from pydantic import BaseModel, Field, validator
from sqlmodel import Field as SQLField, Session, SQLModel, create_engine, select


# ==========================================================
#   MODELLE
# ==========================================================


# Basismodell für Notizen (wird von beiden anderen Klassen geerbt)
class NoteBase(SQLModel):
    # Titel: Index für schnelle Suche, Mindest- und Maximallänge
    title: str = SQLField(index=True, min_length=1, max_length=200)
    # Inhalt der Notiz (Pflichtfeld)
    body: str = SQLField(min_length=1)


# Datenbankmodell (tatsächliche Tabelle)
class Note(NoteBase, table=True):
    # Primärschlüssel-ID
    id: Optional[int] = SQLField(default=None, primary_key=True)
    # Zeitstempel, wann die Notiz erstellt wurde
    created_at: datetime = SQLField(default_factory=datetime.utcnow, index=True)


# Eingabemodell für neue Notizen (wird beim POST verwendet)
class NoteCreate(NoteBase):
    pass


# Ausgabemodell für API-Antworten (wird beim Lesen zurückgegeben)
class NoteRead(NoteBase):
    id: int
    created_at: datetime


# ==========================================================
#   DATENBANK
# ==========================================================

# Verbindung zur SQLite-Datenbank herstellen
# -> Erstellt automatisch eine Datei "notes.db" im Projektordner
engine = create_engine("sqlite:///notes.db", connect_args={"check_same_thread": False})


# Funktion, um Tabellen bei App-Start zu erstellen (falls noch nicht vorhanden)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Session-Generator: Öffnet eine DB-Verbindung für jede Anfrage
def get_session():
    with Session(engine) as session:
        yield session


# ==========================================================
#   FASTAPI-APP INITIALISIERUNG
# ==========================================================

# FastAPI-Instanz erstellen
app = FastAPI(title="Notes API", version="1.0.0")

# --- Optionales CORS: erlaubt Anfragen von anderen Domains (z. B. lokalem Frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # erlaubt alle Ursprünge (für Entwicklung)
    allow_credentials=True,
    allow_methods=["*"],  # erlaubt alle HTTP-Methoden
    allow_headers=["*"],  # erlaubt alle Header
)


# --- Wird beim Start der App ausgeführt ---
@app.on_event("startup")
def on_startup():
    # Tabellen erstellen, falls sie noch nicht existieren
    create_db_and_tables()


# ==========================================================
#   REST-ENDPUNKTE
# ==========================================================


# --- Neue Notiz anlegen ---
@app.post("/api/items", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: NoteCreate, session: Session = Depends(get_session)):
    note = Note(**payload.dict())  # JSON in Note-Objekt umwandeln
    session.add(note)  # Notiz speichern
    session.commit()  # Änderungen schreiben
    session.refresh(note)  # Objekt aktualisieren (ID etc.)
    return note  # Rückgabe an den Client


# --- Alle Notizen abrufen (mit optionaler Filter- und Sortierfunktion) ---
@app.get("/api/items", response_model=List[NoteRead])
def list_items(
    q: Optional[str] = None,  # Suchbegriff (optional)
    sort: Optional[str] = "created_at",  # Sortierfeld (Standard: nach Erstellungsdatum)
    session: Session = Depends(get_session),
):
    stmt = select(Note)
    # Falls ein Suchbegriff angegeben wurde -> Filter anwenden
    if q:
        like = f"%{q}%"
        stmt = stmt.where((Note.title.ilike(like)) | (Note.body.ilike(like)))
    # Sortierung (z. B. -created_at = absteigend)
    if sort in {"created_at", "-created_at", "title", "-title", "id", "-id"}:
        desc = sort.startswith("-")
        field = sort[1:] if desc else sort
        col = getattr(Note, field)
        if desc:
            col = col.desc()
        stmt = stmt.order_by(col)
    # Alle passenden Notizen abrufen
    return session.exec(stmt).all()


# --- Einzelne Notiz per ID abrufen ---
@app.get("/api/items/{item_id}", response_model=NoteRead)
def get_item(item_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, item_id)
    if not note:
        # Falls keine Notiz gefunden -> HTTP 404 Fehler
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return note


# --- Notiz löschen ---
@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, item_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    session.delete(note)
    session.commit()
    return


# ==========================================================
#   FRONTEND-SERVING
# ==========================================================

# Statische Dateien (HTML, JS, CSS) unter /static bereitstellen
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
