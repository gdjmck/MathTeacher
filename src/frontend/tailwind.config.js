/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0f172a',
        mist: '#e2e8f0',
        skyline: '#3b82f6',
        plum: '#7c3aed',
        ember: '#fb7185',
        panel: '#111827',
      },
      boxShadow: {
        glow: '0 20px 45px rgba(59, 130, 246, 0.18)',
      },
      fontFamily: {
        display: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [],
}
