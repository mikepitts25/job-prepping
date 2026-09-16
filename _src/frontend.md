# 7. Frontend: Angular, TypeScript, HTML and CSS

This is a **basic qualification** on your requisition, not a nice-to-have. The
posting asks for "frontend framework development experience using Angular,
JavaScript, CSS, and HTML." If you cannot hold a conversation about Angular, you
will not pass the technical screen, however good the rest is.

The lesson assumes you know nothing about web development. It also assumes you
have done [lesson 4](python-sprint.html) or [lesson 5](python.html), so I will
lean on Python comparisons, which shortens the work considerably.

## 1. Why a C2 system has a frontend at all

It is worth grounding this before the syntax.

An air and missile defense command and control system exists to put a picture
in front of a human being who has to make a decision quickly. The operator
console *is* the product from the user's point of view. Everything discussed in
[lesson 2](track-data.html) — correlation, fusion, track quality — exists to
produce something a battle manager can read at a glance.

That makes UI work on this kind of programme different from commercial web work
in ways worth saying out loud:

- **Latency and staleness are safety properties**, not polish. A display
  showing a track that stopped updating ninety seconds ago, with no indication
  that it is stale, is worse than a blank screen.
- **Density beats whitespace.** Operators want many rows visible at once. The
  airy consumer-web aesthetic is wrong here.
- **Colour carries meaning**, and it is standardised. Affiliation, hostile,
  friend, neutral, unknown, has conventional symbology (see MIL-STD-2525 in
  [lesson 2](track-data.html)). You do not get to choose the palette.
- **It must degrade honestly.** When the feed dies, the UI must say so loudly
  rather than quietly showing the last good picture forever.

Say one of those in the interview and you will sound like someone who has
thought about the domain rather than someone who has built a shopping cart.

## 2. How the web works, in five minutes

A **browser** does three things: it fetches documents over HTTP, renders them,
and runs JavaScript.

Three languages, three jobs. This division is the foundation of everything
else:

| Language | Job | Analogy |
| --- | --- | --- |
| **HTML** | Structure and content | The nouns |
| **CSS** | Presentation | The adjectives |
| **JavaScript** | Behaviour | The verbs |

When the browser loads a page it parses the HTML into a tree of objects called
the **DOM**, the Document Object Model. Every element is a node. JavaScript
manipulates that tree, and the browser re-renders when it changes.

**Angular's entire purpose is to stop you manipulating the DOM by hand.** You
describe what the page should look like for a given state; the framework works
out the DOM changes. Hold onto that sentence; it is the answer to "why use a
framework?"

## 3. HTML

HTML is a tree of **elements**, written as tags.

```html
<article class="track-card" id="track-T001">
  <h2>T-001</h2>
  <p>Altitude: <strong>32,000 ft</strong></p>
</article>
```

An opening tag, content, a closing tag. **Attributes** go in the opening tag:
`class` for styling hooks, `id` for a unique identifier.

A minimal document:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Track Picture</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <h1>Air Picture</h1>
    <script src="app.js"></script>
  </body>
</html>
```

`head` holds metadata the user does not see. `body` holds what they do.

### Use semantic elements

There is a real difference between these two:

```html
<div class="header">Air Picture</div>          <!-- means nothing -->
<h1>Air Picture</h1>                           <!-- means "this is the heading" -->
```

Semantic elements (`header`, `nav`, `main`, `section`, `article`, `aside`,
`footer`, `h1` to `h6`, `table`, `button`, `label`) tell the browser, search
engines and **screen readers** what a thing *is*. A `div` with a click handler
is not a button: it cannot be focused with the keyboard, it does not respond to
Enter or Space, and assistive technology does not announce it. Use `<button>`.

That is not pedantry. On a US government programme, **accessibility is a legal
requirement** under Section 508, and an interviewer may well probe it. Knowing
that semantic HTML is the cheapest route to it is a strong answer.

### Tables, which you will use constantly

A track list is a table. Use a real one:

```html
<table>
  <caption>Current air picture</caption>
  <thead>
    <tr><th scope="col">Track</th><th scope="col">Affiliation</th><th scope="col">Altitude</th></tr>
  </thead>
  <tbody>
    <tr><td>T-001</td><td>Hostile</td><td>32,000 ft</td></tr>
  </tbody>
</table>
```

`thead`, `tbody`, `th` with `scope`, and a `caption` are what let a screen
reader announce "Altitude, 32,000 feet" instead of reading a wall of numbers.

### Forms

```html
<label for="min-confidence">Minimum confidence</label>
<input id="min-confidence" type="number" min="0" max="1" step="0.1" value="0.5">

<label for="affiliation">Affiliation</label>
<select id="affiliation">
  <option value="all">All</option>
  <option value="hostile">Hostile</option>
</select>

<button type="submit">Apply</button>
```

The `for` on the label must match the `id` on the input. That pairing is what
makes clicking the label focus the field, and what makes a screen reader
announce the field's purpose. It is the single most commonly skipped detail in
web forms.

## 4. CSS

CSS is a list of rules. Each has a **selector** saying what to style and
**declarations** saying how.

```css
.track-row {
  color: #1d1b18;
  padding: 8px 12px;
  border-bottom: 1px solid #e3ded5;
}
```

Selectors you need:

```css
h1              { }   /* every h1 element */
.hostile        { }   /* every element with class="hostile" */
#track-T001     { }   /* the element with id="track-T001" */
.track-row td   { }   /* td elements inside .track-row (descendant) */
.track-row.stale{ }   /* elements with BOTH classes */
tr:hover        { }   /* state */
tr:nth-child(even) { } /* alternating rows */
```

**Use classes.** IDs are too specific and cannot repeat; element selectors are
too broad.

### The box model

Every element is a box, and this is the thing beginners get wrong:

```
+-------------------------------------+
|              margin                 |   space OUTSIDE, between boxes
|  +-------------------------------+  |
|  |           border              |  |
|  |  +-------------------------+  |  |
|  |  |        padding          |  |  |   space INSIDE, around content
|  |  |  +-------------------+  |  |  |
|  |  |  |     content       |  |  |  |
```

Set this once, globally, and stop fighting it:

```css
*, *::before, *::after { box-sizing: border-box; }
```

Without it, `width: 200px` plus padding gives a box wider than 200px, because
by default width measures the content only. With it, width means the whole box,
which is what everyone intends.

### Layout: flexbox and grid

Two tools cover almost everything. **Flexbox** lays things out in one direction:

```css
.toolbar {
  display: flex;
  gap: 12px;               /* space between children; better than margins */
  align-items: center;     /* vertical alignment (the cross axis) */
  justify-content: space-between;  /* horizontal distribution (the main axis) */
}
```

**Grid** lays things out in two directions:

```css
.dashboard {
  display: grid;
  grid-template-columns: 280px 1fr;   /* fixed sidebar, rest to the content */
  gap: 16px;
}
```

`1fr` means "one fraction of the space left over." Flexbox for a row or column
of things; grid for a page skeleton.

### Specificity, the thing that confuses everyone

When two rules target the same element, which wins? Roughly: inline styles beat
IDs, IDs beat classes, classes beat element selectors, and on a tie the later
rule wins.

```css
p { color: black; }                  /* weakest */
.warning { color: orange; }          /* beats the above */
#alert { color: red; }               /* beats both */
```

**Never use `!important` to win a fight.** It works, it is invisible from the
markup, and the next person has to use `!important` too. Fix the selector
instead. That answer gets you credit.

### Custom properties and themes

```css
:root {
  --colour-hostile: #b3261e;
  --colour-friend: #0b5a8a;
}

.track-row.hostile { color: var(--colour-hostile); }
```

Variables in CSS. Define once, use everywhere, change a theme in one place.

### Responsive design

```css
@media (max-width: 860px) {
  .dashboard { grid-template-columns: 1fr; }   /* stack on a narrow screen */
}
```

A **media query** applies rules conditionally. On an operator console you may
have a fixed display size, but the tooling around it rarely does.

## 5. JavaScript, for someone who knows Python

Skip the introductions; here is the translation table.

| Python | JavaScript |
| --- | --- |
| `x = 5` | `const x = 5;` or `let x = 5;` |
| `None` | `null` and `undefined` (two of them) |
| `True` / `False` | `true` / `false` |
| `def f(a, b=1):` | `function f(a, b = 1) {}` |
| `lambda x: x * 2` | `(x) => x * 2` |
| `[f(x) for x in xs]` | `xs.map(f)` |
| `[x for x in xs if p(x)]` | `xs.filter(p)` |
| `dict` | object `{}` or `Map` |
| `list` | `Array` |
| f-string | template literal with backticks |
| `#` comment | `//` comment |
| indentation | `{ }` braces, and semicolons |

```javascript
const MAX_TRACKS = 500;      // cannot be reassigned. Your default.
let counter = 0;             // reassignable. Use when you must.
// var                       // the old one. Never use it.
```

**Always `const` unless you need to reassign.** Note that `const` on an object
or array stops you reassigning the *name*, not modifying the contents, exactly
like Python's name-binding model from [lesson 5](python.html).

### Arrow functions and array methods

```javascript
const tracks = [
  { id: 'T-001', affiliation: 'hostile', altitude: 32000 },
  { id: 'T-002', affiliation: 'friend',  altitude: 12000 },
];

const ids = tracks.map((t) => t.id);
const hostiles = tracks.filter((t) => t.affiliation === 'hostile');
const total = tracks.reduce((sum, t) => sum + t.altitude, 0);
const highest = tracks.find((t) => t.altitude > 30000);
const anyHostile = tracks.some((t) => t.affiliation === 'hostile');
const allConfident = tracks.every((t) => t.altitude > 0);

const sorted = [...tracks].sort((a, b) => b.altitude - a.altitude);
```

`map`, `filter` and `reduce` replace most loops. Note `[...tracks]` before
`sort`: **`sort` mutates the array in place**, so copy first if the caller still
needs the original. That is a real bug source and a good detail to mention.

The `...` is the **spread** operator: it expands an array or object.

```javascript
const copy = { ...track };                       // shallow copy
const updated = { ...track, affiliation: 'hostile' };   // copy with a change
const combined = [...listA, ...listB];
```

That "copy with a change" idiom is everywhere in modern frontend code, because
state is treated as immutable: you replace it rather than edit it.

### Equality, which has a trap

```javascript
1 == '1'      // true   -- loose equality, converts types. Avoid.
1 === '1'     // false  -- strict equality, no conversion. Use this.
```

**Always use `===` and `!==`.** The loose ones perform type coercion with rules
nobody remembers.

### Destructuring

```javascript
const { id, altitude } = track;              // pull fields into names
const [first, second] = tracks;              // pull array elements
function show({ id, altitude }) { }          // destructure a parameter
```

Python's tuple unpacking, extended to objects.

### Asynchronous code

This is the concept with no direct Python equivalent for a beginner, and it
matters because every data fetch is asynchronous.

JavaScript in the browser is **single-threaded**. If it waited for the network,
the whole page would freeze. So anything slow returns a **Promise**: an object
representing a result that is not here yet.

```javascript
async function loadTracks() {
  try {
    const response = await fetch('/api/v1/tracks');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const tracks = await response.json();
    return tracks;
  } catch (err) {
    console.error('failed to load tracks', err);
    return [];
  }
}
```

`await` means "pause this function until the promise resolves, without blocking
the page." `async` marks a function that contains `await`. If you have met
Python's `async`/`await`, it is the same idea.

**The trap:** `fetch` only rejects on a *network* failure. A 404 or a 500 is a
successful HTTP exchange as far as `fetch` is concerned, so you must check
`response.ok` yourself. People miss this constantly.

## 6. TypeScript

**Angular is written in TypeScript**, and you will write TypeScript, not
JavaScript.

TypeScript is JavaScript plus a type system. You write types; a compiler checks
them and then erases them, producing plain JavaScript. **Nothing is checked at
runtime.**

Why it exists: JavaScript will happily let `track.altitide` (misspelled) be
`undefined`, and you find out when the display shows blank. TypeScript catches
it before the code runs. That is the same argument as `mypy` in
[lesson 6](python-practice.html), and it carries more weight here because the
codebase is bigger and the failure is visible to an operator.

```typescript
let trackId: string = 'T-001';
let altitude: number = 32000;
let isStale: boolean = false;
let tags: string[] = ['air', 'fast'];
let position: [number, number] = [24.45, 54.37];   // tuple: fixed length
```

### Interfaces and type aliases

```typescript
export type Affiliation = 'friend' | 'hostile' | 'neutral' | 'unknown';

export interface Track {
  readonly trackId: string;
  readonly affiliation: Affiliation;
  readonly altitudeFt: number;
  readonly confidence: number;
  readonly lastSeen: string;      // ISO 8601, UTC
}
```

Two things there are worth pointing out.

`Affiliation` is a **union of literal types**: the only legal values are those
four strings. Assigning `'banana'` is a compile error. That is a type system
doing real work, and it is how you model an enumerated field from an interface
control document.

`readonly` means the field cannot be reassigned after construction. Immutable
data is easier to reason about and safer to pass around, the same argument as
frozen dataclasses in Python.

### Optional fields, null safety and `unknown`

```typescript
interface Filter {
  affiliation?: Affiliation;    // may be absent
  minConfidence?: number;
}

function describe(track: Track | null): string {
  if (track === null) return 'no track';
  return track.trackId;         // safe: the compiler knows it is not null here
}
```

With `strictNullChecks` on, which it should be, the compiler forces you to
handle the null case. That eliminates a whole category of "cannot read property
of undefined" runtime errors.

**`any` versus `unknown`** is the most important distinction in practical
TypeScript:

```typescript
const a: any = JSON.parse(text);
a.whatever.nonsense;          // compiles. Type checking is OFF.

const u: unknown = JSON.parse(text);
u.trackId;                    // compile error: prove what it is first
```

**`any` switches the type system off** for that value and lets bad data through
silently. `unknown` forces you to validate. On a system fed by external
interfaces, data arriving from the wire should be `unknown` and pass through a
validating parser. Saying that in an interview shows you understand what the
type system is for, rather than treating it as decoration.

### Generics, enough to read them

```typescript
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const t = first<Track>(tracks);    // t is Track | undefined
```

`T` is a placeholder for whatever type the caller uses. You will read far more
generics than you write; this level is enough.

## 7. Angular

### What it is and why

Angular is a **component-based framework** for building applications in the
browser, made by Google, written in TypeScript. "Framework" rather than
"library" means it is opinionated and provides the whole structure: components,
routing, dependency injection, HTTP, forms and testing, all in the box. React
is a library and you assemble the rest yourself.

That opinionatedness is precisely why large organisations, and defence
programmes in particular, pick Angular. Every project looks the same, the
conventions are enforced, and a new engineer can find their way around. Say
that if asked "why Angular?"

### Components

A component is the unit: a piece of UI with its own template, styling and
logic.

```typescript
import { Component, computed, inject, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';

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

That compiles under Angular 18 with `strict` on. Take it apart.

**`@Component`** is a **decorator**: metadata attached to the class telling
Angular how to use it. Same concept as a Python decorator.

**`selector`** is the custom HTML tag that places this component:
`<app-track-list></app-track-list>`.

**`standalone: true`** means the component declares its own dependencies in
`imports`, rather than being registered in an `NgModule`. Standalone is the
modern default. Older Angular code uses NgModules everywhere, and on a tech
refresh you will meet both.

**`template`** is the HTML. Inline in backticks here; larger components use
`templateUrl: './track-list.component.html'`.

### The four bindings

This table is the core of Angular and worth memorising:

| Syntax | Direction | Meaning |
| --- | --- | --- |
| `{{ value }}` | class to view | Interpolation: print a value |
| `[property]="expr"` | class to view | Bind a property or attribute |
| `(event)="handler()"` | view to class | Listen for an event |
| `[(ngModel)]="field"` | both | Two-way binding on a form control |

```html
{{ track.trackId }}                                 <!-- print it -->
<tr [class.hostile]="track.affiliation === 'hostile'">  <!-- conditional class -->
<img [src]="track.iconUrl">                          <!-- dynamic attribute -->
<button (click)="refresh()">Refresh</button>         <!-- event -->
<input [(ngModel)]="searchTerm">                     <!-- two-way -->
```

The "banana in a box" `[(...)]` is just `[...]` and `(...)` combined.

### Control flow in templates

```html
@if (loading()) {
  <p>Loading…</p>
} @else if (error()) {
  <p class="error">{{ error() }}</p>
} @else {
  @for (track of tracks(); track track.trackId) {
    <app-track-row [track]="track" />
  } @empty {
    <p>No tracks.</p>
  }
}
```

That `@if` / `@for` syntax arrived in Angular 17. Older code uses structural
directives, and you must be able to read them because that is what is in a
legacy baseline:

```html
<p *ngIf="loading">Loading…</p>
<tr *ngFor="let track of tracks; trackBy: trackById">
```

**`track` / `trackBy` matters for performance.** It tells Angular how to
identify a row across updates so it can reuse the DOM element instead of
destroying and rebuilding it. On a table refreshing at 1 Hz with hundreds of
rows, that is the difference between smooth and unusable. Good interview
detail.

### Signals

```typescript
readonly tracks = signal<Track[]>([]);          // a reactive value
readonly visible = computed(() => ...);         // derived, recalculates automatically

this.tracks.set(newList);                       // replace
this.tracks.update((list) => [...list, extra]); // derive from current
this.tracks();                                  // READ it: note the parentheses
```

A **signal** is a value that knows when it changes, so Angular can update
exactly the parts of the view that depend on it. `computed` derives a new signal
from others and recalculates only when its inputs change.

Signals arrived in Angular 16 and are the current direction. Older code relies
on **zone.js** change detection, which checks everything after every event.
Knowing both exist, and that signals are more precise, is enough depth.

### Services and dependency injection

Components should display things. Anything else — fetching, caching, business
logic — belongs in a **service**.

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

**`@Injectable({ providedIn: 'root' })`** registers the service application-wide
as a single shared instance.

**`inject(HttpClient)`** asks Angular's **dependency injection** system for the
HTTP client. The component never constructs its own. That is the same
dependency injection argument as [lesson 11](ood.html): it makes the thing
testable, because a test supplies a fake instead.

### Observables, and how they differ from Promises

`HttpClient` returns an **Observable** from a library called RxJS, not a
Promise.

- A **Promise** is one future value. It happens once.
- An **Observable** is a stream of values over time. It can emit many, and it
  can be cancelled.

For a single HTTP call the difference barely matters. For a websocket of track
updates, which is exactly what a live air picture needs, it matters a lot.

```typescript
this.service.getTracks().subscribe((tracks) => this.tracks.set(tracks));
```

Nothing happens until you `subscribe`. Observables are lazy.

The operators you will actually meet, inside `.pipe(...)`:

| Operator | Does |
| --- | --- |
| `map` | Transform each emitted value |
| `filter` | Drop values that fail a test |
| `catchError` | Handle a failure, usually returning a fallback |
| `switchMap` | Swap to a new stream, cancelling the previous one |
| `debounceTime` | Wait for a pause; the classic search-box fix |
| `takeUntil` | Complete the stream on a signal; used for cleanup |

`debounceTime(300)` then `switchMap` is *the* pattern for a search box: wait for
the user to stop typing, then cancel any in-flight request when a new one
starts.

**Memory leaks:** a subscription that is never cleaned up keeps running after
the component is destroyed. Modern Angular uses `takeUntilDestroyed()`, or the
`async` pipe in the template which subscribes and unsubscribes for you. Being
able to name that risk is a senior signal.

### Lifecycle hooks

```typescript
export class TrackListComponent implements OnInit, OnDestroy {
  ngOnInit(): void { /* after the component is created: start loading */ }
  ngOnDestroy(): void { /* before it is destroyed: clean up */ }
}
```

`ngOnInit` and `ngOnDestroy` are the two that matter. Do not fetch data in the
constructor; the constructor is for dependency injection, `ngOnInit` is for
initialisation.

### Routing, briefly

```typescript
export const routes: Routes = [
  { path: '', component: TrackListComponent },
  { path: 'tracks/:id', component: TrackDetailComponent },
  { path: '**', component: NotFoundComponent },
];
```

The router swaps components in and out based on the URL without a page reload.
`:id` is a parameter, `**` is the catch-all. Enough for now.

### The CLI

```bash
npm install -g @angular/cli
ng new track-picture            # scaffold a project
ng serve                        # dev server with live reload
ng generate component track-list
ng generate service track
ng build --configuration production
ng test                         # unit tests
ng lint
```

`ng generate` creating the files, the test file and the registration in one
command is a large part of why teams standardise on Angular.

## 8. Testing the frontend

The posting lists **UI/UX test frameworks (Cypress, Selenium, Playwright,
Jest)** under desired skills. Know what each is for.

| Tool | Layer | What it does |
| --- | --- | --- |
| **Jest** / **Vitest** / **Karma+Jasmine** | Unit | Runs functions and components in isolation, no browser |
| **Angular TestBed** | Unit / component | Builds a component with fake dependencies |
| **Cypress** | End to end | Drives a real browser; excellent debugging, runs in-browser |
| **Playwright** | End to end | Drives real Chromium, Firefox and WebKit; fast, parallel, good CI story |
| **Selenium** | End to end | The long-established one; WebDriver standard, every language |

The pyramid from [lesson 14](testing-ci.html) applies unchanged: **many unit
tests, some component tests, few end-to-end tests.** End-to-end tests are slow
and brittle, so use them for a handful of critical journeys, not for coverage.

### Unit-testing the logic

The most valuable structural advice in frontend work:

> **Push logic out of components into plain functions and services.**

A component is hard to test because it needs a rendering environment. A plain
function is trivial to test. So filtering, sorting, formatting and validation
should live outside the component, and the component becomes a thin shell.

```typescript
import { describe, expect, it } from 'vitest';
import { filterTracks, sortForDisplay } from './tracks';

describe('sortForDisplay', () => {
  it('puts hostile first and friend last', () => {
    const sorted = sortForDisplay([
      track({ affiliation: 'friend' }),
      track({ affiliation: 'hostile' }),
    ]);
    expect(sorted.map((t) => t.affiliation)).toEqual(['hostile', 'friend']);
  });

  it('breaks ties by track id, so the order is stable', () => {
    const sorted = sortForDisplay([track({ trackId: 'T-B' }), track({ trackId: 'T-A' })]);
    expect(sorted.map((t) => t.trackId)).toEqual(['T-A', 'T-B']);
  });
});
```

There is a full working version of this, 32 passing tests, in the
[practice repo](../practice/README.html) under `practice/frontend`.

### Component testing with TestBed

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('TrackListComponent', () => {
  let fixture: ComponentFixture<TrackListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrackListComponent],
      providers: [{ provide: TrackService, useValue: fakeTrackService }],
    }).compileComponents();

    fixture = TestBed.createComponent(TrackListComponent);
  });

  it('shows a row per track', () => {
    fixture.componentInstance.tracks.set([track(), track({ trackId: 'T-002' })]);
    fixture.detectChanges();

    const rows = fixture.nativeElement.querySelectorAll('tbody tr');
    expect(rows.length).toBe(2);
  });
});
```

Note `useValue: fakeTrackService`: the real service is replaced with a fake, so
no HTTP happens. `fixture.detectChanges()` triggers rendering; forgetting it is
the classic reason an Angular test sees an empty template.

### End-to-end testing

```typescript
// Playwright
import { expect, test } from '@playwright/test';

test('filtering to hostile hides friendly tracks', async ({ page }) => {
  await page.goto('/');
  await page.getByLabel('Show').selectOption('hostile');
  await expect(page.getByRole('row')).toHaveCount(3);
  await expect(page.getByText('T-002')).toBeHidden();
});
```

Two practices worth stating:

**Select by role and accessible name**, as above, not by CSS class. Class-based
selectors break on every restyle; role-based ones express what the user sees,
and they double as an accessibility check.

**End-to-end tests are where flakiness breeds.** Never wait with a fixed sleep;
wait for a condition. The guidance in [lesson 14](testing-ci.html) about flaky
tests applies with double force here.

## 9. Design tools

The posting names **MockFlow, UXPin and Axure** under desired skills. These are
wireframing and prototyping tools: you mock up a screen and click through it
before anyone writes code. Figma is the common commercial equivalent.

You are not expected to be a designer. What is expected is that you can work
from a wireframe, and that you understand why one exists: **agreeing a screen
with the customer on a mock-up costs hours, and discovering the disagreement
after it is built costs weeks.** On an FMS programme where the customer
reviews capability formally, that is not a small saving. If asked, say that,
and say you are comfortable building from a prototype and feeding problems back.

## 10. Practice

Do these in order. The [practice repo](../practice/README.html) has a
TypeScript module with 32 passing tests you can work against.

**F1.** Write a static HTML page with a semantic heading, a table of five
tracks with a caption and proper `thead`/`th scope`, and a labelled filter
input. No CSS, no JavaScript. Check every input has a matching label.

**F2.** Style it: `box-sizing: border-box` globally, a flexbox toolbar, colour
hostile rows, alternate row shading, and a media query that stacks the layout
under 860 pixels.

**F3.** In plain JavaScript, fetch a JSON list, handle both a network failure
and a non-OK status, and render the rows into the table.

**F4.** Convert it to TypeScript. Define a `Track` interface and an
`Affiliation` union. Turn on `strict`. Parse the payload from `unknown` with a
validating function rather than casting with `as`.

**F5.** Write unit tests for the filtering and sorting logic, including the
empty case and the tie-break.

**F6.** Scaffold an Angular app with `ng new`, create a `TrackService` and a
`TrackListComponent`, and wire them with dependency injection and signals.

**F7.** Write a TestBed test that supplies a fake service and asserts the right
number of rows renders.

F4 and F5 are the highest value if you are short of time: they are what the
interview will probe.

## 11. Questions to be ready for

1. **What is the DOM?** The browser's object tree representing the page.
   JavaScript changes it, the browser re-renders.
2. **Why a framework rather than plain JavaScript?** You describe the desired
   state and the framework computes the DOM changes, instead of you hand-writing
   imperative updates that drift out of sync.
3. **Component versus service?** Components display; services hold data access
   and logic. It keeps components thin and the logic testable.
4. **What is dependency injection and what does it buy?** Angular supplies
   dependencies rather than the class constructing them, so a test can supply a
   fake. Testability first, decoupling second.
5. **Observable versus Promise?** One future value versus a cancellable stream
   of many. HTTP returns an Observable; nothing runs until you subscribe.
6. **`any` versus `unknown`?** `any` disables checking; `unknown` forces you to
   prove the type. External data should be `unknown`.
7. **What does `trackBy` do?** Identifies list items across renders so Angular
   reuses DOM nodes instead of rebuilding them. A performance fix for large
   lists.
8. **How do you avoid a memory leak in a component?** Unsubscribe on destroy,
   via `takeUntilDestroyed`, the `async` pipe, or `ngOnDestroy`.
9. **How do you test a component that calls an API?** Replace the service with a
   fake through the testing module. Never hit the network in a unit test.
10. **Unit versus end-to-end, and how many of each?** Many unit, few end to end.
    End-to-end tests are slow and flaky, so reserve them for critical journeys.
11. **How do you make a UI accessible?** Semantic elements, labels tied to
    inputs, keyboard operability, sufficient colour contrast, and never colour
    as the only signal. On a government programme this is a legal requirement.
12. **What is specificity?** The rule deciding which CSS wins. Do not resolve
    conflicts with `!important`.

## 12. Being honest about your level

If Angular is new to you, do not pretend otherwise. The framing that works:

> "I have not shipped an Angular application. I have built [what you actually
> did from the practice section], so I am comfortable with components,
> services, dependency injection and signals, and I understand the testing
> story. What I would want is a ramp on the existing component structure and
> your conventions before I touch operator-facing screens."

Then be ready to discuss what you built. A candidate who has genuinely written
a typed, tested track list and says so plainly is in much better shape than one
who claims three years of Angular and cannot explain what `trackBy` does.
