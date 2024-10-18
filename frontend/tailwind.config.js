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
      }
    },
    container: {
      center: true,

    },
  },
  plugins: [],
}

