import React from 'react';

const Home: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Welcome to Spotify Clone</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {/* Placeholder for content */}
        <div className="bg-spotify-light-gray p-4 rounded-lg">
          <div className="w-full h-40 bg-spotify-gray rounded mb-4"></div>
          <h3 className="text-white font-semibold mb-2">Liked Songs</h3>
          <p className="text-spotify-text text-sm">Your favorite tracks</p>
        </div>
        <div className="bg-spotify-light-gray p-4 rounded-lg">
          <div className="w-full h-40 bg-spotify-gray rounded mb-4"></div>
          <h3 className="text-white font-semibold mb-2">Discover Weekly</h3>
          <p className="text-spotify-text text-sm">Your weekly mix</p>
        </div>
        <div className="bg-spotify-light-gray p-4 rounded-lg">
          <div className="w-full h-40 bg-spotify-gray rounded mb-4"></div>
          <h3 className="text-white font-semibold mb-2">Daily Mix 1</h3>
          <p className="text-spotify-text text-sm">Made for you</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
