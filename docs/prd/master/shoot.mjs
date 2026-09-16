// Screenshot driver for the mock: launches headless Chrome, drives the page with
// Runtime.evaluate, saves PNGs. No dependencies — Node's built-in WebSocket + fetch.
//
//   node shoot.mjs shots.json          capture every shot
//   node shoot.mjs --eval "expr"       evaluate one expression and print it
import { writeFileSync, readFileSync } from 'node:fs';
import { spawn } from 'node:child_process';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const BASE = process.env.BASE || 'http://localhost:8090/webinar.html';
const W = 1600, H = 1000;

const sleep = ms => new Promise(r => setTimeout(r, ms));

const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`,
  `--window-size=${W},${H}`, '--hide-scrollbars', '--force-device-scale-factor=2',
  '--no-first-run', '--no-default-browser-check',
  '--user-data-dir=/tmp/prd-shoot-profile', 'about:blank'
], { stdio: 'ignore' });

let ws, id = 0;
const pending = new Map();

function send(method, params = {}) {
  return new Promise((res, rej) => {
    const m = ++id;
    pending.set(m, { res, rej });
    ws.send(JSON.stringify({ id: m, method, params }));
  });
}
const evaluate = async expr => {
  const r = await send('Runtime.evaluate', {
    expression: expr, returnByValue: true, awaitPromise: true, userGesture: true
  });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || 'eval failed');
  return r.result?.value;
};

async function connect() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await fetch(`http://127.0.0.1:${PORT}/json/list`).then(r => r.json());
      const page = list.find(t => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(250);
  }
  throw new Error('Chrome never came up');
}

const wsUrl = await connect();
ws = new WebSocket(wsUrl);
ws.addEventListener('message', e => {
  const msg = JSON.parse(e.data);
  if (msg.id && pending.has(msg.id)) {
    const { res, rej } = pending.get(msg.id);
    pending.delete(msg.id);
    msg.error ? rej(new Error(msg.error.message)) : res(msg.result);
  }
});
await new Promise(r => ws.addEventListener('open', r, { once: true }));
await send('Page.enable');
await send('Runtime.enable');

async function load(url) {
  await send('Page.navigate', { url });
  for (let i = 0; i < 80; i++) {
    await sleep(200);
    const ready = await evaluate('document.readyState === "complete" && !!window.openSettingsModal').catch(() => false);
    if (ready) break;
  }
  await sleep(900);   // let the React trees mount
  // helpers the shot definitions lean on
  await evaluate(`
    window.__click = function(text, tag) {
      var els = document.querySelectorAll(tag || '*');
      for (var i = 0; i < els.length; i++) {
        var e = els[i];
        if (e.children.length > 3) continue;
        if ((e.textContent || '').trim() === text && e.offsetParent !== null) { e.click(); return true; }
      }
      return false;
    };
    window.__clickContains = function(text, tag) {
      var els = document.querySelectorAll(tag || '*');
      for (var i = 0; i < els.length; i++) {
        var e = els[i];
        if (e.children.length > 3) continue;
        if ((e.textContent || '').indexOf(text) !== -1 && e.offsetParent !== null) { e.click(); return true; }
      }
      return false;
    };
    window.__clickRelated = function(label) {
      var els = document.querySelectorAll('#page-detail div');
      for (var i = 0; i < els.length; i++) {
        var e = els[i], t = (e.textContent || '').trim();
        if (e.onclick && t.indexOf(label) === 0 && t.length < label.length + 6 && e.offsetParent) { e.click(); return true; }
      }
      return false;
    };
    window.__scrollDetail = function(px) {
      var r = document.getElementById('react-detail-root');
      if (!r) return -1; r.scrollTop = px; return r.scrollTop;
    };
    window.__pick = function(labelText, optionText) {
      var ls = document.querySelectorAll('#page-form label');
      for (var i = 0; i < ls.length; i++) {
        if ((ls[i].textContent || '').trim() !== labelText) continue;
        var g = ls[i].closest('.form-group') || ls[i].parentElement;
        var btn = g.querySelector('.cs-btn'); if (btn) btn.click();
        var opts = g.querySelectorAll('.cs-opt');
        for (var j = 0; j < opts.length; j++) {
          if ((opts[j].textContent || '').trim() === optionText) { opts[j].click(); return true; }
        }
        return 'option not found';
      }
      return 'label not found';
    };
    window.__scrollForm = function(px) {
      var b = document.querySelector('.form-page-body'); if (!b) return -1; b.scrollTop = px; return b.scrollTop;
    };
    window.__scrollTo = function(sel) {
      var e = document.querySelector(sel); if (e) e.scrollIntoView({block:'start'}); return !!e;
    };
    true;
  `);
}

async function shot(file) {
  const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  writeFileSync(`screens/${file}`, Buffer.from(r.data, 'base64'));
  return file;
}

const arg = process.argv[2];
if (arg === '--eval') {
  await load(BASE);
  const out = await evaluate(process.argv[3]);
  console.log(typeof out === 'string' ? out : JSON.stringify(out, null, 1));
} else {
  const shots = JSON.parse(readFileSync(arg, 'utf8'));
  let done = 0;
  for (const s of shots) {
    try {
      await load(BASE + (BASE.includes('?') ? '&' : '?') + 'v=' + Date.now());
      for (const step of (s.steps || (s.setup ? [s.setup] : []))) {
        await evaluate(step);
        await sleep(s.stepWait ?? 700);
      }
      await sleep(s.wait ?? 700);
      if (s.scroll) await evaluate(`(${s.scroll})`);
      await sleep(s.scroll ? 500 : 0);
      await shot(s.file);
      console.log('  ok   ' + s.file);
      done++;
    } catch (e) {
      console.log('  FAIL ' + s.file + ' -> ' + e.message);
    }
  }
  console.log(`\n${done}/${shots.length} captured`);
}

ws.close();
chrome.kill();
process.exit(0);
