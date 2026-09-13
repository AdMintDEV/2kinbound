"""Local dashboard HTML for ranked opportunities."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Forge — Opportunity Pipeline</title>
  <style>
    :root {
      --bg: #0b1020;
      --panel: #141a2e;
      --line: #243049;
      --text: #e8eefc;
      --muted: #93a0c2;
      --strong: #3ee0a1;
      --watch: #f0c14a;
      --weak: #f08a4a;
      --pass: #ef5d7a;
      --accent: #7aa2ff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Inter, system-ui, sans-serif;
      background: radial-gradient(1200px 600px at 10% -10%, #1c2a55 0%, var(--bg) 45%);
      color: var(--text);
    }
    header, main { max-width: 1100px; margin: 0 auto; padding: 24px; }
    h1 { margin: 0 0 8px; font-size: 28px; letter-spacing: 0.02em; }
    p.lede { color: var(--muted); margin: 0 0 24px; }
    .toolbar { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
    button, .file {
      background: var(--accent);
      color: #08101f;
      border: 0;
      border-radius: 8px;
      padding: 10px 14px;
      font-weight: 700;
      cursor: pointer;
    }
    button.secondary { background: #2a3558; color: var(--text); }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 16px;
    }
    .card .label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }
    .card .value { font-size: 28px; margin-top: 6px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
    th { color: var(--muted); font-size: 12px; letter-spacing: 0.06em; }
    .band { font-weight: 700; text-transform: uppercase; font-size: 12px; }
    .strong { color: var(--strong); }
    .watch { color: var(--watch); }
    .weak { color: var(--weak); }
    .pass { color: var(--pass); }
    .bar { height: 8px; background: #22304d; border-radius: 99px; overflow: hidden; width: 120px; }
    .bar > span { display: block; height: 100%; background: var(--accent); }
    .missing { color: var(--weak); font-size: 12px; }
    .detail { color: var(--muted); font-size: 13px; }
    #status { min-height: 20px; color: var(--muted); margin-bottom: 12px; }
    @media (max-width: 800px) {
      .stats { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Forge</h1>
    <p class="lede">Research in. Ranked opportunities out. Missing data lowers the adjusted score instead of inventing conviction.</p>
    <div class="toolbar">
      <button id="reload">Reload ranking</button>
      <button id="rescore" class="secondary">Rescore all</button>
      <label class="file">Load JSON<input id="file" type="file" accept="application/json" hidden /></label>
    </div>
    <div id="status"></div>
    <div class="stats">
      <div class="card"><div class="label">Opportunities</div><div class="value" id="stat-count">0</div></div>
      <div class="card"><div class="label">Strong</div><div class="value strong" id="stat-strong">0</div></div>
      <div class="card"><div class="label">Watch</div><div class="value watch" id="stat-watch">0</div></div>
      <div class="card"><div class="label">Avg score</div><div class="value" id="stat-avg">—</div></div>
    </div>
  </header>
  <main class="card">
    <table>
      <thead>
        <tr>
          <th>Opportunity</th>
          <th>Adjusted</th>
          <th>Band</th>
          <th>Confidence</th>
          <th>Gaps</th>
        </tr>
      </thead>
      <tbody id="rows"></tbody>
    </table>
  </main>
  <script>
    const rows = document.getElementById("rows");
    const status = document.getElementById("status");

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
    }

    function bandClass(band) {
      return band;
    }

    async function fetchJSON(url, options) {
      const response = await fetch(url, options);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Request failed");
      return data;
    }

    function render(items) {
      rows.innerHTML = "";
      const counts = { strong: 0, watch: 0, weak: 0, pass: 0 };
      items.forEach((item) => {
        counts[item.score.band] = (counts[item.score.band] || 0) + 1;
        const tr = document.createElement("tr");
        const missing = escapeHtml((item.score.missing_fields || []).slice(0, 6).join(", ") || "none");
        tr.innerHTML = `
          <td>
            <strong>${escapeHtml(item.record.title)}</strong>
            <div class="detail">${escapeHtml(item.record.summary || "")}</div>
          </td>
          <td>
            ${item.score.adjusted_score.toFixed(1)}
            <div class="bar"><span style="width:${item.score.adjusted_score}%"></span></div>
          </td>
          <td class="band ${bandClass(item.score.band)}">${item.score.band}</td>
          <td>${item.score.confidence.toFixed(0)}%</td>
          <td class="missing">${missing}</td>
        `;
        rows.appendChild(tr);
      });
      document.getElementById("stat-count").textContent = items.length;
      document.getElementById("stat-strong").textContent = counts.strong || 0;
      document.getElementById("stat-watch").textContent = counts.watch || 0;
      const avg = items.length
        ? (items.reduce((sum, item) => sum + item.score.adjusted_score, 0) / items.length).toFixed(1)
        : "—";
      document.getElementById("stat-avg").textContent = avg;
    }

    async function reload() {
      status.textContent = "Loading…";
      const data = await fetchJSON("/api/opportunities");
      render(data.items);
      status.textContent = data.items.length ? "Ranking loaded." : "No scored opportunities yet.";
    }

    document.getElementById("reload").onclick = () => reload().catch((err) => status.textContent = err.message);
    document.getElementById("rescore").onclick = async () => {
      status.textContent = "Rescoring…";
      await fetchJSON("/api/pipeline/rescore", { method: "POST" });
      await reload();
    };
    document.getElementById("file").onchange = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      let payload;
      try {
        payload = JSON.parse(await file.text());
      } catch (err) {
        status.textContent = "Invalid JSON file.";
        return;
      }
      status.textContent = "Running pipeline…";
      const result = await fetchJSON("/api/pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      status.textContent = `Ingested ${result.ingested}, scored ${result.scored}, skipped ${result.skipped}.`;
      await reload();
    };
    reload().catch((err) => status.textContent = err.message);
  </script>
</body>
</html>
"""
