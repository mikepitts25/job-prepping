# 6. The four-hour frontend sprint

Angular, JavaScript, CSS and HTML are a **basic qualification** on your
requisition. If you have four hours and no web background, this is how to spend
them.

Same contract as [the Python sprint](python-sprint.html): you cannot become a
frontend engineer in four hours, but you can become one who has been doing it
for four hours, and that is enough to write a working page, discuss Angular
credibly, and not bluff.

We build **one thing**: an air picture page. A table of tracks, filterable,
that loads from an API, marks stale tracks, and has a test suite. By hour four
it exists twice, once in plain TypeScript and once as an Angular component, so
you can see exactly what the framework does for you.

[Lesson 12](frontend.html) is the thorough reference. This is the sprint.

## The rules

Same as before, and they are what make four hours work.

1. **Type everything. Never paste.**
2. **Look at it.** Keep the page open in a browser. Refresh after every change.
   The feedback loop is the whole advantage of frontend work; use it.
3. **Keep the browser devtools open.** F12. The Console tab shows errors, the
   Elements tab shows the live DOM. You will need both.
4. **Break things on purpose** where I say so.
5. **Respect the clock.** Move on even if a block is unfinished.

## What I am cutting, and why

| Cut | Why |
| --- | --- |
| React, Vue, Svelte | Your req says Angular. |
| Build tooling internals (webpack, Vite config) | The Angular CLI does it. |
| Sass, Tailwind, CSS-in-JS | Plain CSS is enough today and transfers. |
| RxJS beyond four operators | You will read far more than you write. |
| NgModules | Standalone components are the modern default. You will meet modules in legacy code; hour 4 shows you what they look like. |
| State libraries (NgRx) | Signals cover everything you need at this level. |
| Animations, i18n, SSR | Not on the req, not in four hours. |

## Setup: ten minutes, before the clock

```bash
mkdir fesprint && cd fesprint
npm init -y
npm install --save-dev typescript@5.6.3 vitest@2.1.8 jsdom@25.0.1
npx tsc --version         # expect 5.6.3
```

Add `"type": "module"` to `package.json`. Then two config files:

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022", "module": "ES2022", "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM"], "strict": true, "noUnusedLocals": true,
    "skipLibCheck": true, "noEmit": true
  },
  "include": ["*.ts"]
}
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
export default defineConfig({ test: { environment: 'jsdom' } });
```

`jsdom` is a fake browser that runs in Node, so tests can create elements and
click things without opening a real browser. That is what makes hour three
possible.

Start the clock.

---

## Hour 1: a page you can look at

### 0:00 to 0:10 — The three languages

A browser does three things: fetch documents, render them, run JavaScript.

| Language | Job |
| --- | --- |
| **HTML** | Structure and content. The nouns. |
| **CSS** | Presentation. The adjectives. |
| **JavaScript** | Behaviour. The verbs. |

The browser parses your HTML into a tree of objects called the **DOM**.
JavaScript changes that tree; the browser re-renders. Hold that sentence: it is
what Angular exists to automate.

### 0:10 to 0:35 — HTML

Create `index.html` and type this. All of it.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Air Picture</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <h1>Air Picture</h1>

    <div class="toolbar">
      <label for="affiliation">Affiliation</label>
      <select id="affiliation">
        <option value="all">All</option>
        <option value="hostile">Hostile</option>
        <option value="unknown">Unknown</option>
        <option value="friend">Friend</option>
      </select>

      <label for="min-confidence">Min confidence</label>
      <input id="min-confidence" type="number" min="0" max="1" step="0.1" value="0">

      <span id="status" role="status" class="status"></span>
    </div>

    <table>
      <caption>Current tracks, worst confidence first</caption>
      <thead>
        <tr>
          <th scope="col">Track</th>
          <th scope="col">Affiliation</th>
          <th scope="col">Altitude</th>
          <th scope="col">Confidence</th>
        </tr>
      </thead>
      <tbody id="rows"></tbody>
    </table>

    <script type="module" src="app.js"></script>
  </body>
</html>
```

Open it in a browser. It is ugly and empty below the header. That is correct.

What just went past you, and why each bit is there:

**Tags nest into a tree.** `<html>` contains `<head>` and `<body>`. `head` is
metadata nobody sees; `body` is the page.

**`id` names one element** so CSS and JavaScript can find it. `class` groups
many.

**Every `label` has a `for` matching an input's `id`.** That pairing makes
clicking the label focus the field and makes a screen reader announce what the
field is for. It is the single most skipped detail in web forms, and on a US
government programme accessibility is a legal requirement under Section 508.

**`th scope="col"` and `<caption>`** are what let a screen reader announce
"Altitude, 32,000 feet" instead of reading a wall of numbers.

**`role="status"`** on the status span means assistive technology announces
changes to it without stealing focus.

**`<tbody id="rows">` is empty** because JavaScript will fill it.

**Do now, three minutes.** In devtools, Elements tab, find `tbody#rows`. Then
in the Console type `document.getElementById('rows')`. That is the connection
between the markup and the code, and seeing it once makes the rest obvious.

### 0:35 to 1:00 — CSS

Create `styles.css`:

```css
*, *::before, *::after { box-sizing: border-box; }

:root {
  --ink: #1d1b18;
  --line: #e3ded5;
  --hostile: #b3261e;
  --muted: #5f5a52;
}

body {
  margin: 0;
  padding: 24px;
  font: 15px/1.5 system-ui, sans-serif;
  color: var(--ink);
}

h1 { font-size: 22px; margin: 0 0 16px; }

.toolbar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.status { margin-left: auto; color: var(--muted); }

table { border-collapse: collapse; width: 100%; }
caption { text-align: left; color: var(--muted); padding-bottom: 8px; }
th, td { border-bottom: 1px solid var(--line); padding: 6px 10px; text-align: left; }
th { background: #f4f1ec; }
tbody tr:nth-child(even) { background: #faf9f7; }

tr.hostile td:first-child { color: var(--hostile); font-weight: 600; }
tr.stale { opacity: 0.55; font-style: italic; }

@media (max-width: 700px) {
  .toolbar { flex-direction: column; align-items: stretch; }
  .status { margin-left: 0; }
}
```

Refresh. It now looks like software.

The ideas, each of which earns its line:

**`box-sizing: border-box` on everything.** By default `width` measures only
the content, so adding padding makes the box wider than you asked for. This one
line makes `width` mean the whole box, which is what everyone intends. Set it
once in every project and stop fighting it.

**Selectors.** `h1` targets elements, `.toolbar` targets a class, `#rows`
targets an id, `tr.hostile td:first-child` targets the first cell of rows with
that class. Prefer classes: ids are too specific, element selectors too broad.

**Custom properties.** `--hostile` defined once on `:root`, used with
`var(--hostile)`. Variables in CSS. Change a theme in one place.

**Flexbox** lays things out in one direction. `gap` spaces children, and
`margin-left: auto` on the status pushes it to the far end, which is the
idiomatic way to right-align one flex item.

**A media query** applies rules conditionally. Under 700 pixels the toolbar
stacks.

**Do now, five minutes.** Break things and watch:

1. Delete `box-sizing` and add `width: 100%` to `.toolbar` inputs. Watch the
   overflow. Put it back.
2. Change `display: flex` to `display: block` on `.toolbar`. Watch it stack.
3. In devtools, Elements tab, select a `<tr>` and add `class="hostile"` by hand.
   Watch the first cell turn red. That is CSS and HTML meeting.

**Checkpoint, 1:00.** Close the files. From memory, write the CSS rule that
makes every element use border-box sizing, and a flexbox toolbar with a 12 pixel
gap. **Five minutes off.**

---

## Hour 2: make it live

### 1:00 to 1:20 — JavaScript, translated from Python

You know Python. Here is the map.

| Python | JavaScript |
| --- | --- |
| `x = 5` | `const x = 5;` |
| `None` | `null` and `undefined` |
| `def f(a, b=1):` | `function f(a, b = 1) {}` |
| `lambda x: x * 2` | `(x) => x * 2` |
| `[f(x) for x in xs]` | `xs.map(f)` |
| `[x for x in xs if p(x)]` | `xs.filter(p)` |
| `sum(xs)` | `xs.reduce((a, b) => a + b, 0)` |
| `sorted(xs, key=f)` | `[...xs].sort((a, b) => f(a) - f(b))` |
| f-string | `` `backtick ${template}` `` |
| indentation | `{ }` braces |

```javascript
const tracks = [
  { trackId: 'T-001', affiliation: 'hostile', confidence: 0.9 },
  { trackId: 'T-002', affiliation: 'friend', confidence: 0.3 },
];

const ids = tracks.map((t) => t.trackId);
const hostiles = tracks.filter((t) => t.affiliation === 'hostile');
const sorted = [...tracks].sort((a, b) => a.confidence - b.confidence);
```

Four things to burn in now:

**`const` by default**, `let` only when you must reassign, never `var`.

**`===`, never `==`.** The double equals converts types with rules nobody
remembers. `1 == '1'` is true; `1 === '1'` is false. Use the strict one always.

**`sort` mutates the array in place.** `[...tracks]` copies first. That spread
syntax also does "copy with a change": `{ ...track, confidence: 0.5 }`.

**A comparator returns a number**, not a boolean. Negative means "a first."
`(a, b) => a.confidence - b.confidence` sorts ascending. This trips up everyone
coming from Python's `key=`.

### 1:20 to 1:50 — Filtering, sorting, rendering

Now the real work. Create `app.ts` (we will add types in hour three; for now
the logic).

```typescript
export function visibleTracks(tracks, filters) {
  return tracks
    .filter((t) => filters.affiliation === 'all' || t.affiliation === filters.affiliation)
    .filter((t) => t.confidence >= filters.minConfidence)
    .sort((a, b) => a.confidence - b.confidence || a.trackId.localeCompare(b.trackId));
}

export function formatAltitude(feet) {
  return `${Math.round(feet).toLocaleString('en-US')} ft`;
}

export function isStale(track, now, maxAgeSeconds = 30) {
  return (now.getTime() - new Date(track.lastSeen).getTime()) / 1000 > maxAgeSeconds;
}
```

The `|| a.trackId.localeCompare(b.trackId)` is the tie-break, and it is not
decoration. Without it the order of equally-confident rows is unspecified, the
table reshuffles on every refresh, and an operator loses their place. **A
deterministic sort is a usability requirement here, and it is also what makes it
testable.** Say that in an interview.

`isStale` takes `now` as a parameter instead of calling `new Date()` inside.
That is what lets a test move time without waiting, exactly like injecting a
clock in Python.

Now rendering:

```typescript
export function renderRows(tbody, tracks, now) {
  tbody.replaceChildren();

  for (const track of tracks) {
    const row = tbody.ownerDocument.createElement('tr');
    row.classList.add(track.affiliation);
    if (isStale(track, now)) {
      row.classList.add('stale');
    }

    for (const text of [
      track.trackId,
      track.affiliation,
      formatAltitude(track.altitudeFt),
      track.confidence.toFixed(2),
    ]) {
      const cell = tbody.ownerDocument.createElement('td');
      cell.textContent = text;
      row.appendChild(cell);
    }
    tbody.appendChild(row);
  }
}
```

Three deliberate decisions here, each worth stating:

**It takes `tbody` as an argument** rather than looking it up itself. That is
dependency injection in miniature, and it is what lets a test hand it a
detached element.

**`textContent`, never `innerHTML`.** Building markup from data strings is how
cross-site scripting happens: a track id of `<img src=x onerror=alert(1)>`
would execute. `textContent` treats it as text. There is a test for exactly
this in hour three.

**`replaceChildren()` first**, so re-rendering replaces rather than appends.
Forgetting this gives you a table that grows forever, which is a very common
beginner bug.

### 1:50 to 2:00 — Wiring the controls

```typescript
export function wireControls(el, tracks, now) {
  const redraw = () => {
    const filters = {
      affiliation: el.affiliation.value,
      minConfidence: Number(el.minConfidence.value) || 0,
    };
    const shown = visibleTracks(tracks, filters);
    renderRows(el.tbody, shown, now);
    el.status.textContent = `${shown.length} of ${tracks.length} tracks`;
  };

  el.affiliation.addEventListener('change', redraw);
  el.minConfidence.addEventListener('input', redraw);
  redraw();
  return redraw;
}
```

**This function is the whole lesson of hour two.** Every control change calls
one `redraw`, which reads the current state and rebuilds the view. Nothing
patches individual cells.

That discipline is what a framework automates: **describe the view as a
function of the state.** Angular in hour four does exactly this, and now you
will know what it is saving you from.

Note `Number(el.minConfidence.value) || 0`: an empty input gives `""`, and
`Number("")` is `0`, but `Number("abc")` is `NaN`, and every comparison against
`NaN` is false, which would silently hide every row. The `|| 0` catches it.

**Do now, five minutes.** Break it: remove `replaceChildren()` and change the
filter a few times. Watch rows accumulate. Put it back. Then remove `redraw()`
at the end and reload: the table starts empty until you touch a control. Put it
back.

**Take five minutes off.**

---

## Hour 3: types and tests

### 2:00 to 2:25 — TypeScript

TypeScript is JavaScript plus a type system. You write types, a compiler checks
them and erases them, and plain JavaScript comes out. **Nothing is checked at
runtime.**

Why bother: JavaScript will happily let `track.altitide` (misspelled) be
`undefined`, and you find out when an operator sees a blank cell. TypeScript
catches it before the code runs.

Add the types to the top of `app.ts`:

```typescript
export type Affiliation = 'friend' | 'hostile' | 'neutral' | 'unknown';

export interface Track {
  readonly trackId: string;
  readonly affiliation: Affiliation;
  readonly altitudeFt: number;
  readonly confidence: number;
  readonly lastSeen: string;
}

export interface Filters {
  readonly affiliation: Affiliation | 'all';
  readonly minConfidence: number;
}
```

`Affiliation` is a **union of literal types**: those four strings are the only
legal values, and `'banana'` is a compile error. That is how you model an
enumerated field from an interface control document, and it is a type system
doing real work.

`readonly` means the field cannot be reassigned after construction. Immutable
data is safer to pass around, same argument as frozen dataclasses in Python.

Now annotate the functions:

```typescript
export function visibleTracks(tracks: readonly Track[], filters: Filters): Track[] { ... }
export function formatAltitude(feet: number): string { ... }
export function isStale(track: Track, now: Date, maxAgeSeconds = 30): boolean { ... }
export function renderRows(tbody: HTMLElement, tracks: readonly Track[], now: Date): void { ... }
```

Run `npx tsc --noEmit`. Fix what it complains about.

### 2:25 to 2:40 — Validating untrusted data

This is the most important fifteen minutes of the hour.

Data from an API is **not** a `Track` just because you said so. Casting with
`as Track` is a lie the compiler believes. Validate instead:

```typescript
const AFFILIATIONS: readonly string[] = ['friend', 'hostile', 'neutral', 'unknown'];

export function parseTrack(raw: unknown): Track {
  if (typeof raw !== 'object' || raw === null) {
    throw new Error('not an object');
  }
  const r = raw as Record<string, unknown>;

  const trackId = r['trackId'];
  if (typeof trackId !== 'string' || trackId.trim() === '') {
    throw new Error('trackId must be a non-empty string');
  }
  const affiliation = r['affiliation'];
  if (typeof affiliation !== 'string' || !AFFILIATIONS.includes(affiliation)) {
    throw new Error(`affiliation must be one of ${AFFILIATIONS.join(', ')}`);
  }
  const altitudeFt = r['altitudeFt'];
  if (typeof altitudeFt !== 'number' || !Number.isFinite(altitudeFt)) {
    throw new Error('altitudeFt must be a finite number');
  }
  const confidence = r['confidence'];
  if (typeof confidence !== 'number' || confidence < 0 || confidence > 1) {
    throw new Error('confidence must be between 0 and 1');
  }
  const lastSeen = r['lastSeen'];
  if (typeof lastSeen !== 'string') {
    throw new Error('lastSeen must be a string');
  }

  return {
    trackId: trackId.trim(),
    affiliation: affiliation as Affiliation,
    altitudeFt, confidence, lastSeen,
  };
}
```

**`unknown` versus `any` is the distinction to remember.** `any` switches type
checking off and lets bad data through silently. `unknown` forces you to prove
what a value is before using it. External data should always arrive as
`unknown`. That answer alone marks you out in an interview.

And the fetch:

```typescript
export async function loadTracks(fetchFn: typeof fetch = fetch): Promise<Track[]> {
  const response = await fetchFn('/api/v1/tracks');
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const payload: unknown = await response.json();
  if (!Array.isArray(payload)) {
    throw new Error('expected an array');
  }
  const tracks: Track[] = [];
  for (const raw of payload) {
    try {
      tracks.push(parseTrack(raw));
    } catch {
      // One bad record must not blank the operator's screen.
    }
  }
  return tracks;
}
```

**The trap worth knowing:** `fetch` only rejects on a *network* failure. A 404
or a 500 is a perfectly successful HTTP exchange as far as `fetch` is
concerned, so you must check `response.ok` yourself. People miss this
constantly, and it is a good interview answer.

`fetchFn` is a parameter defaulting to the real `fetch`, so a test can pass a
fake. Same injection trick as the clock.

### 2:40 to 3:00 — Tests

```typescript
import { beforeEach, describe, expect, it } from 'vitest';
import { type Track, isStale, parseTrack, renderRows, visibleTracks, wireControls } from './app';

function track(overrides: Partial<Track> = {}): Track {
  return {
    trackId: 'T-001', affiliation: 'unknown', altitudeFt: 10_000,
    confidence: 0.9, lastSeen: '2026-09-16T12:00:00Z', ...overrides,
  };
}

describe('visibleTracks', () => {
  const tracks = [
    track({ trackId: 'T-1', affiliation: 'hostile', confidence: 0.9 }),
    track({ trackId: 'T-2', affiliation: 'friend', confidence: 0.3 }),
    track({ trackId: 'T-3', affiliation: 'hostile', confidence: 0.5 }),
  ];

  it('sorts worst confidence first', () => {
    const shown = visibleTracks(tracks, { affiliation: 'all', minConfidence: 0 });
    expect(shown.map((t) => t.confidence)).toEqual([0.3, 0.5, 0.9]);
  });

  it('breaks ties by track id so rows do not jump between refreshes', () => {
    const tied = [track({ trackId: 'T-B', confidence: 0.5 }), track({ trackId: 'T-A', confidence: 0.5 })];
    const shown = visibleTracks(tied, { affiliation: 'all', minConfidence: 0 });
    expect(shown.map((t) => t.trackId)).toEqual(['T-A', 'T-B']);
  });

  it('can show nothing', () => {
    expect(visibleTracks(tracks, { affiliation: 'all', minConfidence: 0.99 })).toEqual([]);
  });
});

describe('renderRows', () => {
  let tbody: HTMLElement;
  const now = new Date('2026-09-16T12:00:10Z');

  beforeEach(() => {
    document.body.innerHTML = '<table><tbody id="rows"></tbody></table>';
    tbody = document.getElementById('rows')!;
  });

  it('renders one row per track with four cells', () => {
    renderRows(tbody, [track(), track({ trackId: 'T-002' })], now);
    expect(tbody.querySelectorAll('tr')).toHaveLength(2);
    expect(tbody.querySelectorAll('tr:first-child td')).toHaveLength(4);
  });

  it('clears previous rows instead of appending to them', () => {
    renderRows(tbody, [track(), track({ trackId: 'T-002' })], now);
    renderRows(tbody, [track()], now);
    expect(tbody.querySelectorAll('tr')).toHaveLength(1);
  });

  it('does not interpret data as markup', () => {
    renderRows(tbody, [track({ trackId: '<img src=x onerror=alert(1)>' })], now);
    expect(tbody.querySelector('img')).toBeNull();
    expect(tbody.querySelector('td')!.textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

describe('loadTracks', () => {
  it('throws on a non-OK status, which fetch itself would not', async () => {
    const notFound = (async () => new Response('nope', { status: 404 })) as unknown as typeof fetch;
    await expect(loadTracks(notFound)).rejects.toThrow('HTTP 404');
  });
});
```

```bash
npx vitest run
```

Notice what jsdom bought you: **`renderRows` is tested against a real DOM, in
milliseconds, with no browser.** That is why the function takes the element as
an argument.

The XSS test is the one to point at in an interview. It proves a security
property, not just behaviour.

**Do now, ten minutes.** Write tests for `parseTrack` rejecting a bad
affiliation, a string altitude, and a confidence above one. Then break
`renderRows` by switching `textContent` to `innerHTML` and watch the XSS test go
red. Put it back.

**Five minutes off.**

---

## Hour 4: Angular

### 3:00 to 3:15 — What Angular is and why

Angular is a **component-based framework** by Google, written in TypeScript.
"Framework" rather than "library" means it is opinionated and brings everything:
components, routing, dependency injection, HTTP, forms, testing.

That opinionatedness is why large organisations and defence programmes choose
it. Every project looks the same and a new engineer can navigate it. **That is
the answer to "why Angular?"**

You have just hand-written `wireControls`. Angular replaces it: you declare
what the view should be for a given state, and the framework updates the DOM.

```bash
npm install -g @angular/cli
ng new track-picture --standalone --style=css
cd track-picture
ng serve            # http://localhost:4200, live reload
```

### 3:15 to 3:45 — The component

```typescript
import { DecimalPipe } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';

import { Affiliation, Track } from './track.model';
import { TrackService } from './track.service';

@Component({
  selector: 'app-track-list',
  standalone: true,
  imports: [DecimalPipe],
  template: `
    <label>
      Show:
      <select (change)="setFilter($event)">
        <option value="all">All</option>
        <option value="hostile">Hostile</option>
      </select>
    </label>

    <p>{{ visible().length }} of {{ tracks().length }} tracks</p>

    @if (visible().length === 0) {
      <p class="empty">No tracks match.</p>
    } @else {
      <table>
        <tbody>
          @for (track of visible(); track track.trackId) {
            <tr [class.hostile]="track.affiliation === 'hostile'">
              <td>{{ track.trackId }}</td>
              <td>{{ track.affiliation }}</td>
              <td>{{ track.altitudeFt | number: '1.0-0' }} ft</td>
            </tr>
          }
        </tbody>
      </table>
    }
  `,
  styles: [`
    .hostile { color: #b3261e; font-weight: 600; }
    .empty { color: #666; font-style: italic; }
  `],
})
export class TrackListComponent {
  private readonly service = inject(TrackService);

  readonly tracks = signal<Track[]>([]);
  readonly filter = signal<'all' | Affiliation>('all');

  readonly visible = computed(() => {
    const f = this.filter();
    return f === 'all' ? this.tracks() : this.tracks().filter((t) => t.affiliation === f);
  });

  load(): void {
    this.service.getTracks().subscribe((tracks) => this.tracks.set(tracks));
  }

  setFilter(event: Event): void {
    const value = (event.target as HTMLSelectElement).value;
    this.filter.set(value as 'all' | Affiliation);
  }
}
```

**Compare that with hour two.** There is no `createElement`, no
`appendChild`, no `replaceChildren`, no `addEventListener`, no `redraw`. You
declared the table and Angular does the DOM work. That is the trade: you learn
a framework's vocabulary and it removes an entire category of bug.

The pieces:

**`@Component`** is a decorator, metadata on the class. Same idea as a Python
decorator.

**The four bindings**, and this table is the core of Angular:

| Syntax | Direction | Meaning |
| --- | --- | --- |
| `{{ value }}` | class to view | Print a value |
| `[property]="expr"` | class to view | Bind a property |
| `(event)="handler()"` | view to class | Listen |
| `[(ngModel)]="field"` | both | Two-way on a form control |

**`@if` / `@for`** is the modern control flow, Angular 17 and later. Legacy code
uses `*ngIf` and `*ngFor`; you must be able to read both because a tech refresh
means meeting both.

**`track track.trackId`** tells Angular how to identify a row across updates so
it reuses the DOM element rather than rebuilding it. On a table refreshing at
1 Hz with hundreds of rows that is the difference between smooth and unusable.
In older syntax it is `trackBy`. Good interview detail.

**Signals.** `signal()` is a value that knows when it changed; `computed()`
derives from others and recalculates only when inputs change. Note you **read**
a signal by calling it: `this.tracks()`.

### 3:45 to 3:55 — Services and dependency injection

Components display. Everything else goes in a service.

```typescript
import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';

import { Track } from './track.model';

@Injectable({ providedIn: 'root' })
export class TrackService {
  private readonly http = inject(HttpClient);

  getTracks(): Observable<Track[]> {
    return this.http.get<Track[]>('/api/v1/tracks').pipe(
      map((tracks) => tracks.filter((t) => t.confidence >= 0.5)),
      catchError(() => of([])),
    );
  }
}
```

**`inject(HttpClient)`** asks Angular's dependency injection system for the HTTP
client; the component never constructs one. The payoff is testability: a test
supplies a fake.

**Observables, not Promises.** A Promise is one future value. An Observable is
a cancellable stream of many over time, which is what a live track feed
actually is. Nothing happens until you `subscribe`.

The one risk to be able to name: **a subscription that is never cleaned up
keeps running after the component is destroyed.** Use `takeUntilDestroyed()`,
the `async` pipe, or unsubscribe in `ngOnDestroy`.

Testing it:

```typescript
await TestBed.configureTestingModule({
  imports: [TrackListComponent],
  providers: [{ provide: TrackService, useValue: fakeTrackService }],
}).compileComponents();

const fixture = TestBed.createComponent(TrackListComponent);
fixture.componentInstance.tracks.set([track(), track({ trackId: 'T-002' })]);
fixture.detectChanges();
expect(fixture.nativeElement.querySelectorAll('tbody tr').length).toBe(2);
```

`useValue` swaps in the fake. `detectChanges()` triggers rendering; forgetting
it is the classic reason an Angular test sees an empty template.

### 3:55 to 4:00 — Self-test

From memory, write:

1. A labelled `<select>` with a matching `id`, and a table with `thead`/`tbody`.
2. The CSS rule that makes everything border-box, and a flex toolbar.
3. A sort comparator that orders by confidence ascending then id.
4. `renderRows` using `textContent` and `replaceChildren`.
5. A `Track` interface and an `Affiliation` union.
6. The four Angular binding syntaxes and what direction each goes.

Anything you cannot write, retype that section tomorrow.

## What you can honestly claim

**Say:** you write HTML with semantic elements and labelled inputs, style with
flexbox and custom properties, write TypeScript with strict mode, validate
untrusted API data rather than casting it, test DOM code with jsdom, and
understand Angular's components, bindings, signals, dependency injection and
testing model.

**Do not say** you have shipped an Angular application. If asked, use the
framing from [lesson 12](frontend.html) section 12: name what you built, then
ask for a ramp on their component structure and conventions.

## If you get another four hours

1. **[Lesson 12](frontend.html)** end to end, especially sections 4, 6 and 8.
2. **`ng new` for real** and rebuild the page as a proper Angular app with a
   service and routing.
3. **The [practice repo](../practice/README.html)**, `practice/frontend`: 32
   tests against a framework-free TypeScript module.
4. **Write a Playwright test** for one journey: load, filter, assert a row
   count.
5. **Rebuild this page from an empty folder**, without looking. That is worth
   more than reading anything.
