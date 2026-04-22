/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#7DD3FC',
        accent: '#C7D2FE',
        muted: '#64748B'
      }
    },
  },
  plugins: [],
}
