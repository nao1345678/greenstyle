import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // tout ce qui commence par /api ira vers FastAPI
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // /api/users -> /users
      },
    },
  },
  resolve: {
    alias: {
      '@': '/src', // pratique pour les imports
    },
  },
})
