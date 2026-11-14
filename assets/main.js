// Renders research products, talks, and publications from data/*.json.
// To add content, edit the JSON files; no HTML changes needed.

const esc = (s = "") =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const linksHtml = (links = [], cls) =>
  links.length
    ? `<div class="${cls}">${links.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)} ↗</a>`).join("")}</div>`
    : "";

const tagsHtml = (tags = []) =>
  tags.length ? `<ul class="tags">${tags.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>` : "";

const fmtDate = (t) => {
  if (t.dateLabel) return t.dateLabel;
  const d = new Date(t.date + "T12:00:00");
  return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
};

async function load(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path}: ${res.status}`);
  return res.json();
}

function renderProducts(items) {
  const featured = items.filter((p) => p.featured);
  const rest = items.filter((p) => !p.featured);

  document.getElementById("featured").innerHTML = featured
    .map(
      (p) => `
      <article class="card featured">
        <span class="badge">featured · ${esc(p.year || "")}</span>
        <h3>${esc(p.name)}</h3>
        <p class="summary">${esc(p.summary)}</p>
        ${p.details ? `<ul class="details">${p.details.map((d) => `<li>${esc(d)}</li>`).join("")}</ul>` : ""}
        ${tagsHtml(p.tags)}
        ${linksHtml(p.links, "card-links")}
      </article>`
    )
    .join("");

  document.getElementById("product-grid").innerHTML = rest
    .map(
      (p) => `
      <article class="card">
        ${p.year ? `<span class="meta">${esc(p.year)}</span>` : ""}
        <h3>${esc(p.name)}</h3>
        <p>${esc(p.summary)}</p>
        ${tagsHtml(p.tags)}
        ${linksHtml(p.links, "card-links")}
      </article>`
    )
    .join("");
}

function renderTalks(talks) {
  talks.sort((a, b) => b.date.localeCompare(a.date));
  const types = ["All", ...new Set(talks.map((t) => t.type))];
  const filterEl = document.getElementById("talk-filters");
  const listEl = document.getElementById("talk-list");

  const draw = (type) => {
    listEl.innerHTML = talks
      .filter((t) => type === "All" || t.type === type)
      .map(
        (t) => `
        <li class="${t.upcoming ? "upcoming" : ""}">
          <span class="talk-date">${esc(fmtDate(t))}</span>
          <span class="talk-type">${esc(t.type)}</span>
          ${t.upcoming ? '<span class="talk-up">Upcoming</span>' : ""}
          <h3>${esc(t.title)}</h3>
          <p>${esc(t.event)}${t.location ? ` · ${esc(t.location)}` : ""}</p>
          ${t.summary ? `<p>${esc(t.summary)}</p>` : ""}
          ${linksHtml(t.links, "talk-links")}
        </li>`
      )
      .join("");
    filterEl.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.type === type)));
  };

  filterEl.innerHTML = types.map((t) => `<button type="button" data-type="${esc(t)}">${esc(t)}</button>`).join("");
  filterEl.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (b) draw(b.dataset.type);
  });
  draw("All");
}

function renderPubs(pubs) {
  pubs.sort((a, b) => b.year - a.year);
  document.getElementById("pub-list").innerHTML = pubs
    .map(
      (p) => `
      <li>
        <a class="pub-title" href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.title)}</a>
        <div class="pub-meta">${esc(p.authors)} · ${esc(p.venue)} · ${esc(p.year)}</div>
        ${p.award ? `<div class="award">★ ${esc(p.award)}</div>` : ""}
      </li>`
    )
    .join("");
}

document.getElementById("year").textContent = new Date().getFullYear();

Promise.all([load("data/products.json"), load("data/talks.json"), load("data/publications.json")])
  .then(([products, talks, pubs]) => {
    renderProducts(products);
    renderTalks(talks);
    renderPubs(pubs);
  })
  .catch((err) => console.error("Failed to load site data:", err));
