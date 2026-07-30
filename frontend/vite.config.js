import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3001,
    proxy: {
      '/api': {
        // In Docker, 'backend' is the service name resolved by Docker's internal DNS.
        // For local (non-Docker) development, change this to 'http://localhost:8000'.
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
})