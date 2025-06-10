import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';

export default defineConfig({ 
  plugins: [svelte(), tailwindcss()],
  resolve: {
    alias: {
      $lib: path.resolve("./src/lib"),
    },
  },
  optimizeDeps: {
    include: ['monaco-editor']
  },
  define: {
    // Monaco Editor requires these globals for web workers
    global: 'globalThis',
  },
  worker: {
    format: 'es'
  }
});
