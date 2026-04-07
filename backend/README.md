# FastAPI Backend

Phase 1 backend scaffold for the Spotify clone using FastAPI and SQLite.

## Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open the docs at `http://127.0.0.1:8000/docs`.

## Included MVP Areas

- JWT signup/login and profile updates
- Follow and unfollow users
- Track, album, and artist catalog with seeded demo data
- Audio streaming endpoint via remote URL redirect or local file response
- Like tracks, save albums/artists, and recently played history
- Playlist CRUD with add/remove tracks and privacy flag
- Playback state endpoints for play, pause, seek, next, previous, shuffle, repeat, and volume
- Search, autocomplete suggestions, and artist/album/genre filters
