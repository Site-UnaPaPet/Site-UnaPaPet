import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// O .env fica na raiz do projeto (duas pastas acima de src/frontend)
export default defineConfig({
  plugins: [react()],
  envDir: "../..",
});
