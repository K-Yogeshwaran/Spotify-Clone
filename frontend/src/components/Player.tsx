import React, { useState, useRef, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Volume2, 
  Repeat, 
  Shuffle,
  Heart,
  Maximize2,
  ChevronDown
} from 'lucide-react';
import { PlaybackState } from '../types';

const Player: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(0.8);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isShuffleOn, setIsShuffleOn] = useState(false);
  const [repeatMode, setRepeatMode] = useState<'off' | 'track' | 'context'>('off');
  const [isLiked, setIsLiked] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  // Mock current track data
  const currentTrack = {
    title: "Example Track",
    artist: "Example Artist",
    album: "Example Album",
    duration: 180, // 3 minutes in seconds
    coverImage: "https://via.placeholder.com/56/56"
  };

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setProgress(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = Number(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setProgress(newTime);
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-spotify-gray border-t border-spotify-light-gray px-4 py-3">
      <audio
        ref={audioRef}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
      />
      
      <div className="flex items-center justify-between">
        {/* Track Info */}
        <div className="flex items-center space-x-4 flex-1 min-w-0">
          <img
            src={currentTrack.coverImage}
            alt={currentTrack.title}
            className="w-14 h-14 rounded"
          />
          <div className="min-w-0">
            <h4 className="text-white text-sm font-medium truncate hover:underline cursor-pointer">
              {currentTrack.title}
            </h4>
            <p className="text-spotify-text text-xs truncate hover:underline cursor-pointer">
              {currentTrack.artist}
            </p>
          </div>
          <button
            onClick={() => setIsLiked(!isLiked)}
            className={`ml-4 ${isLiked ? 'text-spotify-green' : 'text-spotify-text'} hover:text-white transition-colors`}
          >
            <Heart size={16} fill={isLiked ? 'currentColor' : 'none'} />
          </button>
        </div>

        {/* Player Controls */}
        <div className="flex flex-col items-center max-w-[722px] flex-1">
          <div className="flex items-center space-x-6 mb-2">
            <button
              onClick={() => setIsShuffleOn(!isShuffleOn)}
              className={`text-spotify-text hover:text-white transition-colors ${
                isShuffleOn ? 'text-spotify-green' : ''
              }`}
            >
              <Shuffle size={18} />
            </button>
            <button className="text-spotify-text hover:text-white transition-colors">
              <SkipBack size={20} />
            </button>
            <button
              onClick={handlePlayPause}
              className="bg-white text-black rounded-full p-2 hover:scale-105 transition-transform"
            >
              {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            </button>
            <button className="text-spotify-text hover:text-white transition-colors">
              <SkipForward size={20} />
            </button>
            <button
              onClick={() => {
                const modes: ('off' | 'track' | 'context')[] = ['off', 'track', 'context'];
                const currentIndex = modes.indexOf(repeatMode);
                setRepeatMode(modes[(currentIndex + 1) % modes.length]);
              }}
              className={`text-spotify-text hover:text-white transition-colors ${
                repeatMode !== 'off' ? 'text-spotify-green' : ''
              }`}
            >
              <Repeat size={18} />
            </button>
          </div>
          
          {/* Progress Bar */}
          <div className="flex items-center space-x-2 w-full">
            <span className="text-xs text-spotify-text w-10 text-right">
              {formatTime(progress)}
            </span>
            <input
              type="range"
              min="0"
              max={duration || 0}
              value={progress}
              onChange={handleSeek}
              className="flex-1 h-1 bg-spotify-light-gray rounded-lg appearance-none cursor-pointer slider"
            />
            <span className="text-xs text-spotify-text w-10">
              {formatTime(duration)}
            </span>
          </div>
        </div>

        {/* Volume and Controls */}
        <div className="flex items-center space-x-4 flex-1 justify-end">
          <button className="text-spotify-text hover:text-white transition-colors">
            <Maximize2 size={18} />
          </button>
          <div className="flex items-center space-x-2">
            <button className="text-spotify-text hover:text-white transition-colors">
              <Volume2 size={18} />
            </button>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={volume}
              onChange={(e) => setVolume(Number(e.target.value))}
              className="w-24 h-1 bg-spotify-light-gray rounded-lg appearance-none cursor-pointer"
            />
          </div>
          <button className="text-spotify-text hover:text-white transition-colors">
            <ChevronDown size={18} />
          </button>
        </div>
      </div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 12px;
          height: 12px;
          background: white;
          border-radius: 50%;
          cursor: pointer;
        }
        .slider::-moz-range-thumb {
          width: 12px;
          height: 12px;
          background: white;
          border-radius: 50%;
          cursor: pointer;
          border: none;
        }
      `}</style>
    </div>
  );
};

export default Player;
