// Run the REAL fillNeeds() of fleet.html's copy form against a small DOM.
//
// The form lists one checkbox per risk the owner must acknowledge, and the
// server refuses the copy without every one. Two ways it went wrong:
//   - the page refreshes every 60 s and rebuilt the boxes unticked, so an
//     owner who ticked them and waited lost them, and the copy was refused;
//   - a failed lookup left an empty panel with Run enabled, so the copy went
//     out with no ticks and was refused with no word why.
//
//   node scripts/copy_needs_check.mjs
// Exits non-zero on any mismatch.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import './i18n_stub.mjs';

const html = readFileSync('app/templates/fleet.html', 'utf8');

function extract(name) {
  const start = html.indexOf(`function ${name}(`);
  if (start < 0) throw new Error(`fleet.html no longer defines ${name}() — this check is stale`);
  let i = html.indexOf('{', start), depth = 0;
  for (let j = i; j < html.length; j++) {
    if (html[j] === '{') depth++;
    else if (html[j] === '}' && --depth === 0) return html.slice(start, j + 1);
  }
  throw new Error(`unbalanced braces reading ${name}()`);
}

const esc = s => String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

// The panel's checkboxes, read back from the HTML fillNeeds wrote.
const box = {
  innerHTML: '',
  querySelectorAll(sel) {
    const all = sel === 'input[data-ack]';
    assert.ok(all || sel === 'input[data-ack]:checked', sel);
    const re = all ? /<input type="checkbox" data-ack="([a-z_]+)"( checked)?>/g : /<input type="checkbox" data-ack="([a-z_]+)" checked>/g;
    return [...this.innerHTML.matchAll(re)].map(m => ({dataset: {ack: m[1]}}));
  },
};
const tick = key => { box.innerHTML = box.innerHTML.replace(`data-ack="${key}">`, `data-ack="${key}" checked>`); };
const untick = key => { box.innerHTML = box.innerHTML.replace(`data-ack="${key}" checked>`, `data-ack="${key}">`); };
const run = {disabled: false};
const slug = {value: 'mysterium'};
const proxy = {value: '3'};
let retryHandler = null;
const document = {
  getElementById: id => ({
    'copy-needs': box,
    'copy-run': run,
    'copy-slug': slug,
    'copy-proxy': proxy,
    'copy-needs-retry': {addEventListener: (_, fn) => { retryHandler = fn; }},
  })[id],
};
let answer = {needs: ['net_admin', 'tun_device', 'no_inbound'], volumes: ['mysterium-data-p3']};
let during = null; // runs while the request is out, as an owner's click would
let hold = null; // a request left open until the check answers it, as a slow worker would
const CP = {api: async () => {
  if (hold) { const open = hold; hold = null; return open.promise; }
  if (during) { during(); during = null; }
  if (answer instanceof Error) throw answer;
  return answer;
}};
const opened = () => { const o = {}; o.promise = new Promise((resolve, reject) => { o.resolve = resolve; o.reject = reject; }); return o; };

const fillNeeds = new Function(
  'document', 'CP', 'esc', 't',
  `let _needsAsked = 0;\nlet _needsFor = '';\nlet _needsTicked = new Set();\n${extract('ackText')}\nreturn async ${extract('fillNeeds')};`,
)(document, CP, esc, globalThis.t);

await fillNeeds();
assert.equal(run.disabled, false, 'Run is on once the needs are known');
assert.equal(box.querySelectorAll('input[data-ack]:checked').length, 0, 'nothing is ticked for the owner');
assert.match(box.innerHTML, /data-ack="net_admin"/);

// The owner ticks two; the 60 s refresh asks again for the same service and proxy.
tick('net_admin');
tick('no_inbound');
await fillNeeds();
assert.deepEqual(
  box.querySelectorAll('input[data-ack]:checked').map(el => el.dataset.ack), ['net_admin', 'no_inbound'],
  'a refresh of the same service and proxy keeps the ticks',
);

// The owner ticks one and unticks another while the refresh is out: the boxes show that.
during = () => { tick('tun_device'); untick('net_admin'); };
await fillNeeds();
assert.deepEqual(
  box.querySelectorAll('input[data-ack]:checked').map(el => el.dataset.ack), ['tun_device', 'no_inbound'],
  'ticks changed during a refresh are kept',
);

// Another proxy: the ticks answered the old one's needs, so they go.
proxy.value = '4';
await fillNeeds();
assert.equal(box.querySelectorAll('input[data-ack]:checked').length, 0, 'another proxy clears the ticks');

// The lookup fails: the owner is told, Run stays off, and Try again asks again.
answer = new Error('worker offline');
await fillNeeds();
assert.equal(run.disabled, true, 'Run stays off while the needs are unknown');
assert.match(box.innerHTML, /could not read what this service needs behind this proxy \(worker offline\)/);
assert.equal(typeof retryHandler, 'function', 'the retry button asks again');
answer = {needs: ['net_admin'], volumes: []};
await retryHandler();
assert.equal(run.disabled, false, 'a retry that works turns Run back on');
assert.match(box.innerHTML, /data-ack="net_admin"/);

// The owner ticks, a refresh of the same service and proxy fails, and Try again works: the tick is still there.
tick('net_admin');
answer = new Error('worker offline');
await fillNeeds();
assert.equal(run.disabled, true, 'Run stays off while the needs are unknown');
answer = {needs: ['net_admin'], volumes: []};
await retryHandler();
assert.deepEqual(
  box.querySelectorAll('input[data-ack]:checked').map(el => el.dataset.ack), ['net_admin'],
  'a failed refresh and its retry keep the ticks',
);

// The account risk's line names the service and its terms, not another service's.
proxy.value = '5';
answer = {needs: ['account_risk'], volumes: [], name: 'Packetwave', risk_source: 'https://packetwave.example/terms'};
await fillNeeds();
assert.match(box.innerHTML, /Your Packetwave account may be suspended/, 'the account risk names its own service');
assert.match(box.innerHTML, /https:\/\/packetwave\.example\/terms/, 'and links its terms');
assert.doesNotMatch(box.innerHTML, /Honeygain/, 'never Honeygain\'s');

// A refusal keeps Run off.
answer = {refusal: 'Storj needs inbound connections on a published port.'};
await fillNeeds();
assert.equal(run.disabled, true, 'a refused service cannot be run');
// A worker change empties the service list while a lookup is out: its late answer is dropped.
for (const late of [o => o.resolve({needs: ['net_admin'], volumes: []}), o => o.reject(new Error('worker offline'))]) {
  slug.value = 'mysterium';
  hold = opened();
  const open = hold;
  const out = fillNeeds();
  slug.value = '';
  await fillNeeds();
  late(open);
  await out;
  assert.equal(box.innerHTML, '', 'a late answer or failure for the old service leaves the cleared panel');
  assert.equal(run.disabled, false, 'Run stays as the empty selection left it');
}
console.log('Copy form: the ticks survive a refresh, a failed lookup is shown with a retry, and Run waits for the needs.');

// ---- The copy list: the "reduced isolation" badge and Withdraw are for isolation ticks only ----
const listBox = {innerHTML: ''};
const render = new Function(
  'document', 'esc', 't', 'ackText', 'workerName', 'capLine', 'copyStatus', '_proxies',
  `return ${extract('render')};`,
)(
  {getElementById: id => (id === 'proxy-list' ? listBox : null)}, esc, globalThis.t,
  new Function('t', `${extract('ackText')}\nreturn ackText;`)(globalThis.t),
  () => 'box1', () => '', () => ({status: 'running', via: ''}),
  [{id: 3, name: 'Gate', kind: 'socks5', host: 'h', port: 1, cap: {}, copies: [
    {worker_id: 1, slug: 'honeygain', acknowledged: ['account_risk']},
    {worker_id: 1, slug: 'bitping', acknowledged: ['net_raw']},
  ]}],
);
render();
const rows = listBox.innerHTML.split('<div>').slice(1);
const honeygainRow = rows.find(r => r.includes('data-copy="3:1:honeygain"'));
const bitpingRow = rows.find(r => r.includes('data-copy="3:1:bitping"'));
assert.doesNotMatch(honeygainRow, /reduced isolation/, 'the account risk is no reduced isolation');
assert.match(honeygainRow, /data-cmd="remove">Remove</, 'and its copy is removed, not withdrawn');
assert.match(bitpingRow, /reduced isolation/, 'NET_RAW still shows the badge');
assert.match(bitpingRow, /data-cmd="remove">Withdraw</, 'and Withdraw');
console.log('Copy list: only isolation ticks show the badge and Withdraw.');
