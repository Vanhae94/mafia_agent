/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        noir: {
          900: '#09090b', // Main Background
          800: '#18181b', // Panel Background
          700: '#27272a', // Border
        },
        neon: {
          cyan: '#06b6d4', // Safe/System
          pink: '#f43f5e', // Danger/Suspect
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glow-cyan': '0 0 10px rgba(6, 182, 212, 0.5)',
        'glow-pink': '0 0 10px rgba(244, 63, 94, 0.5)',
      }
    },
  },
  plugins: [],
}