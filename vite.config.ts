import {defineConfig} from "vite";
import react from "@vitejs/plugin-react";
import {cpSync} from "node:fs";
import {resolve} from "node:path";

// Standalone pages are copied after Vite builds the React entry points.
const staticPages = [
  "qregime.html",
  "playground.html",
  "qaly.html",
  "work.html",
  "blog.html",
  "timeline.html",
  "quantum-pipeline.html"
];

export default defineConfig({
  plugins:[react(),{
    name:"copy-static-site-files",
    closeBundle(){
      cpSync("data","dist/data",{recursive:true});
      cpSync("assets","dist/assets",{recursive:true});
      for (const page of staticPages) cpSync(page,resolve("dist",page));
    }
  }],
  // The site is deployed at the root of maldoalberto.github.io.
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
        about:resolve(process.cwd(),"about.html"),
        media:resolve(process.cwd(),"media.html")
      }
    }
  }
});
