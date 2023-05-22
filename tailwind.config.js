module.exports = {
  mode: 'jit',
  content: ['./PACEr/templates/**/*.html', './PACEr/static/**/*.js'],
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [
    require('flowbite/plugin')
  ],
}
