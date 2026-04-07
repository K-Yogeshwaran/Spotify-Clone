from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Album, Artist, Track


def seed_catalog(db: Session) -> None:
    if db.scalar(select(Artist.id).limit(1)) is not None:
        return

    catalog = [
        {
            "artist": {"name": "Neon Harbor", "genre": "Synthwave", "bio": "Retro night-drive duo."},
            "album": {"title": "Midnight Signals", "genre": "Synthwave", "release_year": 2023},
            "tracks": [
                {"title": "City Pulse", "duration_seconds": 218, "genre": "Synthwave", "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
                {"title": "Headlights", "duration_seconds": 201, "genre": "Synthwave", "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
            ],
        },
        {
            "artist": {"name": "Maple Static", "genre": "Indie Pop", "bio": "Warm hooks and hazy guitars."},
            "album": {"title": "Soft Corners", "genre": "Indie Pop", "release_year": 2024},
            "tracks": [
                {"title": "Postcards", "duration_seconds": 187, "genre": "Indie Pop", "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
                {"title": "Windowseat", "duration_seconds": 194, "genre": "Indie Pop", "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"},
            ],
        },
        {
            "artist": {"name": "Paper Tigers", "genre": "Alt Rock", "bio": "Loud choruses, tight riffs."},
            "album": {"title": "Static Bloom", "genre": "Alt Rock", "release_year": 2022},
            "tracks": [
                {"title": "Afterglow Arcade", "duration_seconds": 233, "genre": "Alt Rock", "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"},
                {"title": "Voltage Youth", "duration_seconds": 210, "genre": "Alt Rock", "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"},
            ],
        },
    ]

    for entry in catalog:
        artist = Artist(**entry["artist"])
        album = Album(**entry["album"], artist=artist)
        db.add_all([artist, album])
        db.flush()
        for track_data in entry["tracks"]:
            db.add(Track(**track_data, artist=artist, album=album))
    db.commit()
