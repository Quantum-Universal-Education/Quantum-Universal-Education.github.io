import {defineConfig} from "vite";
import react from "@vitejs/plugin-react";
import {cpSync} from "node:fs";
export default defineConfig({
  plugins:[react(),{
    name:"copy-static-site-files",
    closeBundle(){
      cpSync("data","dist/data",{recursive:true});
      cpSync("assets","dist/assets",{recursive:true});
      cpSync("qregime.html","dist/qregime.html");
      cpSync("playground.html","dist/playground.html");
    }
  }],
  base:"/",
  build:{outDir:"dist",emptyOutDir:true}
});