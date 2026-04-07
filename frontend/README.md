# Spotify Clone Frontend

A modern React frontend for the Spotify Clone application, built with TypeScript, Tailwind CSS, and modern tooling.

## Features Implemented

### Core Structure
- **React 18** with TypeScript for type safety
- **Vite** for fast development and building
- **Tailwind CSS** with Spotify-inspired color scheme
- **React Router** for client-side routing
- **React Query** for data fetching and caching
- **Axios** for API communication

### UI Components
- **Sidebar Navigation** - Collapsible sidebar with Spotify-style navigation
- **Music Player** - Full-featured player with controls, progress bar, volume
- **Layout System** - Responsive layout with main content area
- **Authentication Pages** - Login and signup with Spotify-like design

### Pages
- **Home** - Dashboard with playlists and recommendations
- **Browse** - Music catalog browsing
- **Library** - User's saved music
- **Search** - Music search functionality
- **Playlist** - Individual playlist views
- **Artist** - Artist profile pages
- **Album** - Album detail pages
- **Profile** - User profile management

### Authentication
- **Login/Signup** - Full authentication flow
- **Token Management** - JWT token handling
- **Protected Routes** - Route guards for authenticated users
- **User Context** - Global authentication state

### API Integration
- **Comprehensive API Services** - All backend endpoints integrated
- **Error Handling** - Centralized error handling
- **Request Interceptors** - Automatic token injection
- **Type Safety** - Full TypeScript types for API responses

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **React Router** - Routing
- **React Query** - Data fetching
- **Axios** - HTTP client
- **Lucide React** - Icons

### Development Tools
- **ESLint** - Code linting
- **PostCSS** - CSS processing
- **Autoprefixer** - CSS vendor prefixes

## Project Structure

```
frontend/
src/
  components/          # Reusable UI components
    Layout.tsx        # Main layout component
    Sidebar.tsx        # Navigation sidebar
    Player.tsx         # Music player
  pages/               # Page components
    Home.tsx          # Home page
    Login.tsx         # Login page
    Signup.tsx        # Signup page
    Browse.tsx        # Browse page
    Library.tsx       # Library page
    Search.tsx        # Search page
    Playlist.tsx      # Playlist page
    Artist.tsx        # Artist page
    Album.tsx         # Album page
    Profile.tsx       # Profile page
  context/            # React contexts
    AuthContext.tsx   # Authentication context
  services/           # API services
    api.ts           # Axios configuration
    index.ts         # API endpoints
  types/              # TypeScript types
    index.ts         # Type definitions
  utils/              # Utility functions
  hooks/              # Custom React hooks
  App.tsx             # Main app component
  main.tsx            # Entry point
  index.css           # Global styles
```

## Backend Integration

The frontend is designed to work with the FastAPI backend with these key features:

- **Authentication** - JWT-based authentication
- **Music Catalog** - Tracks, artists, albums
- **Playback** - Music player controls
- **Playlists** - User playlists
- **Library** - Saved music and favorites
- **Search** - Music discovery

## Styling

The application uses a Spotify-inspired design system:

- **Color Scheme** - Black, green, and gray tones matching Spotify
- **Typography** - Inter font family
- **Responsive Design** - Mobile, tablet, and desktop layouts
- **Dark Theme** - Consistent dark theme throughout

## Next Steps

To complete the Spotify Clone:

1. **Install Dependencies** - Run `npm install` to install all packages
2. **Start Backend** - Ensure the FastAPI backend is running
3. **Test Application** - Start the development server and test functionality
4. **Implement Features** - Add catalog browsing, search, and playlist management
5. **Polish UI** - Add animations, loading states, and micro-interactions

## Contributing

This is a learning project demonstrating modern React development practices and API integration.
