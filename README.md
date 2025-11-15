![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Ruff](https://img.shields.io/badge/lint-ruff-ec4a3f?logo=ruff&logoColor=white)
![CI](https://github.com/KlimTU/FynnKlimHA2/actions/workflows/CI.yml/badge.svg)

# Einführungsblatt Aufgabe 2  

## Teammitglieder  

Fynn Kaschta, Klim Trinko

## Projektbeschreibung  

Einfache Notizen-Web-App mit Persistenz  

- Frontend: Statische HTML-Seite (Svelte)  
- Backend: FastAPI (Python) + SQLite  

## Anleitung zum Aufsetzen und Starten  

macOS (Terminal):  
1. cd ppvs-fynnklim/backend  
2. python3 -m venv venv  
3. source venv/bin/activate  

Windows (PowerShell):  
1. cd ppvs-fynnklim\backend  
2. python -m venv venv  
3. venv\Scripts\Activate  

4. pip install -r ../requirements.txt  
5. cd ..  
6. uvicorn backend.main:app --reload  
7. Öffnen Sie http://127.0.0.1:8000/  
8. Viel Spaß!  

Dieses Projekt steht unter der [MIT License](LICENSE).  
Copyright (c) 2025 Fynn Kaschta & Klim Trinko
