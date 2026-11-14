# maldoalberto.github.io

Personal site of Alberto Maldonado Romo: research products, talks, and publications.
Plain HTML, CSS, and JavaScript served by GitHub Pages. No build step.

## Add content

Edit the JSON files in `data/`. The page renders them automatically.

- `data/products.json`: research products. Set `"featured": true` to show one at the top.
- `data/talks.json`: talks and workshops. `date` (YYYY-MM-DD) sorts the list; `dateLabel` overrides the shown date; `"upcoming": true` adds a badge.
- `data/publications.json`: selected publications.

Example talk:

```json
{
  "date": "2027-03-10",
  "type": "Talk",
  "title": "Talk title",
  "event": "Event name",
  "location": "City",
  "links": [{ "label": "Slides", "url": "https://..." }]
}
```

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

The previous site (2022) lives on the `legacy-2022` branch.
