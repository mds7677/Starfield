import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    allowedHosts:['lqnuwe-46-216-23-61.ru.tuna.am'],
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true // необходимо для Docker volume
    }
  },
  base: '/',
  publicDir: 'public',
})
