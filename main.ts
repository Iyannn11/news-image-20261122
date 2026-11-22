// main.ts — entrypoint for the News 22 broadsheet entry.
// Copies entry.png (rendered by render.py) into the output directory.
// Written as plain JavaScript inside .ts so any Node runner handles it.
// Uses MAKEFUN_BOT_DIR for the source and MAKEFUN_OUTPUT_DIR (or /output)
// for the destination. Never uses process.cwd().
const fs = require("fs");
const path = require("path");

const botDir = process.env.MAKEFUN_BOT_DIR || __dirname;
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const src = path.join(botDir, "entry.png");
const dst = path.join(outDir, "entry.png");

fs.mkdirSync(outDir, { recursive: true });
fs.copyFileSync(src, dst);

const a = fs.readFileSync(src);
const b = fs.readFileSync(dst);
if (!a.equals(b)) {
  console.error("output does not match entry.png");
  process.exit(1);
}
console.log("entry.png -> " + dst + " (" + a.length + " bytes)");
