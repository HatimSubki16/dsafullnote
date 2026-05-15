from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "DSA_Study_Notes_From_Slides.md"
SITE = ROOT / "dsa-github-page"
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


def fence_language(line: str) -> str:
    lang = line.strip().strip("`").strip()
    return lang or "text"


def is_table_separator(line: str) -> bool:
    return re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line) is not None


def is_table_start(lines: list[str], idx: int) -> bool:
    return (
        idx + 1 < len(lines)
        and lines[idx].strip().startswith("|")
        and is_table_separator(lines[idx + 1])
    )


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
    out.append("</tr></thead>")
    out.append("<tbody>")
    for row in body:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{inline_markup(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out), idx


def close_list(stack: list[int], target_level: int, output: list[str]) -> None:
    while stack and stack[-1] >= target_level:
        output.append("</ul>")
        stack.pop()


def parse_markdown(markdown: str) -> tuple[str, list[dict[str, str]], list[dict[str, str]]]:
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
    in_code = False
    code_lang = "text"
    code_lines: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            close_list(list_stack, 0, output)
            output.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_code() -> None:
        if code_lines:
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
            close_list(list_stack, 0, output)
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
                code_lang = fence_language(stripped)
            idx += 1
            continue

        if in_code:
            code_lines.append(line)
            idx += 1
            continue

        if is_table_start(lines, idx):
            flush_paragraph()
            close_list(list_stack, 0, output)
            table_html, idx = parse_table(lines, idx)
            output.append(table_html)
            continue

        if not stripped:
            flush_paragraph()
            close_list(list_stack, 0, output)
            idx += 1
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            close_list(list_stack, 0, output)
            if source_note_open:
                output.append("</section>")
            output.append(f'<section class="source-note"><h2>{inline_markup(stripped[2:].strip())}</h2>')
            source_note_open = True
            idx += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_list(list_stack, 0, output)
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
            close_list(list_stack, 0, output)
            if current_article_open:
                output.append("</article>")
            title = stripped[4:].strip()
            sub_id = slugify(f"{current_chapter_title}-{title}", used)
            subtopics.append(
                {
                    "id": sub_id,
                    "title": title,
                    "chapter": current_chapter,
                    "chapterTitle": current_chapter_title,
                }
            )
            output.append(
                f'<article class="subtopic-card" id="{sub_id}" '
                f'data-chapter="{current_chapter}" data-title="{html.escape(title)}">'
                f'<h3>{inline_markup(title)}</h3>'
            )
            current_article_open = True
            idx += 1
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            close_list(list_stack, 0, output)
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
            close_list(list_stack, 0, output)
            output.append(f'<p class="numbered-step">{inline_markup(stripped)}</p>')
            idx += 1
            continue

        paragraph.append(stripped)
        idx += 1

    flush_paragraph()
    close_list(list_stack, 0, output)
    if current_article_open:
        output.append("</article>")
    if current_chapter_open:
        output.append("</section>")
    if source_note_open:
        output.append("</section>")

    return "\n".join(output), chapters, subtopics


def make_visual_asset() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / "dsa-map.png"
    img = Image.new("RGB", (1200, 520), "#f8faf7")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 38)
        label_font = ImageFont.truetype("arial.ttf", 23)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        title_font = label_font = small_font = ImageFont.load_default()

    colorset = {
        "ink": "#1f2937",
        "line": "#73806f",
        "teal": "#0f766e",
        "amber": "#b45309",
        "rose": "#be123c",
        "leaf": "#4d7c0f",
        "paper": "#ffffff",
    }

    draw.rounded_rectangle((28, 28, 1172, 492), radius=28, fill="#ffffff", outline="#d8dfd2", width=3)
    draw.text((70, 62), "Data Structures and Algorithms", fill=colorset["ink"], font=title_font)
    draw.text((72, 110), "ADT -> STL -> Lists -> Stacks -> Trees -> Graphs -> Sorting -> Searching", fill="#52604f", font=small_font)

    # Stack blocks
    x, y = 92, 188
    for i, color in enumerate(["#dbeafe", "#fde68a", "#bbf7d0", "#fecdd3"]):
        draw.rounded_rectangle((x, y + i * 44, x + 150, y + 34 + i * 44), radius=8, fill=color, outline="#6b7280", width=2)
    draw.text((122, 372), "Stack", fill=colorset["ink"], font=label_font)

    # Linked nodes
    node_y = 242
    for i, cx in enumerate([330, 430, 530]):
        draw.ellipse((cx, node_y, cx + 58, node_y + 58), fill="#ccfbf1", outline=colorset["teal"], width=3)
        draw.text((cx + 20, node_y + 16), str(i + 1), fill=colorset["ink"], font=label_font)
        if i < 2:
            draw.line((cx + 58, node_y + 29, cx + 100, node_y + 29), fill=colorset["line"], width=4)
            draw.polygon([(cx + 100, node_y + 29), (cx + 88, node_y + 22), (cx + 88, node_y + 36)], fill=colorset["line"])
    draw.text((392, 372), "Linked List", fill=colorset["ink"], font=label_font)

    # Tree
    tree_nodes = [(760, 190), (690, 285), (830, 285), (650, 375), (730, 375), (875, 375)]
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]:
        x1, y1 = tree_nodes[a]
        x2, y2 = tree_nodes[b]
        draw.line((x1 + 24, y1 + 24, x2 + 24, y2 + 24), fill=colorset["line"], width=4)
    for i, (cx, cy) in enumerate(tree_nodes):
        draw.ellipse((cx, cy, cx + 48, cy + 48), fill="#ffedd5", outline=colorset["amber"], width=3)
        draw.text((cx + 16, cy + 12), chr(65 + i), fill=colorset["ink"], font=small_font)
    draw.text((742, 438), "Tree", fill=colorset["ink"], font=label_font)

    # Graph
    graph_nodes = [(1010, 190), (1090, 245), (1050, 335), (945, 320), (930, 225)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (4, 2), (0, 3)]
    for a, b in edges:
        x1, y1 = graph_nodes[a]
        x2, y2 = graph_nodes[b]
        draw.line((x1, y1, x2, y2), fill=colorset["line"], width=3)
    for cx, cy in graph_nodes:
        draw.ellipse((cx - 19, cy - 19, cx + 19, cy + 19), fill="#fce7f3", outline=colorset["rose"], width=3)
    draw.text((984, 372), "Graph", fill=colorset["ink"], font=label_font)

    img.save(path, optimize=True)


def write_site(content_html: str, chapters: list[dict[str, str]], subtopics: list[dict[str, str]]) -> None:
    SITE.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)

    chapter_buttons = "\n".join(
        f'<button type="button" class="chapter-tab" data-chapter="{chapter["id"]}">{html.escape(chapter["title"].replace("Chapter ", "Ch. "))}</button>'
        for chapter in chapters
    )
    subtopic_buttons = "\n".join(
        f'<button type="button" class="subtopic-chip" data-target="{sub["id"]}" data-chapter="{sub["chapter"]}">'
        f'<span>{html.escape(sub["title"])}</span><small>{html.escape(sub["chapterTitle"].replace("Chapter ", "Ch. "))}</small></button>'
        for sub in subtopics
    )

    index = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Interactive DSA study page generated from the provided lecture slides.">
  <title>DSA Study Hub</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <div class="header-copy">
      <p class="eyebrow">CSEB3213 DSA Study Hub</p>
      <h1>Data Structures and Algorithms</h1>
      <div class="meta-strip" aria-label="Study guide summary">
        <span>{len(chapters)} sections</span>
        <span>{len(subtopics)} subtopics</span>
        <span>Static GitHub Pages</span>
      </div>
    </div>
    <img src="assets/dsa-map.png" alt="Visual map of stacks, linked lists, trees, and graphs.">
  </header>

  <main>
    <section class="study-console" aria-label="Interactive content">
      <div class="console-toolbar">
        <label class="search-box">
          <span>Search</span>
          <input id="topicSearch" type="search" placeholder="linked list, stack, tree, sorting...">
        </label>
        <button type="button" class="reset-button" id="resetFilters">All topics</button>
      </div>
      <div class="chapter-tabs" id="chapterTabs">
        {chapter_buttons}
      </div>
      <div class="subtopic-grid" id="subtopicGrid">
        {subtopic_buttons}
      </div>
    </section>

    <div class="content-layout">
      <aside class="quick-map" aria-label="Chapter map">
        <p>Chapter Map</p>
        <nav>
          {''.join(f'<a href="#{chapter["id"]}">{html.escape(chapter["title"])}</a>' for chapter in chapters)}
        </nav>
      </aside>
      <section class="notes-content" id="notesContent">
        {content_html}
      </section>
    </div>
  </main>

  <button type="button" class="top-button" id="topButton" aria-label="Back to top">Top</button>
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
  --bg: #f8faf7;
  --paper: #ffffff;
  --ink: #1f2937;
  --muted: #5f6b5b;
  --line: #d8dfd2;
  --teal: #0f766e;
  --amber: #b45309;
  --rose: #be123c;
  --leaf: #4d7c0f;
  --soft-teal: #e6fffb;
  --soft-amber: #fff7ed;
  --soft-rose: #fff1f2;
  --shadow: 0 16px 40px rgba(31, 41, 55, 0.08);
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}

button,
input {
  font: inherit;
}

.site-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 520px);
  gap: 28px;
  align-items: center;
  max-width: 1180px;
  margin: 0 auto;
  padding: 32px 22px 18px;
}

.header-copy {
  min-width: 0;
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--teal);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  max-width: 760px;
  font-size: 42px;
  line-height: 1.05;
  letter-spacing: 0;
}

.site-header img {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
}

.meta-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 18px;
}

.meta-strip span {
  display: inline-flex;
  min-height: 32px;
  align-items: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  padding: 5px 10px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 700;
}

main {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 22px 56px;
}

.study-console {
  position: sticky;
  top: 0;
  z-index: 10;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: var(--shadow);
  padding: 14px;
  backdrop-filter: blur(12px);
}

.console-toolbar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
  align-items: end;
}

.search-box {
  display: grid;
  gap: 5px;
}

.search-box span {
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.search-box input {
  width: 100%;
  min-height: 42px;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 9px 12px;
  color: var(--ink);
  background: #fbfdf9;
}

.reset-button,
.chapter-tab,
.subtopic-chip,
.copy-code,
.top-button {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  color: var(--ink);
  cursor: pointer;
}

.reset-button {
  min-height: 42px;
  padding: 8px 14px;
  font-weight: 800;
}

.reset-button:hover,
.chapter-tab:hover,
.subtopic-chip:hover,
.top-button:hover {
  border-color: var(--teal);
}

.chapter-tabs {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  overflow-x: auto;
  padding-bottom: 3px;
}

.chapter-tab {
  flex: 0 0 auto;
  min-height: 34px;
  padding: 6px 10px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 800;
}

.chapter-tab.active {
  border-color: var(--teal);
  background: var(--soft-teal);
  color: var(--teal);
}

.subtopic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 8px;
  max-height: 230px;
  overflow: auto;
  margin-top: 12px;
  padding-right: 3px;
}

.subtopic-chip {
  display: grid;
  gap: 2px;
  min-height: 64px;
  padding: 9px 10px;
  text-align: left;
  align-content: center;
}

.subtopic-chip span {
  overflow-wrap: anywhere;
  font-size: 13px;
  font-weight: 800;
}

.subtopic-chip small {
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
}

.subtopic-chip.active {
  border-color: var(--amber);
  background: var(--soft-amber);
}

.subtopic-chip.hidden,
.subtopic-card.hidden,
.chapter-section.hidden {
  display: none;
}

.content-layout {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 22px;
  margin-top: 24px;
}

.quick-map {
  position: sticky;
  top: 322px;
  align-self: start;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  padding: 14px;
}

.quick-map p {
  margin: 0 0 10px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.quick-map nav {
  display: grid;
  gap: 7px;
}

.quick-map a {
  color: var(--ink);
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
}

.quick-map a:hover {
  color: var(--teal);
}

.notes-content {
  min-width: 0;
}

.source-note,
.chapter-section,
.subtopic-card {
  scroll-margin-top: 340px;
}

.chapter-section {
  margin-bottom: 24px;
}

.chapter-section > h2 {
  margin: 0 0 12px;
  border-left: 6px solid var(--teal);
  padding: 12px 16px;
  border-radius: 8px;
  background: var(--paper);
  box-shadow: var(--shadow);
  font-size: 24px;
  line-height: 1.2;
}

.subtopic-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  margin: 12px 0;
  padding: 18px;
}

.subtopic-card:target {
  border-color: var(--amber);
  box-shadow: 0 0 0 3px rgba(180, 83, 9, 0.14);
}

.subtopic-card h3 {
  margin: 0 0 10px;
  font-size: 19px;
  line-height: 1.25;
}

.subtopic-card h4 {
  margin: 18px 0 8px;
  color: var(--rose);
  font-size: 15px;
}

.subtopic-card p,
.source-note p {
  margin: 8px 0;
}

.note-list {
  margin: 6px 0 10px 18px;
  padding: 0;
}

.note-list .note-list {
  margin-top: 4px;
}

li {
  margin: 3px 0;
}

.numbered-step {
  position: relative;
  margin: 6px 0;
  border-left: 3px solid var(--leaf);
  padding-left: 10px;
  font-weight: 700;
}

code {
  border: 1px solid #d8dfd2;
  border-radius: 5px;
  background: #f3f4f6;
  padding: 1px 4px;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 0.93em;
}

.code-shell {
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #111827;
  margin: 12px 0;
}

.code-bar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  padding: 8px 10px;
  color: #d1d5db;
  font-size: 12px;
  font-weight: 800;
}

.copy-code {
  min-height: 28px;
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
  padding: 4px 9px;
  font-size: 12px;
  font-weight: 800;
}

pre {
  overflow-x: auto;
  margin: 0;
  padding: 14px;
  color: #f9fafb;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.55;
}

pre code {
  border: 0;
  background: transparent;
  padding: 0;
  color: inherit;
}

.table-wrap {
  overflow-x: auto;
  margin: 12px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 640px;
  background: var(--paper);
}

th,
td {
  border: 1px solid var(--line);
  padding: 9px 10px;
  text-align: left;
  vertical-align: top;
}

th {
  background: #eef5ed;
}

.top-button {
  position: fixed;
  right: 18px;
  bottom: 18px;
  min-height: 38px;
  padding: 7px 12px;
  opacity: 0;
  pointer-events: none;
  font-weight: 800;
  transition: opacity 160ms ease;
}

.top-button.visible {
  opacity: 1;
  pointer-events: auto;
}

.empty-state {
  border: 1px dashed var(--line);
  border-radius: 8px;
  padding: 18px;
  background: var(--paper);
  color: var(--muted);
  font-weight: 800;
}

@media (max-width: 900px) {
  .site-header {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 32px;
  }

  .content-layout {
    grid-template-columns: 1fr;
  }

  .quick-map {
    position: static;
  }

  .study-console {
    position: static;
  }

  .source-note,
  .chapter-section,
  .subtopic-card {
    scroll-margin-top: 20px;
  }
}

@media (max-width: 560px) {
  main,
  .site-header {
    padding-left: 14px;
    padding-right: 14px;
  }

  .console-toolbar {
    grid-template-columns: 1fr;
  }

  .subtopic-grid {
    grid-template-columns: 1fr;
    max-height: 260px;
  }
}
"""


JS = r"""
const searchInput = document.querySelector("#topicSearch");
const resetButton = document.querySelector("#resetFilters");
const chapterButtons = Array.from(document.querySelectorAll(".chapter-tab"));
const subtopicButtons = Array.from(document.querySelectorAll(".subtopic-chip"));
const subtopicCards = Array.from(document.querySelectorAll(".subtopic-card"));
const chapterSections = Array.from(document.querySelectorAll(".chapter-section"));
const topButton = document.querySelector("#topButton");
let activeChapter = "all";

function normalize(value) {
  return value.toLowerCase().trim();
}

function setActiveChapter(chapter) {
  activeChapter = chapter;
  chapterButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.chapter === chapter);
  });
  applyFilters();
}

function applyFilters() {
  const query = normalize(searchInput.value);
  let visibleCount = 0;

  subtopicButtons.forEach((button) => {
    const matchesChapter = activeChapter === "all" || button.dataset.chapter === activeChapter;
    const matchesSearch = !query || normalize(button.innerText).includes(query);
    button.classList.toggle("hidden", !(matchesChapter && matchesSearch));
  });

  subtopicCards.forEach((card) => {
    const title = normalize(card.dataset.title || card.innerText);
    const body = normalize(card.innerText);
    const matchesChapter = activeChapter === "all" || card.dataset.chapter === activeChapter;
    const matchesSearch = !query || title.includes(query) || body.includes(query);
    const visible = matchesChapter && matchesSearch;
    card.classList.toggle("hidden", !visible);
    if (visible) visibleCount++;
  });

  chapterSections.forEach((section) => {
    const hasVisibleCard = Array.from(section.querySelectorAll(".subtopic-card")).some((card) => !card.classList.contains("hidden"));
    section.classList.toggle("hidden", !hasVisibleCard);
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
    empty.textContent = "No matching subtopics.";
    document.querySelector("#notesContent").prepend(empty);
  }
}

chapterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setActiveChapter(button.dataset.chapter);
    const target = document.querySelector(`#${button.dataset.chapter}`);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

subtopicButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const target = document.querySelector(`#${button.dataset.target}`);
    if (target) {
      subtopicButtons.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      history.replaceState(null, "", `#${button.dataset.target}`);
    }
  });
});

searchInput.addEventListener("input", applyFilters);

resetButton.addEventListener("click", () => {
  activeChapter = "all";
  searchInput.value = "";
  chapterButtons.forEach((button) => button.classList.remove("active"));
  subtopicButtons.forEach((button) => button.classList.remove("active"));
  applyFilters();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

document.querySelectorAll(".copy-code").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.closest(".code-shell").querySelector("pre").innerText;
    await navigator.clipboard.writeText(code);
    const original = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => {
      button.textContent = original;
    }, 1000);
  });
});

window.addEventListener("scroll", () => {
  topButton.classList.toggle("visible", window.scrollY > 650);
});

topButton.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

const firstAll = document.createElement("button");
firstAll.type = "button";
firstAll.className = "chapter-tab";
firstAll.textContent = "All";
firstAll.addEventListener("click", () => {
  activeChapter = "all";
  chapterButtons.forEach((button) => button.classList.remove("active"));
  applyFilters();
});
document.querySelector("#chapterTabs").prepend(firstAll);

applyFilters();
"""


README = """# DSA Study Hub

Static GitHub Pages site generated from `DSA_Study_Notes_From_Slides.md`.

## Files

- `index.html` - main interactive study page
- `styles.css` - page styling
- `script.js` - search, filters, subtopic navigation, code-copy actions
- `assets/dsa-map.png` - subject visual asset

## Publish on GitHub Pages

1. Copy this folder's contents into a GitHub repository.
2. Commit and push.
3. In GitHub, open `Settings > Pages`.
4. Choose the branch and root folder that contains `index.html`.
5. Save, then open the Pages URL GitHub provides.
"""


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    content_html, chapters, subtopics = parse_markdown(markdown)
    make_visual_asset()
    write_site(content_html, chapters, subtopics)
    print(SITE)
    print(f"chapters={len(chapters)} subtopics={len(subtopics)}")


if __name__ == "__main__":
    main()
