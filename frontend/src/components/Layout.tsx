import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Player from './Player';

const Layout: React.FC = () => {
  return (
    <div className="h-screen bg-spotify-black flex flex-col">
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-gradient-to-b from-spotify-gray to-spotify-black">
          <div className="p-8">
            <Outlet />
          </div>
        </main>
      </div>
      <Player />
    </div>
  );
};

export default Layout;
