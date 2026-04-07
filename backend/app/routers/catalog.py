from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Album, Artist, Track
from app.schemas import AlbumOut, ArtistOut, SearchResponse, SuggestionResponse, TrackOut
from app.services import search_catalog, stream_track_response, suggestion_terms, track_query


router = APIRouter(tags=["catalog"])


@router.get("/tracks", response_model=list[TrackOut])
def list_tracks(db: Session = Depends(get_db)):
    return list(db.scalars(track_query()).unique())


@router.get("/tracks/{track_id}", response_model=TrackOut)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.scalars(track_query().where(Track.id == track_id)).unique().first()
    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.get("/tracks/{track_id}/stream")
def stream_track(track_id: int, db: Session = Depends(get_db)):
    track = db.scalar(select(Track).where(Track.id == track_id))
    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return stream_track_response(track)


@router.get("/artists", response_model=list[ArtistOut])
def list_artists(db: Session = Depends(get_db)):
    return list(db.scalars(select(Artist).order_by(Artist.name)))


@router.get("/albums", response_model=list[AlbumOut])
def list_albums(db: Session = Depends(get_db)):
    return list(db.scalars(select(Album).options(joinedload(Album.artist)).order_by(Album.title)).unique())


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(min_length=1),
    artist: str | None = None,
    album: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    tracks, artists, albums = search_catalog(db, q, artist=artist, album=album, genre=genre)
    return SearchResponse(
        tracks=[TrackOut.model_validate(track) for track in tracks],
        artists=[ArtistOut.model_validate(item) for item in artists],
        albums=[AlbumOut.model_validate(item) for item in albums],
    )


@router.get("/search/suggestions", response_model=SuggestionResponse)
def suggestions(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return SuggestionResponse(suggestions=suggestion_terms(db, q))
