import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Search, 
  Library, 
  Plus, 
  Heart, 
  Rss,
  ChevronLeft,
  ChevronRight,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  Maximize2,
  Mic2,
  ListMusic,
  MonitorSpeaker,
  ChevronDown
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const location = useLocation();

  const navigationItems = [
    { icon: Home, label: 'Home', path: '/' },
    { icon: Search, label: 'Search', path: '/search' },
    { icon: Library, label: 'Your Library', path: '/library' },
  ];

  const libraryItems = [
    { icon: Plus, label: 'Create Playlist', action: 'create-playlist' },
    { icon: Heart, label: 'Liked Songs', path: '/collection/tracks' },
    { icon: Rss, label: 'Your Episodes', path: '/collection/episodes' },
  ];

  const isActivePath = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  return (
    <div className={`bg-spotify-black p-6 flex flex-col transition-all duration-300 ${
      isCollapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Navigation */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="text-spotify-text hover:text-white transition-colors"
            >
              {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
            </button>
            {!isCollapsed && (
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-spotify-green rounded-full flex items-center justify-center">
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 text-black">
                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.349c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                  </svg>
                </div>
                <span className="text-white font-bold text-xl">Spotify</span>
              </div>
            )}
          </div>
        </div>

        {!isCollapsed && (
          <nav className="space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-4 p-3 rounded-lg transition-colors ${
                    isActivePath(item.path)
                      ? 'bg-spotify-white text-black'
                      : 'text-spotify-text hover:text-white'
                  }`}
                >
                  <Icon size={24} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        )}
      </div>

      {/* Library Section */}
      {!isCollapsed && (
        <div className="flex-1 overflow-hidden flex flex-col">
          <div className="mb-4">
            <div className="flex items-center justify-between mb-4">
              <span className="text-spotify-text font-semibold text-sm uppercase tracking-wider">
                Library
              </span>
              <button className="text-spotify-text hover:text-white">
                <Plus size={20} />
              </button>
            </div>
            <div className="space-y-2">
              {libraryItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.label}
                    to={item.path || '#'}
                    className="flex items-center space-x-4 p-3 rounded-lg text-spotify-text hover:text-white transition-colors"
                  >
                    <Icon size={20} />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Playlists */}
          <div className="flex-1 overflow-y-auto">
            <div className="space-y-1">
              <div className="p-3 rounded-lg text-spotify-text hover:text-white transition-colors cursor-pointer">
                <span className="font-medium">Chill Hits</span>
              </div>
              <div className="p-3 rounded-lg text-spotify-text hover:text-white transition-colors cursor-pointer">
                <span className="font-medium">Deep Focus</span>
              </div>
              <div className="p-3 rounded-lg text-spotify-text hover:text-white transition-colors cursor-pointer">
                <span className="font-medium">Discover Weekly</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Player Controls (when collapsed) */}
      {isCollapsed && (
        <div className="border-t border-spotify-light-gray pt-4 space-y-4">
          <button className="text-spotify-text hover:text-white">
            <Home size={20} />
          </button>
          <button className="text-spotify-text hover:text-white">
            <Search size={20} />
          </button>
          <button className="text-spotify-text hover:text-white">
            <Library size={20} />
          </button>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
