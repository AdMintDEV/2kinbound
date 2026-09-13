const MM_PER_IN = 25.4;
const STEEL_LB_IN3 = 0.2836;
const SIZES = {
  A: { I: 11320, area: 173, od: 25.0, wall: 2.0 },
  B: { I: 8509, area: 114, od: 25.0, wall: 1.2 },
  C: { I: 6695, area: 91, od: 25.0, wall: 1.2 },
  D: { I: 18015, area: 126, od: 35.0, wall: 1.2 },
};
const APPLICATIONS = [
  ["Front Bulkhead", "B", "Aluminum allowed"],
  ["Front Bulkhead Support", "C", "Aluminum allowed"],
  ["Front Hoop", "A", "Aluminum allowed"],
  ["Front Hoop Bracing", "B", "Aluminum allowed"],
  ["Side Impact Structure", "B", "Aluminum allowed"],
  ["Bent / Multi Upper SIS", "D", "Aluminum allowed"],
  ["Main Hoop", "A", "Steel only"],
  ["Main Hoop Bracing", "B", "Steel only"],
  ["Main Hoop Bracing Supports", "C", "Aluminum allowed"],
  ["Harness Attachment", "B", "Aluminum allowed"],
  ["Shoulder Harness Bar", "A", "Steel only"],
  ["Shoulder Harness Bar Bracing", "C", "Aluminum allowed"],
  ["Battery Pack Mounting", "B", "Aluminum allowed"],
  ["Component Protection", "C", "Aluminum allowed"],
  ["Structural Tubing", "C", "Aluminum allowed"],
];
// Teaser only. Full Size A/B/C/D map is merchant-only (Team Pack). Do not expand.
const CATALOG = [
  ["round", 1.0, 0.095],
  ["round", 1.0, 0.083],
  ["round", 1.375, 0.049],
  ["square", 1.0, 0.065],
];

function roundProps(od, wall) {
  const inner = od - 2 * wall;
  if (inner < 0) throw new Error("wall thicker than section");
  const area = Math.PI / 4 * (od * od - inner * inner);
  const I = Math.PI / 64 * (od ** 4 - inner ** 4);
  return { inner, area, I };
}

function squareProps(side, wall) {
  const inner = side - 2 * wall;
  if (inner < 0) throw new Error("wall thicker than section");
  const area = side * side - inner * inner;
  const I = (side ** 4 - inner ** 4) / 12;
  return { inner, area, I };
}

function evaluate(shape, odMm, wallMm) {
  const props = shape === "square" ? squareProps(odMm, wallMm) : roundProps(odMm, wallMm);
  const areaIn2 = props.area / (MM_PER_IN * MM_PER_IN);
  const lbFt = areaIn2 * 12 * STEEL_LB_IN3;
  const sizes = {};
  Object.entries(SIZES).forEach(([name, req]) => {
    const checks = {
      I: props.I + 1e-9 >= req.I,
      area: props.area + 1e-9 >= req.area,
      od: odMm + 1e-9 >= req.od,
      wall: wallMm + 1e-9 >= req.wall,
    };
    sizes[name] = { ...checks, pass: Object.values(checks).every(Boolean) };
  });
  return {
    ...props,
    odMm,
    wallMm,
    lbFt,
    sizes,
    warning: Math.abs(odMm - 25) < 0.05 && wallMm <= 2.01,
  };
}

function nest(lengths, stock, kerf, endTrim) {
  const usable = stock - 2 * endTrim;
  const pieces = lengths.filter((n) => n > 0).sort((a, b) => b - a);
  const tooLong = pieces.filter((n) => n > usable);
  if (tooLong.length) throw new Error("A piece is longer than usable stock (" + usable.toFixed(2) + ")");
  const sticks = [];
  const remainders = [];
  pieces.forEach((length) => {
    let placed = false;
    for (let i = 0; i < remainders.length; i += 1) {
      const extra = sticks[i].length ? kerf : 0;
      if (length + extra <= remainders[i] + 1e-9) {
        sticks[i].push(length);
        remainders[i] -= length + extra;
        placed = true;
        break;
      }
    }
    if (!placed) {
      sticks.push([length]);
      remainders.push(usable - length);
    }
  });
  return { usable, sticks, remainders, count: sticks.length, cut: pieces.reduce((a, b) => a + b, 0), waste: remainders.reduce((a, b) => a + b, 0) };
}

function fmt(n, d) { return Number(n).toFixed(d); }
function mark(ok) { return ok ? '<span class="pass">PASS</span>' : '<span class="fail">FAIL</span>'; }

function toMm(value, units) { return units === "in" ? value * MM_PER_IN : value; }

function renderChecker() {
  const status = document.getElementById("check-status");
  try {
    const units = document.getElementById("units").value;
    const shape = document.getElementById("shape").value;
    const od = toMm(Number(document.getElementById("od").value), units);
    const wall = toMm(Number(document.getElementById("wall").value), units);
    const result = evaluate(shape, od, wall);
    document.getElementById("m-area").textContent = fmt(result.area, 1);
    document.getElementById("m-i").textContent = fmt(result.I, 0);
    document.getElementById("m-mass").textContent = fmt(result.lbFt, 3);
    document.getElementById("m-id").textContent = fmt(result.inner, 2);
    const rows = Object.keys(SIZES).map((name) => {
      const s = result.sizes[name];
      return `<tr><td>Size ${name}</td><td>${mark(s.I)}</td><td>${mark(s.area)}</td><td>${mark(s.od)}</td><td>${mark(s.wall)}</td><td>${mark(s.pass)}</td></tr>`;
    }).join("");
    document.getElementById("size-rows").innerHTML = rows;
    let note = "Unofficial check against published 2026 F.3.4.1 minima. Official SES still governs.";
    if (result.warning) note = "Min OD + min wall is not enough. This 25 mm × 2.0 mm style section fails I and/or area for Size A — the rules say this explicitly.";
    if (Math.abs(od - 34.925) < 0.02) note = "1.375 in = 34.925 mm, which is 0.075 mm under the 35.0 mm Size D OD minimum. The published example size fails a strict millimeter table.";
    status.textContent = note;
  } catch (err) {
    status.textContent = err.message;
  }
}

function renderApps() {
  document.getElementById("app-rows").innerHTML = APPLICATIONS.map(([name, size, note]) =>
    `<tr><td>${name}</td><td>Size ${size}</td><td>${note}</td></tr>`
  ).join("");
}

function renderCatalog() {
  document.getElementById("cat-rows").innerHTML = CATALOG.map(([shape, od, wall]) => {
    const r = evaluate(shape, od * MM_PER_IN, wall * MM_PER_IN);
    const flags = ["A", "B", "C", "D"].map((s) => mark(r.sizes[s].pass)).join("</td><td>");
    return `<tr><td>${shape}</td><td>${od} × ${wall}</td><td>${fmt(r.area, 1)}</td><td>${fmt(r.I, 0)}</td><td>${fmt(r.lbFt, 3)}</td><td>${flags}</td></tr>`;
  }).join("");
}

function parseLengths(text) {
  return text.split(/[\s,;]+/).map((n) => Number(n)).filter((n) => !Number.isNaN(n) && n > 0);
}

function renderNest() {
  const status = document.getElementById("nest-status");
  try {
    const units = document.getElementById("nest-units").value;
    const lengths = parseLengths(document.getElementById("cuts").value);
    if (!lengths.length) throw new Error("Paste cut lengths first.");
    const stock = Number(document.getElementById("stock").value);
    const kerf = Number(document.getElementById("kerf").value);
    const trim = Number(document.getElementById("trim").value);
    const price = Number(document.getElementById("price").value);
    const plan = nest(lengths, stock, kerf, trim);
    const cost = plan.count * stock * (units === "in" ? price / 12 : price / 1000);
    document.getElementById("nest-out").innerHTML = plan.sticks.map((stick, i) =>
      `<tr><td>${i + 1}</td><td>${stick.map((n) => fmt(n, 2)).join(" + ")}</td><td>${fmt(plan.remainders[i], 2)}</td></tr>`
    ).join("");
    status.textContent = `${plan.count} stick(s), ${fmt(plan.cut, 1)} ${units} cut, leftover ${fmt(plan.waste, 1)} ${units}. Material ≈ $${fmt(cost, 2)} at the $/ft or $/m you entered (not a supplier quote).`;
    window.lastNestCsv = ["stick,cuts,remainder"].concat(
      plan.sticks.map((stick, i) => `${i + 1},"${stick.join(" ")}",${plan.remainders[i].toFixed(3)}`)
    ).join("\n");
  } catch (err) {
    status.textContent = err.message;
  }
}

function downloadNest() {
  if (!window.lastNestCsv) {
    renderNest();
  }
  if (!window.lastNestCsv) return;
  const blob = new Blob([window.lastNestCsv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "stick-buy-list.csv";
  a.click();
  URL.revokeObjectURL(url);
}

function applyPreset(od, wall, shape) {
  document.getElementById("units").value = "in";
  document.getElementById("shape").value = shape || "round";
  document.getElementById("od").value = od;
  document.getElementById("wall").value = wall;
  renderChecker();
}

function setupPay() {
  const cfg = window.TUBECHECK_PAY || {};
  const btn = document.getElementById("buy");
  const note = document.getElementById("pay-note");
  if (cfg.paymentUrl) {
    btn.href = cfg.paymentUrl;
    btn.textContent = `Buy Team Pack — $${cfg.priceUsd || 9}`;
    note.textContent = "Checkout delivers the catalog (Payhip download or Stripe file attachment). This site does not host the paid file.";
  } else {
    btn.href = "./pack.html";
    btn.textContent = "Team Pack — checkout not connected";
    note.textContent = "The checker above is free. The $9 pack is not a download on this site. Owner: attach the catalog to Payhip or a Stripe Payment Link, then paste the URL into docs/config.js (see PAYMENT.md).";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderApps();
  renderCatalog();
  applyPreset(1, 0.095, "round");
  document.getElementById("run").onclick = renderChecker;
  document.getElementById("nest-run").onclick = renderNest;
  document.getElementById("nest-dl").onclick = downloadNest;
  setupPay();
});
