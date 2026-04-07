import time
from fastapi import FastAPI
from app.routers import auth, catalog, library, playback, playlists, users


app = FastAPI(title="Spotify Clone API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    # No database creation needed with Supabase
    print("Spotify Clone API starting up with Supabase backend...")


@app.get("/health")
def health():
    return {"status": "okay", "database": "supabase"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(catalog.router)
app.include_router(library.router)
app.include_router(playlists.router)
app.include_router(playback.router)
