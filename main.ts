// News 22 R4 entrypoint: copy the rendered broadsheet to the output dir.
// The image lives next to this file in the repository; resolve it from the
// bot directory (or this file's own directory), never from process.cwd(),
// so the run works no matter which directory the grader starts it in.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const botDir =
  process.env.MAKEFUN_BOT_DIR ?? dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "entry.png"), join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
