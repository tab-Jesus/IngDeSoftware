import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const browser=await chromium.launch({headless:true,channel:'msedge'});
const page=await browser.newPage({viewport:{width:1440,height:900}});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
await page.goto(pathToFileURL(path.join(root,'presentacion/index.html')).href);
await page.waitForTimeout(800);
for(let i=1;i<=5;i++){
 if(await page.locator('#counter').textContent()!==`${i} / 5`)throw Error('Contador incorrecto');
 await page.screenshot({path:path.join(root,`tmp/slides/html-${i}.png`)});
 if(i<5){await page.keyboard.press('ArrowRight');await page.waitForTimeout(800)}
}
await page.locator('#notesButton').click();
if(!await page.locator('#notes').isVisible())throw Error('Notas no visibles');
await page.keyboard.press('Home');
if(!await page.locator('#prev').isDisabled())throw Error('Límite inicial incorrecto');
const broken=await page.locator('img').evaluateAll(images=>images.filter(i=>!i.complete||!i.naturalWidth).length);
if(broken||errors.length)throw Error(JSON.stringify({broken,errors}));
await page.setViewportSize({width:390,height:844});
await page.locator('#notesButton').click();
await page.waitForTimeout(800);
await page.screenshot({path:path.join(root,'tmp/slides/mobile.png')});
if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Desborde horizontal');
await browser.close();
await fs.writeFile(path.join(root,'evidencia/presentacion_qa.txt'),'QA navegador Edge: 5 diapositivas; navegación por teclado; límites; notas; imágenes locales; sin errores JavaScript; viewport móvil 390 x 844 sin desborde horizontal.\nPPTX: validación de integridad, geometría, fuentes y reimportación aprobada; revisión visual de las cinco diapositivas. Transiciones presentes en el archivo; no se verificó reproducción en PowerPoint.\n');
console.log('QA HTML aprobado.');
