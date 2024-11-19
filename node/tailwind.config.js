/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        transparent: 'transparent',
        primary: '#1d4ed8',
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
  darkMode: 'class',
}

