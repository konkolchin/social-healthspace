import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

export default defineConfig({
  plugins: [react()],
  base: '/social-healthspace/' // Add this line - should match your repository name
})