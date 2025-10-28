import esbuild from 'esbuild';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PYTHON_WIDGETS_DIR = path.join(
  __dirname,
  '..',
  'src',
  'pdum',
  'coiled',
  'widgets'
);
const STYLES_PATH = path.join(__dirname, 'src', 'styles.css');

function ensurePythonDir() {
  if (!fs.existsSync(PYTHON_WIDGETS_DIR)) {
    fs.mkdirSync(PYTHON_WIDGETS_DIR, { recursive: true });
  }
}

const DIST_DIR = path.join(__dirname, 'dist');

async function build() {
  ensurePythonDir();

  if (!fs.existsSync(DIST_DIR)) {
    fs.mkdirSync(DIST_DIR, { recursive: true });
  }

  await esbuild.build({
    entryPoints: ['src/index-iife.ts'],
    outfile: path.join(DIST_DIR, 'index.js'),
    bundle: true,
    minify: true,
    sourcemap: true,
    target: ['es2020'],
    format: 'iife',
    globalName: 'CoiledWidgets',
    define: {
      __WIDGET_STYLES__: JSON.stringify(fs.readFileSync(STYLES_PATH, 'utf8')),
    },
  });

  const dest = path.join(PYTHON_WIDGETS_DIR, 'index.js');
  fs.copyFileSync(path.join(DIST_DIR, 'index.js'), dest);
  console.log(`Copied widget bundle to ${dest}`);
}

build().catch((error) => {
  console.error(error);
  process.exit(1);
});
