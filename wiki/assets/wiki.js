(() => {
  "use strict";

  const VERSION_LABELS = {
    keyan: "科研备忘录",
    zhihu: "知乎解释版",
    xiaohongshu: "小红书版",
  };
  const FIELD_ORDER = [
    "世界模型与评测",
    "数据工程与质量",
    "多模态感知",
    "VLA 与模型",
    "空间智能与导航",
    "跨本体与控制",
    "产业与应用",
  ];
  const state = {
    manifest: null,
    topic: null,
    version: "zhihu",
    drawerMode: "recent",
    expandedFields: new Set(),
    searchIndex: null,
    topicCache: new Map(),
    searchTimer: null,
  };
  const mobileNavigationQuery = window.matchMedia("(max-width: 780px)");

  const el = (id) => document.getElementById(id);
  const nodes = {
    sidebar: el("sidebar"),
    sidebarToggle: el("sidebar-toggle"),
    sidebarScrim: el("sidebar-scrim"),
    fieldNav: el("field-nav"),
    recentResearch: el("recent-research"),
    topicCount: el("topic-count"),
    snapshotTime: el("snapshot-time"),
    welcome: el("welcome-view"),
    welcomeGrid: el("welcome-grid"),
    article: el("article-view"),
    error: el("error-view"),
    errorMessage: el("error-message"),
    articleField: el("article-field"),
    articleDate: el("article-date"),
    articleTitle: el("article-title"),
    articleExcerpt: el("article-excerpt"),
    versionTabs: el("version-tabs"),
    versionArticleTitle: el("version-article-title"),
    readingLength: el("reading-length"),
    articleBody: el("article-body"),
    evidenceButton: el("evidence-button"),
    evidenceDrawer: el("evidence-drawer"),
    evidenceTitle: el("evidence-title"),
    evidenceSource: el("evidence-source"),
    evidenceBody: el("evidence-body"),
    drawerScrim: el("drawer-scrim"),
    tocNav: el("toc-nav"),
    progress: el("reading-progress"),
    searchDialog: el("search-dialog"),
    searchInput: el("search-input"),
    searchResults: el("search-results"),
    searchCount: el("search-count"),
    refreshButton: el("refresh-button"),
    refreshLabel: el("refresh-label"),
    toast: el("toast"),
  };

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  function formatDate(value) {
    if (!value || value === "0000-00-00") return "日期未标注";
    const date = new Date(`${value}T00:00:00`);
    if (Number.isNaN(date.getTime())) return value;
    return new Intl.DateTimeFormat("zh-CN", { year: "numeric", month: "long", day: "numeric" }).format(date);
  }

  function formatSnapshot(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "成果快照时间未知";
    return `快照更新于 ${new Intl.DateTimeFormat("zh-CN", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(date)}`;
  }

  async function fetchJson(path, bust = false) {
    const suffix = bust ? `${path.includes("?") ? "&" : "?"}t=${Date.now()}` : "";
    const response = await fetch(`${path}${suffix}`, { cache: bust ? "no-store" : "default" });
    if (!response.ok) throw new Error(`读取失败（${response.status}）`);
    return response.json();
  }

  async function loadManifest(bust = false) {
    const manifest = await fetchJson("data/manifest.json", bust);
    if (!Array.isArray(manifest.topics) || !manifest.topics.length) throw new Error("成果索引为空");
    state.manifest = manifest;
    nodes.topicCount.textContent = manifest.topics.length;
    nodes.snapshotTime.textContent = formatSnapshot(manifest.generated_at);
    renderFieldTree();
    renderWelcome();
    return manifest;
  }

  function orderedFields() {
    const fields = state.manifest?.fields || [];
    return [...fields].sort((left, right) => {
      const leftIndex = FIELD_ORDER.indexOf(left.name);
      const rightIndex = FIELD_ORDER.indexOf(right.name);
      if (leftIndex === -1 && rightIndex === -1) return left.name.localeCompare(right.name, "zh-CN");
      if (leftIndex === -1) return 1;
      if (rightIndex === -1) return -1;
      return leftIndex - rightIndex;
    });
  }

  function renderFieldTree() {
    if (!state.manifest) return;
    nodes.recentResearch.classList.toggle("is-active", state.drawerMode === "recent");
    nodes.fieldNav.innerHTML = orderedFields().map((field, index) => {
      const expanded = state.expandedFields.has(field.name);
      const topics = state.manifest.topics.filter((topic) => topic.field === field.name);
      const childrenId = `field-topics-${index}`;
      return `
        <section class="tree-folder ${expanded ? "is-expanded" : ""}">
          <button class="tree-folder-row" type="button" data-field="${escapeHtml(field.name)}" aria-expanded="${expanded}" aria-controls="${childrenId}">
            <span class="folder-icon" aria-hidden="true"></span>
            <span>${escapeHtml(field.name)}</span>
            <span class="tree-count" aria-label="${field.count} 篇">${field.count}</span>
            <span class="tree-chevron" aria-hidden="true">›</span>
          </button>
          <div class="tree-children" id="${childrenId}">
            ${topics.map((topic) => `
              <button class="tree-topic ${state.topic?.id === topic.id ? "is-active" : ""}" type="button" data-topic-id="${escapeHtml(topic.id)}" ${state.topic?.id === topic.id ? 'aria-current="page"' : ""}>
                <span>${escapeHtml(topic.title)}</span>
              </button>`).join("")}
          </div>
        </section>`;
    }).join("");
  }

  function renderWelcome() {
    const topics = state.manifest.topics.slice(0, 6);
    nodes.welcomeGrid.innerHTML = topics.map((topic) => `
      <button type="button" class="welcome-card" data-topic-id="${topic.id}">
        <small>${escapeHtml(topic.field)}</small>
        <strong>${escapeHtml(topic.title)}</strong>
        <span>${escapeHtml(formatDate(topic.date))} · 默认知乎解释版</span>
      </button>`).join("");
  }

  function parseRoute() {
    const match = location.hash.match(/^#\/topic\/([^?]+)(?:\?version=(keyan|zhihu|xiaohongshu))?/);
    return match ? { id: decodeURIComponent(match[1]), version: match[2] || "zhihu" } : null;
  }

  function setRoute(topicId, version = "zhihu", replace = false) {
    const hash = `#/topic/${encodeURIComponent(topicId)}?version=${version}`;
    if (replace) history.replaceState(null, "", hash);
    else location.hash = hash;
  }

  async function loadTopic(identifier, requestedVersion = "zhihu") {
    const manifestItem = state.manifest.topics.find((item) => item.id === identifier);
    if (!manifestItem) {
      showWelcome();
      return;
    }
    try {
      let topic = state.topicCache.get(identifier);
      if (!topic) {
        const snapshot = encodeURIComponent(state.manifest.generated_at || "latest");
        topic = await fetchJson(`data/topics/${identifier}.json?v=${snapshot}`);
        state.topicCache.set(identifier, topic);
      }
      state.topic = topic;
      state.version = topic.versions[requestedVersion] ? requestedVersion : "zhihu";
      state.drawerMode = null;
      state.expandedFields.add(topic.field);
      renderArticle();
      closeMobileSidebar();
      window.scrollTo({ top: 0, behavior: "instant" });
    } catch (error) {
      showError(`无法读取“${manifestItem.title}”：${error.message}`);
    }
  }

  function renderArticle() {
    const topic = state.topic;
    const version = topic.versions[state.version];
    nodes.welcome.hidden = true;
    nodes.error.hidden = true;
    nodes.article.hidden = false;
    nodes.articleField.textContent = topic.field;
    nodes.articleDate.textContent = formatDate(topic.date);
    nodes.articleDate.dateTime = topic.date;
    nodes.articleTitle.textContent = topic.title;
    nodes.articleExcerpt.textContent = topic.excerpt;
    nodes.versionArticleTitle.textContent = version.article_title;
    nodes.readingLength.textContent = `约 ${Math.max(1, Math.round(version.characters / 520))} 分钟阅读`;
    nodes.articleBody.innerHTML = version.html;
    nodes.evidenceButton.disabled = !topic.evidence.available;
    nodes.evidenceButton.title = topic.evidence.available ? "打开证据附录" : "这个话题没有随附证据文档";
    [...nodes.versionTabs.querySelectorAll("[data-version]")].forEach((button) => {
      const active = button.dataset.version === state.version;
      button.setAttribute("aria-selected", String(active));
      button.tabIndex = active ? 0 : -1;
    });
    renderToc(version.toc || []);
    renderFieldTree();
    bindArticleLinks();
    updateProgress();
    document.title = `${topic.title}｜具身智能研究 Wiki`;
  }

  function renderToc(toc) {
    const filtered = toc.filter((item) => item.level >= 2).slice(0, 16);
    nodes.tocNav.innerHTML = filtered.length
      ? filtered.map((item) => `<a href="#${escapeHtml(item.id)}" data-level="${item.level}">${escapeHtml(item.label)}</a>`).join("")
      : '<span class="search-empty">本页没有分节目录</span>';
  }

  function bindArticleLinks() {
    nodes.articleBody.querySelectorAll("[data-open-evidence]").forEach((button) => button.addEventListener("click", openEvidence));
    nodes.articleBody.querySelectorAll('a[href^="#"]').forEach((link) => link.addEventListener("click", (event) => {
      const target = document.getElementById(link.getAttribute("href").slice(1));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }));
  }

  function switchVersion(version) {
    if (!state.topic?.versions[version] || version === state.version) return;
    state.version = version;
    setRoute(state.topic.id, version, true);
    renderArticle();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showWelcome() {
    state.topic = null;
    nodes.article.hidden = true;
    nodes.error.hidden = true;
    nodes.welcome.hidden = false;
    nodes.tocNav.innerHTML = "";
    nodes.progress.style.width = "0";
    state.drawerMode = "recent";
    renderFieldTree();
    document.title = "具身智能研究 Wiki";
  }

  function showError(message) {
    nodes.article.hidden = true;
    nodes.welcome.hidden = true;
    nodes.error.hidden = false;
    nodes.errorMessage.textContent = message;
  }

  function route() {
    const parsed = parseRoute();
    if (parsed) loadTopic(parsed.id, parsed.version);
    else showWelcome();
  }

  function openEvidence() {
    if (!state.topic?.evidence.available) return;
    nodes.evidenceTitle.textContent = state.topic.evidence.label;
    nodes.evidenceSource.textContent = `来源：${state.topic.source_directory}/${state.topic.evidence.source_file}`;
    nodes.evidenceBody.innerHTML = state.topic.evidence.html;
    nodes.evidenceDrawer.classList.add("is-open");
    nodes.drawerScrim.classList.add("is-open");
    nodes.evidenceDrawer.setAttribute("aria-hidden", "false");
    syncBodyScroll();
    el("evidence-close").focus();
  }

  function closeEvidence() {
    nodes.evidenceDrawer.classList.remove("is-open");
    nodes.drawerScrim.classList.remove("is-open");
    nodes.evidenceDrawer.setAttribute("aria-hidden", "true");
    syncBodyScroll();
  }

  function openSidebar() {
    if (state.topic?.field) state.expandedFields.add(state.topic.field);
    renderFieldTree();
    if (isMobileNavigation()) {
      nodes.sidebar.classList.add("is-open");
      nodes.sidebarScrim.classList.add("is-open");
    } else {
      document.body.classList.remove("sidebar-collapsed");
    }
    nodes.sidebar.inert = false;
    nodes.sidebar.setAttribute("aria-hidden", "false");
    nodes.sidebarToggle.setAttribute("aria-expanded", "true");
    nodes.sidebarToggle.setAttribute("aria-label", "关闭研究导航");
    nodes.sidebarToggle.dataset.tooltip = "关闭研究导航";
    syncBodyScroll();
    requestAnimationFrame(() => {
      const target = nodes.sidebar.querySelector(".tree-topic.is-active, .tree-shortcut.is-active, .tree-folder-row");
      target?.focus();
      target?.scrollIntoView({ block: "nearest" });
    });
  }

  function closeSidebar() {
    if (nodes.sidebar.contains(document.activeElement)) nodes.sidebarToggle.focus();
    if (isMobileNavigation()) nodes.sidebar.classList.remove("is-open");
    else document.body.classList.add("sidebar-collapsed");
    nodes.sidebarScrim.classList.remove("is-open");
    nodes.sidebar.inert = true;
    nodes.sidebar.setAttribute("aria-hidden", "true");
    nodes.sidebarToggle.setAttribute("aria-expanded", "false");
    nodes.sidebarToggle.setAttribute("aria-label", "打开研究导航");
    nodes.sidebarToggle.dataset.tooltip = "打开研究导航";
    syncBodyScroll();
  }

  function syncBodyScroll() {
    const overlayOpen = (isMobileNavigation() && nodes.sidebar.classList.contains("is-open")) || nodes.evidenceDrawer.classList.contains("is-open");
    document.body.style.overflow = overlayOpen ? "hidden" : "";
  }

  function isMobileNavigation() {
    return mobileNavigationQuery.matches;
  }

  function sidebarIsOpen() {
    return isMobileNavigation()
      ? nodes.sidebar.classList.contains("is-open")
      : !document.body.classList.contains("sidebar-collapsed");
  }

  function closeMobileSidebar() {
    if (isMobileNavigation()) closeSidebar();
  }

  function syncSidebarForViewport() {
    nodes.sidebar.classList.remove("is-open");
    nodes.sidebarScrim.classList.remove("is-open");
    if (isMobileNavigation()) {
      if (nodes.sidebar.contains(document.activeElement)) nodes.sidebarToggle.focus();
      document.body.classList.remove("sidebar-collapsed");
      nodes.sidebar.inert = true;
      nodes.sidebar.setAttribute("aria-hidden", "true");
      nodes.sidebarToggle.setAttribute("aria-expanded", "false");
      nodes.sidebarToggle.setAttribute("aria-label", "打开研究导航");
      nodes.sidebarToggle.dataset.tooltip = "打开研究导航";
    } else {
      document.body.classList.remove("sidebar-collapsed");
      nodes.sidebar.inert = false;
      nodes.sidebar.setAttribute("aria-hidden", "false");
      nodes.sidebarToggle.setAttribute("aria-expanded", "true");
      nodes.sidebarToggle.setAttribute("aria-label", "关闭研究导航");
      nodes.sidebarToggle.dataset.tooltip = "关闭研究导航";
    }
    syncBodyScroll();
  }

  function focusFieldRow(fieldName) {
    requestAnimationFrame(() => {
      const row = [...nodes.fieldNav.querySelectorAll("[data-field]")].find((button) => button.dataset.field === fieldName);
      row?.focus();
    });
  }

  function showRecentResearch() {
    state.drawerMode = "recent";
    closeMobileSidebar();
    if (!location.hash || location.hash === "#/") {
      history.replaceState(null, "", "#/");
      showWelcome();
    } else {
      location.hash = "#/";
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function ensureSearchIndex() {
    if (!state.searchIndex) {
      const snapshot = encodeURIComponent(state.manifest?.generated_at || "latest");
      state.searchIndex = await fetchJson(`data/search-index.json?v=${snapshot}`);
    }
    return state.searchIndex;
  }

  async function openSearch() {
    if (!nodes.searchDialog.open) nodes.searchDialog.showModal();
    nodes.searchInput.focus();
    try {
      await ensureSearchIndex();
      if (!nodes.searchInput.value.trim()) renderSearchResults("");
    } catch (error) {
      nodes.searchResults.innerHTML = `<p class="search-empty">搜索索引读取失败：${escapeHtml(error.message)}</p>`;
    }
  }

  function normalizeSearch(value) {
    return value.normalize("NFKC").toLocaleLowerCase("zh-CN").replace(/\s+/g, " ").trim();
  }

  function makeSnippet(text, query) {
    const normalized = normalizeSearch(text);
    const at = normalized.indexOf(query);
    const start = Math.max(0, at >= 0 ? at - 48 : 0);
    const raw = text.slice(start, start + 150);
    const escaped = escapeHtml(`${start > 0 ? "…" : ""}${raw}${start + 150 < text.length ? "…" : ""}`);
    if (!query) return escaped;
    const safeQuery = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return escaped.replace(new RegExp(`(${safeQuery})`, "ig"), "<mark>$1</mark>");
  }

  function search(query) {
    const normalizedQuery = normalizeSearch(query);
    if (!normalizedQuery) return [];
    const terms = normalizedQuery.split(" ").filter(Boolean);
    const results = [];
    for (const topic of state.searchIndex.topics) {
      for (const [versionKey, version] of Object.entries(topic.versions)) {
        const haystack = normalizeSearch(`${topic.title} ${topic.field} ${version.article_title} ${version.text}`);
        if (!terms.every((term) => haystack.includes(term))) continue;
        let score = 0;
        const titleText = normalizeSearch(`${topic.title} ${version.article_title}`);
        if (titleText.includes(normalizedQuery)) score += 12;
        if (normalizeSearch(topic.title) === normalizedQuery) score += 20;
        score += Math.max(0, 5 - haystack.indexOf(normalizedQuery) / 1000);
        results.push({ topic, versionKey, version, score });
      }
    }
    return results.sort((a, b) => b.score - a.score || b.topic.date.localeCompare(a.topic.date)).slice(0, 60);
  }

  function renderSearchResults(query) {
    const value = query.trim();
    if (!value) {
      nodes.searchCount.textContent = `${state.searchIndex?.topics.length || 0} 个话题，覆盖三种表达版本`;
      nodes.searchResults.innerHTML = '<p class="search-empty">可以搜索概念、结论、论文名或研究问题。</p>';
      return;
    }
    const results = search(value);
    nodes.searchCount.textContent = `找到 ${results.length} 个版本匹配`;
    nodes.searchResults.innerHTML = results.length ? results.map((result) => `
      <button type="button" class="search-result" data-topic-id="${result.topic.id}" data-version="${result.versionKey}">
        <span class="search-result-badge">${escapeHtml(VERSION_LABELS[result.versionKey])}</span>
        <span><strong>${escapeHtml(result.topic.title)}</strong><p>${makeSnippet(result.version.text, normalizeSearch(value))}</p></span>
      </button>`).join("") : '<p class="search-empty">没有找到匹配内容。试试更短的关键词。</p>';
  }

  function selectSearchResult(button) {
    const { topicId, version } = button.dataset;
    nodes.searchDialog.close();
    nodes.searchInput.value = "";
    setRoute(topicId, version);
  }

  function isLocalRefreshAvailable() {
    return ["localhost", "127.0.0.1", "::1"].includes(location.hostname);
  }

  async function refreshWiki() {
    nodes.refreshButton.disabled = true;
    nodes.refreshButton.classList.add("is-spinning");
    const previous = state.manifest?.generated_at;
    try {
      if (isLocalRefreshAvailable()) {
        setRefreshLabel("扫描成果中");
        const response = await fetch("api/refresh", { method: "POST" });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || "刷新失败");
        state.topicCache.clear();
        state.searchIndex = null;
        await loadManifest(true);
        route();
        showToast(`刷新完成：已准备 ${payload.topics} 个最新完整话题。`);
      } else {
        setRefreshLabel("检查更新中");
        await loadManifest(true);
        if (previous === state.manifest.generated_at) showToast("已经是线上最新版本。下一次发布后可在这里检查更新。");
        else {
          state.topicCache.clear();
          state.searchIndex = null;
          route();
          showToast("已载入最新发布版本。");
        }
      }
    } catch (error) {
      showToast(`刷新失败：${error.message}`);
    } finally {
      nodes.refreshButton.disabled = false;
      nodes.refreshButton.classList.remove("is-spinning");
      setRefreshLabel(isLocalRefreshAvailable() ? "刷新成果" : "检查更新");
    }
  }

  function setRefreshLabel(label) {
    nodes.refreshLabel.textContent = label;
    nodes.refreshButton.setAttribute("aria-label", label);
    nodes.refreshButton.dataset.tooltip = label;
  }

  function showToast(message) {
    nodes.toast.textContent = message;
    nodes.toast.classList.add("is-visible");
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => nodes.toast.classList.remove("is-visible"), 3600);
  }

  function updateProgress() {
    if (!state.topic || nodes.article.hidden) return;
    const start = nodes.article.offsetTop;
    const end = start + nodes.article.offsetHeight - window.innerHeight;
    const percent = end <= start ? 100 : Math.min(100, Math.max(0, ((window.scrollY - start) / (end - start)) * 100));
    nodes.progress.style.width = `${percent}%`;
  }

  function goNext() {
    if (!state.topic) return;
    const topics = state.manifest.topics;
    const current = topics.findIndex((topic) => topic.id === state.topic.id);
    const next = topics[(current + 1) % topics.length];
    setRoute(next.id, "zhihu");
  }

  function bindEvents() {
    window.addEventListener("hashchange", route);
    window.addEventListener("scroll", updateProgress, { passive: true });
    mobileNavigationQuery.addEventListener("change", syncSidebarForViewport);
    nodes.sidebarToggle.addEventListener("click", () => sidebarIsOpen() ? closeSidebar() : openSidebar());
    nodes.sidebarScrim.addEventListener("click", closeSidebar);
    nodes.fieldNav.addEventListener("click", (event) => {
      const topicButton = event.target.closest("[data-topic-id]");
      if (topicButton) {
        state.drawerMode = null;
        closeMobileSidebar();
        setRoute(topicButton.dataset.topicId, "zhihu");
        return;
      }
      const fieldButton = event.target.closest("[data-field]");
      if (!fieldButton) return;
      const fieldName = fieldButton.dataset.field;
      state.drawerMode = null;
      if (state.expandedFields.has(fieldName)) state.expandedFields.delete(fieldName);
      else state.expandedFields.add(fieldName);
      renderFieldTree();
      focusFieldRow(fieldName);
    });
    nodes.welcomeGrid.addEventListener("click", (event) => {
      const button = event.target.closest("[data-topic-id]");
      if (button) setRoute(button.dataset.topicId, "zhihu");
    });
    nodes.recentResearch.addEventListener("click", showRecentResearch);
    nodes.versionTabs.addEventListener("click", (event) => {
      const button = event.target.closest("[data-version]");
      if (button) switchVersion(button.dataset.version);
    });
    nodes.tocNav.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const target = document.getElementById(link.getAttribute("href").slice(1));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    nodes.evidenceButton.addEventListener("click", openEvidence);
    el("evidence-close").addEventListener("click", closeEvidence);
    nodes.drawerScrim.addEventListener("click", closeEvidence);
    el("search-trigger").addEventListener("click", openSearch);
    el("search-close").addEventListener("click", () => nodes.searchDialog.close());
    nodes.searchInput.addEventListener("input", () => {
      clearTimeout(state.searchTimer);
      state.searchTimer = setTimeout(() => renderSearchResults(nodes.searchInput.value), 90);
    });
    nodes.searchResults.addEventListener("click", (event) => {
      const button = event.target.closest("[data-topic-id][data-version]");
      if (button) selectSearchResult(button);
    });
    nodes.refreshButton.addEventListener("click", refreshWiki);
    el("retry-button").addEventListener("click", () => init(true));
    el("next-topic").addEventListener("click", goNext);
    document.addEventListener("keydown", (event) => {
      const tag = document.activeElement?.tagName;
      if (event.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") {
        event.preventDefault();
        openSearch();
      }
      if (event.key === "Escape") {
        closeEvidence();
        closeSidebar();
      }
    });
  }

  async function init(bust = false) {
    try {
      await loadManifest(bust);
      setRefreshLabel(isLocalRefreshAvailable() ? "刷新成果" : "检查更新");
      route();
    } catch (error) {
      showError(`成果索引读取失败：${error.message}`);
    }
  }

  syncSidebarForViewport();
  bindEvents();
  init();
})();
