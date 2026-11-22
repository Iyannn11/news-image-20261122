import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

// The entry image is produced by render.py and shipped in the repo.
// Copy it to the grader's output directory.
const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "entry.png"), join(outDir, "entry.png"));
console.log("wrote /output/entry.png");
