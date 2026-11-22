import { copyFileSync, statSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? process.cwd();
const src = join(botDir, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
const bytes = statSync(dst).size;
const srcBytes = statSync(src).size;
if (bytes !== srcBytes) {
  throw new Error(`copy mismatch: ${bytes} != ${srcBytes}`);
}
console.log(`copied entry.png to ${dst} (${bytes} bytes, verified)`);
