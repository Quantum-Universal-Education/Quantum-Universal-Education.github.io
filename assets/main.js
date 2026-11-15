// Renders research products, talks, and publications from data/*.json.
// To add content, edit the JSON files; no HTML changes needed.

const esc = (s = "") =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const linksHtml = (links = [], cls) =>
  links.length
    ? `<div class="${cls}">${links
        .map((l) =>
          /^https?:/.test(l.url)
            ? `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)} ↗</a>`
            : `<a href="${esc(l.url)}">${esc(l.label)} →</a>`
        )
        .join("")}</div>`
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

  renderVideos(talks);
  filterEl.innerHTML = types.map((t) => `<button type="button" data-type="${esc(t)}">${esc(t)}</button>`).join("");
  filterEl.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (b) draw(b.dataset.type);
  });
  draw("All");
}

// Builds the Videos grid from every YouTube link in talks.json.
function renderVideos(talks) {
  const videos = [];
  talks.forEach((t) =>
    (t.links || []).forEach((l) => {
      const m = /youtube\.com\/watch\?v=([\w-]{11})/.exec(l.url);
      if (m) videos.push({ id: m[1], url: l.url, title: t.title, event: t.event, date: fmtDate(t), label: l.label });
    })
  );
  if (!videos.length) return;
  document.getElementById("videos").hidden = false;
  document.getElementById("video-grid").innerHTML = videos
    .map(
      (v) => `
      <a class="video" href="${esc(v.url)}" target="_blank" rel="noopener">
        <div class="thumb"><img src="https://i.ytimg.com/vi/${v.id}/hqdefault.jpg" alt="" loading="lazy"></div>
        <div class="vbody">
          <div class="vtitle">${esc(v.title)}${/\((EN|ES)\)/.test(v.label) ? ` <span class="vmeta">${esc(v.label.match(/\((EN|ES)\)/)[1])}</span>` : ""}</div>
          <div class="vmeta">${esc(v.date)} · ${esc(v.event)}</div>
        </div>
      </a>`
    )
    .join("");
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

const fmtMonth = (d) => {
  const [y, m] = String(d).split("-");
  return m ? new Date(+y, +m - 1, 15).toLocaleDateString("en-US", { year: "numeric", month: "short" }) : y;
};

function renderNews(items) {
  items.sort((a, b) => String(b.date).localeCompare(String(a.date)));
  document.getElementById("news-list").innerHTML = items
    .map(
      (n) => `
      <li>
        <span class="news-date">${esc(fmtMonth(n.date))}</span>
        <div>
          <a class="news-title" href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.title)}</a>
          <div class="news-source">${esc(n.source)}</div>
          ${n.summary ? `<p>${esc(n.summary)}</p>` : ""}
          ${(n.extra || []).map((x) => `<a class="news-extra" href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.label)} ↗</a>`).join(" ")}
        </div>
      </li>`
    )
    .join("");
}

function renderPosts(posts) {
  document.getElementById("post-grid").innerHTML = posts
    .map(
      (p) => `
      <figure class="post">
        <iframe src="${esc(p.embed)}" height="${Number(p.height) || 600}" title="${esc(p.title)}" loading="lazy" allowfullscreen></iframe>
        <figcaption><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.title)} ↗</a></figcaption>
      </figure>`
    )
    .join("");
}

function renderPhotos(photos) {
  if (!photos.length) return;
  document.getElementById("photos").hidden = false;
  document.getElementById("photo-grid").innerHTML = photos
    .map(
      (p) => `
      <figure class="photo">
        <img src="${esc(p.src)}" alt="${esc(p.alt || p.caption || "")}" loading="lazy">
        ${p.caption ? `<figcaption>${esc(p.caption)}</figcaption>` : ""}
      </figure>`
    )
    .join("");
}

function renderMetrics(m) {
  const years = Object.entries(m.citations_per_year.years);
  const max = Math.max(...years.map(([, v]) => v));
  document.getElementById("impact").hidden = false;
  document.getElementById("impact-asof").textContent = `Figures as of ${fmtMonth(m.as_of)}.`;
  document.getElementById("cite-caption").innerHTML =
    `Citations per year · <a href="${esc(m.citations_per_year.url)}" target="_blank" rel="noopener">${esc(m.citations_per_year.source)} ↗</a>`;
  const bars = document.getElementById("cite-bars");
  bars.setAttribute("aria-label", "Citations per year: " + years.map(([y, v]) => `${y}: ${v}`).join(", "));
  bars.innerHTML = years
    .map(
      ([y, v]) => `
      <div class="cite-bar">
        <span class="cite-val">${v}</span>
        <div class="cite-fill" style="height:${Math.max(4, (v / max) * 100)}%"></div>
        <span class="cite-year mono">${esc(y)}</span>
      </div>`
    )
    .join("");
  document.getElementById("impact-tiles").innerHTML = m.tiles
    .map((t) => `<li><strong>${esc(t.value)}</strong><span>${esc(t.label)}</span></li>`)
    .join("");
}

function setupShare() {
  const url = encodeURIComponent(location.origin + location.pathname);
  const text = encodeURIComponent(document.title);
  const el = document.getElementById("share");
  if (!el) return;
  el.innerHTML = `
    <span>Share this site:</span>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url=${url}" target="_blank" rel="noopener">LinkedIn</a>
    <a href="https://x.com/intent/post?url=${url}&text=${text}" target="_blank" rel="noopener">X</a>
    <button type="button" id="copy-link">Copy link</button>`;
  document.getElementById("copy-link").addEventListener("click", async (e) => {
    try {
      await navigator.clipboard.writeText(decodeURIComponent(url));
      e.target.textContent = "Copied ✓";
    } catch {
      e.target.textContent = decodeURIComponent(url);
    }
  });
}

document.getElementById("year").textContent = new Date().getFullYear();
setupShare();

const sections = [
  ["data/products.json", renderProducts],
  ["data/talks.json", renderTalks],
  ["data/publications.json", renderPubs],
  ["data/news.json", renderNews],
  ["data/posts.json", renderPosts],
  ["data/photos.json", renderPhotos],
  ["data/metrics.json", renderMetrics],
];
// Each section loads independently so one bad file does not blank the page.
sections.forEach(([path, render]) =>
  load(path)
    .then(render)
    .catch((err) => console.error("Failed to load", path, err))
);
