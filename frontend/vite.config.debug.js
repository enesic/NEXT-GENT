import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    build: {
        minify: false,
        sourcemap: true,
        rollupOptions: {
            onwarn(warning, warn) {
                console.log('ROLLUP WARNING:', warning.message)
                warn(warning)
            }
        }
    }
})
