import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import PlaybackAction, PlaybackStateOut, RepeatRequest, SeekRequest, VolumeRequest
from app.services import (
    add_recently_played,
    advance_queue,
    ensure_playback_state,
    get_track_or_404,
    serialize_playback_state,
    update_queue,
)


router = APIRouter(prefix="/playback", tags=["playback"])


@router.get("", response_model=PlaybackStateOut)
def get_state(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = ensure_playback_state(db, current_user)
    return serialize_playback_state(db, state)


@router.post("/play", response_model=PlaybackStateOut)
def play(
    payload: PlaybackAction,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    state = ensure_playback_state(db, current_user)
    if payload.queue_track_ids is not None:
        valid_track_ids = [get_track_or_404(db, track_id).id for track_id in payload.queue_track_ids]
        update_queue(state, valid_track_ids)
    if payload.track_id is not None:
        track = get_track_or_404(db, payload.track_id)
        state.current_track_id = track.id
        state.position_seconds = 0
        add_recently_played(db, current_user.id, track.id)
        queue = json.loads(state.queue_track_ids or "[]")
        if track.id not in queue:
            queue.insert(0, track.id)
            update_queue(state, queue)
    if state.current_track_id is None:
        raise HTTPException(status_code=400, detail="Provide a track_id or an existing current track")
    state.is_playing = True
    db.add(state)
    db.commit()
    db.refresh(state)
    return serialize_playback_state(db, state)


@router.post("/pause", response_model=PlaybackStateOut)
def pause(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = ensure_playback_state(db, current_user)
    state.is_playing = False
    db.add(state)
    db.commit()
    db.refresh(state)
    return serialize_playback_state(db, state)


@router.post("/seek", response_model=PlaybackStateOut)
def seek(payload: SeekRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = ensure_playback_state(db, current_user)
    state.position_seconds = payload.position_seconds
    db.add(state)
    db.commit()
    db.refresh(state)
    return serialize_playback_state(db, state)


@router.post("/next", response_model=PlaybackStateOut)
def next_track(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = ensure_playback_state(db, current_user)
    advance_queue(db, state, 1)
    if state.current_track_id:
        add_recently_played(db, current_user.id, state.current_track_id)
    return serialize_playback_state(db, state)


@router.post("/previous", response_model=PlaybackStateOut)
def previous_track(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = ensure_playback_state(db, current_user)
    advance_queue(db, state, -1)
    return serialize_playback_state(db, state)


@router.post("/shuffle", response_model=PlaybackStateOut)
def toggle_shuffle(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = ensure_playback_state(db, current_user)
    state.shuffle_enabled = not state.shuffle_enabled
    db.add(state)
    db.commit()
    db.refresh(state)
    return serialize_playback_state(db, state)


@router.post("/repeat", response_model=PlaybackStateOut)
def set_repeat(
    payload: RepeatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    state = ensure_playback_state(db, current_user)
    state.repeat_mode = payload.repeat_mode
    db.add(state)
    db.commit()
    db.refresh(state)
    return serialize_playback_state(db, state)


@router.post("/volume", response_model=PlaybackStateOut)
def set_volume(
    payload: VolumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    state = ensure_playback_state(db, current_user)
    state.volume = payload.volume
    db.add(state)
    db.commit()
    db.refresh(state)
    return serialize_playback_state(db, state)
