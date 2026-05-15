from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "DSA_Study_Notes_From_Slides.md"
SITE = ROOT / "dsa-github-page"
DOCS = ROOT / "docs"
ASSETS = SITE / "assets"


def slugify(text: str, used: set[str]) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    base = base or "section"
    slug = base
    count = 2
    while slug in used:
        slug = f"{base}-{count}"
        count += 1
    used.add(slug)
    return slug


def inline_markup(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def classify_topic(title: str, chapter: str) -> str:
    text = f"{title} {chapter}".lower()
    critical = [
        r"\balgorithm\b",
        r"\binsertion\b",
        r"\bdeletion\b",
        r"\breversal\b",
        r"\binfix\b",
        r"\bpostfix\b",
        r"\bdijkstra\b",
        r"\bkruskal\b",
        r"\bsort(?:ing)?\b",
        r"\bsearch(?:ing)?\b",
        r"\bhash(?:ing)?\b",
        r"\bbalanced\b",
        r"\bbst\b",
    ]
    important = [
        r"\bcomplexity\b",
        r"\bbig o\b",
        r"\btraversal\b",
        r"\blinked list\b",
        r"\bstack\b",
        r"\bqueue\b",
        r"\btree\b",
        r"\bgraph\b",
        r"\bvector\b",
        r"\bstl\b",
        r"\badt\b",
    ]
    if any(re.search(pattern, text) for pattern in critical):
        return "critical"
    if any(re.search(pattern, text) for pattern in important):
        return "important"
    return "basic"


def is_table_separator(line: str) -> bool:
    return re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line) is not None


def is_table_start(lines: list[str], idx: int) -> bool:
    return idx + 1 < len(lines) and lines[idx].strip().startswith("|") and is_table_separator(lines[idx + 1])


def parse_table(lines: list[str], idx: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    while idx < len(lines) and lines[idx].strip().startswith("|"):
        if not is_table_separator(lines[idx]):
            raw = lines[idx].strip().strip("|")
            rows.append([cell.strip() for cell in raw.split("|")])
        idx += 1

    if not rows:
        return "", idx

    head = rows[0]
    body = rows[1:]
    out = ['<div class="table-wrap"><table>']
    out.append("<thead><tr>")
    for cell in head:
        out.append(f"<th>{inline_markup(cell)}</th>")
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{inline_markup(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out), idx


def close_lists(stack: list[int], target_level: int, output: list[str]) -> None:
    while stack and stack[-1] >= target_level:
        output.append("</ul>")
        stack.pop()


def parse_markdown(markdown: str) -> tuple[str, list[dict[str, str]], list[dict[str, str]], int]:
    lines = markdown.splitlines()
    output: list[str] = []
    chapters: list[dict[str, str]] = []
    subtopics: list[dict[str, str]] = []
    used: set[str] = set()
    current_chapter = ""
    current_chapter_title = ""
    current_article_open = False
    current_chapter_open = False
    source_note_open = False
    list_stack: list[int] = []
    paragraph: list[str] = []
    in_code = False
    code_lang = "text"
    code_lines: list[str] = []
    code_count = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            close_lists(list_stack, 0, output)
            output.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_code() -> None:
        nonlocal code_count
        if not code_lines:
            return
        code_count += 1
        code = html.escape("\n".join(code_lines).rstrip())
        output.append(
            '<div class="code-shell">'
            f'<div class="code-bar"><span>{html.escape(code_lang)}</span>'
            '<button class="copy-code" type="button">Copy</button></div>'
            f'<pre><code>{code}</code></pre></div>'
        )
        code_lines.clear()

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists(list_stack, 0, output)
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
                code_lang = stripped.strip("`").strip() or "text"
            idx += 1
            continue

        if in_code:
            code_lines.append(line)
            idx += 1
            continue

        if is_table_start(lines, idx):
            flush_paragraph()
            close_lists(list_stack, 0, output)
            table_html, idx = parse_table(lines, idx)
            output.append(table_html)
            continue

        if not stripped:
            flush_paragraph()
            close_lists(list_stack, 0, output)
            idx += 1
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            close_lists(list_stack, 0, output)
            if source_note_open:
                output.append("</section>")
            output.append(f'<section class="source-note"><h2>{inline_markup(stripped[2:].strip())}</h2>')
            source_note_open = True
            idx += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_lists(list_stack, 0, output)
            if source_note_open:
                output.append("</section>")
                source_note_open = False
            if current_article_open:
                output.append("</article>")
                current_article_open = False
            if current_chapter_open:
                output.append("</section>")
            title = stripped[3:].strip()
            chapter_id = slugify(title, used)
            current_chapter = chapter_id
            current_chapter_title = title
            chapters.append({"id": chapter_id, "title": title})
            output.append(
                f'<section class="chapter-section" id="{chapter_id}" data-title="{html.escape(title)}">'
                f'<h2>{inline_markup(title)}</h2>'
            )
            current_chapter_open = True
            idx += 1
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            close_lists(list_stack, 0, output)
            if current_article_open:
                output.append("</article>")
            title = stripped[4:].strip()
            sub_id = slugify(f"{current_chapter_title}-{title}", used)
            level = classify_topic(title, current_chapter_title)
            subtopics.append(
                {
                    "id": sub_id,
                    "title": title,
                    "chapter": current_chapter,
                    "chapterTitle": current_chapter_title,
                    "level": level,
                }
            )
            output.append(
                f'<article class="subtopic-card" id="{sub_id}" data-chapter="{current_chapter}" '
                f'data-level="{level}" data-title="{html.escape(title)}">'
                f'<div class="card-heading"><h3>{inline_markup(title)}</h3><span class="level-badge {level}">{level.upper()}</span></div>'
            )
            current_article_open = True
            idx += 1
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            close_lists(list_stack, 0, output)
            output.append(f"<h4>{inline_markup(stripped[5:].strip())}</h4>")
            idx += 1
            continue

        bullet = re.match(r"^(\s*)-\s+(.*)$", line)
        if bullet:
            flush_paragraph()
            level = len(bullet.group(1)) // 2
            while list_stack and list_stack[-1] > level:
                output.append("</ul>")
                list_stack.pop()
            while not list_stack or list_stack[-1] < level:
                output.append('<ul class="note-list">')
                list_stack.append(level)
            output.append(f"<li>{inline_markup(bullet.group(2))}</li>")
            idx += 1
            continue

        numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
        if numbered:
            flush_paragraph()
            close_lists(list_stack, 0, output)
            output.append(f'<p class="numbered-step">{inline_markup(stripped)}</p>')
            idx += 1
            continue

        paragraph.append(stripped)
        idx += 1

    flush_paragraph()
    close_lists(list_stack, 0, output)
    if current_article_open:
        output.append("</article>")
    if current_chapter_open:
        output.append("</section>")
    if source_note_open:
        output.append("</section>")

    return "\n".join(output), chapters, subtopics, code_count


def make_visual_asset() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / "dsa-circuit.png"
    img = Image.new("RGB", (1280, 520), "#050a12")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("consolab.ttf", 36)
        label_font = ImageFont.truetype("consola.ttf", 22)
        small_font = ImageFont.truetype("consola.ttf", 15)
    except OSError:
        title_font = label_font = small_font = ImageFont.load_default()

    cyan = "#00d9ff"
    green = "#20e3a2"
    red = "#ff5f78"
    amber = "#ffb84d"
    grid = "#07364a"

    for x in range(0, 1281, 120):
        draw.line((x, 0, x, 520), fill=grid, width=1)
    for y in range(0, 521, 88):
        draw.line((0, y, 1280, y), fill=grid, width=1)

    points = [(90, 390), (255, 295), (445, 315), (640, 238), (805, 110), (1040, 145), (1190, 245)]
    draw.line(points, fill="#7c3f30", width=5)
    for x, y in points[2:]:
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), outline="#b4624a", width=4)

    blocks = [
        (92, 142, "ADT", cyan),
        (240, 210, "STL", green),
        (390, 152, "LIST", red),
        (548, 250, "STACK", amber),
        (742, 182, "TREE", cyan),
        (930, 282, "GRAPH", green),
    ]
    for x, y, label, color in blocks:
        draw.rounded_rectangle((x, y, x + 118, y + 54), radius=8, fill="#0e1728", outline=color, width=2)
        draw.text((x + 18, y + 16), label, fill=color, font=label_font)
        draw.line((x + 118, y + 27, x + 165, y + 27), fill=color, width=2)
        draw.ellipse((x + 160, y + 22, x + 170, y + 32), fill=color)

    draw.text((86, 54), "CSEB3213 // DSA FOCUS MAP", fill=cyan, font=title_font)
    draw.text((90, 96), "clickable notes | algorithms | code drills | exam checklist", fill="#8fb6c8", font=small_font)
    img.save(path, optimize=True)


def write_site(content_html: str, chapters: list[dict[str, str]], subtopics: list[dict[str, str]], code_count: int) -> None:
    SITE.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)

    chapter_links = "\n".join(
        f'<a href="#{chapter["id"]}" data-chapter-link="{chapter["id"]}"><span></span>{html.escape(chapter["title"])}</a>'
        for chapter in chapters
    )
    chapter_buttons = "\n".join(
        f'<button type="button" class="chapter-tab" data-chapter="{chapter["id"]}">{html.escape(chapter["title"].replace("Chapter ", "Ch. "))}</button>'
        for chapter in chapters
    )
    subtopic_buttons = "\n".join(
        f'<button type="button" class="subtopic-chip {sub["level"]}" data-target="{sub["id"]}" '
        f'data-chapter="{sub["chapter"]}" data-level="{sub["level"]}">'
        f'<span>{html.escape(sub["title"])}</span><small>{html.escape(sub["chapterTitle"].replace("Chapter ", "Ch. "))}</small></button>'
        for sub in subtopics
    )
    checklist_items = "\n".join(
        f'<label class="check-row" data-level="{sub["level"]}" data-chapter="{sub["chapter"]}">'
        f'<input type="checkbox" data-check-id="{sub["id"]}"><span>{html.escape(sub["title"])}</span>'
        f'<small>{sub["level"].upper()}</small></label>'
        for sub in subtopics
    )

    index = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Digital DSA interactive study dashboard generated from the lecture slides.">
  <title>CSEB3213 DSA Study Dashboard</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <strong>CSEB3213</strong>
        <span>Data Structures & Algorithms</span>
      </div>
      <label class="sidebar-search">
        <span>Search topics</span>
        <input id="sideSearch" type="search" placeholder="linked list, stack, tree...">
      </label>
      <nav class="sidebar-nav" aria-label="Study navigation">
        <p>Overview</p>
        <a href="#dashboard" class="active"><i class="dot green"></i>Dashboard</a>
        <a href="#study-checklist"><i class="dot cyan"></i>Study Checklist</a>
        <a href="#topic-command"><i class="dot rose"></i>Topic Navigator</a>
        <p>Study Notes</p>
        {chapter_links}
      </nav>
    </aside>

    <div class="main-panel">
      <header class="topbar">
        <div class="filter-row" aria-label="Topic filters">
          <span>Filter:</span>
          <button type="button" class="filter-pill active" data-filter="all">All Topics</button>
          <button type="button" class="filter-pill" data-filter="critical">Very Critical</button>
          <button type="button" class="filter-pill" data-filter="important">Important</button>
          <button type="button" class="filter-pill" data-filter="basic">Basic</button>
          <button type="button" class="filter-pill" id="expandAll">Expand All</button>
        </div>
        <button type="button" class="print-button" id="printButton">Print / PDF</button>
      </header>

      <main>
        <section class="hero" id="dashboard">
          <img src="assets/dsa-circuit.png" alt="Digital DSA circuit map.">
          <div class="hero-copy">
            <p class="terminal-kicker">interactive.focus.notes</p>
            <h1>Data Structures<br>and Algorithms</h1>
            <p>Digital study dashboard rebuilt from your uploaded lecture notes. Use the sidebar, search, filters, progress checklist, and clickable topics to revise faster.</p>
            <div class="stats-grid">
              <div><strong>{len(chapters)}</strong><span>sections</span></div>
              <div><strong>{len(subtopics)}</strong><span>topics</span></div>
              <div><strong>{code_count}</strong><span>code blocks</span></div>
              <div><strong>PDF</strong><span>ready</span></div>
            </div>
          </div>
        </section>

        <section class="panel-card progress-card" id="study-checklist">
          <div class="panel-title">
            <div>
              <span class="square-check">✓</span>
              <h2>Study Progress Checklist</h2>
            </div>
            <strong id="progressLabel">0%</strong>
          </div>
          <div class="progress-track"><span id="progressBar"></span></div>
          <div class="checklist" id="checklist">
            {checklist_items}
          </div>
        </section>

        <section class="panel-card topic-command" id="topic-command">
          <div class="panel-title">
            <div>
              <span class="square-check">⌘</span>
              <h2>Click a Covered Subtopic</h2>
            </div>
            <button type="button" class="ghost-button" id="resetFilters">Reset</button>
          </div>
          <div class="command-search">
            <input id="topicSearch" type="search" placeholder="Search all 116 subtopics...">
          </div>
          <div class="chapter-tabs" id="chapterTabs">
            {chapter_buttons}
          </div>
          <div class="subtopic-grid" id="subtopicGrid">
            {subtopic_buttons}
          </div>
        </section>

        <section class="notes-content" id="notesContent">
          {content_html}
        </section>
      </main>
    </div>
  </div>

  <button type="button" class="top-button" id="topButton">Top</button>
  <script src="script.js"></script>
</body>
</html>
"""

    (SITE / "index.html").write_text(index, encoding="utf-8")
    (SITE / "styles.css").write_text(CSS, encoding="utf-8")
    (SITE / "script.js").write_text(JS, encoding="utf-8")
    (SITE / "README.md").write_text(README, encoding="utf-8")


CSS = r"""
:root {
  --bg: #050912;
  --panel: #0e1728;
  --panel-2: #111d31;
  --line: #213550;
  --grid: #07364a;
  --text: #eef7ff;
  --muted: #91a4ba;
  --cyan: #00d9ff;
  --green: #20e3a2;
  --rose: #ff5f78;
  --amber: #ffb84d;
  --purple: #7c5cff;
  --shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
  --sidebar: 292px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background:
    radial-gradient(circle at 82% 12%, rgba(0, 217, 255, 0.12), transparent 28%),
    radial-gradient(circle at 32% 80%, rgba(124, 92, 255, 0.14), transparent 24%),
    var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}

button, input { font: inherit; }

.app-shell {
  display: grid;
  grid-template-columns: var(--sidebar) minmax(0, 1fr);
  min-height: 100vh;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid var(--line);
  background: #0c1322;
  padding: 22px 16px;
}

.brand strong {
  display: block;
  color: var(--cyan);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 15px;
  letter-spacing: 1.5px;
}

.brand span {
  display: block;
  margin-top: 5px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
}

.sidebar-search {
  display: grid;
  gap: 7px;
  margin: 22px 0 26px;
}

.sidebar-search span {
  color: var(--muted);
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
}

input {
  width: 100%;
  min-height: 40px;
  border: 1px solid #25405f;
  border-radius: 6px;
  outline: none;
  background: #111c2f;
  color: var(--text);
  padding: 9px 12px;
}

input:focus {
  border-color: var(--cyan);
  box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.14);
}

.sidebar-nav {
  display: grid;
  gap: 2px;
}

.sidebar-nav p {
  margin: 18px 0 8px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.sidebar-nav a {
  display: grid;
  grid-template-columns: 12px minmax(0, 1fr);
  gap: 8px;
  align-items: center;
  min-height: 34px;
  border-left: 2px solid transparent;
  padding: 7px 8px;
  color: var(--muted);
  text-decoration: none;
  font-size: 13px;
  font-weight: 750;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  border-left-color: var(--cyan);
  background: #142036;
  color: var(--text);
}

.sidebar-nav a span,
.dot {
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: var(--rose);
}

.dot.green, .sidebar-nav a:nth-of-type(3n) span { background: var(--green); }
.dot.cyan, .sidebar-nav a:nth-of-type(3n + 1) span { background: var(--cyan); }
.dot.rose, .sidebar-nav a:nth-of-type(3n + 2) span { background: var(--rose); }

.main-panel { min-width: 0; }

.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  min-height: 56px;
  border-bottom: 1px solid var(--line);
  background: rgba(5, 9, 18, 0.92);
  padding: 10px 32px;
  backdrop-filter: blur(16px);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  align-items: center;
}

.filter-row span {
  color: var(--muted);
  font-size: 13px;
  font-weight: 800;
}

.filter-pill,
.print-button,
.ghost-button,
.subtopic-chip,
.chapter-tab,
.copy-code,
.top-button {
  border: 1px solid #284465;
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font-weight: 800;
}

.filter-pill,
.print-button,
.ghost-button {
  min-height: 30px;
  padding: 5px 14px;
  font-size: 13px;
}

.filter-pill:hover,
.print-button:hover,
.ghost-button:hover,
.chapter-tab:hover,
.subtopic-chip:hover {
  border-color: var(--cyan);
  color: var(--text);
}

.filter-pill.active {
  border-color: var(--cyan);
  background: var(--cyan);
  color: #06101d;
}

.print-button {
  color: var(--cyan);
  border-color: var(--cyan);
}

main {
  min-width: 0;
}

.hero {
  position: relative;
  min-height: 300px;
  border-bottom: 1px solid var(--line);
  overflow: hidden;
  background:
    linear-gradient(rgba(0, 217, 255, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 217, 255, 0.12) 1px, transparent 1px);
  background-size: 220px 110px;
}

.hero img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.45;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(5, 9, 18, 0.96), rgba(5, 9, 18, 0.72), rgba(5, 9, 18, 0.94));
}

.hero-copy {
  position: relative;
  z-index: 1;
  max-width: 880px;
  padding: 74px 32px 38px;
}

.terminal-kicker {
  margin: 0 0 10px;
  color: var(--green);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 13px;
  font-weight: 900;
}

h1 {
  margin: 0;
  color: var(--cyan);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 46px;
  line-height: 1.02;
  letter-spacing: 0;
  text-shadow: 0 0 28px rgba(0, 217, 255, 0.28);
}

.hero-copy > p:not(.terminal-kicker) {
  max-width: 780px;
  color: #dbeafe;
  font-size: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(92px, 1fr));
  gap: 18px;
  max-width: 540px;
  margin-top: 26px;
}

.stats-grid div {
  display: grid;
  gap: 2px;
}

.stats-grid strong {
  color: #ff6b3a;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 22px;
}

.stats-grid span {
  color: #9fb3c8;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 1.3px;
  text-transform: uppercase;
}

.panel-card {
  width: min(1056px, calc(100% - 64px));
  margin: 32px 32px 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(17, 29, 49, 0.86);
  box-shadow: var(--shadow);
}

.panel-title {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  border-bottom: 1px solid var(--line);
  padding: 18px 20px;
}

.panel-title > div {
  display: flex;
  gap: 12px;
  align-items: center;
}

.square-check {
  display: inline-grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border: 1px solid rgba(0, 217, 255, 0.5);
  border-radius: 6px;
  color: var(--cyan);
  background: rgba(0, 217, 255, 0.08);
  font-weight: 900;
}

.panel-title h2 {
  margin: 0;
  font-size: 24px;
}

#progressLabel {
  color: var(--green);
}

.progress-track {
  height: 6px;
  background: #0b1322;
}

.progress-track span {
  display: block;
  width: 0%;
  height: 100%;
  background: linear-gradient(90deg, var(--cyan), var(--green));
  transition: width 180ms ease;
}

.checklist {
  display: grid;
  max-height: 430px;
  overflow: auto;
  padding: 12px 20px 18px;
}

.check-row {
  display: grid;
  grid-template-columns: 18px minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  min-height: 39px;
  border-bottom: 1px solid var(--line);
  color: var(--text);
  font-size: 14px;
  font-weight: 750;
}

.check-row input {
  width: 15px;
  min-height: 15px;
  accent-color: var(--cyan);
}

.check-row small,
.level-badge {
  border: 1px solid rgba(32, 227, 162, 0.32);
  border-radius: 999px;
  padding: 2px 9px;
  color: var(--green);
  font-size: 10px;
  font-weight: 900;
}

.check-row[data-level="critical"] small,
.level-badge.critical {
  border-color: rgba(255, 95, 120, 0.42);
  color: var(--rose);
}

.check-row[data-level="important"] small,
.level-badge.important {
  border-color: rgba(0, 217, 255, 0.42);
  color: var(--cyan);
}

.command-search {
  padding: 16px 20px 0;
}

.chapter-tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 14px 20px 6px;
}

.chapter-tab {
  flex: 0 0 auto;
  min-height: 32px;
  padding: 5px 12px;
}

.chapter-tab.active {
  border-color: var(--cyan);
  background: rgba(0, 217, 255, 0.12);
  color: var(--cyan);
}

.subtopic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 9px;
  max-height: 300px;
  overflow: auto;
  padding: 14px 20px 20px;
}

.subtopic-chip {
  display: grid;
  gap: 4px;
  min-height: 68px;
  border-radius: 8px;
  padding: 10px 12px;
  text-align: left;
  background: #0d1728;
}

.subtopic-chip span {
  overflow-wrap: anywhere;
  color: var(--text);
  font-size: 13px;
}

.subtopic-chip small {
  color: var(--muted);
  font-size: 11px;
}

.subtopic-chip.critical { border-color: rgba(255, 95, 120, 0.42); }
.subtopic-chip.important { border-color: rgba(0, 217, 255, 0.42); }
.subtopic-chip.basic { border-color: rgba(32, 227, 162, 0.28); }
.subtopic-chip.active {
  border-color: var(--amber);
  box-shadow: 0 0 0 3px rgba(255, 184, 77, 0.13);
}

.hidden { display: none !important; }

.notes-content {
  width: min(1056px, calc(100% - 64px));
  margin: 32px 32px 80px;
}

.source-note,
.chapter-section,
.subtopic-card {
  scroll-margin-top: 82px;
}

.source-note,
.chapter-section > h2,
.subtopic-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(17, 29, 49, 0.78);
  box-shadow: var(--shadow);
}

.source-note {
  padding: 18px 20px;
  margin-bottom: 18px;
}

.chapter-section {
  margin-bottom: 28px;
}

.chapter-section > h2 {
  margin: 0 0 14px;
  border-left: 4px solid var(--cyan);
  padding: 16px 18px;
  color: var(--cyan);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 22px;
}

.subtopic-card {
  margin: 12px 0;
  padding: 18px 20px;
}

.subtopic-card:target {
  border-color: var(--amber);
  box-shadow: 0 0 0 3px rgba(255, 184, 77, 0.16), var(--shadow);
}

.card-heading {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: start;
  margin-bottom: 10px;
}

.card-heading h3 {
  margin: 0;
  color: var(--text);
  font-size: 20px;
  line-height: 1.25;
}

.subtopic-card h4 {
  margin: 20px 0 8px;
  color: var(--cyan);
  font-size: 15px;
}

.subtopic-card p,
.source-note p {
  margin: 8px 0;
  color: #d9e8f7;
}

.note-list {
  margin: 7px 0 10px 20px;
  padding: 0;
  color: #dcecff;
}

.note-list .note-list {
  margin-top: 4px;
}

li {
  margin: 3px 0;
}

.numbered-step {
  margin: 8px 0;
  border-left: 3px solid var(--green);
  padding-left: 10px;
  color: #ecfeff;
  font-weight: 750;
}

code {
  border: 1px solid #274663;
  border-radius: 5px;
  background: #07101e;
  color: var(--cyan);
  padding: 1px 5px;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 0.93em;
}

.code-shell {
  overflow: hidden;
  border: 1px solid #284465;
  border-radius: 8px;
  background: #050912;
  margin: 14px 0;
}

.code-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #1f334d;
  padding: 8px 10px;
  color: var(--green);
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 12px;
}

.copy-code {
  min-height: 28px;
  border-radius: 6px;
  padding: 4px 9px;
  color: var(--cyan);
  font-size: 12px;
}

pre {
  overflow-x: auto;
  margin: 0;
  padding: 15px;
  color: #eef7ff;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.55;
}

pre code {
  border: 0;
  background: transparent;
  color: inherit;
  padding: 0;
}

.table-wrap {
  overflow-x: auto;
  margin: 14px 0;
}

table {
  width: 100%;
  min-width: 640px;
  border-collapse: collapse;
  background: #0b1424;
}

th,
td {
  border: 1px solid var(--line);
  padding: 9px 10px;
  text-align: left;
  vertical-align: top;
}

th {
  color: var(--cyan);
  background: #101e32;
}

.top-button {
  position: fixed;
  right: 18px;
  bottom: 18px;
  min-height: 38px;
  border-radius: 8px;
  padding: 7px 12px;
  color: var(--cyan);
  background: #0d1728;
  opacity: 0;
  pointer-events: none;
  transition: opacity 160ms ease;
}

.top-button.visible {
  opacity: 1;
  pointer-events: auto;
}

.empty-state {
  border: 1px dashed #284465;
  border-radius: 8px;
  padding: 18px;
  background: #0d1728;
  color: var(--muted);
  font-weight: 900;
}

@media (max-width: 980px) {
  :root { --sidebar: 0px; }
  .app-shell { grid-template-columns: 1fr; }
  .sidebar {
    position: relative;
    height: auto;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
  .sidebar-nav {
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  }
  .topbar {
    position: static;
    align-items: flex-start;
    flex-direction: column;
    padding: 12px 18px;
  }
  .hero-copy { padding: 54px 18px 32px; }
  h1 { font-size: 34px; }
  .panel-card,
  .notes-content {
    width: calc(100% - 28px);
    margin-left: 14px;
    margin-right: 14px;
  }
  .source-note,
  .chapter-section,
  .subtopic-card {
    scroll-margin-top: 20px;
  }
}

@media (max-width: 620px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .panel-title,
  .card-heading {
    align-items: flex-start;
    flex-direction: column;
  }
  .subtopic-grid {
    grid-template-columns: 1fr;
  }
}

@media print {
  body { background: white; color: black; }
  .sidebar, .topbar, .topic-command, .top-button { display: none; }
  .app-shell { display: block; }
  .hero, .panel-card, .source-note, .chapter-section > h2, .subtopic-card {
    box-shadow: none;
    background: white;
    color: black;
  }
}
"""


JS = r"""
const sideSearch = document.querySelector("#sideSearch");
const topicSearch = document.querySelector("#topicSearch");
const resetButton = document.querySelector("#resetFilters");
const chapterButtons = Array.from(document.querySelectorAll(".chapter-tab"));
const filterButtons = Array.from(document.querySelectorAll(".filter-pill[data-filter]"));
const subtopicButtons = Array.from(document.querySelectorAll(".subtopic-chip"));
const subtopicCards = Array.from(document.querySelectorAll(".subtopic-card"));
const chapterSections = Array.from(document.querySelectorAll(".chapter-section"));
const checkboxes = Array.from(document.querySelectorAll("[data-check-id]"));
const progressLabel = document.querySelector("#progressLabel");
const progressBar = document.querySelector("#progressBar");
const topButton = document.querySelector("#topButton");
const printButton = document.querySelector("#printButton");
let activeChapter = "all";
let activeLevel = "all";

function normalize(value) {
  return value.toLowerCase().trim();
}

function combinedQuery() {
  return normalize(`${sideSearch.value} ${topicSearch.value}`);
}

function setActiveChapter(chapter) {
  activeChapter = chapter;
  chapterButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.chapter === chapter);
  });
  applyFilters();
}

function setActiveLevel(level) {
  activeLevel = level;
  filterButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === level);
  });
  applyFilters();
}

function matchesQuery(element, query) {
  return !query || normalize(element.innerText).includes(query);
}

function applyFilters() {
  const query = combinedQuery();
  let visibleCount = 0;

  subtopicButtons.forEach((button) => {
    const chapterMatch = activeChapter === "all" || button.dataset.chapter === activeChapter;
    const levelMatch = activeLevel === "all" || button.dataset.level === activeLevel;
    const queryMatch = matchesQuery(button, query);
    button.classList.toggle("hidden", !(chapterMatch && levelMatch && queryMatch));
  });

  subtopicCards.forEach((card) => {
    const chapterMatch = activeChapter === "all" || card.dataset.chapter === activeChapter;
    const levelMatch = activeLevel === "all" || card.dataset.level === activeLevel;
    const queryMatch = matchesQuery(card, query);
    const visible = chapterMatch && levelMatch && queryMatch;
    card.classList.toggle("hidden", !visible);
    if (visible) visibleCount++;
  });

  document.querySelectorAll(".check-row").forEach((row) => {
    const chapterMatch = activeChapter === "all" || row.dataset.chapter === activeChapter;
    const levelMatch = activeLevel === "all" || row.dataset.level === activeLevel;
    const queryMatch = matchesQuery(row, query);
    row.classList.toggle("hidden", !(chapterMatch && levelMatch && queryMatch));
  });

  chapterSections.forEach((section) => {
    const visible = Array.from(section.querySelectorAll(".subtopic-card")).some((card) => !card.classList.contains("hidden"));
    section.classList.toggle("hidden", !visible);
  });

  updateEmptyState(visibleCount);
}

function updateEmptyState(visibleCount) {
  let empty = document.querySelector(".empty-state");
  if (visibleCount > 0) {
    if (empty) empty.remove();
    return;
  }
  if (!empty) {
    empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No matching topics. Try clearing filters.";
    document.querySelector("#notesContent").prepend(empty);
  }
}

function updateProgress() {
  const total = checkboxes.length;
  const done = checkboxes.filter((box) => box.checked).length;
  const percent = total ? Math.round((done / total) * 100) : 0;
  progressLabel.textContent = `${percent}%`;
  progressBar.style.width = `${percent}%`;
}

function saveChecks() {
  const checked = checkboxes.filter((box) => box.checked).map((box) => box.dataset.checkId);
  localStorage.setItem("dsa-study-checks", JSON.stringify(checked));
  updateProgress();
}

function loadChecks() {
  const checked = new Set(JSON.parse(localStorage.getItem("dsa-study-checks") || "[]"));
  checkboxes.forEach((box) => {
    box.checked = checked.has(box.dataset.checkId);
  });
  updateProgress();
}

const allButton = document.createElement("button");
allButton.type = "button";
allButton.className = "chapter-tab active";
allButton.textContent = "All";
allButton.dataset.chapter = "all";
document.querySelector("#chapterTabs").prepend(allButton);

chapterButtons.push(allButton);

chapterButtons.forEach((button) => {
  if (!button.dataset.chapter) return;
  button.addEventListener("click", () => {
    setActiveChapter(button.dataset.chapter);
    const target = document.querySelector(`#${button.dataset.chapter}`);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => setActiveLevel(button.dataset.filter));
});

subtopicButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const target = document.querySelector(`#${button.dataset.target}`);
    if (!target) return;
    subtopicButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", `#${button.dataset.target}`);
  });
});

sideSearch.addEventListener("input", () => {
  topicSearch.value = sideSearch.value;
  applyFilters();
});

topicSearch.addEventListener("input", () => {
  sideSearch.value = topicSearch.value;
  applyFilters();
});

resetButton.addEventListener("click", () => {
  activeChapter = "all";
  activeLevel = "all";
  sideSearch.value = "";
  topicSearch.value = "";
  chapterButtons.forEach((button) => button.classList.toggle("active", button.textContent === "All"));
  filterButtons.forEach((button) => button.classList.toggle("active", button.dataset.filter === "all"));
  subtopicButtons.forEach((button) => button.classList.remove("active"));
  applyFilters();
});

document.querySelector("#expandAll").addEventListener("click", () => {
  activeChapter = "all";
  activeLevel = "all";
  sideSearch.value = "";
  topicSearch.value = "";
  applyFilters();
  document.querySelector("#notesContent").scrollIntoView({ behavior: "smooth", block: "start" });
});

document.querySelectorAll(".copy-code").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.closest(".code-shell").querySelector("pre").innerText;
    await navigator.clipboard.writeText(code);
    const original = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => {
      button.textContent = original;
    }, 900);
  });
});

checkboxes.forEach((box) => box.addEventListener("change", saveChecks));
loadChecks();
applyFilters();

printButton.addEventListener("click", () => window.print());

window.addEventListener("scroll", () => {
  topButton.classList.toggle("visible", window.scrollY > 650);
});

topButton.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
"""


README = """# CSEB3213 DSA Study Dashboard

Static GitHub Pages dashboard generated from `DSA_Study_Notes_From_Slides.md`.

## Publish on GitHub Pages

Recommended setting:

- Branch: `main`
- Folder: `/docs`

The root folder also contains a copy of the same site, so `/root` publishing works too.
"""


def copy_site_to(destination: Path) -> None:
    destination.mkdir(exist_ok=True)
    for name in ["index.html", "styles.css", "script.js", "README.md"]:
        shutil.copy2(SITE / name, destination / name)
    asset_dest = destination / "assets"
    asset_dest.mkdir(exist_ok=True)
    shutil.copy2(ASSETS / "dsa-circuit.png", asset_dest / "dsa-circuit.png")
    (destination / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    content_html, chapters, subtopics, code_count = parse_markdown(markdown)
    make_visual_asset()
    write_site(content_html, chapters, subtopics, code_count)
    copy_site_to(DOCS)
    copy_site_to(ROOT)
    print(SITE)
    print(f"chapters={len(chapters)} subtopics={len(subtopics)} code_blocks={code_count}")


if __name__ == "__main__":
    main()
