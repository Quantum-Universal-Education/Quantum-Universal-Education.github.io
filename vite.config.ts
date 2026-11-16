import {defineConfig} from "vite";
import react from "@vitejs/plugin-react";
import {cpSync} from "node:fs";
import {resolve} from "node:path";
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
  build:{
    outDir:"dist",
    emptyOutDir:true,
    rollupOptions:{
      input:{
        home:resolve(__dirname,"index.html"),
        research:resolve(__dirname,"research.html"),
        publications:resolve(__dirname,"publications.html"),
        talks:resolve(__dirname,"talks.html"),
        updates:resolve(__dirname,"updates.html"),
        about:resolve(__dirname,"about.html")
      }
    }
  }
});