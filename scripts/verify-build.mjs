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
for (const page of requiredPages.slice(0,7)) {
  const html=readFileSync(join("dist",page),"utf8");
  if (!html.includes("assets/") && !html.includes("/assets/")) failures.push("No built asset references in "+page);
}
if (failures.length) {
  console.error("Build verification failed:\n- "+failures.join("\n- "));
  process.exit(1);
}
console.log("Build verification passed: "+requiredPages.length+" pages and "+requiredData.length+" JSON data files are present and valid.");
