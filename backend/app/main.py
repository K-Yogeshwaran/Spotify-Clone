import time
from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
from app.routers import auth, catalog, library, playback, playlists, users
from app.seed import seed_catalog


app = FastAPI(title="Spotify Clone API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            with SessionLocal() as db:
                seed_catalog(db)
            print("Database connected and seeded successfully!")
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(
                    f"Failed to connect to database after {max_retries} attempts: {e}"
                )
                raise
            print(
                f"Database connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds..."
            )
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff


@app.get("/health")
def health():
    return {"status": "okay"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(catalog.router)
app.include_router(library.router)
app.include_router(playlists.router)
app.include_router(playback.router)
