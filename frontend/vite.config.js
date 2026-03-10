import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import legacy from '@vitejs/plugin-legacy'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        legacy({
            targets: ['defaults', 'not IE 11'],
            additionalLegacyPolyfills: ['regenerator-runtime/runtime']
        })
    ],
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
        target: 'es2015',
        outDir: 'dist',
        assetsDir: 'assets',
        emptyOutDir: true,
        sourcemap: false,
        minify: false,
        manifest: true,
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
