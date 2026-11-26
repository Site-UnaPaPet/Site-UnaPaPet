import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// O .env fica na raiz do projeto (duas pastas acima de src/frontend)
export default defineConfig({
  plugins: [react(), tailwindcss()],
  envDir: "../..",
  resolve: {
    // "@/components/..." aponta para src/frontend/components/... (o shadcn usa esse atalho)
    alias: { "@": path.resolve(import.meta.dirname) },
  },
});
