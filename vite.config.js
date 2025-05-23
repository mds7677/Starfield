import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    allowedHosts:['vievzq-46-216-23-61.ru.tuna.am'],
    watch: {
      usePolling: true
    },
    proxy: {
      '/api': {
        target:'http://backend:5000', // <-- замени на адрес и порт твоего backend сервера
        changeOrigin: true,
        secure:false,
      }
    }
  },
  base: '/',
  publicDir: 'public',
})
