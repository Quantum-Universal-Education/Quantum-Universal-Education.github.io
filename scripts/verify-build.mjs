import {existsSync,readdirSync,readFileSync} from "node:fs";
import {join} from "node:path";

const requiredPages = [
  "index.html","research.html","publications.html","talks.html",
  "updates.html","about.html","media.html","qregime.html",
  "playground.html","qaly.html","timeline.html","quantum-pipeline.html"
];
const requiredData = [
  "products.json","talks.json","publications.json","news.json",
  "posts.json","photos.json","media.json","metrics.json"
];
const failures = [];
for (const file of requiredPages) {
  if (!existsSync(join("dist",file))) failures.push("Missing page: "+file);
}
for (const file of requiredData) {
  const path=join("dist","data",file);
  if (!existsSync(path)) failures.push("Missing data file: "+path);
  else {
    try { JSON.parse(readFileSync(path,"utf8")); }
    catch (error) { failures.push("Invalid JSON: "+path+" ("+error.message+")"); }
  }
}
const assetFiles = readdirSync(join("dist","assets"));
if (!assetFiles.some(file => file.endsWith(".css"))) failures.push("No compiled CSS file found in dist/assets.");
if (!assetFiles.some(file => file.endsWith(".js"))) failures.push("No compiled JavaScript file found in dist/assets.");
// React entry pages must contain Vite's production bundles, never raw TSX source paths.
const reactEntryPages = ["index.html","research.html","publications.html","talks.html","updates.html","about.html","media.html"];
for (const page of reactEntryPages) {
  const path=join("dist",page);
  if (!existsSync(path)) continue;
  const html=readFileSync(path,"utf8");
  if (html.includes("/src/main.tsx")) failures.push("Unbuilt React entrypoint found in "+page+"; deploy the Vite dist output, not repository source.");
  if (!/src=["'][^"']*assets\/[^"']+\.js["']/.test(html)) failures.push("No compiled JavaScript entry bundle found in "+page);
}
for (const page of requiredPages.slice(0,7)) {
  const html=readFileSync(join("dist",page),"utf8");
  if (!html.includes("assets/") && !html.includes("/assets/")) failures.push("No built asset references in "+page);
}
if (failures.length) {
  console.error("Build verification failed:\n- "+failures.join("\n- "));
  process.exit(1);
}
console.log("Build verification passed: "+requiredPages.length+" pages and "+requiredData.length+" JSON data files are present and valid.");
