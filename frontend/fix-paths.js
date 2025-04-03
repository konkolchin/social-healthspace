import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const indexPath = join(__dirname, 'dist', 'index.html');
let content = readFileSync(indexPath, 'utf8');

// Replace absolute paths with the correct GitHub Pages paths
content = content.replace(/src="\/assets\//g, 'src="/social-healthspace/assets/');
content = content.replace(/href="\/assets\//g, 'href="/social-healthspace/assets/');

writeFileSync(indexPath, content);
console.log('Fixed asset paths in index.html'); 