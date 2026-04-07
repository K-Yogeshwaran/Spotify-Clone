from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1, max_length=120)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    avatar_url: str | None = None
    bio: str | None = Field(default=None, max_length=500)


class PublicUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    avatar_url: str | None = None
    bio: str | None = None
    created_at: datetime


class UserProfile(PublicUser):
    follower_count: int = 0
    following_count: int = 0


class ArtistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: str | None = None
    image_url: str | None = None
    genre: str | None = None


class AlbumOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cover_image: str | None = None
    genre: str | None = None
    release_year: int | None = None
    artist: ArtistOut


class TrackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    duration_seconds: int
    genre: str | None = None
    audio_url: str | None = None
    audio_path: str | None = None
    artist: ArtistOut
    album: AlbumOut


class FollowResponse(BaseModel):
    following_user_id: int
    is_following: bool


class PlaylistCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool = True
    cover_image: str | None = None


class PlaylistUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool | None = None
    cover_image: str | None = None


class PlaylistTrackAdd(BaseModel):
    track_id: int


class PlaylistTrackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    position: int
    added_at: datetime
    track: TrackOut


class PlaylistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    is_public: bool
    cover_image: str | None = None
    created_at: datetime
    updated_at: datetime
    owner: PublicUser
    tracks: list[PlaylistTrackOut] = []


class PlaybackAction(BaseModel):
    track_id: int | None = None
    queue_track_ids: list[int] | None = None


class SeekRequest(BaseModel):
    position_seconds: float = Field(ge=0)


class VolumeRequest(BaseModel):
    volume: float = Field(ge=0, le=1)


class RepeatRequest(BaseModel):
    repeat_mode: Literal["off", "one", "all"]


class PlaybackStateOut(BaseModel):
    current_track: TrackOut | None = None
    is_playing: bool
    position_seconds: float
    volume: float
    shuffle_enabled: bool
    repeat_mode: Literal["off", "one", "all"]
    queue_track_ids: list[int]


class SearchResponse(BaseModel):
    tracks: list[TrackOut]
    artists: list[ArtistOut]
    albums: list[AlbumOut]


class SuggestionResponse(BaseModel):
    suggestions: list[str]


class LibrarySnapshot(BaseModel):
    liked_tracks: list[TrackOut]
    saved_albums: list[AlbumOut]
    saved_artists: list[ArtistOut]
    recently_played: list[TrackOut]
