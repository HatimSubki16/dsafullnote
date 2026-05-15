# Static Interactive Note Page Pattern

Source analyzed: `C:\clone Repo\dsafullnote\index.html`

## Core Idea

Build a full study-note experience as one standalone `index.html` file:

- HTML for content and structure
- CSS in a single `<style>` block
- JavaScript in a single `<script>` block
- Optional CDN assets for fonts and syntax highlighting
- No bundler, framework, backend, or build step required

This pattern is good for exam notes, programming notes, course guides, cheat sheets, and self-contained learning dashboards.

## Page Architecture

Use this structure:

```html
<nav id="sidebar">...</nav>
<div id="main">
  <div class="topbar">...</div>
  <div class="content">
    <div class="checklist-card">...</div>
    <div class="chapter" id="ch1">...</div>
    <div class="chapter" id="ch2">...</div>
  </div>
</div>
<button id="mobile-toggle">...</button>
```

Important layout rules:

- Fixed left sidebar for navigation.
- Sticky topbar with title and search.
- Main content offset by `--sidebar-w`.
- Responsive breakpoint around `768px`: sidebar slides offscreen and opens with a floating mobile button.
- `html { scroll-behavior: smooth; scroll-padding-top: 80px; }` for pleasant anchor navigation.

## Styling System

Start with CSS custom properties:

```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #1e2530;
  --border: #2a3040;
  --accent: #00e5c5;
  --accent2: #f9a825;
  --accent3: #f06292;
  --text: #e6edf3;
  --muted: #7a8899;
  --sidebar-w: 260px;
}
```

Reusable UI classes:

- `.chapter`, `.chapter-header`, `.chapter-num`, `.chapter-title`
- `.section`, `.section-title`
- `.card`, `.card-accent`, `.card-warning`, `.card-danger`
- `.exam-badge`
- `.tbl`
- `.badge`, `.badge-green`, `.badge-yellow`, `.badge-red`, `.badge-blue`
- `.code-wrapper`, `.copy-btn`
- `.collapsible-btn`, `.collapsible-body`
- `.visualizer`, `.viz-title`, `.viz-input-row`, `.viz-input`, `.viz-panel`
- `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-sm`

## Content Pattern

Each topic should be written as a chapter with sections:

```html
<div class="chapter" id="ch1">
  <div class="chapter-header">
    <span class="chapter-num">CH 01</span>
    <span class="chapter-title">Topic Name</span>
  </div>

  <div class="section" id="important-section">
    <div class="section-title">
      <span class="exam-badge">EXAM</span>
      Key Concept
    </div>
    <div class="card card-accent">
      ...
    </div>
  </div>
</div>
```

For notes, mix:

- Short explanations in cards.
- Comparison tables for memorization.
- Code blocks for implementations.
- Collapsible sections for long code or secondary details.
- Mnemonics and badges for exam-critical points.
- Interactive visualizers for algorithms or workflows.

## JavaScript Interaction Pattern

Keep the JS modular by feature, even inside one file.

### Checklist

- Store checklist topics in an array of objects.
- Generate checklist DOM dynamically.
- Save completion state with `localStorage`.
- Update a progress bar and text counter.

Pattern:

```js
const checkItems = [{ id: "topic", label: "Topic Name" }];
localStorage.setItem("note_check_" + item.id, "1");
```

Use a page-specific storage prefix, for example `dsa_check_`, `math_check_`, or `os_check_`.

### Navigation

- Sidebar links call `scrollTo("chapter-id")`.
- Scroll listener checks which chapter is currently near the top.
- Matching `.nav-link` receives `.active`.
- On mobile, close the sidebar after clicking a link.

### Search

- Topbar search reads `.chapter.innerText`.
- Hide chapters whose text does not include the query.
- Simple and effective for static notes.

### Collapsible Blocks

Use adjacent button/body markup:

```html
<button class="collapsible-btn" onclick="toggleCollapse(this)">Title</button>
<div class="collapsible-body">Hidden content</div>
```

JS toggles `.open` on both elements.

### Copy Code

Each code block gets:

```html
<div class="code-wrapper">
  <button class="copy-btn" onclick="copyCode(this)">copy</button>
  <pre><code class="language-cpp">...</code></pre>
</div>
```

JS uses `navigator.clipboard.writeText(...)`, then briefly changes the button label to `copied!`.

### Visualizers

Each interactive demo has:

- A `.visualizer` wrapper.
- Inputs with stable IDs.
- Buttons using small feature functions.
- A dedicated output area.
- Feature-local state variables.

Examples from the analyzed page:

- Big-O chart using `<canvas>`.
- Bracket checker using stack simulation and a generated table.
- Infix-to-postfix stepper using stack/output panels.
- Linked-list reversal animation using timed DOM updates.
- Tree traversal using inline SVG.
- Insertion sort bars using dynamic div heights.
- Binary search using highlighted array cells.

## External Assets

The page uses:

- Google Fonts: `Space Mono`, `Syne`, `DM Sans`
- Prism CSS/JS from CDN
- Prism C++ component for syntax highlighting

This keeps the file static but still polished.

## Important Implementation Notes

- IDs in sidebar links, chapter containers, section anchors, and JS arrays must stay synchronized.
- Prefer data arrays for repeated interactive UI, like checklists and visualizer steps.
- Use CSS variables heavily so the design can be rethemed quickly.
- For code-heavy notes, Prism plus copy buttons is a high-value pattern.
- Keep visualizer functions independent so each can be copied into another note page.
- Use responsive grids with `auto-fill` and `minmax(...)` for checklist/cards.
- The analyzed file appears to show mojibake for some symbols in this terminal view. When editing, keep the file saved as UTF-8 and verify special characters render correctly in the browser.

## Reusable Build Recipe

1. Define the theme in `:root`.
2. Create fixed sidebar navigation and sticky topbar search.
3. Add a generated progress checklist with `localStorage`.
4. Write notes as `.chapter` and `.section` blocks.
5. Use cards, badges, tables, and collapsibles to make dense notes readable.
6. Wrap code in `.code-wrapper` with a copy button and Prism language class.
7. Add interactive demos only where they improve understanding.
8. Give each demo its own state, inputs, render function, and reset/start controls.
9. Add mobile sidebar behavior.
10. Test by opening the file directly in a browser.

