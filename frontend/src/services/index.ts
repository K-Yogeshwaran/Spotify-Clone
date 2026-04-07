import { api } from './api';
import { 
  AuthTokens, 
  User, 
  UserCreate, 
  UserLogin, 
  UserProfileUpdate,
  Track,
  Artist,
  Album,
  Playlist,
  PlaybackState,
  LibrarySnapshot,
  SearchResponse,
  SuggestionResponse
} from '../types';

// Auth APIs
export const authApi = {
  signup: (userData: UserCreate) => 
    api.post<AuthTokens>('/auth/signup', userData),
  
  login: (credentials: UserLogin) => 
    api.post<AuthTokens>('/auth/login', credentials),
  
  getCurrentUser: () => 
    api.get<User>('/auth/me'),
  
  updateProfile: (userData: UserProfileUpdate) => 
    api.patch<User>('/auth/me', userData),
};

// Catalog APIs
export const catalogApi = {
  getTracks: () => 
    api.get<Track[]>('/tracks'),
  
  getTrack: (id: number) => 
    api.get<Track>(`/tracks/${id}`),
  
  streamTrack: (id: number) => 
    api.get(`/tracks/${id}/stream`, { responseType: 'blob' }),
  
  getArtists: () => 
    api.get<Artist[]>('/artists'),
  
  getAlbums: () => 
    api.get<Album[]>('/albums'),
  
  search: (query: string, filters?: { artist?: string; album?: string; genre?: string }) => 
    api.get<SearchResponse>('/search', { params: { q: query, ...filters } }),
  
  getSuggestions: (query: string) => 
    api.get<SuggestionResponse>('/search/suggestions', { params: { q: query } }),
};

// Playback APIs
export const playbackApi = {
  getState: () => 
    api.get<PlaybackState>('/playback'),
  
  play: (data?: { track_id?: number; queue_track_ids?: number[] }) => 
    api.post<PlaybackState>('/playback/play', data),
  
  pause: () => 
    api.post<PlaybackState>('/playback/pause'),
  
  next: () => 
    api.post<PlaybackState>('/playback/next'),
  
  previous: () => 
    api.post<PlaybackState>('/playback/previous'),
  
  seek: (positionSeconds: number) => 
    api.post<PlaybackState>('/playback/seek', { position_seconds: positionSeconds }),
  
  toggleShuffle: () => 
    api.post<PlaybackState>('/playback/shuffle'),
  
  setRepeat: (repeatMode: 'off' | 'track' | 'context') => 
    api.post<PlaybackState>('/playback/repeat', { repeat_mode: repeatMode }),
  
  setVolume: (volume: number) => 
    api.post<PlaybackState>('/playback/volume', { volume }),
};

// Playlist APIs
export const playlistApi = {
  getPlaylists: () => 
    api.get<Playlist[]>('/playlists'),
  
  createPlaylist: (data: { title: string; description?: string; is_public?: boolean }) => 
    api.post<Playlist>('/playlists', data),
  
  getPlaylist: (id: number) => 
    api.get<Playlist>(`/playlists/${id}`),
  
  updatePlaylist: (id: number, data: { title?: string; description?: string; is_public?: boolean }) => 
    api.patch<Playlist>(`/playlists/${id}`, data),
  
  deletePlaylist: (id: number) => 
    api.delete(`/playlists/${id}`),
  
  addTrack: (playlistId: number, trackId: number) => 
    api.post<Playlist>(`/playlists/${playlistId}/tracks`, { track_id: trackId }),
  
  removeTrack: (playlistId: number, playlistTrackId: number) => 
    api.delete<Playlist>(`/playlists/${playlistId}/tracks/${playlistTrackId}`),
};

// Library APIs
export const libraryApi = {
  getLibrary: () => 
    api.get<LibrarySnapshot>('/library'),
  
  likeTrack: (trackId: number) => 
    api.post(`/library/tracks/${trackId}/like`),
  
  unlikeTrack: (trackId: number) => 
    api.delete(`/library/tracks/${trackId}/like`),
  
  saveAlbum: (albumId: number) => 
    api.post(`/library/albums/${albumId}/save`),
  
  unsaveAlbum: (albumId: number) => 
    api.delete(`/library/albums/${albumId}/save`),
  
  saveArtist: (artistId: number) => 
    api.post(`/library/artists/${artistId}/save`),
  
  unsaveArtist: (artistId: number) => 
    api.delete(`/library/artists/${artistId}/save`),
};

// User APIs
export const userApi = {
  getUser: (id: number) => 
    api.get<User>(`/users/${id}`),
  
  followUser: (id: number) => 
    api.post(`/users/${id}/follow`),
  
  unfollowUser: (id: number) => 
    api.delete(`/users/${id}/follow`),
};
