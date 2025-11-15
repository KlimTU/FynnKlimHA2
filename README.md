![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge\&logo=svelte\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge\&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge\&logo=sqlite\&logoColor=white)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)
![Ruff](https://img.shields.io/badge/ruff-linter-ec4a3f?logo=ruff\&logoColor=white\&style=for-the-badge)
![CI](https://github.com/KlimTU/FynnKlimHA2/actions/workflows/ci.yml/badge.svg)

# Einführungsblatt Aufgabe 2

## Teammitglieder

Fynn Kaschta, Klim Trinko

## Projektbeschreibung

Einfache Notizen-Web-App mit Persistenz.

Funktionen:

* Erstellen und Löschen von Notizen
* Finden per ID und Sortieren von Notizen
* Nutzung einer lokalen Datenbank für Persistenz

Technologien:

* **Frontend:** Svelte (statische HTML-Seite)
* **Backend:** FastAPI (Python)
* **Datenbank:** SQLite

macOS (Terminal):
1. cd FynnKlimHA2
2. python3 -m venv venv
3. source venv/bin/activate

Windows (PowerShell):
1. cd FynnKlimHA2
2. python -m venv venv
3. venv\Scripts\Activate

4. pip install -r requirements.txt
5. uvicorn backend.main:app --reload
6. Öffnen Sie http://127.0.0.1:8000/
7. Viel Spaß!


## Anleitung zum Ausführen der Tests  

1. PYTHONPATH=. pytest -v


Dieses Projekt steht unter der [MIT License](LICENSE).

Copyright (c) 2025
Fynn Kaschta & Klim Trinko



Dieses Projekt steht unter der [MIT License](LICENSE).  
Copyright (c) 2025 Fynn Kaschta & Klim Trinko

