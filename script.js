
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
