// Round 1 entry for news-image-20261122: copy the pre-rendered front page
// (entry.png, drawn by render.py in this same repository) to the output
// directory. Node 22 standard library only; no network. The image is
// located via MAKEFUN_BOT_DIR (the bot directory the grader uses), never
// from the working directory; as a fallback it is looked up next to this
// file itself.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const MAX_BYTES = 1048576; // 1 MiB, the competition's size cap

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
let src = join(botDir, "entry.png");
if (!existsSync(src)) {
  src = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error(`entry.png not found in ${botDir} or next to main.ts`);
  process.exit(1);
}
const size = statSync(src).size;
if (size > MAX_BYTES) {
  console.error(`entry.png is ${size} bytes, over the 1 MiB limit`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`wrote ${dest} (${size} bytes)`);
