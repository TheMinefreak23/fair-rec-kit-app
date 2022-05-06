import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      options: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('b-'),
        },
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  test: {
    // enable jest-like global test APIs
    globals: true,
    // simulate DOM with happy-dom
    // (requires installing happy-dom as a peer dependency)
    environment: 'happy-dom',
  },

  /*  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000/api',
        ws: true,
        changeOrigin: true,
      },
    },
  },*/
})
