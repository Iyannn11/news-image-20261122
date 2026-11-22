// main.ts — hand in the front page: copy entry.png to /output.
//
// Runs on Node 22 with the standard library only. The entry image lives
// next to this file, so it is resolved from this file's own location (never
// from the working directory, which the grader does not guarantee) or from
// MAKEFUN_BOT_DIR when that is set. The output directory is /output, or
// $MAKEFUN_OUTPUT_DIR when that is set (local runs).
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const botDir =
  process.env.MAKEFUN_BOT_DIR ?? dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const src = join(botDir, "entry.png");
const dst = join(outDir, "entry.png");
const hash = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex");
const srcHash = hash(src);
copyFileSync(src, dst);
const { size } = statSync(dst);
if (size === 0) throw new Error("entry.png copied empty");
if (hash(dst) !== srcHash) throw new Error("entry.png copy mismatch");
console.log(`copied entry.png (${size} bytes, sha256 ${srcHash}) to ${dst}`);
