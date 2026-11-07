#!/usr/bin/env python3
"""Generate a sortable/filterable HTML report from a scan.py report_data.json.

Usage:
    python3 report.py report_data.json --output account-cleanup-report.html

Publish the HTML so the user can browse, sort, and filter before picking
what to delete. Entries whose category starts with "EXCLUDE:" are shown in
a separate flagged panel and are not counted in the reclaimable total.
"""
import argparse
import colorsys
import hashlib
import json


def human(n):
    for unit in ["B", "K", "M", "G", "T"]:
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}{unit}"
        n /= 1024
    return f"{n:.1f}P"


def color_for(category):
    h = int(hashlib.md5(category.encode()).hexdigest(), 16) % 360
    r, g, b = colorsys.hls_to_rgb(h / 360, 0.42, 0.45)
    light = "#%02X%02X%02X" % (int(r * 255), int(g * 255), int(b * 255))
    r, g, b = colorsys.hls_to_rgb(h / 360, 0.72, 0.5)
    dark = "#%02X%02X%02X" % (int(r * 255), int(g * 255), int(b * 255))
    return light, dark


def build_html(data):
    entries = [e for e in data["entries"] if not e["category"].startswith("EXCLUDE:")]
    flagged = [e for e in data["entries"] if e["category"].startswith("EXCLUDE:")]
    entries.sort(key=lambda e: -e["size_bytes"])
    flagged.sort(key=lambda e: -e["size_bytes"])
    total = sum(e["size_bytes"] for e in entries)

    cat_totals = {}
    for e in entries:
        cat_totals[e["category"]] = cat_totals.get(e["category"], 0) + e["size_bytes"]
    cats_sorted = sorted(cat_totals.items(), key=lambda x: -x[1])

    segs, legend_rows = [], []
    for cat, tot in cats_sorted:
        pct = tot / total * 100 if total else 0
        light, dark = color_for(cat)
        n = sum(1 for e in entries if e["category"] == cat)
        segs.append(f'<div class="seg" style="--w:{pct:.4f}%; --c-light:{light}; --c-dark:{dark};" title="{cat}: {human(tot)} ({pct:.1f}%)"></div>')
        legend_rows.append(
            f'<div class="legend-row" data-cat="{cat}">'
            f'<div class="legend-swatch" style="--c-light:{light}; --c-dark:{dark};"></div>'
            f'<div class="legend-text"><div class="legend-head">'
            f'<span class="legend-name">{cat}</span><span class="legend-size">{human(tot)}</span>'
            f'<span class="legend-count">{n} dirs</span></div></div></div>'
        )

    table_rows = []
    for e in entries:
        light, dark = color_for(e["category"])
        table_rows.append(
            f'<tr data-cat="{e["category"]}" data-size="{e["size_bytes"]:.0f}" data-path="{e["path"].lower()}">'
            f'<td class="col-cat"><span class="tag" style="--c-light:{light}; --c-dark:{dark};">{e["category"]}</span></td>'
            f'<td class="col-size">{e["size_str"]}</td>'
            f'<td class="col-scope">{e["scope"]}</td>'
            f'<td class="col-path"><span class="path">{e["path"]}</span></td></tr>'
        )

    flagged_rows = "".join(
        f'<div class="flag-row"><span class="flag-size">{e["size_str"]}</span>'
        f'<span class="flag-cat">{e["category"].replace("EXCLUDE:", "")}</span>'
        f'<span class="flag-path">{e["path"]}</span>'
        f'<span class="flag-note">{e.get("note") or ""}</span></div>'
        for e in flagged
    )
    flagged_total = sum(e["size_bytes"] for e in flagged)

    return HTML_TEMPLATE.format(
        total=human(total),
        n_entries=len(entries),
        segs_html="\n        ".join(segs),
        legend_html="\n        ".join(legend_rows),
        rows_html="\n      ".join(table_rows),
        flagged_section=(
            f'<div class="git-card"><div class="git-card-head">'
            f'<span class="git-card-title">Flagged for review — not counted above</span>'
            f'<span class="git-card-total">{human(flagged_total)} across {len(flagged)}</span></div>'
            f'<p class="git-card-note">Keep-list items, admin-only paths, or other entries that need a human decision. Not counted in the reclaimable total.</p>'
            f'<div class="git-list">{flagged_rows}</div></div>'
            if flagged else ""
        ),
    )


HTML_TEMPLATE = """<title>macOS Account Cleanup Report</title>
<style>
:root {{
  --bg: #F3F4F2; --bg-raised: #FFFFFF; --ink: #1B1E21; --ink-dim: #5B6169;
  --border: #DADCD8; --accent: #0E7C86; --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; --radius: 3px;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #14171A; --bg-raised: #1B1F23; --ink: #E4E7E9; --ink-dim: #9AA0A6; --border: #2C3136; --accent: #4FC3CE; }}
}}
:root[data-theme="dark"] {{ --bg: #14171A; --bg-raised: #1B1F23; --ink: #E4E7E9; --ink-dim: #9AA0A6; --border: #2C3136; --accent: #4FC3CE; }}
:root[data-theme="light"] {{ --bg: #F3F4F2; --bg-raised: #FFFFFF; --ink: #1B1E21; --ink-dim: #5B6169; --border: #DADCD8; --accent: #0E7C86; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--sans); margin: 0; padding: 2.5rem 1.5rem 4rem; line-height: 1.5; }}
.wrap {{ max-width: 1120px; margin: 0 auto; }}
h1 {{ font-size: 1.7rem; font-weight: 650; margin: 0 0 0.35rem; text-wrap: balance; }}
.sub {{ color: var(--ink-dim); font-size: 0.92rem; max-width: 62ch; }}
.total-card {{ background: var(--bg-raised); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem 1.5rem; margin: 1.5rem 0 1rem; }}
.total-figure {{ display: flex; align-items: baseline; gap: 0.6rem; margin-bottom: 1rem; }}
.total-figure .num {{ font-family: var(--mono); font-size: 2.4rem; font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }}
.total-figure .label {{ color: var(--ink-dim); font-size: 0.9rem; }}
.stackbar {{ display: flex; width: 100%; height: 14px; border-radius: 2px; overflow: hidden; border: 1px solid var(--border); }}
.seg {{ width: var(--w); background: var(--c-light); }}
@media (prefers-color-scheme: dark) {{ .seg {{ background: var(--c-dark); }} }}
:root[data-theme="dark"] .seg {{ background: var(--c-dark); }}
:root[data-theme="light"] .seg {{ background: var(--c-light); }}
.legend {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 0.6rem; margin: 1.5rem 0 2rem; }}
.legend-row {{ display: flex; gap: 0.65rem; padding: 0.7rem 0.8rem; background: var(--bg-raised); border: 1px solid var(--border); border-radius: var(--radius); cursor: pointer; }}
.legend-row:hover {{ border-color: var(--accent); }}
.legend-row.active {{ border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }}
.legend-swatch {{ width: 10px; border-radius: 2px; flex: none; background: var(--c-light); }}
@media (prefers-color-scheme: dark) {{ .legend-swatch {{ background: var(--c-dark); }} }}
:root[data-theme="dark"] .legend-swatch {{ background: var(--c-dark); }}
.legend-head {{ display: flex; align-items: baseline; gap: 0.5rem; flex-wrap: wrap; }}
.legend-name {{ font-weight: 600; font-size: 0.86rem; }}
.legend-size {{ font-family: var(--mono); font-size: 0.82rem; color: var(--accent); font-variant-numeric: tabular-nums; }}
.legend-count {{ font-size: 0.76rem; color: var(--ink-dim); }}
.git-card {{ background: color-mix(in srgb, var(--ink-dim) 6%, var(--bg-raised)); border: 1px dashed var(--border); border-radius: var(--radius); padding: 1rem 1.25rem; margin: 0 0 2rem; }}
.git-card-head {{ display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.35rem; }}
.git-card-title {{ font-weight: 600; font-size: 0.88rem; }}
.git-card-total {{ font-family: var(--mono); font-size: 0.85rem; color: var(--ink-dim); }}
.git-card-note {{ font-size: 0.8rem; color: var(--ink-dim); margin: 0 0 0.75rem; max-width: 72ch; }}
.git-list {{ display: grid; gap: 0.25rem; font-family: var(--mono); font-size: 0.78rem; }}
.flag-row {{ display: grid; grid-template-columns: 5em 10em 1fr 1fr; gap: 0.75rem; }}
.flag-size, .flag-cat {{ color: var(--ink-dim); }}
.toolbar {{ display: flex; gap: 0.75rem; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; }}
.toolbar input[type="search"] {{ font-family: var(--mono); font-size: 0.85rem; padding: 0.5rem 0.7rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--bg-raised); color: var(--ink); min-width: 260px; flex: 1; }}
.toolbar .count {{ font-size: 0.8rem; color: var(--ink-dim); font-family: var(--mono); }}
.clear-btn {{ font-size: 0.78rem; padding: 0.4rem 0.7rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--bg-raised); color: var(--ink-dim); cursor: pointer; }}
.table-scroll {{ overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); background: var(--bg-raised); }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
thead th {{ text-align: left; font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink-dim); padding: 0.65rem 0.9rem; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: var(--bg-raised); cursor: pointer; white-space: nowrap; }}
thead th.sorted::after {{ content: " \\2193"; }}
thead th.sorted.asc::after {{ content: " \\2191"; }}
tbody td {{ padding: 0.5rem 0.9rem; border-bottom: 1px solid var(--border); vertical-align: top; }}
tbody tr:hover {{ background: color-mix(in srgb, var(--accent) 6%, transparent); }}
.col-size {{ font-family: var(--mono); text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
.col-scope {{ font-family: var(--mono); color: var(--ink-dim); font-size: 0.78rem; white-space: nowrap; }}
.col-path {{ font-family: var(--mono); font-size: 0.8rem; }}
.path {{ white-space: nowrap; }}
.tag {{ display: inline-block; font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 2px; background: color-mix(in srgb, var(--c-light) 16%, var(--bg-raised)); color: var(--c-light); border: 1px solid color-mix(in srgb, var(--c-light) 40%, transparent); white-space: nowrap; }}
@media (prefers-color-scheme: dark) {{ .tag {{ color: var(--c-dark); background: color-mix(in srgb, var(--c-dark) 14%, var(--bg-raised)); border-color: color-mix(in srgb, var(--c-dark) 40%, transparent); }} }}
:root[data-theme="dark"] .tag {{ color: var(--c-dark); background: color-mix(in srgb, var(--c-dark) 14%, var(--bg-raised)); }}
tr.hidden {{ display: none; }}
</style>
<div class="wrap">
  <header>
    <h1>macOS account cleanup report</h1>
    <p class="sub">Nothing has been deleted. Review, filter, and pick what to clean up.</p>
  </header>
  <div class="total-card">
    <div class="total-figure"><span class="num">{total}</span><span class="label">reclaimable across {n_entries} directories</span></div>
    <div class="stackbar">
        {segs_html}
    </div>
  </div>
  <div class="legend">
        {legend_html}
  </div>
  {flagged_section}
  <div class="toolbar">
    <input type="search" id="search" placeholder="Filter by path...">
    <button class="clear-btn" id="clearFilters">Clear filters</button>
    <span class="count" id="visibleCount"></span>
  </div>
  <div class="table-scroll">
    <table id="report-table">
      <thead><tr><th data-key="cat">Category</th><th data-key="size" class="sorted">Size</th><th data-key="scope">Scope</th><th data-key="path">Path</th></tr></thead>
      <tbody>
      {rows_html}
      </tbody>
    </table>
  </div>
</div>
<script>
(function() {{
  var table = document.getElementById('report-table');
  var tbody = table.querySelector('tbody');
  var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
  var searchInput = document.getElementById('search');
  var visibleCount = document.getElementById('visibleCount');
  var activeCats = new Set();
  var sortKey = 'size', sortAsc = false;
  function applyFilters() {{
    var q = searchInput.value.toLowerCase(); var n = 0;
    rows.forEach(function(r) {{
      var show = (!q || r.dataset.path.indexOf(q) !== -1) && (activeCats.size === 0 || activeCats.has(r.dataset.cat));
      r.classList.toggle('hidden', !show); if (show) n++;
    }});
    visibleCount.textContent = n + ' / ' + rows.length + ' shown';
  }}
  function sortRows() {{
    rows.sort(function(a, b) {{
      var av, bv;
      if (sortKey === 'size') {{ av = parseFloat(a.dataset.size); bv = parseFloat(b.dataset.size); }}
      else if (sortKey === 'cat') {{ av = a.dataset.cat; bv = b.dataset.cat; }}
      else if (sortKey === 'scope') {{ av = a.querySelector('.col-scope').textContent; bv = b.querySelector('.col-scope').textContent; }}
      else {{ av = a.dataset.path; bv = b.dataset.path; }}
      if (av < bv) return sortAsc ? -1 : 1; if (av > bv) return sortAsc ? 1 : -1; return 0;
    }});
    rows.forEach(function(r) {{ tbody.appendChild(r); }});
  }}
  table.querySelectorAll('thead th').forEach(function(th) {{
    th.addEventListener('click', function() {{
      var key = th.dataset.key;
      if (sortKey === key) sortAsc = !sortAsc; else {{ sortKey = key; sortAsc = false; }}
      table.querySelectorAll('thead th').forEach(function(t) {{ t.classList.remove('sorted', 'asc'); }});
      th.classList.add('sorted'); if (sortAsc) th.classList.add('asc');
      sortRows();
    }});
  }});
  document.querySelectorAll('.legend-row').forEach(function(row) {{
    row.addEventListener('click', function() {{
      var cat = row.dataset.cat;
      if (activeCats.has(cat)) {{ activeCats.delete(cat); row.classList.remove('active'); }}
      else {{ activeCats.add(cat); row.classList.add('active'); }}
      applyFilters();
    }});
  }});
  searchInput.addEventListener('input', applyFilters);
  document.getElementById('clearFilters').addEventListener('click', function() {{
    searchInput.value = ''; activeCats.clear();
    document.querySelectorAll('.legend-row').forEach(function(r) {{ r.classList.remove('active'); }});
    applyFilters();
  }});
  sortRows(); applyFilters();
}})();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("report_json")
    ap.add_argument("--output", default="account-cleanup-report.html")
    args = ap.parse_args()
    with open(args.report_json) as f:
        data = json.load(f)
    html = build_html(data)
    with open(args.output, "w") as f:
        f.write(html)
    print(f"written {args.output}")


if __name__ == "__main__":
    main()
