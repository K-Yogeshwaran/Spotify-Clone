export interface User {
  id: number;
  email: string;
  name: string;
  avatar_url?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

export interface Track {
  id: number;
  title: string;
  duration_seconds: number;
  artist_id: number;
  album_id: number;
  genre?: string;
  audio_url?: string;
  audio_path?: string;
  artist: Artist;
  album: Album;
  created_at: string;
  updated_at: string;
}

export interface Artist {
  id: number;
  name: string;
  bio?: string;
  image_url?: string;
  genre?: string;
  created_at: string;
  updated_at: string;
}

export interface Album {
  id: number;
  title: string;
  cover_image?: string;
  artist_id: number;
  genre?: string;
  release_year?: number;
  artist: Artist;
  created_at: string;
  updated_at: string;
}

export interface Playlist {
  id: number;
  owner_id: number;
  title: string;
  description?: string;
  is_public: boolean;
  cover_image?: string;
  owner: User;
  tracks: PlaylistTrack[];
  created_at: string;
  updated_at: string;
}

export interface PlaylistTrack {
  id: number;
  playlist_id: number;
  track_id: number;
  position: number;
  added_at: string;
  track: Track;
}

export interface PlaybackState {
  id: number;
  user_id: number;
  current_track_id?: number;
  is_playing: boolean;
  position_seconds: number;
  volume: number;
  shuffle_enabled: boolean;
  repeat_mode: 'off' | 'track' | 'context';
  queue_track_ids?: string;
  user: User;
  current_track?: Track;
  created_at: string;
  updated_at: string;
}

export interface LibrarySnapshot {
  liked_tracks: Track[];
  saved_albums: Album[];
  saved_artists: Artist[];
  recently_played: Track[];
}

export interface SearchResponse {
  tracks: Track[];
  artists: Artist[];
  albums: Album[];
}

export interface SuggestionResponse {
  suggestions: string[];
}

export interface AuthTokens {
  access_token: string;
}

export interface UserCreate {
  email: string;
  password: string;
  name: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserProfileUpdate {
  name?: string;
  avatar_url?: string;
  bio?: string;
}
