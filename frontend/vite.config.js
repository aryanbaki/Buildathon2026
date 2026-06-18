import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  assetsInclude: ["**/*.glb", "**/*.gltf"],
  plugins: [react()],
  server: { port: 3000 },
});
