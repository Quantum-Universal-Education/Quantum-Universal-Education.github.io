// Quantum Circuit Playground — React 18 + htm (no build step).
// Statevector simulator for up to 4 qubits. Qubit 0 is the least significant
// bit, and kets are printed as |q(n-1) ... q1 q0⟩ (Qiskit convention).

const { useState, useMemo, useEffect } = React;
const html = htm.bind(React.createElement);

const COLS = 8;
const S2 = Math.SQRT1_2;

// 2x2 gates as [[re, im], ...] in row-major order: [a, b, c, d]
const C = (re, im = 0) => [re, im];
const GATES = {
  H: { label: "H", m: [C(S2), C(S2), C(S2), C(-S2)], info: "Hadamard: creates superposition" },
  X: { label: "X", m: [C(0), C(1), C(1), C(0)], info: "Pauli-X: bit flip" },
  Y: { label: "Y", m: [C(0), C(0, -1), C(0, 1), C(0)], info: "Pauli-Y: bit and phase flip" },
  Z: { label: "Z", m: [C(1), C(0), C(0), C(-1)], info: "Pauli-Z: phase flip" },
  S: { label: "S", m: [C(1), C(0), C(0), C(0, 1)], info: "S: quarter-turn phase (√Z)" },
  SDG: { label: "S†", m: [C(1), C(0), C(0), C(0, -1)], info: "S†: inverse of S" },
  T: { label: "T", m: [C(1), C(0), C(0), C(S2, S2)], info: "T: eighth-turn phase (√S)" },
  TDG: { label: "T†", m: [C(1), C(0), C(0), C(S2, -S2)], info: "T†: inverse of T" },
  CTRL: { label: "●", info: "Control: every other gate in this column acts only when all controls are |1⟩" },
  TARG: { label: "⊕", info: "Target: X applied when all controls in the column are |1⟩" },
};
const PALETTE = ["H", "X", "Y", "Z", "S", "SDG", "T", "TDG", "CTRL", "TARG"];

const emptyGrid = (n) => Array.from({ length: n }, () => Array(COLS).fill(null));

const PRESETS = {
  "Superposition": { n: 1, ops: [[0, 0, "H"]] },
  "Bell state": { n: 2, ops: [[0, 0, "H"], [0, 1, "CTRL"], [1, 1, "TARG"]] },
  "GHZ (3 qubits)": { n: 3, ops: [[0, 0, "H"], [0, 1, "CTRL"], [1, 1, "TARG"], [1, 2, "CTRL"], [2, 2, "TARG"]] },
  "Phase kickback": { n: 2, ops: [[1, 0, "X"], [0, 1, "H"], [1, 1, "H"], [0, 2, "CTRL"], [1, 2, "TARG"], [0, 3, "H"], [1, 3, "H"]] },
  "Toffoli (AND)": { n: 3, ops: [[0, 0, "X"], [1, 0, "X"], [0, 1, "CTRL"], [1, 1, "CTRL"], [2, 1, "TARG"]] },
  // Compiled order finding for N = 15, a = 11 (period r = 2).
  // q0, q1: counting register. q2, q3: bits 1 and 3 of the work register,
  // which holds 11^x mod 15 ∈ {1 = 0001, 11 = 1011}; bits 0 and 2 never change.
  "Shor: factor 15 (a = 11)": {
    n: 4,
    ops: [
      [0, 0, "H"], [1, 0, "H"],
      [0, 1, "CTRL"], [2, 1, "TARG"], [3, 1, "TARG"],
      [0, 2, "CTRL"], [1, 2, "TARG"],
      [1, 3, "CTRL"], [0, 3, "TARG"],
      [0, 4, "CTRL"], [1, 4, "TARG"],
      [0, 5, "H"],
      [0, 6, "CTRL"], [1, 6, "SDG"],
      [1, 7, "H"],
    ],
    note: "shor",
  },
};

function presetGrid(name) {
  const p = PRESETS[name];
  const g = emptyGrid(p.n);
  p.ops.forEach(([q, c, k]) => (g[q][c] = k));
  return g;
}

// ---- simulator ----
function simulate(grid, noise = null) {
  const n = grid.length;
  const dim = 1 << n;
  let re = new Float64Array(dim), im = new Float64Array(dim);
  re[0] = 1;

  const apply1 = (q, m, ctrlMask = 0) => {
    const bit = 1 << q;
    for (let i = 0; i < dim; i++) {
      if (i & bit || (i & ctrlMask) !== ctrlMask) continue;
      const j = i | bit;
      const [ar, ai, br, bi] = [re[i], im[i], re[j], im[j]];
      const [[m0r, m0i], [m1r, m1i], [m2r, m2i], [m3r, m3i]] = m;
      re[i] = m0r * ar - m0i * ai + m1r * br - m1i * bi;
      im[i] = m0r * ai + m0i * ar + m1r * bi + m1i * br;
      re[j] = m2r * ar - m2i * ai + m3r * br - m3i * bi;
      im[j] = m2r * ai + m2i * ar + m3r * bi + m3i * br;
    }
  };

  const applyDamping = (q, p) => {
    if (p <= 0) return;
    const bit = 1 << q;
    let excited = 0;
    for (let i = 0; i < dim; i++) if (i & bit) excited += re[i] ** 2 + im[i] ** 2;
    const jumpProbability = p * excited;
    if (Math.random() < jumpProbability && excited > 0) {
      for (let i = 0; i < dim; i++) if (!(i & bit)) {
        const j = i | bit;
        re[i] = Math.sqrt(p) * re[j];
        im[i] = Math.sqrt(p) * im[j];
        re[j] = 0; im[j] = 0;
      }
    } else {
      const scale = Math.sqrt(1 - p);
      for (let i = 0; i < dim; i++) if (i & bit) { re[i] *= scale; im[i] *= scale; }
    }
    let norm = 0;
    for (let i = 0; i < dim; i++) norm += re[i] ** 2 + im[i] ** 2;
    if (norm > 0) { const inv = 1 / Math.sqrt(norm); for (let i = 0; i < dim; i++) { re[i] *= inv; im[i] *= inv; } }
  };
  const applyNoiseChannel = (q, p, type) => {
    if (!noise || p <= 0) return;
    if (type === "amplitude_damping") { applyDamping(q, p); return; }
    if (Math.random() >= p) return;
    if (type === "bit_flip") apply1(q, GATES.X.m);
    else if (type === "phase_flip") apply1(q, GATES.Z.m);
    else if (type === "bit_phase_flip") apply1(q, GATES.Y.m);
    else if (type === "phase_damping") {
      const phaseError = (1 - Math.sqrt(1 - p)) / 2;
      if (Math.random() < phaseError) apply1(q, GATES.Z.m);
    } else {
      const pauli = ["X", "Y", "Z"][Math.floor(Math.random() * 3)];
      apply1(q, GATES[pauli].m);
    }
  };
  const applyOneQubitNoise = (q, p) => applyNoiseChannel(q, p, noise?.type || "depolarizing");
  const applyTwoQubitNoise = (qa, qb, p) => {
    if (!noise || p <= 0) return;
    const type = noise.type || "depolarizing";
    if (type === "amplitude_damping") {
      applyDamping(qa, p); applyDamping(qb, p); return;
    }
    if (type === "phase_damping") {
      applyNoiseChannel(qa, p, type); applyNoiseChannel(qb, p, type); return;
    }
    if (Math.random() >= p) return;
    const paulis = ["I", "X", "Y", "Z"];
    if (type === "bit_flip") {
      if (Math.random() < 0.5) apply1(qa, GATES.X.m);
      else apply1(qb, GATES.X.m);
    } else if (type === "phase_flip") {
      if (Math.random() < 0.5) apply1(qa, GATES.Z.m);
      else apply1(qb, GATES.Z.m);
    } else if (type === "bit_phase_flip") {
      if (Math.random() < 0.5) apply1(qa, GATES.Y.m);
      else apply1(qb, GATES.Y.m);
    } else {
      const choice = 1 + Math.floor(Math.random() * 15);
      const a = Math.floor(choice / 4), b = choice % 4;
      if (paulis[a] !== "I") apply1(qa, GATES[paulis[a]].m);
      if (paulis[b] !== "I") apply1(qb, GATES[paulis[b]].m);
    }
  };

  for (let c = 0; c < COLS; c++) {
    let ctrlMask = 0;
    const controls = [];
    const targets = [];
    for (let q = 0; q < n; q++) {
      const g = grid[q][c];
      if (g === "CTRL") { ctrlMask |= 1 << q; controls.push(q); }
      else if (g === "TARG") targets.push(q);
    }
    for (let q = 0; q < n; q++) {
      const g = grid[q][c];
      if (g && GATES[g].m) {
        apply1(q, GATES[g].m, ctrlMask);
        if (controls.length) controls.forEach((control) => applyTwoQubitNoise(control, q, noise?.p2 || 0));
        else applyOneQubitNoise(q, noise?.p1 || 0);
      }
    }
    for (const t of targets) {
      const bit = 1 << t;
      for (let i = 0; i < dim; i++) {
        if (i & bit || (i & ctrlMask) !== ctrlMask) continue;
        const j = i | bit;
        [re[i], re[j]] = [re[j], re[i]];
        [im[i], im[j]] = [im[j], im[i]];
      }
      if (controls.length) controls.forEach((control) => applyTwoQubitNoise(control, t, noise?.p2 || 0));
      else applyOneQubitNoise(t, noise?.p1 || 0);
    }
  }
  return Array.from({ length: dim }, (_, i) => ({
    i,
    ket: i.toString(2).padStart(n, "0"),
    re: Math.abs(re[i]) < 1e-12 ? 0 : re[i],
    im: Math.abs(im[i]) < 1e-12 ? 0 : im[i],
    p: re[i] * re[i] + im[i] * im[i],
  }));
}

// Monte Carlo shots: each shot gets an independent stochastic noise trajectory
// followed by a computational-basis measurement.
function runNoisyShots(grid, ideal, type, p1, p2, shots) {
  const counts = Array(1 << grid.length).fill(0);
  let fidelitySum = 0;
  for (let shot = 0; shot < shots; shot++) {
    const state = simulate(grid, { type, p1, p2 });
    let overlapRe = 0, overlapIm = 0;
    for (let i = 0; i < state.length; i++) {
      overlapRe += ideal[i].re * state[i].re + ideal[i].im * state[i].im;
      overlapIm += ideal[i].re * state[i].im - ideal[i].im * state[i].re;
    }
    fidelitySum += overlapRe * overlapRe + overlapIm * overlapIm;
    let r = Math.random(), outcome = state[state.length - 1].i;
    for (const item of state) { r -= item.p; if (r <= 0) { outcome = item.i; break; } }
    counts[outcome]++;
  }
  return {
    fidelity: fidelitySum / shots,
    rows: counts.map((count, i) => ({
      i, ket: i.toString(2).padStart(grid.length, "0"), count, probability: count / shots,
    })),
  };
}

// ---- OpenQASM 2.0 export ----
// Same order as simulate(): single-qubit gates first, then controlled-X per column.
// Gates in one column act on different qubits and share the same controls, so they commute.
const MCX = ["x", "cx", "ccx", "c3x"];
const QASM1 = { H: "h", X: "x", Y: "y", Z: "z", S: "s", SDG: "sdg", T: "t", TDG: "tdg" };
const QASM_CTRL = { H: "ch", X: "cx", Y: "cy", Z: "cz", S: "cu1(pi/2)", SDG: "cu1(-pi/2)", T: "cu1(pi/4)", TDG: "cu1(-pi/4)" };
// Two-qubit gate count of each singly-controlled gate, as qregime's profile() reports it.
const CTRL_COST = { H: 2, X: 1, Y: 1, Z: 1, S: 2, SDG: 2, T: 2, TDG: 2 };
function toQasm(grid) {
  const n = grid.length;
  const lines = ["OPENQASM 2.0;", 'include "qelib1.inc";', `qreg q[${n}];`, `creg c[${n}];`];
  for (let c = 0; c < COLS; c++) {
    const ctrls = [];
    const targs = [];
    for (let q = 0; q < n; q++) if (grid[q][c] === "CTRL") ctrls.push(q);
    for (let q = 0; q < n; q++) {
      const g = grid[q][c];
      if (g === "TARG") targs.push(q);
      else if (g && g !== "CTRL") {
        if (ctrls.length === 0) lines.push(`${QASM1[g]} q[${q}];`);
        else if (ctrls.length === 1) lines.push(`${QASM_CTRL[g]} q[${ctrls[0]}],q[${q}];`);
        else lines.push(`// not in qelib1: ${GATES[g].label} on q[${q}] with ${ctrls.length} controls`);
      }
    }
    for (const t of targs) {
      const args = [...ctrls, t].map((q) => `q[${q}]`).join(",");
      lines.push(`${MCX[ctrls.length]} ${args};`);
    }
  }
  lines.push("measure q -> c;");
  return lines.join("\n") + "\n";
}

// ---- gate counts (two-qubit count drives qregime's analytic proxy) ----
// Standard decompositions: CCX = 6 CX, C3X = 14 CX (Barenco et al. / Qiskit).
const CX_COST = [0, 1, 6, 14];
function gateCounts(grid) {
  const n = grid.length;
  let oneQ = 0, twoQ = 0, depth = 0, unsupported = 0;
  for (let c = 0; c < COLS; c++) {
    let ctrls = 0, used = false;
    for (let q = 0; q < n; q++) if (grid[q][c] === "CTRL") ctrls++;
    for (let q = 0; q < n; q++) {
      const g = grid[q][c];
      if (g && GATES[g].m) {
        used = true;
        if (ctrls === 0) oneQ++;
        else if (ctrls === 1) twoQ += CTRL_COST[g];
        else unsupported++;
      }
      if (g === "TARG") { used = true; ctrls === 0 ? oneQ++ : (twoQ += CX_COST[ctrls]); }
    }
    if (used) depth++;
  }
  return { oneQ, twoQ, depth, unsupported };
}

// ---- expectation values ⟨ψ|P|ψ⟩ for a Pauli string ----
// String is written like a ket: leftmost character acts on q(n-1).
function pauliExpectation(state, pauli) {
  const n = pauli.length;
  let xmask = 0;
  const ops = [];
  for (let k = 0; k < n; k++) {
    const q = n - 1 - k;
    const p = pauli[k];
    ops.push([q, p]);
    if (p === "X" || p === "Y") xmask |= 1 << q;
  }
  let sum = 0;
  for (const s of state) {
    // P|i⟩ = phase · |i ^ xmask⟩
    let pr = 1, pi = 0;
    for (const [q, p] of ops) {
      const bit = (s.i >> q) & 1;
      if (p === "Z" && bit) { pr = -pr; pi = -pi; }
      if (p === "Y") {
        // Y|0⟩ = i|1⟩, Y|1⟩ = −i|0⟩
        const f = bit ? -1 : 1;
        [pr, pi] = [-pi * f, pr * f];
      }
    }
    const j = state[s.i ^ xmask];
    // conj(ψ_j) · phase · ψ_i, real part
    const ar = pr * s.re - pi * s.im;
    const ai = pr * s.im + pi * s.re;
    sum += j.re * ar + j.im * ai;
  }
  return Math.abs(sum) < 1e-12 ? 0 : sum;
}

// Hardware profiles and p_2q values copied from qregime (src/qregime/tool.py).
const HARDWARE = [
  { key: "superconductor_ibm", name: "Superconducting (IBM heavy-hex)", p2q: 0.0032 },
  { key: "trapped_ion_quantinuum_h2", name: "Trapped-ion Quantinuum H2", p2q: 0.001 },
  { key: "trapped_ion_ionq_oxford", name: "Trapped-ion IonQ/Oxford Ionics", p2q: 0.0001 },
];

// ---- URL sharing: #n=3&c=H.0.0,CTRL.0.1,TARG.1.1 ----
function encode(grid) {
  const ops = [];
  grid.forEach((row, q) => row.forEach((g, c) => g && ops.push(`${g}.${q}.${c}`)));
  return `n=${grid.length}&c=${ops.join(",")}`;
}
function decode(hash) {
  const params = new URLSearchParams(hash.replace(/^#/, ""));
  const n = Math.min(4, Math.max(1, parseInt(params.get("n"), 10) || 0));
  if (!params.get("n")) return null;
  const g = emptyGrid(n);
  (params.get("c") || "").split(",").filter(Boolean).forEach((tok) => {
    const [k, q, c] = tok.split(".");
    if (GATES[k] && +q < n && +c < COLS) g[+q][+c] = k;
  });
  return g;
}

const fmt = (x) => (x === 0 ? "0" : x.toFixed(3).replace(/\.?0+$/, ""));
const fmtAmp = ({ re, im }) => {
  if (re === 0 && im === 0) return "0";
  if (im === 0) return fmt(re);
  if (re === 0) return `${fmt(im)}i`;
  return `${fmt(re)} ${im < 0 ? "−" : "+"} ${fmt(Math.abs(im))}i`;
};
const phaseHue = ({ re, im }) => ((Math.atan2(im, re) * 180) / Math.PI + 360) % 360;

// ---- components ----
function Palette({ selected, onSelect }) {
  return html`
    <div class="pg-palette" role="toolbar" aria-label="Gates">
      ${PALETTE.map(
        (k) => html`
          <button key=${k} type="button" class=${"pg-gate" + (selected === k ? " is-selected" : "")}
            title=${GATES[k].info} aria-pressed=${selected === k} onClick=${() => onSelect(k)}>
            ${GATES[k].label}
          </button>`
      )}
      <button type="button" class=${"pg-gate pg-erase" + (selected === null ? " is-selected" : "")}
        title="Eraser: click a cell to remove its gate" aria-pressed=${selected === null} onClick=${() => onSelect(null)}>⌫</button>
    </div>`;
}

function Circuit({ grid, onCell }) {
  return html`
    <div class="pg-circuit">
      ${grid.map(
        (row, q) => html`
          <div class="pg-wire" key=${q}>
            <span class="pg-qlabel mono">q${q} |0⟩</span>
            <div class="pg-cells">
              ${row.map((g, c) => {
                const colHasCtrl = grid.some((r) => r[c] === "CTRL");
                const colHasTarget = grid.some((r) => r[c] && r[c] !== "CTRL");
                const linked = colHasCtrl && colHasTarget && !!g;
                return html`
                  <button key=${c} type="button" class=${"pg-cell" + (g ? " has-gate" : "") + (linked ? " is-linked" : "") + (g === "CTRL" || g === "TARG" ? " is-ctrl" : "")}
                    aria-label=${`qubit ${q}, step ${c + 1}${g ? ": " + GATES[g].info : ""}`}
                    onClick=${() => onCell(q, c)}>
                    ${g ? GATES[g].label : ""}
                  </button>`;
              })}
            </div>
          </div>`
      )}
    </div>`;
}

function Results({ state }) {
  const top = state.reduce((a, b) => (b.p > a.p ? b : a), state[0]);
  return html`
    <div class="pg-results">
      <h3>Measurement probabilities</h3>
      <div class="pg-bars">
        ${state.map(
          (s) => html`
            <div class="pg-bar" key=${s.i} title=${`|${s.ket}⟩: ${(s.p * 100).toFixed(1)}%`}>
              <div class="pg-bar-track"><div class="pg-bar-fill" style=${{ height: `${s.p * 100}%` }}></div></div>
              <span class="pg-bar-pct">${s.p > 0.0005 ? Math.round(s.p * 100) + "%" : ""}</span>
              <span class="pg-bar-ket mono">${s.ket}</span>
            </div>`
        )}
      </div>
      <p class="pg-note">Most likely outcome: <strong class="mono">|${top.ket}⟩</strong> (${(top.p * 100).toFixed(1)}%)</p>

      <h3>State vector</h3>
      <table class="pg-amps">
        <thead><tr><th>Basis</th><th>Amplitude</th><th>Phase</th></tr></thead>
        <tbody>
          ${state.filter((s) => s.p > 1e-9).map(
            (s) => html`
              <tr key=${s.i}>
                <td class="mono">|${s.ket}⟩</td>
                <td class="mono">${fmtAmp(s)}</td>
                <td><span class="pg-phase" style=${{ background: `hsl(${phaseHue(s)} 70% 45%)` }}></span>${Math.round(phaseHue(s))}°</td>
              </tr>`
          )}
        </tbody>
      </table>
    </div>`;
}

function QasmPanel({ grid }) {
  const qasm = useMemo(() => toQasm(grid), [grid]);
  const [msg, setMsg] = useState("");
  useEffect(() => setMsg(""), [qasm]);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(qasm);
      setMsg("Copied ✓");
    } catch {
      setMsg("Select the text and copy it");
    }
  };
  const download = () => {
    const url = URL.createObjectURL(new Blob([qasm], { type: "text/plain" }));
    const a = Object.assign(document.createElement("a"), { href: url, download: "circuit.qasm" });
    a.click();
    URL.revokeObjectURL(url);
  };
  return html`
    <div class="pg-panel">
      <div class="pg-panel-head">
        <h3>OpenQASM 2.0</h3>
        <div class="pg-actions">
          <button type="button" class="btn" onClick=${copy}>${msg || "Copy"}</button>
          <button type="button" class="btn" onClick=${download}>Download .qasm</button>
          <a class="btn primary" href="qregime.html#demo">Analyze in qregime →</a>
        </div>
      </div>
      <pre class="pg-qasm mono">${qasm}</pre>
      <p class="pg-note">Run it through qregime to decide between QEM, partial QEC, and FTQC: <span class="mono">qregime decide circuit.qasm</span>.</p>
    </div>`;
}

const fmtE = (x) => (Math.abs(x) < 5e-4 ? "0.000" : (x < 0 ? "−" : "+") + Math.abs(x).toFixed(3));

function Expectations({ state, n, fidelity }) {
  const [custom, setCustom] = useState("Z".repeat(n));
  useEffect(() => setCustom((s) => (s.length === n ? s : "Z".repeat(n))), [n]);
  const valid = new RegExp(`^[IXYZ]{${n}}$`).test(custom);
  const single = (q, p) => {
    const s = Array(n).fill("I");
    s[n - 1 - q] = p;
    return pauliExpectation(state, s.join(""));
  };
  const pairs = [];
  for (let a = 0; a < n; a++)
    for (let b = a + 1; b < n; b++) {
      const s = Array(n).fill("I");
      s[n - 1 - a] = "Z";
      s[n - 1 - b] = "Z";
      pairs.push({ label: `Z${b}Z${a}`, v: pauliExpectation(state, s.join("")) });
    }
  const customVal = valid ? pauliExpectation(state, custom) : null;
  return html`
    <div class="pg-panel">
      <h3>Expectation values</h3>
      <table class="pg-amps">
        <thead><tr><th>Qubit</th><th>⟨X⟩</th><th>⟨Y⟩</th><th>⟨Z⟩</th></tr></thead>
        <tbody>
          ${Array.from({ length: n }, (_, q) => html`
            <tr key=${q}><td class="mono">q${q}</td>
              ${["X", "Y", "Z"].map((p) => html`<td key=${p} class="mono">${fmtE(single(q, p))}</td>`)}
            </tr>`)}
        </tbody>
      </table>
      ${pairs.length > 0 && html`
        <div class="pg-chips">
          ${pairs.map((p) => html`<span key=${p.label} class="pg-chip mono">⟨${p.label}⟩ = ${fmtE(p.v)}</span>`)}
        </div>`}
      <label class="pg-custom">
        <span>Custom Pauli string (leftmost acts on q${n - 1})</span>
        <input class="mono" value=${custom} maxlength=${n} spellcheck="false"
          onInput=${(e) => setCustom(e.target.value.toUpperCase())} />
        <span class="mono pg-custom-val">
          ${valid
            ? html`ideal ⟨${custom}⟩ = ${fmtE(customVal)} · noisy (IBM profile) ≈ ${fmtE(customVal * fidelity)}`
            : `Use ${n} characters from I, X, Y, Z`}
        </span>
      </label>
    </div>`;
}

function NoiseSimulation({ grid, ideal }) {
  const [type, setType] = useState("depolarizing");
  const [p1, setP1] = useState(0.001);
  const [p2, setP2] = useState(0.01);
  const [shots, setShots] = useState(500);
  const [run, setRun] = useState(0);
  const result = useMemo(() => runNoisyShots(grid, ideal, type, p1, p2, shots), [grid, ideal, type, p1, p2, shots, run]);
  const rows = result.rows.map((item) => ({ ...item, ideal: ideal[item.i]?.p || 0 }));
  const names = {
    depolarizing: "Depolarizing",
    bit_flip: "Bit flip (X)",
    phase_flip: "Phase flip (Z)",
    bit_phase_flip: "Bit-phase flip (Y)",
    amplitude_damping: "Amplitude damping",
    phase_damping: "Phase damping",
  };
  return html`
    <div class="pg-panel pg-noise-lab">
      <h3>Noise Lab · noise channels & fidelity</h3>
      <p class="pg-note">Choose a noise channel and its error probability. The simulator uses stochastic pure-state trajectories (quantum jumps / Pauli errors), then averages state fidelity and measurement outcomes over independent runs. This is a pedagogical channel model, not a hardware-calibrated noise simulator.</p>
      <div class="pg-noise-controls">
        <label>Noise channel
          <select value=${type} onChange=${(e) => setType(e.target.value)}>
            ${Object.entries(names).map(([key, name]) => html`<option key=${key} value=${key}>${name}</option>`)}
          </select>
        </label>
        <label>Single-qubit error probability
          <strong class="mono">${(p1 * 100).toFixed(2)}%</strong>
          <input type="range" min="0" max="0.2" step="0.001" value=${p1} onInput=${(e) => setP1(Number(e.target.value))} />
        </label>
        <label>Two-qubit error probability
          <strong class="mono">${(p2 * 100).toFixed(2)}%</strong>
          <input type="range" min="0" max="0.2" step="0.001" value=${p2} onInput=${(e) => setP2(Number(e.target.value))} />
        </label>
        <label>Monte Carlo trajectories / shots
          <strong class="mono">${shots.toLocaleString()}</strong>
          <input type="range" min="100" max="2000" step="100" value=${shots} onInput=${(e) => setShots(Number(e.target.value))} />
        </label>
      </div>
      <div class="pg-noise-fidelity">
        <span>Average state fidelity</span>
        <strong class="mono">${(result.fidelity * 100).toFixed(2)}%</strong>
        <span class="pg-rel"><span style=${{ width: `${result.fidelity * 100}%` }}></span></span>
        <small>Ideal circuit = 100% · estimated over ${shots.toLocaleString()} trajectories</small>
      </div>
      <div class="pg-actions"><button type="button" class="btn" onClick=${() => setRun((v) => v + 1)}>Run again ↻</button></div>
      <div class="pg-table-scroll">
        <table class="pg-amps">
          <thead><tr><th>Outcome</th><th>Ideal probability</th><th>Noisy counts</th><th>Observed probability</th></tr></thead>
          <tbody>
            ${rows.map((r) => html`<tr key=${r.i}>
              <td class="mono">|${r.ket}⟩</td>
              <td class="mono">${(r.ideal * 100).toFixed(1)}%</td>
              <td class="mono">${r.count.toLocaleString()} / ${shots.toLocaleString()}</td>
              <td><span class="pg-rel"><span style=${{ width: `${r.probability * 100}%` }}></span></span>
                <span class="mono">${(r.probability * 100).toFixed(1)}%</span></td>
            </tr>`)}
          </tbody>
        </table>
      </div>
      <p class="pg-note">Fidelity is the average pure-state overlap squared between each noisy trajectory and the ideal output state. It is not the same as shot-distribution similarity. Increase the trajectory count for a less noisy Monte Carlo estimate.</p>
    </div>`;
}

function NoiseEstimate({ grid }) {
  const { oneQ, twoQ, depth, unsupported } = gateCounts(grid);
  return html`
    <div class="pg-panel">
      <h3>Noise estimate (qregime proxy)</h3>
      <p class="pg-note">
        ${oneQ} single-qubit gates · ${twoQ} two-qubit gates (counted as qregime does: CCX = 6, controlled H/S/T = 2) · depth ${depth}.
        Reliability uses qregime's analytic proxy <span class="mono">(1 − p₂q)^two_qubit_count</span>, which counts two-qubit gate errors only.
        ${unsupported > 0 && html` <strong>${unsupported} multi-controlled gate(s) other than X are simulated but left out of this count and the QASM export.</strong>`}
      </p>
      <table class="pg-amps">
        <thead><tr><th>Hardware profile</th><th>p₂q</th><th>Reliability</th></tr></thead>
        <tbody>
          ${HARDWARE.map((h) => {
            const r = Math.pow(1 - h.p2q, twoQ);
            return html`<tr key=${h.key}>
              <td>${h.name}</td><td class="mono">${h.p2q}</td>
              <td><span class="pg-rel"><span style=${{ width: `${r * 100}%` }}></span></span> <span class="mono">${(r * 100).toFixed(2)}%</span></td>
            </tr>`;
          })}
        </tbody>
      </table>
      <p class="pg-note">The noisy expectation values above scale the ideal ones by this factor (a global depolarizing approximation). For the full decision, with noisy simulation and FTQC cost, use the qregime demo.</p>
    </div>`;
}

const SHOR_KEY = "Shor: factor 15 (a = 11)";
const gcd = (a, b) => (b === 0 ? a : gcd(b, a % b));

// Shown only while the circuit is exactly the Shor preset.
function ShorPanel({ state }) {
  // Marginal distribution of the counting register (q1 q0).
  const counts = [0, 0, 0, 0];
  state.forEach((s) => (counts[s.i & 3] += s.p));
  const rows = counts.map((p, x) => ({ x, bits: x.toString(2).padStart(2, "0"), p, phase: x / 4 }));
  const N = 15, a = 11, r = 2;
  const half = Math.pow(a, r / 2) % N;
  const f1 = gcd(half - 1, N), f2 = gcd(half + 1, N);
  return html`
    <div class="pg-panel pg-shor">
      <h3>How Shor's algorithm factors 15</h3>
      <ol class="pg-steps">
        <li><strong>Superposition.</strong> H on the counting qubits q0, q1 prepares every exponent x = 0…3 at once.</li>
        <li><strong>Modular exponentiation.</strong> The work qubits q2, q3 store 11<sup>x</sup> mod 15. It alternates 1, 11, 1, 11, so only q0 controls it: two CNOTs flip bits 1 and 3 (0001 ↔ 1011).</li>
        <li><strong>Inverse QFT.</strong> A swap (three CNOTs), H, controlled-S†, and H turn that period into a peak in the counting register.</li>
        <li><strong>Classical post-processing.</strong> Read the counting register as x, the phase is x/4, and its denominator is the period r.</li>
      </ol>
      <table class="pg-amps">
        <thead><tr><th>Counting register (q1 q0)</th><th>x</th><th>Phase x/4</th><th>Probability</th></tr></thead>
        <tbody>
          ${rows.map((row) => html`<tr key=${row.x}>
            <td class="mono">|${row.bits}⟩</td><td class="mono">${row.x}</td><td class="mono">${row.phase}</td>
            <td><span class="pg-rel"><span style=${{ width: `${row.p * 100}%` }}></span></span> <span class="mono">${(row.p * 100).toFixed(1)}%</span></td>
          </tr>`)}
        </tbody>
      </table>
      <p class="pg-result mono">
        phase 1/2 ⇒ r = ${r} · 11<sup>r/2</sup> mod 15 = ${half} · gcd(${half} − 1, 15) = ${f1} · gcd(${half} + 1, 15) = ${f2} ⇒ <strong>15 = ${f2} × ${f1}</strong>
      </p>
      <p class="pg-note">
        This is a compiled circuit: it uses the known period to shrink the work register to two qubits, as early hardware demonstrations did.
        A Shor circuit without that shortcut is far larger. On the <a href="qregime.html">qregime page</a>, a 16-qubit Shor-like circuit
        (T-count 3,930) lands in <strong>GAP</strong> on IBM heavy-hex noise and needs partial QEC on Quantinuum H2.
      </p>
    </div>`;
}

function App() {
  const [grid, setGrid] = useState(() => decode(location.hash) || presetGrid("Bell state"));
  const [selected, setSelected] = useState("H");
  const [copied, setCopied] = useState(false);
  const state = useMemo(() => simulate(grid), [grid]);

  useEffect(() => {
    history.replaceState(null, "", "#" + encode(grid));
    setCopied(false);
  }, [grid]);

  const onCell = (q, c) =>
    setGrid((g) => g.map((row, qi) => row.map((v, ci) => (qi === q && ci === c ? (v === selected ? null : selected) : v))));

  const setQubits = (n) =>
    setGrid((g) => Array.from({ length: n }, (_, q) => g[q] || Array(COLS).fill(null)));

  const share = async () => {
    try {
      await navigator.clipboard.writeText(location.href);
      setCopied(true);
    } catch {
      prompt("Copy this link:", location.href);
    }
  };

  return html`
    <div class="pg">
      <div class="pg-toolbar">
        <label>Example
          <select onChange=${(e) => e.target.value && setGrid(presetGrid(e.target.value))} value="">
            <option value="">Load an example…</option>
            ${Object.keys(PRESETS).map((k) => html`<option key=${k} value=${k}>${k}</option>`)}
          </select>
        </label>
        <label>Qubits
          <select value=${grid.length} onChange=${(e) => setQubits(+e.target.value)}>
            ${[1, 2, 3, 4].map((n) => html`<option key=${n} value=${n}>${n}</option>`)}
          </select>
        </label>
        <button type="button" class="btn" onClick=${() => setGrid(emptyGrid(grid.length))}>Clear</button>
        <button type="button" class="btn primary" onClick=${share}>${copied ? "Link copied ✓" : "Share circuit"}</button>
      </div>
      <${Palette} selected=${selected} onSelect=${setSelected} />
      <p class="pg-hint">Pick a gate, then click a cell to place it. Click it again to remove it. ● controls every other gate in its column: ● + ⊕ is a CNOT, two ● + ⊕ a Toffoli, ● + S† a controlled-S†.</p>
      <${Circuit} grid=${grid} onCell=${onCell} />
      ${encode(grid) === encode(presetGrid(SHOR_KEY)) && html`<${ShorPanel} state=${state} />`}
      <${Results} state=${state} />
      <${Expectations} state=${state} n=${grid.length} fidelity=${Math.pow(1 - HARDWARE[0].p2q, gateCounts(grid).twoQ)} />
      <${NoiseSimulation} grid=${grid} ideal=${state} />
      <${NoiseEstimate} grid=${grid} />
      <${QasmPanel} grid=${grid} />
    </div>`;
}

ReactDOM.createRoot(document.getElementById("playground")).render(html`<${App} />`);
