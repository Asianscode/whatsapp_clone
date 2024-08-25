import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,  // Set the port to 8000
    proxy: {
      // Proxy API requests to the backend server
      '/api': 'http://localhost:8000',
    },
  },
})
