from __future__ import annotations

import json
import random
from pathlib import Path

from fastapi import HTTPException, status
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.models import (
    Album,
    Artist,
    Follow,
    PlaybackState,
    Playlist,
    PlaylistTrack,
    RecentlyPlayed,
    Track,
    User,
)
from app.schemas import PlaybackStateOut, PublicUser, TrackOut, UserProfile


def ensure_playback_state(db: Session, user: User) -> PlaybackState:
    state = db.scalar(select(PlaybackState).where(PlaybackState.user_id == user.id))
    if state is None:
        state = PlaybackState(user_id=user.id, queue_track_ids="[]")
        db.add(state)
        db.commit()
        db.refresh(state)
    return state


def track_query() -> Select[tuple[Track]]:
    return select(Track).options(
        joinedload(Track.artist), joinedload(Track.album).joinedload(Album.artist)
    )


def get_track_or_404(db: Session, track_id: int) -> Track:
    track = db.scalar(track_query().where(Track.id == track_id))
    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


def get_playlist_or_404(db: Session, playlist_id: int) -> Playlist:
    playlist = db.scalar(
        select(Playlist)
        .options(
            joinedload(Playlist.owner),
            joinedload(Playlist.tracks)
            .joinedload(PlaylistTrack.track)
            .joinedload(Track.artist),
            joinedload(Playlist.tracks)
            .joinedload(PlaylistTrack.track)
            .joinedload(Track.album)
            .joinedload(Album.artist),
        )
        .where(Playlist.id == playlist_id)
    )
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


def serialize_playback_state(db: Session, state: PlaybackState) -> PlaybackStateOut:
    queue_track_ids = json.loads(state.queue_track_ids or "[]")
    current_track = None
    if state.current_track_id is not None:
        current_track = get_track_or_404(db, state.current_track_id)
    return PlaybackStateOut(
        current_track=TrackOut.model_validate(current_track) if current_track else None,
        is_playing=state.is_playing,
        position_seconds=state.position_seconds,
        volume=state.volume,
        shuffle_enabled=state.shuffle_enabled,
        repeat_mode=state.repeat_mode,
        queue_track_ids=queue_track_ids,
    )


def add_recently_played(db: Session, user_id: int, track_id: int) -> None:
    db.add(RecentlyPlayed(user_id=user_id, track_id=track_id))
    db.commit()


def ensure_queue(
    state: PlaybackState, fallback_track_id: int | None = None
) -> list[int]:
    queue = json.loads(state.queue_track_ids or "[]")
    if not queue and fallback_track_id is not None:
        queue = [fallback_track_id]
    return queue


def update_queue(state: PlaybackState, queue_track_ids: list[int]) -> None:
    state.queue_track_ids = json.dumps(queue_track_ids)


def advance_queue(db: Session, state: PlaybackState, step: int) -> PlaybackState:
    queue = ensure_queue(state, state.current_track_id)
    if not queue:
        raise HTTPException(status_code=400, detail="Playback queue is empty")

    if state.repeat_mode == "one" and state.current_track_id is not None:
        state.position_seconds = 0
        state.is_playing = True
        db.commit()
        return state

    if state.shuffle_enabled and len(queue) > 1:
        candidates = [
            track_id for track_id in queue if track_id != state.current_track_id
        ]
        # Use candidates if available, otherwise use queue (single track case)
        if candidates:
            next_track_id = random.choice(candidates)
        else:
            # Queue has only one track, which is the current track
            next_track_id = queue[0]
    else:
        current_index = (
            queue.index(state.current_track_id)
            if state.current_track_id in queue
            else 0
        )
        target_index = current_index + step
        if target_index >= len(queue):
            if state.repeat_mode == "all":
                target_index = 0
            else:
                state.is_playing = False
                db.commit()
                return state
        elif target_index < 0:
            if state.repeat_mode == "all":
                target_index = len(queue) - 1
            else:
                state.is_playing = False
                db.commit()
                return state
        next_track_id = queue[target_index]

    state.current_track_id = next_track_id
    state.position_seconds = 0
    state.is_playing = True
    db.commit()
    return state


def user_profile(db: Session, user: User) -> UserProfile:
    follower_count = (
        db.scalar(
            select(func.count())
            .select_from(Follow)
            .where(Follow.following_id == user.id)
        )
        or 0
    )
    following_count = (
        db.scalar(
            select(func.count())
            .select_from(Follow)
            .where(Follow.follower_id == user.id)
        )
        or 0
    )
    base = PublicUser.model_validate(user).model_dump()
    return UserProfile(
        **base, follower_count=follower_count, following_count=following_count
    )


def search_catalog(
    db: Session,
    query: str,
    artist: str | None = None,
    album: str | None = None,
    genre: str | None = None,
) -> tuple[list[Track], list[Artist], list[Album]]:
    normalized = f"%{query.strip()}%"
    track_stmt = (
        track_query()
        .join(Track.artist)
        .join(Track.album)
        .where(
            or_(
                Track.title.ilike(normalized),
                Artist.name.ilike(normalized),
                Album.title.ilike(normalized),
            )
        )
    )
    artist_stmt = select(Artist).where(Artist.name.ilike(normalized))
    album_stmt = (
        select(Album)
        .options(joinedload(Album.artist))
        .where(Album.title.ilike(normalized))
    )

    if artist:
        track_stmt = track_stmt.where(Artist.name.ilike(f"%{artist}%"))
    if album:
        track_stmt = track_stmt.where(Album.title.ilike(f"%{album}%"))
    if genre:
        track_stmt = track_stmt.where(
            or_(
                Track.genre.ilike(f"%{genre}%"),
                Album.genre.ilike(f"%{genre}%"),
                Artist.genre.ilike(f"%{genre}%"),
            )
        )
        artist_stmt = artist_stmt.where(Artist.genre.ilike(f"%{genre}%"))
        album_stmt = album_stmt.where(Album.genre.ilike(f"%{genre}%"))

    return (
        list(db.scalars(track_stmt.limit(20)).unique()),
        list(db.scalars(artist_stmt.limit(10))),
        list(db.scalars(album_stmt.limit(10)).unique()),
    )


def suggestion_terms(db: Session, query: str) -> list[str]:
    normalized = f"{query.strip()}%"
    tracks = db.scalars(
        select(Track.title).where(Track.title.ilike(normalized)).limit(5)
    ).all()
    artists = db.scalars(
        select(Artist.name).where(Artist.name.ilike(normalized)).limit(5)
    ).all()
    albums = db.scalars(
        select(Album.title).where(Album.title.ilike(normalized)).limit(5)
    ).all()
    seen: list[str] = []
    for term in [*tracks, *artists, *albums]:
        if term not in seen:
            seen.append(term)
    return seen[:10]


def stream_track_response(track: Track):
    if track.audio_url:
        return RedirectResponse(track.audio_url)
    if track.audio_path:
        file_path = Path(track.audio_path)
        if not file_path.is_file():
            raise HTTPException(
                status_code=404, detail="Audio file not found on server"
            )
        return FileResponse(
            path=file_path, media_type="audio/mpeg", filename=file_path.name
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Track does not have a configured audio source",
    )
