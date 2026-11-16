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
        home:resolve(process.cwd(),"index.html"),
        research:resolve(process.cwd(),"research.html"),
        publications:resolve(process.cwd(),"publications.html"),
        talks:resolve(process.cwd(),"talks.html"),
        updates:resolve(process.cwd(),"updates.html"),
        about:resolve(process.cwd(),"about.html")
      }
    }
  }
});