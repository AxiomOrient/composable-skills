const state = {
  query: "",
  layer: "all",
  family: "all",
};

const layerOrder = ["workflow", "atomic", "control"];
const layerDescriptions = {
  workflow: "한 덩어리 작업을 처음부터 끝까지 묶는 진입점",
  atomic: "하나의 책임만 수행하는 정밀 공구",
  control: "반복과 종료 조건을 관리하는 제어 장치",
};

const numberFormat = new Intl.NumberFormat("ko-KR");

boot();

async function boot() {
  try {
    const response = await fetch("./data/skills.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    hydrateMetrics(payload.stats);
    hydrateDocLinks(payload.repoUrl);
    renderFamilyOverview(payload.stats.familyCards);
    renderFilterControls(payload.stats.familyCards);
    bindEvents(payload);
    renderAtlas(payload);
    revealSections();
  } catch (error) {
    renderErrorState(error);
  }
}

function hydrateMetrics(stats) {
  setText("metric-skills", numberFormat.format(stats.skillsCount));
  setText("metric-workflows", numberFormat.format(stats.workflowCount));
  setText("metric-atomic", numberFormat.format(stats.atomicCount));
  setText("metric-control", numberFormat.format(stats.controlCount));
}

function hydrateDocLinks(repoUrl) {
  const links = {
    repo: repoUrl,
    readme: repoUrl,
    system: `${repoUrl}/blob/main/docs/SKILL-SYSTEM.md`,
    guide: `${repoUrl}/blob/main/docs/ATOMIC-SKILLS-GUIDE.md`,
    skills: `${repoUrl}/tree/main/skills`,
  };

  document.querySelectorAll("[data-doc-link]").forEach((anchor) => {
    const key = anchor.dataset.docLink;
    if (links[key]) {
      anchor.href = links[key];
    }
  });
}

function renderFamilyOverview(familyCards) {
  const container = document.getElementById("family-overview");
  container.innerHTML = familyCards
    .map(
      (family) => `
        <article class="family-card">
          <p class="family-card__count">${numberFormat.format(family.count)}</p>
          <h3>${escapeHtml(family.labelKo)}</h3>
          <p class="family-card__meta">${escapeHtml(family.labelEn)}</p>
          <p>${escapeHtml(family.summaryKo)}</p>
        </article>
      `
    )
    .join("");
}

function renderFilterControls(familyCards) {
  const layerFilters = [
    { value: "all", label: "전체" },
    { value: "workflow", label: "워크플로" },
    { value: "atomic", label: "원자 스킬" },
    { value: "control", label: "제어 스킬" },
  ];

  document.getElementById("layer-filters").innerHTML = layerFilters
    .map((filter) => renderChip(filter.value, filter.label, "layer"))
    .join("");

  const familyFilters = [{ value: "all", label: "전체" }].concat(
    familyCards.map((family) => ({
      value: family.family,
      label: `${family.labelKo} (${family.count})`,
    }))
  );

  document.getElementById("family-filters").innerHTML = familyFilters
    .map((filter) => renderChip(filter.value, filter.label, "family"))
    .join("");

  syncChipState();
}

function bindEvents(payload) {
  const search = document.getElementById("skill-search");
  search.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    renderAtlas(payload);
  });

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter-kind]");
    if (!button) {
      return;
    }

    const kind = button.dataset.filterKind;
    const value = button.dataset.filterValue;
    state[kind] = value;
    syncChipState();
    renderAtlas(payload);
  });
}

function renderAtlas(payload) {
  const filteredSkills = filterSkills(payload.skills);
  const results = document.getElementById("atlas-results");
  const missingCount = filteredSkills.filter((skill) => skill.missingContract).length;
  const summary = document.getElementById("atlas-summary");

  summary.textContent = `${numberFormat.format(filteredSkills.length)}개 스킬 표시 중. ${
    missingCount ? `${numberFormat.format(missingCount)}개는 현재 저장소 스냅샷에 계약 파일이 없습니다.` : "모든 표시 스킬에 계약 파일이 있습니다."
  }`;

  if (!filteredSkills.length) {
    results.innerHTML = `
      <p class="empty-state">
        검색 조건에 맞는 스킬이 없습니다. 이름 대신 문제 상황으로 검색해 보세요.
      </p>
    `;
    return;
  }

  results.innerHTML = layerOrder
    .map((layer) => renderLayerSection(layer, filteredSkills))
    .filter(Boolean)
    .join("");

  revealSections();
}

function filterSkills(skills) {
  return skills.filter((skill) => {
    if (state.layer !== "all" && skill.layer !== state.layer) {
      return false;
    }

    if (state.family !== "all" && skill.family !== state.family) {
      return false;
    }

    if (!state.query) {
      return true;
    }

    const quickPick = skill.quickPick ? `${skill.quickPick.need} ${skill.quickPick.why}` : "";
    const searchText = [
      skill.name,
      skill.summaryKo,
      skill.description,
      skill.purpose,
      quickPick,
      skill.familyInfo.label_ko,
      skill.layerLabel.ko,
      skill.familyInfo.value_ko,
      ...skill.useWhen,
      ...skill.doNotUseWhen,
      ...skill.expansion,
    ]
      .join(" ")
      .toLowerCase();

    return searchText.includes(state.query);
  });
}

function renderLayerSection(layer, skills) {
  const layerSkills = skills.filter((skill) => skill.layer === layer);
  if (!layerSkills.length) {
    return "";
  }

  const familyNames = [...new Set(layerSkills.map((skill) => skill.family))];
  const familySections = familyNames
    .map((family) => {
      const familySkills = layerSkills.filter((skill) => skill.family === family);
      return renderFamilySection(familySkills);
    })
    .join("");

  const label = layerSkills[0].layerLabel;
  return `
    <section class="atlas-layer reveal">
      <div class="atlas-layer__header">
        <div>
          <p class="eyebrow">${escapeHtml(label.en)}</p>
          <h3 class="atlas-layer__title">${escapeHtml(label.ko)}</h3>
        </div>
        <p class="atlas-layer__meta">${escapeHtml(layerDescriptions[layer])}</p>
      </div>
      ${familySections}
    </section>
  `;
}

function renderFamilySection(skills) {
  const family = skills[0].familyInfo;
  return `
    <section class="family-group">
      <div class="family-group__header">
        <div>
          <h4 class="family-group__title">${escapeHtml(family.label_ko)}</h4>
          <p class="family-group__meta">${escapeHtml(family.summary_ko)}</p>
        </div>
        <p class="family-group__meta">${numberFormat.format(skills.length)}개</p>
      </div>
      <div class="skill-grid">
        ${skills.map((skill) => renderSkillCard(skill)).join("")}
      </div>
    </section>
  `;
}

function renderSkillCard(skill) {
  const quickPick = skill.quickPick
    ? `<p class="skill-card__quick"><strong>추천 상황:</strong> ${escapeHtml(skill.quickPick.need)}</p>`
    : "";
  const description = skill.description
    ? `<p class="skill-card__description"><strong>계약 요약:</strong> ${escapeHtml(skill.description)}</p>`
    : "";
  const status = skill.missingContract
    ? `<span class="status-pill">contract missing</span>`
    : "";
  const useWhen = renderList(skill.useWhen);
  const doNotUseWhen = renderList(skill.doNotUseWhen);
  const expansion = renderList(skill.expansion.map((item) => `$${item}`));
  const sourceLabel = skill.missingContract ? "소스 디렉터리 보기" : "계약 파일 보기";
  const details = skill.missingContract
    ? `
      <div class="detail-block">
        <h4>상태</h4>
        <p>이 스킬은 현재 저장소 스냅샷에 <code>SKILL.md</code>가 없습니다. 사이트는 숨기지 않고 이 상태를 그대로 보여 줍니다.</p>
      </div>
    `
    : `
      <div class="detail-block">
        <h4>Purpose</h4>
        <p>${escapeHtml(skill.purpose)}</p>
      </div>
      ${useWhen ? `<div class="detail-block"><h4>Use When</h4>${useWhen}</div>` : ""}
      ${doNotUseWhen ? `<div class="detail-block"><h4>Do Not Use When</h4>${doNotUseWhen}</div>` : ""}
      ${expansion ? `<div class="detail-block"><h4>Expansion</h4>${expansion}</div>` : ""}
    `;

  return `
    <article class="skill-card ${skill.missingContract ? "is-missing" : ""}">
      <div class="skill-card__meta">
        <span class="pill">${escapeHtml(skill.layerLabel.ko)}</span>
        <span class="pill">${escapeHtml(skill.familyInfo.label_ko)}</span>
        ${status}
      </div>

      <h3><code>${escapeHtml(skill.name)}</code></h3>
      <p class="skill-card__summary">${escapeHtml(skill.summaryKo || skill.familyInfo.summary_ko)}</p>
      <p class="skill-card__gain"><strong>사용자가 얻는 것:</strong> ${escapeHtml(skill.familyInfo.value_ko)}</p>
      ${quickPick}
      ${description}

      <details>
        <summary>더 보기</summary>
        <div class="skill-card__details">
          ${details}
          <a class="skill-card__link" href="${escapeHtml(skill.sourceUrl)}">${sourceLabel}</a>
        </div>
      </details>
    </article>
  `;
}

function renderList(items) {
  if (!items || !items.length) {
    return "";
  }

  return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderChip(value, label, kind) {
  return `
    <button
      type="button"
      class="chip"
      data-filter-kind="${kind}"
      data-filter-value="${value}"
    >
      ${escapeHtml(label)}
    </button>
  `;
}

function syncChipState() {
  document.querySelectorAll("[data-filter-kind]").forEach((button) => {
    const kind = button.dataset.filterKind;
    const value = button.dataset.filterValue;
    button.classList.toggle("is-active", state[kind] === value);
  });
}

function renderErrorState(error) {
  document.getElementById("atlas-summary").textContent = "카탈로그를 불러오지 못했습니다.";
  document.getElementById("atlas-results").innerHTML = `
    <p class="empty-state">
      <strong>오류:</strong> ${escapeHtml(String(error.message || error))}
      <br />
      <code>python3 scripts/build_site_data.py</code> 후 정적 서버로 확인해 보세요.
    </p>
  `;
}

function revealSections() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  document.querySelectorAll(".reveal").forEach((node, index) => {
    node.style.setProperty("--delay", `${Math.min(index * 30, 360)}ms`);
  });
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) {
    node.textContent = value;
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
