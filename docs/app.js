(() => {
  const state = {
    tools: [],
    job: "all",
    license: "all",
    deployment: "all",
    reqifOnly: false,
    query: "",
    compareIds: ["strictdoc", "reqview", "jama-connect"],
  };

  const els = {
    grid: document.getElementById("tool-grid"),
    count: document.getElementById("results-count"),
    search: document.getElementById("filter-search"),
    license: document.getElementById("filter-license"),
    deployment: document.getElementById("filter-deployment"),
    reqif: document.getElementById("filter-reqif"),
    jobButtons: document.querySelectorAll("[data-job]"),
    compareTable: document.getElementById("compare-table"),
    matcherWorkflow: document.getElementById("match-workflow"),
    matcherRegulated: document.getElementById("match-regulated"),
    matcherBudget: document.getElementById("match-budget"),
    matcherResults: document.getElementById("matcher-results"),
    copyPrBtn: document.getElementById("copy-pr-btn"),
    prSnippet: document.getElementById("pr-snippet"),
  };

  function escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function filteredTools() {
    const q = state.query.trim().toLowerCase();
    return state.tools.filter((tool) => {
      if (state.job !== "all" && !tool.jobs.includes(state.job)) return false;
      if (state.license !== "all" && tool.license_type !== state.license) return false;
      if (state.deployment !== "all" && !tool.deployment.includes(state.deployment)) return false;
      if (state.reqifOnly && !tool.capabilities.reqif) return false;
      if (q) {
        const hay = `${tool.name} ${tool.tagline} ${tool.best_for} ${(tool.compliance || []).join(" ")}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }

  function renderGrid() {
    const list = filteredTools();
    els.count.textContent = `${list.length} of ${state.tools.length} tools shown`;

    if (!list.length) {
      els.grid.innerHTML = `<div class="cut tool-card"><h3 class="tool-card__name">No matching tools</h3><p class="tool-card__tagline">Clear one or more filters to view all ${state.tools.length} verified requirements management tools.</p></div>`;
      return;
    }

    els.grid.innerHTML = list
      .map((tool) => {
        const caps = tool.capabilities;
        const isCompared = state.compareIds.includes(tool.id);
        const capItems = [
          ["Traceability", caps.traceability_matrix],
          ["ReqIF", caps.reqif],
          ["Baselines", caps.baselines],
          ["Git", caps.git_integration],
          ["Test linking", caps.test_linking],
        ];
        const complianceText = tool.compliance.length
          ? tool.compliance.join(", ")
          : "General engineering";
        const githubLink = tool.github
          ? `<a href="${escapeHtml(tool.github)}" target="_blank" rel="noopener">GitHub</a>`
          : "";

        return `
          <article class="cut tool-card" data-id="${escapeHtml(tool.id)}">
            <div class="tool-card__top">
              <h3 class="tool-card__name">${escapeHtml(tool.name)}</h3>
              <span class="tool-card__license">${escapeHtml(tool.license_name)}</span>
            </div>
            <p class="tool-card__tagline">${escapeHtml(tool.tagline)}</p>
            <p class="tool-card__meta">Pricing: ${escapeHtml(tool.pricing)}</p>
            <p class="tool-card__meta">Standards: ${escapeHtml(complianceText)}</p>
            <div class="tool-card__caps">
              ${capItems
                .map(
                  ([label, yes]) =>
                    `<span class="cap-tag ${yes ? "cap-tag--yes" : ""}">${escapeHtml(label)}: ${yes ? "Yes" : "No"}</span>`
                )
                .join("")}
            </div>
            <div class="tool-card__foot">
              <div class="tool-card__links">
                <a href="${escapeHtml(tool.website)}" target="_blank" rel="noopener">Official site</a>
                ${githubLink}
              </div>
              <button type="button" class="key key--sm ${isCompared ? "key--active" : ""}" data-compare="${escapeHtml(tool.id)}">
                ${isCompared ? "In compare" : "Compare"}
              </button>
            </div>
          </article>
        `;
      })
      .join("");
  }

  function renderComparison() {
    const selected = state.compareIds
      .map((id) => state.tools.find((t) => t.id === id))
      .filter(Boolean);

    if (!selected.length) {
      els.compareTable.innerHTML = `<tbody><tr><td>Select up to 3 tools from the directory above to compare capabilities side by side.</td></tr></tbody>`;
      return;
    }

    const rows = [
      ["License", (t) => `${t.license_type} (${t.license_name})`],
      ["Deployment", (t) => t.deployment.join(", ")],
      ["Pricing", (t) => t.pricing],
      ["Traceability matrix", (t) => (t.capabilities.traceability_matrix ? "Yes" : "No")],
      ["ReqIF import/export", (t) => (t.capabilities.reqif ? "Yes" : "No")],
      ["Baselines & versioning", (t) => (t.capabilities.baselines ? "Yes" : "No")],
      ["Impact analysis", (t) => (t.capabilities.impact_analysis ? "Yes" : "No")],
      ["Git integration", (t) => (t.capabilities.git_integration ? "Yes" : "No")],
      ["Test case linking", (t) => (t.capabilities.test_linking ? "Yes" : "No")],
      ["Compliance standards", (t) => (t.compliance.length ? t.compliance.join(", ") : "General")],
      ["Best for", (t) => t.best_for],
    ];

    const headCells = selected
      .map((t) => `<th>${escapeHtml(t.name)}</th>`)
      .join("");

    const bodyRows = rows
      .map(([label, fn]) => {
        const cells = selected.map((t) => `<td>${escapeHtml(fn(t))}</td>`).join("");
        return `<tr><th scope="row">${escapeHtml(label)}</th>${cells}</tr>`;
      })
      .join("");

    els.compareTable.innerHTML = `
      <thead><tr><th>Capability</th>${headCells}</tr></thead>
      <tbody>${bodyRows}</tbody>
    `;
  }

  function renderMatcher() {
    if (!state.tools.length) return;
    const workflow = els.matcherWorkflow.value;
    const regulated = els.matcherRegulated.value === "yes";
    const budget = els.matcherBudget.value;

    const ranked = state.tools
      .map((tool) => {
        let score = 0;
        if (tool.jobs.includes(workflow)) score += 4;
        if (regulated) {
          if (tool.compliance.length) score += 3;
          if (tool.capabilities.traceability_matrix && tool.capabilities.baselines) score += 2;
          if (tool.capabilities.reqif) score += 1;
        } else if (tool.jobs.includes("agile") || tool.jobs.includes("git-native")) {
          score += 2;
        }
        if (budget === "free" && tool.license_type === "open-source") score += 4;
        if (budget === "freemium" && ["open-source", "freemium"].includes(tool.license_type)) score += 3;
        if (budget === "enterprise" && tool.category === "enterprise-alm") score += 2;
        return { tool, score };
      })
      .sort((a, b) => b.score - a.score || b.tool.compliance.length - a.tool.compliance.length)
      .slice(0, 3);

    els.matcherResults.innerHTML = ranked
      .map(({ tool }, index) => {
        const gh = tool.github
          ? ` · <a href="${escapeHtml(tool.github)}" target="_blank" rel="noopener">GitHub</a>`
          : "";
        return `
          <div class="cut tool-card">
            <div class="tool-card__top">
              <h3 class="tool-card__name">#${index + 1} ${escapeHtml(tool.name)}</h3>
              <span class="tool-card__license">${escapeHtml(tool.license_name)}</span>
            </div>
            <p class="tool-card__tagline">${escapeHtml(tool.best_for)}</p>
            <p class="tool-card__meta">Pricing: ${escapeHtml(tool.pricing)}</p>
            <div class="tool-card__foot">
              <div class="tool-card__links">
                <a href="${escapeHtml(tool.website)}" target="_blank" rel="noopener">Official site</a>${gh}
              </div>
            </div>
          </div>
        `;
      })
      .join("");
  }

  function bindEvents() {
    els.jobButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        state.job = btn.dataset.job;
        els.jobButtons.forEach((b) => {
          b.classList.toggle("key--active", b === btn);
          b.setAttribute("aria-pressed", String(b === btn));
        });
        renderGrid();
      });
    });

    els.search.addEventListener("input", (e) => {
      state.query = e.target.value;
      renderGrid();
    });

    els.license.addEventListener("change", (e) => {
      state.license = e.target.value;
      renderGrid();
    });

    els.deployment.addEventListener("change", (e) => {
      state.deployment = e.target.value;
      renderGrid();
    });

    els.reqif.addEventListener("change", (e) => {
      state.reqifOnly = e.target.checked;
      renderGrid();
    });

    els.grid.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-compare]");
      if (!btn) return;
      const id = btn.dataset.compare;
      if (state.compareIds.includes(id)) {
        state.compareIds = state.compareIds.filter((x) => x !== id);
      } else {
        if (state.compareIds.length >= 3) state.compareIds.shift();
        state.compareIds.push(id);
      }
      renderGrid();
      renderComparison();
    });

    [els.matcherWorkflow, els.matcherRegulated, els.matcherBudget].forEach((sel) => {
      sel.addEventListener("change", renderMatcher);
    });

    if (els.copyPrBtn && els.prSnippet) {
      els.copyPrBtn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(els.prSnippet.textContent);
          els.copyPrBtn.textContent = "Copied JSON template";
          setTimeout(() => {
            els.copyPrBtn.textContent = "Copy JSON template";
          }, 1800);
        } catch {
          els.copyPrBtn.textContent = "Copy manually";
        }
      });
    }
  }

  async function init() {
    bindEvents();
    try {
      const res = await fetch("./tools.json");
      const data = await res.json();
      state.tools = data.tools || [];
      renderGrid();
      renderComparison();
      renderMatcher();
    } catch {
      els.count.textContent = "Load via local HTTP server or GitHub Pages to query tools.json dynamically.";
    }
  }

  init();
})();
