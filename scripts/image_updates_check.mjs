// Run the REAL app/static/js/image_updates.js and check that a choice the
// owner has not saved yet survives every refresh.
//
// The section reloads its data every minute, after a save and after Check now.
// A reload that answered after the owner changed a select drew the controls
// again from the server's copy, so the change was lost without a word. The
// script now counts changes, and draws the controls again only when every
// change is saved. Only running it proves that, so this drives the script with
// a tiny DOM and API answers that arrive when the check says so.
//   node scripts/image_updates_check.mjs
// Exits non-zero on any mismatch.
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {t} from './i18n_stub.mjs';

const src = readFileSync('app/static/js/image_updates.js', 'utf8');

function makePage() {
  const listeners = {root: {}, doc: {}};
  const root = {
    innerHTML: '',
    renders: 0,
    addEventListener: (type, fn) => { listeners.root[type] = fn; },
    querySelectorAll: () => [],
    // The error line the controls carry, present once they are drawn.
    errorLine: {hidden: true, textContent: ''},
    // The overrides and a select in them; each drawing makes new ones, closed and not focused.
    details: null,
    select: null,
    contains: () => true,
    querySelector: (sel) => {
      if (sel === '[data-updates-load-error]') return html.includes('data-updates-load-error') ? root.errorLine : null;
      if (sel === 'details.add-worker') return html.includes('add-worker') ? root.details : null;
      if (sel === '[data-updates-service="honeygain"]') return html ? root.select : null;
      return null;
    },
  };
  // Count each time the controls are drawn.
  let html = '';
  const fresh = () => {
    root.details = {open: false};
    root.select = {focused: false, getAttribute: (a) => (a === 'data-updates-service' ? 'honeygain' : null)};
    root.select.focus = () => { root.select.focused = true; doc.activeElement = root.select; };
  };
  Object.defineProperty(root, 'innerHTML', {
    get: () => html,
    set: (v) => { html = v; root.renders += 1; fresh(); },
  });
  const pending = [];
  const calls = [];
  const api = (url, opts = {}) => new Promise((resolve, reject) => {
    calls.push({url, method: opts.method || 'GET', body: opts.body});
    pending.push({resolve, reject});
  });
  const settle = async () => { for (let i = 0; i < 5; i++) await Promise.resolve(); };
  const data = {
    settings: {mode: 'auto', hour: 4, workers: {}, services: {}},
    settle_seconds: 120, workers: [], services: [], history: [], running: false,
  };
  // The fleet choice, a control whose value a check can change.
  const modeEl = {value: 'auto'};
  const doc = {
    activeElement: null,
    getElementById: (id) => (id === 'updates-body' ? root : id === 'updates-mode' ? modeEl : null),
    addEventListener: (type, fn) => { listeners.doc[type] = fn; },
  };
  const context = {
    document: doc,
    window: {CPI18N: globalThis.CPI18N},
    CP: {api, toast: () => {}},
    t,
    setInterval: (fn) => { context.tick = fn; },
    String, Number, Object, JSON, Promise, Array, Date,
  };
  vm.runInNewContext(src, context);
  return {
    root,
    calls,
    change: () => listeners.root.change(),
    // Pick a fleet choice on the page, as the owner does, without saving it.
    pickMode: (value) => { modeEl.value = value; listeners.root.change(); },
    // The fleet choice as the page drew it, with no change by the owner.
    showMode: (value) => { modeEl.value = value; },
    click: (action) => listeners.doc.click({target: {closest: () => ({dataset: {updatesAction: action}})}}),
    tick: () => context.tick(),
    // Answer the oldest open request, then let the script run on.
    answer: async (body = data) => { pending.shift().resolve(body); await settle(); },
    // Answer the newest open request first, as a slow older one arrives later.
    answerNewest: async (body = data) => { pending.pop().resolve(body); await settle(); },
    fail: async (message) => { pending.shift().reject(new Error(message)); await settle(); },
    open: () => pending.length,
    // The owner opens the overrides and puts the focus on an app's select, changing nothing.
    browse: () => { root.details.open = true; doc.activeElement = root.select; },
    data,
  };
}

const failures = [];
let checksRun = 0;
const check = (name, ok, detail) => { checksRun++; if (!ok) failures.push(`${name}: ${detail}`); };

// 1. The first load draws the section.
let p = makePage();
await p.answer();
check('the first load draws the controls', p.root.renders === 1, `drawn ${p.root.renders} times`);

// 2. A change made while a refresh is on its way is kept.
p = makePage();
await p.answer();
p.tick();
p.change();
await p.answer();
check('a refresh that answers after a change keeps it', p.root.renders === 1, `drawn ${p.root.renders} times`);
p.tick();
check('the minute refresh waits while a change is not saved', p.open() === 0, `${p.open()} request(s) sent`);

// 3. A save clears the changes it sent, and only those.
p = makePage();
await p.answer();
p.change();
p.click('save');
check('Save sends a PUT', p.calls.at(-1).method === 'PUT', `sent ${p.calls.at(-1).method}`);
p.change();
await p.answer({});
await p.answer();
check('a change made during the save survives the reload after it', p.root.renders === 1, `drawn ${p.root.renders} times`);
p.click('save');
await p.answer({});
await p.answer();
check('once every change is saved, the reload draws the controls', p.root.renders === 2, `drawn ${p.root.renders} times`);

// 4. Check now keeps a change that is not saved.
p = makePage();
await p.answer();
p.change();
p.click('run');
check('Check now posts the run', p.calls.at(-1).url === '/api/image-updates/run', `sent ${p.calls.at(-1).url}`);
await p.answer({status: 'started'});
await p.answer();
check('Check now keeps a change that is not saved', p.root.renders === 1, `drawn ${p.root.renders} times`);

// 5. A positive control: with no change, Check now's reload draws again.
p = makePage();
await p.answer();
p.click('run');
await p.answer({status: 'started'});
await p.answer();
check('with no change, the reload after Check now draws the controls', p.root.renders === 2, `drawn ${p.root.renders} times`);

// 6. An older load that answers after a newer one is thrown away.
p = makePage();
await p.answer();
p.tick();
p.tick();
const off = {...p.data, settings: {...p.data.settings, mode: 'off'}};
await p.answerNewest(off);
await p.answer();
check('an older load that answers last draws nothing', p.root.renders === 2, `drawn ${p.root.renders} times`);
check('the newest answer is the one shown', p.root.innerHTML.includes('value="off" selected'), 'the fleet choice is not the newest answer');

// 6b. A stored choice with no control on the page is sent back with a save:
// the server replaces the whole map, so leaving it out would drop it.
p = makePage();
await p.answer({...p.data, settings: {...p.data.settings, services: {gone: 'off'}, workers: {9: 'notify'}}});
p.click('save');
const put = p.calls.at(-1);
check('a save keeps an app choice with no control', put.body?.services?.gone === 'off', JSON.stringify(put.body));
check('a save keeps a box choice with no control', put.body?.workers?.[9] === 'notify', JSON.stringify(put.body));

// 6b2. An app that left every box but keeps a saved choice still gets a
// control, so the owner can change that choice; a listed app is not doubled.
p = makePage();
await p.answer({...p.data, services: [{slug: 'honeygain', name: 'Honeygain'}], settings: {...p.data.settings, services: {gone: 'auto', honeygain: 'off'}}});
check('a saved choice for an app on no box has a control', p.root.innerHTML.includes('data-updates-service="gone"'), p.root.innerHTML);
check('an app on a box has one control', p.root.innerHTML.split('data-updates-service="honeygain"').length === 2, p.root.innerHTML);

// 6c. Two saves run one after the other, in the order they were asked for.
p = makePage();
await p.answer();
p.change();
p.click('save');
p.change();
p.click('save');
const puts = () => p.calls.filter((c) => c.method === 'PUT').length;
check('a second save waits for the first', puts() === 1, `${puts()} PUTs in flight`);
await p.answer({});
await p.answer();
check('the second save goes once the first is done', puts() === 2, `${puts()} PUTs sent`);

// 6d. A save takes the page as it is when asked for: a change made while it
// waits in the queue is not sent with it, and stays unsaved.
p = makePage();
await p.answer();
p.change();
p.click('save');
p.pickMode('off');
p.click('save');
p.pickMode('auto');
await p.answer({});
await p.answer();
await p.answer({});
await p.answer();
const queuedPut = p.calls.filter((c) => c.method === 'PUT')[1];
check('a queued save sends the page as it was when asked for', queuedPut && queuedPut.body.mode === 'off', JSON.stringify(queuedPut && queuedPut.body));
check('a change made after a queued save stays unsaved', p.root.renders === 1, `drawn ${p.root.renders} times`);

// 7. A reload that fails keeps the controls and a change not saved, and says so.
p = makePage();
await p.answer();
p.change();
p.click('run');
await p.answer({status: 'started'});
await p.fail('the dashboard did not answer');
check('a failed reload keeps the controls', p.root.renders === 1, `drawn ${p.root.renders} times`);
check('a failed reload shows its error beside them', !p.root.errorLine.hidden && p.root.errorLine.textContent.includes('did not answer'), JSON.stringify(p.root.errorLine));
// 5. A refresh keeps the overrides open and the focus where the owner left it.
p = makePage();
await p.answer();
p.browse();
p.tick();
await p.answer();
check('a refresh draws the controls again', p.root.renders === 2, `drawn ${p.root.renders} times`);
check('a refresh keeps the overrides open', p.root.details.open === true, JSON.stringify(p.root.details));
check('a refresh keeps the focus on the same control', p.root.select.focused === true, JSON.stringify(p.root.select));
// 5b. Enable sets the fleet choice on the page too: a change made while its
// save waits, saved after it, sends auto, never the off the page showed.
p = makePage();
await p.answer({...p.data, settings: {...p.data.settings, mode: 'off', offer: true}});
p.showMode('off');
p.click('enable');
check('Enable sends auto', p.calls.at(-1).method === 'PUT' && p.calls.at(-1).body.mode === 'auto', JSON.stringify(p.calls.at(-1)));
p.change();
await p.answer({});
await p.answer({...p.data, settings: {...p.data.settings, mode: 'auto'}});
p.click('save');
check('a save after Enable keeps auto', p.calls.at(-1).body.mode === 'auto', JSON.stringify(p.calls.at(-1).body));
p = makePage();
await p.fail('the dashboard did not answer');
check('a first load that fails says so in place of the controls', p.root.innerHTML.includes('did not answer'), p.root.innerHTML);

if (failures.length) {
  console.error(`image updates check FAILED (${failures.length} of ${checksRun}):\n  ${failures.join('\n  ')}`);
  process.exit(1);
}
console.log(`image updates check: ${checksRun} checks passed`);
