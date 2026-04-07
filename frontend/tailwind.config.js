/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'spotify-black': '#191414',
        'spotify-green': '#1DB954',
        'spotify-gray': '#1E1E1E',
        'spotify-light-gray': '#282828',
        'spotify-lighter-gray': '#3E3E3E',
        'spotify-white': '#FFFFFF',
        'spotify-text': '#B3B3B3',
      },
      fontFamily: {
        'circular': ['Circular', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
