# Cosmic Synaptic — Flask Backend + Frontend

This package contains a minimal Flask backend (`app.py`) providing a `/predict` POST endpoint and a static frontend (`static/index.html`) that calls the API. It's ready to deploy to Render or Railway.

## To run locally
1. python -m venv env
2. source env/bin/activate  # or env\Scripts\activate on Windows
3. pip install -r requirements.txt
4. python app.py
5. Open http://localhost:5000

## To deploy to Render (recommended)
1. Create a GitHub repo with these files.
2. On Render, create a new Web Service and connect to the repo; Render will auto-detect Python and use `gunicorn`.
3. Set the build command (if needed): `pip install -r requirements.txt`
4. Start command usually `gunicorn app:app` (Procfile included).

See Render docs: https://render.com/docs/deploy-flask

