
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
