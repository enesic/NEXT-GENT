import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src')
        }
    },
    server: {
        port: 5173,
        open: true,
        proxy: {
            '/api/v1': {
                target: 'http://localhost:8001',
                changeOrigin: true,
                secure: false,
                rewrite: (path) => path
            }
        }
    },
    build: {
        outDir: 'dist',
        assetsDir: 'assets',
        emptyOutDir: true, // Ensure old files are removed on build
        sourcemap: false,
        manifest: true, // Enable build manifest
        rollupOptions: {
            output: {
                // Return to standard hashing for better caching behavior, 
                // relying on Nginx no-cache for index.html to handle updates.
                entryFileNames: `assets/[name]-[hash].js`,
                chunkFileNames: `assets/[name]-[hash].js`,
                assetFileNames: `assets/[name]-[hash].[ext]`
            }
        }
    }
})
