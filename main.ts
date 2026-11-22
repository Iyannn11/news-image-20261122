import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR;
if (!botDir) {
  throw new Error("MAKEFUN_BOT_DIR is not set");
}
const src = join(botDir, "entry.png");
const outDir = "/output";
if (!existsSync(src)) {
  throw new Error("entry.png not found in " + botDir);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
// Verify the copy landed byte-identical before reporting success.
const srcSize = statSync(src).size;
const dstSize = statSync(join(outDir, "entry.png")).size;
if (srcSize !== dstSize) {
  throw new Error("copy size mismatch: " + srcSize + " vs " + dstSize);
}
console.log("copied entry.png to /output/entry.png (" + dstSize + " bytes, verified)");
