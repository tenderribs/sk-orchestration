/** @type {import('tailwindcss').Config} */

export default {
  content: ['./src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'primary': 'rgb(15, 5, 160)',
        'secondary': 'rgb(115, 115, 115)',
      },
      fontFamily: {
        sans: ['HelveticaNeue', 'sans-serif']
      },
      screens: {
        'hd': '1920px',
      }
    },
    container: {
      center: true,
      padding: '2rem'
    },
  },
  plugins: [],
}

