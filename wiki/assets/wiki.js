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
  // Mirrors WORKFLOW_STAGE_LABELS in serve_research_wiki.py — keep in sync.
  const WORKFLOW_STAGES = [
    ["init", "初始化"],
    ["plan", "查询规划"],
    ["retrieval", "arXiv 检索"],
    ["mining", "全文挖掘"],
    ["packet", "综述包"],
    ["writing", "成稿撰写"],
    ["audit", "审计门"],
    ["settle", "落盘发布"],
  ];
  const CHAT_WIDTH_KEY = "wiki.chat.width";
  const CHAT_WIDTH_MIN = 340;
  const CHAT_WIDTH_MAX = 760;
  const CHAT_DEFAULT_WIDTH = 420;
  const state = {
    manifest: null,
    topic: null,
    version: "zhihu",
    drawerMode: "recent",
    expandedFields: new Set(),
    searchIndex: null,
    topicCache: new Map(),
    searchTimer: null,
    dataBase: "data",
    snapshotId: "legacy",
    pointerResolved: false,
    // Quick-read (速读) tab state: markdown cache keyed by paper id, plus the
    // id currently generating. Memory only — never persisted.
    quickRead: new Map(),
    quickReadGenerating: null,
    chat: {
      open: false,
      serverEnabled: false,
      sessionId: null,
      streaming: false,
      controller: null,
      messages: [],
      focused: false,
      widthPx: null,
      dragging: false,
      // Workflow (workspace) mode: null when the panel is in topic chat mode.
      wsId: null,
      workflowAvailable: false,
      stage: null,
      awaitingInput: false,
      // Pending @-quote contexts gathered from selections (article, evidence,
      // reader). Each becomes a <selection_context> block on the next send.
      quotes: [],
      // Workflow conversations live in their own history; the panel shows one
      // pane at a time (topic chat vs workflow chat).
      wsMessages: [],
      wsSessionId: null,
      // Paper-chat state: one conversation per arXiv id, cached server-side.
      paperId: null,
      paperMessages: [],
      paperSessionId: null,
      pane: "topic",
    },
  };
  // Chat scroll-lock should match the CSS full-width breakpoint (780px).
  const chatMobileQuery = window.matchMedia("(max-width: 780px)");
  const mobileNavigationQuery = window.matchMedia("(max-width: 900px)");
  // Thrown when the snapshot pointer or manifest does not exist yet — the
  // brand-new knowledge-base shape, distinct from a broken/partial deploy.
  class MissingSnapshotError extends Error {
    constructor(message) {
      super(message);
      this.name = "MissingSnapshotError";
    }
  }

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
    tocPanel: el("sidebar-toc"),
    progress: el("reading-progress"),
    searchDialog: el("search-dialog"),
    searchInput: el("search-input"),
    searchResults: el("search-results"),
    searchCount: el("search-count"),
    refreshButton: el("refresh-button"),
    refreshLabel: el("refresh-label"),
    toast: el("toast"),
    chatPanel: el("chat-panel"),
    chatShowTopic: el("chat-show-topic"),
    chatShowPaper: el("chat-show-paper"),
    chatShowWorkflow: el("chat-show-workflow"),
    paperIdForm: el("paper-id-form"),
    paperIdInput: el("paper-id-input"),
    chatOpenButton: el("chat-open-button"),
    chatClose: el("chat-close"),
    chatExpand: el("chat-expand"),
    chatResizer: el("chat-resizer"),
    chatReset: el("chat-reset"),
    chatTitle: el("chat-title"),
    chatSessionMeta: el("chat-session-meta"),
    chatMessages: el("chat-messages"),
    chatStatus: el("chat-status"),
    chatForm: el("chat-form"),
    chatInput: el("chat-input"),
    chatSend: el("chat-send"),
    chatStop: el("chat-stop"),
    homeChatHero: el("home-chat-hero"),
    homeChatForm: el("home-chat-form"),
    homeChatInput: el("home-chat-input"),
    homeChatSend: el("home-chat-send"),
    interviewCard: el("interview-card"),
    chatModel: el("chat-model"),
    readerViewHeader: el("reader-view-header"),
    readerViewId: el("reader-view-id"),
    readerViewTitle: el("reader-view-title"),
    readerBack: el("reader-back-button"),
    readerQuickReadTab: el("reader-quickread-tab"),
    readerQuickReadBody: el("reader-quickread-body"),
    readerOpenExternal: el("reader-open-external"),
    readerProgress: el("reader-progress"),
    readerProgressBar: el("reader-progress-bar"),
    readerProgressLabel: el("reader-progress-label"),
    articleHeader: el("article-header"),
    articleFooter: el("article-footer"),
    readingMeta: el("reading-meta"),
    selectionPopup: el("selection-popup"),
    selectionCite: el("selection-cite"),
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

  function formatTopicUpdated(value) {
    if (!value || value === "0000-00-00") return "时间未标注";
    return `更新于 ${value}`;
  }

  async function fetchJson(path, bust = false) {
    const suffix = bust ? `${path.includes("?") ? "&" : "?"}t=${Date.now()}` : "";
    const response = await fetch(`${path}${suffix}`, { cache: bust ? "no-store" : "default" });
    if (!response.ok) throw new Error(`读取失败（${response.status}）`);
    return response.json();
  }

  function dataPath(relative) {
    return `${state.dataBase}/${relative}`;
  }

  async function resolveDataBase(bust = false) {
    if (state.pointerResolved && !bust) return state.dataBase;
    const suffix = bust ? `?t=${Date.now()}` : "";
    const response = await fetch(`data/current.json${suffix}`, { cache: "no-store" });
    const previous = state.dataBase;
    if (response.status === 404) {
      state.dataBase = "data";
      state.snapshotId = "legacy";
    } else {
      if (!response.ok) throw new Error(`读取快照指针失败（${response.status}）`);
      const pointer = await response.json();
      const expected = `snapshots/${pointer.snapshot_id}`;
      if (!/^[A-Za-z0-9._-]+$/.test(pointer.snapshot_id || "") || pointer.base_path !== expected) {
        throw new Error("快照指针格式无效");
      }
      state.dataBase = `data/${pointer.base_path}`;
      state.snapshotId = pointer.snapshot_id;
    }
    state.pointerResolved = true;
    if (previous !== state.dataBase) {
      state.topicCache.clear();
      state.searchIndex = null;
    }
    return state.dataBase;
  }

  async function loadManifest(bust = false) {
    await resolveDataBase(bust);
    let manifest;
    try {
      manifest = await fetchJson(dataPath("manifest.json"), bust);
    } catch (error) {
      // resolveDataBase already tolerates a missing pointer (legacy mode);
      // a missing manifest on top of that is a brand-new empty knowledge base.
      if (/\(404\)$/.test(error.message)) {
        throw new MissingSnapshotError("完成第一次文献综述并刷新后，这里会出现话题列表。");
      }
      throw error;
    }
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
                <span class="tree-topic-title">${escapeHtml(topic.title)}</span>
                <small class="tree-topic-meta">${escapeHtml(formatTopicUpdated(topic.date))}</small>
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
        topic = await fetchJson(`${dataPath(`topics/${identifier}.json`)}?v=${snapshot}`);
        state.topicCache.set(identifier, topic);
      }
      state.topic = topic;
      const defaultVersion = topic.available_versions?.includes("zhihu") ? "zhihu" : topic.available_versions?.[0] || "zhihu";
      state.version = topic.versions[requestedVersion] ? requestedVersion : defaultVersion;
      state.drawerMode = null;
      state.expandedFields.add(topic.field);
      if (state.chat.pane === "workflow") {
        // The workflow pane stays put; the title reflects both contexts.
        setChatTitle(`综述工作流 · ${topic.title}`);
      } else {
        resetChatView(); // clears the TOPIC pane only
        setChatTitle(topic.title);
        if (state.chat.open) loadChatState();
        nodes.chatInput.disabled = false;
        nodes.chatInput.placeholder = "就本话题提问，或让 Claude 写综述草稿…";
      }
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
    setReaderView(false);
    if (state.readerAbort) state.readerAbort.abort();
    nodes.articleBody.className = "markdown-body";
    nodes.articleField.textContent = topic.field;
    nodes.articleDate.textContent = formatDate(topic.date);
    nodes.articleDate.dateTime = topic.date;
    nodes.articleTitle.textContent = version.article_title;
    nodes.articleExcerpt.textContent = topic.excerpt;
    nodes.versionArticleTitle.textContent = `所属话题：${topic.title}`;
    nodes.readingLength.textContent = `约 ${Math.max(1, Math.round(version.characters / 520))} 分钟阅读`;
    nodes.articleBody.innerHTML = version.html;
    const repeatedTitle = nodes.articleBody.firstElementChild;
    if (repeatedTitle?.tagName === "H1") repeatedTitle.remove();
    nodes.evidenceButton.disabled = !topic.evidence.available;
    nodes.evidenceButton.title = topic.evidence.available ? "打开证据附录" : "这个话题没有随附证据文档";
    const available = topic.available_versions || Object.keys(topic.versions);
    [...nodes.versionTabs.querySelectorAll("[data-version]")].forEach((button) => {
      const present = available.includes(button.dataset.version);
      button.hidden = !present;
      const active = button.dataset.version === state.version;
      button.setAttribute("aria-selected", String(active));
      button.tabIndex = active ? 0 : -1;
    });
    nodes.tocPanel.hidden = false;
    renderToc(version.toc || []);
    renderFieldTree();
    bindArticleLinks();
    bindReaderLinks(nodes.articleBody);
    updateProgress();
    document.title = `${version.article_title}｜空间智能研究 Wiki`;
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
    nodes.tocPanel.hidden = true;
    if (state.readerAbort) state.readerAbort.abort();
    setReaderView(false);
    state.drawerMode = "recent";
    if (state.chat.pane === "workflow") {
      // The workflow pane survives on the homepage (switch back via 主题对话).
      setChatTitle("综述工作流");
      if (state.chat.open) loadWorkflowState();
    } else {
      resetChatView();
      setChatTitle("研究助手");
      nodes.chatInput.disabled = true;
      nodes.chatInput.placeholder = "先选择一个话题，再开始对话。";
    }
    syncChatPane();
    renderFieldTree();
    document.title = "空间智能研究 Wiki";
  }

  function showError(message) {
    nodes.article.hidden = true;
    nodes.welcome.hidden = true;
    nodes.error.hidden = false;
    nodes.tocPanel.hidden = true;
    nodes.errorMessage.textContent = message;
  }

  // First-run knowledge base: nothing published yet (or no snapshot at all).
  // Keep the shell usable and explain the next step instead of an error.
  function showEmptyLibrary(detail) {
    state.manifest = { topics: [], fields: [], generated_at: null };
    nodes.topicCount.textContent = "0";
    nodes.snapshotTime.textContent = "暂无成果快照";
    nodes.error.hidden = true;
    nodes.welcome.hidden = false;
    nodes.article.hidden = true;
    nodes.welcomeGrid.innerHTML = `
      <div class="welcome-card is-empty">
        <small>空知识库</small>
        <strong>还没有可发布的完整成果</strong>
        <span>${escapeHtml(detail)}</span>
        <span>在上方输入框描述你想综述的主题，开始第一次综述。</span>
      </div>`;
    renderFieldTree();
  }

  function setRouteHash(hash) {
    if (location.hash === hash) route();
    else location.hash = hash;
  }

  function route() {
    const paperId = parsePaperRoute();
    if (paperId) {
      loadPaper(paperId);
      return;
    }
    const parsed = parseRoute();
    if (parsed) loadTopic(parsed.id, parsed.version);
    else showWelcome();
  }

  function openEvidence() {
    if (!state.topic?.evidence.available) return;
    nodes.evidenceTitle.textContent = state.topic.evidence.label;
    nodes.evidenceSource.textContent = `来源：${state.topic.source_directory}/${state.topic.evidence.source_file}`;
    nodes.evidenceBody.innerHTML = state.topic.evidence.html;
    bindReaderLinks(nodes.evidenceBody);
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
    const overlayOpen = (isMobileNavigation() && nodes.sidebar.classList.contains("is-open"))
      || nodes.evidenceDrawer.classList.contains("is-open")
      || (chatMobileQuery.matches && state.chat.open);
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
      state.searchIndex = await fetchJson(`${dataPath("search-index.json")}?v=${snapshot}`);
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
    probeChatAvailability(); // the server may have restarted with chat on/off
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

  // ---- 研究助手对话（本地 claude CLI）----

  function chatAvailable() {
    if (!isLocalRefreshAvailable()) return false; // GitHub Pages has no server API
    return state.chat.serverEnabled === true;
  }

  // Ask the server whether chat is actually enabled (claude found, --no-chat
  // unset). The hostname check above only short-circuits static hosting.
  async function probeChatAvailability() {
    state.chat.serverEnabled = false;
    state.chat.workflowAvailable = false;
    syncChatAvailability();
    if (!isLocalRefreshAvailable()) return;
    try {
      const response = await fetch("api/chat/state", { cache: "no-store" });
      const payload = await response.json();
      state.chat.serverEnabled = Boolean(response.ok && payload.enabled);
      state.chat.workflowAvailable = Boolean(response.ok && payload.enabled && payload.workflow);
    } catch {
      state.chat.serverEnabled = false;
      state.chat.workflowAvailable = false;
    }
    syncChatAvailability();
  }

  function syncChatAvailability() {
    const available = chatAvailable();
    nodes.chatOpenButton.hidden = !available;
    syncHeroVisibility();
  }

  function syncHeroVisibility() {
    if (!nodes.homeChatHero) return;
    nodes.homeChatHero.hidden = !state.chat.workflowAvailable;
  }

  // ---- chat panel sizing: split-screen dock + fullscreen focus ------------
  // The open panel docks beside the article: its width is published as the
  // --chat-dock custom property on :root, which is the app-shell grid's 4th
  // column, so the article reflows. The divider drags that width; ⤢ takes the
  // panel fullscreen (out of the split, covering the viewport). The dock is
  // 0 unless the panel is open — the initial page never reserves space.
  // The reader panel publishes its own --reader-dock column and sits to the
  // LEFT of the chat dock (right: var(--chat-dock)) so paper + chat can be
  // visible together. The main-content max-width caps the article column, so
  // when docks squeeze the middle the article just stays at its cap.

  function clampChatWidth(width) {
    const max = Math.min(CHAT_WIDTH_MAX, Math.round(window.innerWidth * 0.38));
    return Math.max(Math.min(CHAT_WIDTH_MIN, max), Math.min(width, max));
  }

  function applyChatWidth() {
    if (chatMobileQuery.matches) {
      document.documentElement.style.setProperty("--chat-dock", "0px");
      return;
    }
    const width = state.chat.widthPx || CHAT_DEFAULT_WIDTH;
    document.documentElement.style.setProperty("--chat-dock", `${width}px`);
  }

  // Single source of truth for the dock column: 0 whenever the panel is
  // closed, mobile, or fullscreen; the saved/default width when open.
  function syncChatDock() {
    if (state.chat.open && !state.chat.focused && !chatMobileQuery.matches) {
      applyChatWidth();
    } else {
      document.documentElement.style.setProperty("--chat-dock", "0px");
    }
  }


  function setChatFocused(focused) {
    state.chat.focused = focused;
    nodes.chatPanel.classList.toggle("is-focused", focused);
    nodes.chatExpand.setAttribute("aria-pressed", String(focused));
    nodes.chatExpand.textContent = focused ? "⤡" : "⤢";
    nodes.chatExpand.dataset.tooltip = focused ? "退出全屏" : "全屏对话";
    syncChatDock();
    syncBodyScroll();
  }

  function toggleChatFocus() {
    setChatFocused(!state.chat.focused);
  }

  function bindChatResizer() {
    const resizer = nodes.chatResizer;
    if (!resizer) return;
    resizer.addEventListener("pointerdown", (event) => {
      if (chatMobileQuery.matches || state.chat.focused) return;
      event.preventDefault();
      resizer.setPointerCapture(event.pointerId);
      resizer.classList.add("is-dragging");
      state.chat.dragging = true;
      const startX = event.clientX;
      const startWidth = nodes.chatPanel.getBoundingClientRect().width;
      const onMove = (moveEvent) => {
        state.chat.widthPx = clampChatWidth(startWidth + (startX - moveEvent.clientX));
        applyChatWidth();
      };
      const onUp = () => {
        resizer.removeEventListener("pointermove", onMove);
        resizer.removeEventListener("pointerup", onUp);
        resizer.classList.remove("is-dragging");
        state.chat.dragging = false;
        try {
          localStorage.setItem(CHAT_WIDTH_KEY, String(state.chat.widthPx));
        } catch {
          // storage unavailable (private mode) — width just won't persist
        }
      };
      resizer.addEventListener("pointermove", onMove);
      resizer.addEventListener("pointerup", onUp);
    });
    try {
      const stored = Number(localStorage.getItem(CHAT_WIDTH_KEY));
      if (Number.isFinite(stored) && stored > 0) state.chat.widthPx = clampChatWidth(stored);
    } catch {
      // ignore storage errors
    }
    chatMobileQuery.addEventListener("change", () => {
      syncChatDock();
        syncBodyScroll();
    });
    syncChatDock();
  }

  function setChatOpen(open) {
    if (open && !chatAvailable()) return;
    state.chat.open = open;
    nodes.chatPanel.classList.toggle("is-open", open);
    nodes.chatPanel.setAttribute("aria-hidden", String(!open));
    nodes.chatOpenButton.setAttribute("aria-expanded", String(open));
    if (open) {
      if (state.chat.wsId) {
        setChatTitle("综述工作流");
        loadWorkflowState();
      } else if (state.chat.pane === "paper") {
        setChatTitle(state.chat.paperId ? `论文 ${state.chat.paperId}` : "论文精读");
        if (state.chat.paperId) loadPaperChatState();
      } else if (state.topic) {
        setChatTitle(state.topic.title);
        loadChatState();
      }
      applyChatWidth(); // publish the dock column when open
      setTimeout(() => nodes.chatInput.focus(), 220);
    } else {
      // Collapse the split: the article reclaims the full width.
      syncChatDock();
    }
    syncBodyScroll();
  }

  function setChatTitle(title) {
    nodes.chatTitle.textContent = title || "研究助手";
  }

  // Pane switching: the topic conversation and the workflow conversation each
  // keep their own history; the two header buttons swap the visible pane.
  // Chrome-only half of syncChatPane: buttons, forms, placeholders. Split from
  // the message rendering so a pane switch that will immediately load fresh
  // server history can skip the redundant in-memory render.
  function syncPaneChrome() {
    const workflow = state.chat.pane === "workflow";
    const paper = state.chat.pane === "paper";
    // One button per pane; a button is active/enabled exactly when its pane is.
    for (const [button, pane] of [
      [nodes.chatShowTopic, "topic"],
      [nodes.chatShowPaper, "paper"],
      [nodes.chatShowWorkflow, "workflow"],
    ]) {
      button.classList.toggle("is-active", state.chat.pane === pane);
      button.disabled = state.chat.pane !== pane;
    }
    nodes.chatShowWorkflow.hidden = !Boolean(state.chat.wsId) && !workflow;
    nodes.paperIdForm.hidden = !paper;
    nodes.chatInput.placeholder = workflow
      ? "对大纲提修改意见，或回复「继续」…"
      : paper
        ? state.chat.paperId
          ? "围绕这篇论文提问…"
          : "先在上方输入 arXiv 论文 ID 并载入。"
        : state.topic
          ? "就本话题提问，或让 Claude 写综述草稿…"
          : "先选择一个话题，再开始对话。";
  }

  function syncChatPane() {
    syncPaneChrome();
    const workflow = state.chat.pane === "workflow";
    const paper = state.chat.pane === "paper";
    if (workflow) {
      renderChatMessages();
      renderTimeline();
      setChatSessionMeta(state.chat.wsSessionId ? `会话 ${String(state.chat.wsSessionId).slice(0, 8)} · 可继续追问` : "");
    } else {
      renderTimeline(); // removes the timeline outside workflow mode
      renderChatMessages();
      if (paper) {
        const meta = state.chat.paperSessionId
          ? `会话 ${String(state.chat.paperSessionId).slice(0, 8)} · 可继续追问`
          : "";
        setChatSessionMeta(
          meta + (state.chat.paperId ? `${meta ? " · " : ""}论文 ${state.chat.paperId}` : "")
        );
      } else {
        setChatSessionMeta(state.chat.sessionId ? `会话 ${String(state.chat.sessionId).slice(0, 8)} · 可继续追问` : "");
      }
    }
  }

  function switchChatPane(pane) {
    if (state.chat.pane === pane) return;
    if (state.chat.streaming) {
      showToast("正在流式输出，等本轮结束再切换对话。");
      return;
    }
    state.chat.pane = pane;
    nodes.chatMessages.innerHTML = "";
    setChatStatus(null);
    // The state loaders below fetch server history and render it; without one,
    // syncChatPane's own render shows the in-memory history (first paint).
    const loaderWillRender =
      (pane === "workflow" && state.chat.wsId && state.chat.open) ||
      (pane === "paper") ||
      (pane === "topic" && state.topic && state.chat.open);
    if (loaderWillRender) {
      syncPaneChrome();
    } else {
      syncChatPane();
    }
    if (pane === "workflow" && state.chat.wsId && state.chat.open) loadWorkflowState();
    else if (pane === "paper") loadPaperChatState();
    else if (pane === "topic" && state.topic && state.chat.open) loadChatState();
  }

  function setChatSessionMeta(text) {
    nodes.chatSessionMeta.textContent = text || "";
  }

  function setChatStatus(text) {
    if (!text) {
      nodes.chatStatus.hidden = true;
      nodes.chatStatus.textContent = "";
      return;
    }
    nodes.chatStatus.textContent = text;
    nodes.chatStatus.hidden = false;
  }

  function setChatStreaming(streaming) {
    state.chat.streaming = streaming;
    nodes.chatSend.disabled = streaming;
    nodes.chatStop.hidden = !streaming;
  }

  function chatNearBottom() {
    const box = nodes.chatMessages;
    return box.scrollHeight - box.scrollTop - box.clientHeight < 80;
  }

  // Autoscroll reads layout; coalesce to one scroll per frame while deltas
  // stream in instead of forcing a reflow per SSE event.
  let chatScrollPending = false;
  function chatScrollToBottom(force = false) {
    if (!force && !chatNearBottom()) return;
    if (chatScrollPending) return;
    chatScrollPending = true;
    requestAnimationFrame(() => {
      chatScrollPending = false;
      nodes.chatMessages.scrollTop = nodes.chatMessages.scrollHeight;
    });
  }

  function appendChatMessage(role, text) {
    const item = document.createElement("div");
    item.className = `chat-msg chat-msg-${role}`;
    const body = document.createElement("div");
    body.className = role === "assistant" ? "chat-msg-text markdown-body" : "chat-msg-text";
    body.textContent = text;
    item.appendChild(body);
    nodes.chatMessages.appendChild(item);
    chatScrollToBottom(true);
    return item;
  }

  function appendChatSystemNote(text) {
    const note = document.createElement("p");
    note.className = "chat-system-note";
    note.textContent = text;
    nodes.chatMessages.appendChild(note);
    chatScrollToBottom(true);
  }

  function appendChatError(text) {
    const note = document.createElement("p");
    note.className = "chat-msg-error";
    note.textContent = text;
    nodes.chatMessages.appendChild(note);
    chatScrollToBottom(true);
  }

  function setChatSession(sessionId) {
    if (state.chat.pane === "workflow") {
      state.chat.wsSessionId = sessionId || null;
    } else if (state.chat.pane === "paper") {
      state.chat.paperSessionId = sessionId || null;
    } else {
      state.chat.sessionId = sessionId || null;
    }
    setChatSessionMeta(
      sessionId ? `会话 ${String(sessionId).slice(0, 8)} · 可继续追问` : "新话题 · 还没有对话记录"
    );
  }

  function activeMessages() {
    if (state.chat.pane === "workflow") return state.chat.wsMessages;
    if (state.chat.pane === "paper") return state.chat.paperMessages;
    return state.chat.messages;
  }

  function renderChatMessages() {
    nodes.chatMessages.innerHTML = "";
    for (const message of activeMessages()) {
      const item = appendChatMessage(message.role, "");
      const body = item.querySelector(".chat-msg-text");
      if (message.role === "assistant") body.innerHTML = renderChatMarkdown(message.text);
      else body.textContent = message.text;
    }
    chatScrollToBottom(true);
  }

  function resetChatView() {
    if (state.chat.pane === "workflow") {
      state.chat.wsSessionId = null;
      state.chat.wsMessages = [];
    } else if (state.chat.pane === "paper") {
      state.chat.paperSessionId = null;
      state.chat.paperMessages = [];
    } else {
      state.chat.sessionId = null;
      state.chat.messages = [];
    }
    nodes.chatMessages.innerHTML = "";
    setChatSessionMeta("");
    setChatStatus(null);
  }

  async function loadChatState() {
    if (!state.topic) return;
    const topicId = state.topic.id;
    try {
      const response = await fetch(`api/chat/state?topic=${encodeURIComponent(topicId)}`, { cache: "no-store" });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `读取失败（${response.status}）`);
      if (state.topic?.id !== topicId) return; // topic switched mid-flight
      state.chat.messages = Array.isArray(payload.messages) ? payload.messages : [];
      renderChatMessages();
      state.chat.sessionId = payload.session_id || null;
      setChatSessionMeta(payload.session_id ? `会话 ${String(payload.session_id).slice(0, 8)} · 可继续追问` : "");
    } catch (error) {
      setChatSessionMeta(`对话状态读取失败：${error.message}`);
    }
  }

  // Minimal markdown for finished assistant replies: fenced code, inline code,
  // bold, links, headings, lists, paragraphs. Input is escaped first, so no
  // raw HTML ever reaches innerHTML.
  function renderChatMarkdown(text) {
    const escaped = escapeHtml(text);
    const fences = [];
    const withFences = escaped.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (_match, lang, code) => {
      fences.push(`<pre><code${lang ? ` data-lang="${lang}"` : ""}>${code.replace(/\n$/, "")}</code></pre>`);
      return ` FENCE${fences.length - 1} `;
    });
    const inline = withFences
      .replace(/`([^`\n]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    const blocks = inline.split(/\n{2,}/).map((block) => {
      const fenceMatch = block.match(/^ FENCE(\d+) $/);
      if (fenceMatch) return fences[Number(fenceMatch[1])];
      const lines = block.split("\n");
      if (lines.every((line) => /^\s*([-*]|\d+\.)\s+/.test(line))) {
        const items = lines.map((line) => `<li>${line.replace(/^\s*([-*]|\d+\.)\s+/, "")}</li>`).join("");
        return /^\s*\d+\./.test(lines[0]) ? `<ol>${items}</ol>` : `<ul>${items}</ul>`;
      }
      const heading = block.match(/^(#{1,4})\s+(.*)$/);
      if (heading) {
        const level = Math.min(heading[1].length + 1, 6);
        return `<h${level}>${heading[2]}</h${level}>`;
      }
      return `<p>${block.replace(/\n/g, "<br>")}</p>`;
    });
    return blocks.join("");
  }

  function renderFinalAssistant(item, text) {
    const body = item.querySelector(".chat-msg-text");
    body.innerHTML = text ? renderChatMarkdown(text) : "";
  }

  // Incremental markdown during streaming: re-render the accumulated reply on
  // an animation-frame cadence so line breaks, headings and lists appear as
  // they arrive instead of piling into one pre-wrap run. Cheap for chat-length
  // texts (≤ a few KB); the final render still happens once at stream end.
  function makeStreamingRenderer(item) {
    const body = item.querySelector(".chat-msg-text");
    let acc = "";
    let scheduled = false;
    let lastRendered = 0;
    // Full re-render of the accumulated text is O(n) per call; rAF alone still
    // re-renders at 60fps (multi-MB regex work on long workflow replies).
    // Throttle to ~5 renders/s while streaming; the final text is always
    // rendered by renderFinalAssistant.
    const RENDER_INTERVAL_MS = 200;
    return {
      append(text) {
        acc += text || "";
        if (scheduled) return;
        const wait = Math.max(0, RENDER_INTERVAL_MS - (Date.now() - lastRendered));
        scheduled = true;
        setTimeout(() => {
          scheduled = false;
          lastRendered = Date.now();
          body.innerHTML = renderChatMarkdown(acc);
          chatScrollToBottom();
        }, wait);
      },
      text() {
        return acc;
      },
    };
  }

  // ---- inline arXiv reader -------------------------------------------------
  // arXiv links in articles/evidence open the paper IN THIS PAGE: the reader
  // is a view inside #article-view (same layout as a topic card), hash-routed
  // as #/paper/<id> so browser Back returns to the topic. Documents are cached
  // in memory + sessionStorage and rendered progressively while the response
  // streams in (first fetch paints before the whole paper has arrived).

  const ARXIV_ID_RE = /^(?:[a-z-]+(?:\.[A-Za-z]{2})?\/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?$/i;
  const READER_CACHE_KEY = "wiki.reader.cache.v1";
  const READER_CACHE_LIMIT = 6; // sessionStorage entries to keep

  const readerCache = new Map(); // paper_id → {title, body_html}

  function parseArxivLink(href) {
    if (!href) return null;
    let candidate = href.trim();
    if (/^\/api\/reader\//.test(candidate)) {
      candidate = candidate.slice("/api/reader/".length);
    }
    if (/^https?:\/\//i.test(candidate)) {
      try {
        const url = new URL(candidate);
        if (!/(^|\.)arxiv\.org$/i.test(url.hostname)) return null;
        const match = url.pathname.match(/\/(?:abs|html|pdf|doi)\/(.+?)(?:\.pdf)?\/?$/);
        if (!match) return null;
        candidate = match[1];
      } catch {
        return null;
      }
    }
    candidate = candidate.replace(/\.html$/i, "").replace(/\/+$/, "");
    if (!ARXIV_ID_RE.test(candidate)) return null;
    return candidate.replace(/v\d+$/i, "");
  }

  // Bind a container's arXiv links (and in-doc citation links) to the
  // same-page reader. Regular external links keep their behavior.
  function bindReaderLinks(container) {
    container.querySelectorAll('a[href]').forEach((link) => {
      const paperId = parseArxivLink(link.getAttribute("href")) || parseArxivLink(link.dataset.arxiv || "");
      if (!paperId) return;
      link.classList.add("arxiv-reader-link");
      link.addEventListener("click", (event) => {
        event.preventDefault();
        openReader(paperId);
      });
    });
  }

  function cacheRead(paperId) {
    if (readerCache.has(paperId)) return readerCache.get(paperId);
    try {
      const store = JSON.parse(sessionStorage.getItem(READER_CACHE_KEY) || "{}");
      if (store[paperId]) {
        readerCache.set(paperId, store[paperId]);
        return store[paperId];
      }
    } catch {
      // storage unavailable — memory cache only
    }
    return null;
  }

  function cacheWrite(paperId, entry) {
    readerCache.set(paperId, entry);
    try {
      const store = JSON.parse(sessionStorage.getItem(READER_CACHE_KEY) || "{}");
      store[paperId] = entry;
      const keys = Object.keys(store);
      while (keys.length > READER_CACHE_LIMIT) delete store[keys.shift()];
      sessionStorage.setItem(READER_CACHE_KEY, JSON.stringify(store));
    } catch {
      // storage full/unavailable — memory cache already updated
    }
  }

  function paperRoute(paperId) {
    return `#/paper/${encodeURIComponent(paperId)}`;
  }

  function parsePaperRoute() {
    const match = location.hash.match(/^#\/paper\/([^?]+)/);
    return match ? decodeURIComponent(match[1]) : null;
  }

  function readerViewActive() {
    return !nodes.readerViewHeader.hidden;
  }

  function setReaderView(on) {
    nodes.articleHeader.hidden = on;
    nodes.readerViewHeader.hidden = !on;
    nodes.readingMeta.hidden = on;
    nodes.articleFooter.hidden = on;
    nodes.tocPanel.hidden = on;
    // Leaving the reader must also undo switchReaderTab(true): otherwise the
    // 速读 card stays visible (and #article-body stays hidden) on top of
    // every subsequently rendered topic card.
    if (!on) resetQuickReadTab();
  }

  function showReaderSkeleton(paperId) {
    nodes.article.hidden = false;
    nodes.welcome.hidden = true;
    nodes.error.hidden = true;
    setReaderView(true);
    nodes.readerViewId.textContent = `arXiv:${paperId}`;
    nodes.readerViewTitle.textContent = "正在加载论文…";
    nodes.readerOpenExternal.onclick = () => window.open(`https://arxiv.org/abs/${paperId}`, "_blank", "noopener");
    nodes.articleBody.className = "markdown-body reader-document";
    nodes.articleBody.innerHTML =
      '<div class="reader-skeleton">' +
      '<div class="reader-skel-line is-title"></div>' +
      '<div class="reader-skel-line"></div>'.repeat(8) +
      "</div>";
    nodes.readerProgress.hidden = false;
    nodes.readerProgressBar.style.width = "8%";
    nodes.readerProgressLabel.textContent = "正在获取全文…（首次需要几秒，之后走本地缓存）";
    document.title = `arXiv:${paperId}｜空间智能研究 Wiki`;
  }

  function setReaderTitleFromDoc(doc) {
    const title = doc.querySelector("title")?.textContent?.trim();
    if (title) {
      nodes.readerViewTitle.textContent = title;
      document.title = `${title}｜空间智能研究 Wiki`;
    }
  }

  function extractReaderBody(doc) {
    // The cleaned server document is a standalone page; lift its body content
    // (styles were inlined into <head> — carry them into the main document).
    const frag = document.createDocumentFragment();
    doc.querySelectorAll("style").forEach((styleNode) => {
      // Namespace paper styles under .reader-document to avoid leaking into
      // the wiki chrome.
      const scoped = document.createElement("style");
      scoped.textContent = (styleNode.textContent || "")
        .replace(/(^|\n)body\s*{/, "\n.reader-document {")
        .replace(/(^|\n)(h1|h2|h3|h4|a|img|figure|figcaption|table|td|th)\s*([,{])/g,
          "\n.reader-document $1$2$3");
      frag.appendChild(scoped);
    });
    const body = doc.body;
    if (!body) return frag;
    for (const node of [...body.childNodes]) {
      if (node.nodeType === Node.ELEMENT_NODE && ["style", "script"].includes(node.tagName.toLowerCase())) continue;
      frag.appendChild(node);
    }
    return frag;
  }

  function renderReaderMath() {
    // Paper pages carry LaTeX source in code.math-inline (from the server's
    // LaTeXML cleanup). Render with KaTeX when the CDN is reachable; leave
    // the readable source in place otherwise.
    const mathNodes = nodes.articleBody.querySelectorAll("code.math-inline");
    if (!mathNodes.length || typeof window.katex !== "object" || !window.katex) return;
    mathNodes.forEach((node) => {
      const source = node.textContent || "";
      const holder = document.createElement("span");
      holder.className = "math-rendered";
      try {
        window.katex.render(source, holder, { throwOnError: false, displayMode: false });
        node.replaceWith(holder);
      } catch {
        // keep the raw source
      }
    });
  }

  function bindReaderDocumentLinks(container, paperId) {
    container.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const linked = parseArxivLink(link.dataset.arxiv || "");
        if (linked) {
          setRouteHash(paperRoute(linked));
          return;
        }
        const href = link.getAttribute("href") || "";
        if (href.startsWith("#")) {
          container.querySelector(href)?.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }

  async function loadPaper(paperId) {
    if (state.readerAbort) state.readerAbort.abort();
    const controller = new AbortController();
    state.readerAbort = controller;
    resetQuickReadTab();
    showReaderSkeleton(paperId);

    // Warm cache: paint instantly, no fetch at all.
    const cached = cacheRead(paperId);
    if (cached) {
      const doc = new DOMParser().parseFromString(
        `<!doctype html><html><head><title>${escapeHtml(cached.title)}</title></head><body>${cached.body_html}</body></html>`,
        "text/html",
      );
      setReaderTitleFromDoc(doc);
      nodes.articleBody.innerHTML = "";
      const frag = extractReaderBody(doc);
      nodes.articleBody.appendChild(frag);
      nodes.readerProgress.hidden = true;
      bindReaderDocumentLinks(nodes.articleBody, paperId);
      renderReaderMath();
      window.scrollTo({ top: 0, behavior: "instant" });
      return;
    }

    try {
      const response = await fetch(`api/reader/${paperId}`, { signal: controller.signal });
      if (!response.ok) throw new Error(`读取失败（${response.status}）`);
      const text = await response.text();
      if (controller.signal.aborted) return;
      const doc = new DOMParser().parseFromString(text, "text/html");

      if (doc.body?.dataset.readerDoc === "unavailable") {
        nodes.articleBody.innerHTML = "";
        nodes.articleBody.appendChild(extractReaderBody(doc));
        nodes.readerProgress.hidden = true;
        setReaderTitleFromDoc(doc);
        return;
      }

      // Streaming paint: push the body content in progressively — first the
      // head sections, then the rest as one pass over top-level nodes.
      setReaderTitleFromDoc(doc);
      const frag = extractReaderBody(doc);
      nodes.articleBody.innerHTML = "";
      nodes.articleBody.appendChild(frag);
      nodes.readerProgressBar.style.width = "100%";
      nodes.readerProgressLabel.textContent = "加载完成";
      setTimeout(() => { nodes.readerProgress.hidden = true; }, 600);
      bindReaderDocumentLinks(nodes.articleBody, paperId);
      renderReaderMath();
      window.scrollTo({ top: 0, behavior: "instant" });

      // Cache for the next visit (memory + sessionStorage).
      const bodyHtml = doc.body ? doc.body.innerHTML : "";
      cacheWrite(paperId, { title: doc.title || `arXiv:${paperId}`, body_html: bodyHtml });
    } catch (error) {
      if (controller.signal.aborted) return;
      nodes.articleBody.innerHTML = `<p class="reader-load-error">论文加载失败：${escapeHtml(error.message)}</p>`;
      nodes.readerProgress.hidden = true;
    } finally {
      if (state.readerAbort === controller) state.readerAbort = null;
    }
  }

  function openReader(paperId) {
    const target = paperRoute(paperId);
    if (location.hash === target) loadPaper(paperId);
    else location.hash = target; // hashchange → loadPaper
  }

  function closeReaderToTopic() {
    if (state.readerAbort) state.readerAbort.abort();
    if (state.topic) setRoute(state.topic.id, state.version, false);
    else setRouteHash("#/");
  }

  // ---- quick-read (速读) tab ------------------------------------------------
  // The reader shows either the paper document or its single-paper quick-read
  // card. The card is generated server-side by quick_read_paper.py (pooled,
  // deep-read gated); the tab loads lazily on first click.

  function resetQuickReadTab() {
    nodes.readerQuickReadTab.setAttribute("aria-pressed", "false");
    nodes.readerQuickReadTab.classList.remove("is-active");
    nodes.readerQuickReadBody.hidden = true;
    nodes.readerQuickReadBody.innerHTML = "";
    nodes.articleBody.hidden = false;
  }

  function switchReaderTab(showQuickRead) {
    nodes.readerQuickReadTab.setAttribute("aria-pressed", String(showQuickRead));
    nodes.readerQuickReadTab.classList.toggle("is-active", showQuickRead);
    nodes.readerQuickReadBody.hidden = !showQuickRead;
    nodes.articleBody.hidden = showQuickRead;
  }

  function renderQuickReadCard(paperId, markdown) {
    nodes.readerQuickReadBody.innerHTML = markdown ? renderChatMarkdown(markdown) : "";
    bindReaderLinks(nodes.readerQuickReadBody);
  }

  function quickReadPlaceholder(paperId, payload) {
    const agentReady = payload?.agent_available !== false;
    const deepStatus = payload?.deep_read_status || "未深读";
    return `
      <div class="quickread-placeholder">
        <p><strong>还没有这篇论文的速读卡。</strong></p>
        <p>速读基于已审计的深读笔记生成（当前深读状态：${escapeHtml(deepStatus)}），首次生成约需 1-3 分钟。</p>
        <button type="button" id="quickread-generate-button" ${agentReady ? "" : "disabled"}>生成速读</button>
        ${agentReady ? "" : '<p class="reader-load-error">claude CLI 不可用，无法生成速读。</p>'}
      </div>`;
  }

  async function loadQuickReadState(paperId) {
    if (state.quickRead.has(paperId)) {
      renderQuickReadCard(paperId, state.quickRead.get(paperId));
      return;
    }
    nodes.readerQuickReadBody.innerHTML = '<p class="reader-load-error">正在检查速读缓存…</p>';
    try {
      const response = await fetch(`api/paper/quickread/state?id=${encodeURIComponent(paperId)}`);
      if (!response.ok) throw new Error(`状态读取失败（${response.status}）`);
      const payload = await response.json();
      if (payload.quick_read && payload.markdown) {
        state.quickRead.set(paperId, payload.markdown);
        renderQuickReadCard(paperId, payload.markdown);
        return;
      }
      nodes.readerQuickReadBody.innerHTML = quickReadPlaceholder(paperId, payload);
      const button = nodes.readerQuickReadBody.querySelector("#quickread-generate-button");
      if (button) button.addEventListener("click", () => generateQuickRead(paperId));
    } catch (error) {
      nodes.readerQuickReadBody.innerHTML =
        `<p class="reader-load-error">速读状态读取失败：${escapeHtml(error.message)}</p>`;
    }
  }

  async function generateQuickRead(paperId) {
    if (state.quickReadGenerating) return;
    state.quickReadGenerating = paperId;
    nodes.readerProgress.hidden = false;
    nodes.readerProgressBar.style.width = "30%";
    nodes.readerProgressLabel.textContent = "正在生成速读（深读校验 → 写作简报 → 成稿）…";
    const button = nodes.readerQuickReadBody.querySelector("#quickread-generate-button");
    if (button) { button.disabled = true; button.textContent = "生成中…"; }
    try {
      const response = await fetch("api/paper/quickread", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ arxiv_id: paperId }),
      });
      if (response.status === 409) {
        showToast("该论文已有速读生成正在进行，请稍候。");
        return;
      }
      if (!response.ok) throw new Error(`生成请求失败（${response.status}）`);
      await consumeSSE(response, (event) => {
        if (event.type === "stage") {
          nodes.readerProgressLabel.textContent = event.detail || "正在生成速读…";
        } else if (event.type === "quickread_done") {
          state.quickRead.set(paperId, event.markdown);
          renderQuickReadCard(paperId, event.markdown);
        } else if (event.type === "topic_error") {
          nodes.readerQuickReadBody.innerHTML =
            `<p class="reader-load-error">${escapeHtml(event.message || "速读生成失败")}</p>`;
        }
      });
    } catch (error) {
      nodes.readerQuickReadBody.innerHTML =
        `<p class="reader-load-error">速读生成失败：${escapeHtml(error.message)}</p>`;
    } finally {
      state.quickReadGenerating = null;
      nodes.readerProgressBar.style.width = "100%";
      nodes.readerProgressLabel.textContent = "速读完成";
      setTimeout(() => { nodes.readerProgress.hidden = true; }, 600);
    }
  }

  // ---- selection → @-quote context ----------------------------------------
  // Selecting text in the article, evidence drawer, or reader iframe shows a
  // "引用到对话" chip; clicking it stores the excerpt as a pending quote that
  // rides along with the next message (rendered as chips above the composer,
  // like an @ mention).

  const QUOTE_MAX_CHARS = 1200;

  function selectionContainer(selection) {
    const node = selection.anchorNode;
    if (!node) return null;
    const element = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    return element?.closest?.("#article-body, #evidence-body") || null; // article-body also hosts the reader view
  }

  function usableSelection() {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) return null;
    const rangeCount = selection.rangeCount;
    if (!rangeCount) return null;
    // Only plain-text selections rooted in quotable containers.
    if (!selectionContainer(selection)) return null;
    const text = String(selection).replace(/\s+/g, " ").trim();
    if (text.length < 2) return null;
    return { text: text.slice(0, QUOTE_MAX_CHARS), truncated: text.length > QUOTE_MAX_CHARS };
  }

  function positionSelectionPopup(selection) {
    const rect = selection.getRangeAt(0).getBoundingClientRect();
    const popup = nodes.selectionPopup;
    popup.hidden = false;
    const left = Math.min(Math.max(8, rect.left + rect.width / 2 - popup.offsetWidth / 2), window.innerWidth - popup.offsetWidth - 8);
    const top = Math.max(8, rect.top - popup.offsetHeight - 8);
    popup.style.left = `${left}px`;
    popup.style.top = `${top}px`;
  }

  function addQuote(quote) {
    state.chat.quotes.push(quote);
    renderQuoteChips();
  }

  function removeQuote(index) {
    state.chat.quotes.splice(index, 1);
    renderQuoteChips();
  }

  function renderQuoteChips() {
    let strip = nodes.chatForm.querySelector(".chat-quote-strip");
    if (!state.chat.quotes.length) {
      strip?.remove();
      return;
    }
    if (!strip) {
      strip = document.createElement("div");
      strip.className = "chat-quote-strip";
      nodes.chatForm.prepend(strip);
    }
    strip.innerHTML = state.chat.quotes.map((quote, index) => `
      <span class="chat-quote-chip" title="${escapeHtml(quote.text)}">
        <span class="chat-quote-source">${escapeHtml(quote.source)}</span>
        <span class="chat-quote-text">${escapeHtml(quote.text.slice(0, 60))}${quote.text.length > 60 ? "…" : ""}</span>
        <button type="button" class="chat-quote-remove" data-quote-index="${index}" aria-label="移除引用">×</button>
      </span>`).join("");
  }

  function selectionSourceLabel() {
    if (readerViewActive()) return "论文";
    if (state.topic) return state.topic.title || "本文";
    return "页面";
  }

  function bindSelectionQuote() {
    document.addEventListener("pointerup", (event) => {
      if (nodes.selectionPopup.contains(event.target)) return;
      const quote = usableSelection();
      if (!quote) {
        nodes.selectionPopup.hidden = true;
        return;
      }
      quote.source = selectionSourceLabel();
      positionSelectionPopup(window.getSelection());
    });
    document.addEventListener("selectionchange", () => {
      if (!usableSelection()) nodes.selectionPopup.hidden = true;
    });
    nodes.selectionCite.addEventListener("click", () => {
      const quote = usableSelection();
      nodes.selectionPopup.hidden = true;
      window.getSelection()?.removeAllRanges();
      if (quote) {
        addQuote(quote);
        if (!state.chat.open) setChatOpen(true);
        nodes.chatInput.focus();
      }
    });
    nodes.chatForm.addEventListener("click", (event) => {
      const button = event.target.closest("[data-quote-index]");
      if (button) removeQuote(Number(button.dataset.quoteIndex));
    });
  }

  function composeMessageWithContext(message) {
    if (!state.chat.quotes.length) return message;
    const blocks = state.chat.quotes.map((quote, index) => {
      const origin = quote.paper_id ? `（arXiv:${quote.paper_id}）` : "";
      return `<quote_${index + 1} source="${quote.source}${origin}">\n${quote.text}\n</quote_${index + 1}>`;
    });
    return `${blocks.join("\n")}\n\n${message}`;
  }

  function consumeQuotes() {
    const quotes = state.chat.quotes;
    state.chat.quotes = [];
    renderQuoteChips();
    return quotes;
  }

  // ---- workflow mode (综述工作流) ----------------------------------------

  function paperMode() {
    return state.chat.pane === "paper";
  }

  // ---- paper chat (单篇论文精读对话) ---------------------------------------
  // One conversation per arXiv id, cached server-side by id. First contact
  // triggers prepare (extraction → pool → deep read) with visible progress;
  // later visits reuse the cache instantly.

  async function loadPaperChatState() {
    setChatTitle("论文精读");
    if (!state.chat.paperId) return;
    try {
      const response = await fetch(`api/paper/chat/state?id=${encodeURIComponent(state.chat.paperId)}`);
      if (!response.ok) return;
      const payload = await response.json();
      if (!payload.enabled) return;
      state.chat.paperMessages = Array.isArray(payload.messages) ? payload.messages : [];
      state.chat.paperSessionId = payload.session_id || null;
      renderChatMessages();
      const status = payload.deep_read_status
        ? `深读 ${payload.deep_read_status}`
        : payload.pooled ? "已入池（未深读）" : "未入池";
      setChatSessionMeta(`论文 ${state.chat.paperId} · ${status}`);
    } catch {
      // state probe is best-effort; the chat still works
    }
  }

  async function loadPaperById(rawId) {
    const arxivId = String(rawId || "").trim().replace(/^arxiv:/i, "").split("/").pop().replace(/v\d+$/i, "");
    if (!/^\d{4}\.\d{4,5}$/.test(arxivId)) {
      showToast("请输入有效的 arXiv ID，例如 2402.10329。");
      return;
    }
    if (state.chat.streaming) {
      showToast("正在流式输出，等本轮结束再切换论文。");
      return;
    }
    state.chat.paperId = arxivId;
    state.chat.paperMessages = [];
    state.chat.paperSessionId = null;
    nodes.chatMessages.innerHTML = "";
    setChatStatus(null);
    syncChatPane();
    setChatTitle(`论文 ${arxivId}`);
    await loadPaperChatState();
    nodes.chatInput.focus();
  }

  async function streamPaperChat(composedMessage, displayText) {
    if (!state.chat.paperId) {
      showToast("先在上方输入 arXiv 论文 ID 并载入。");
      nodes.paperIdInput.focus();
      return;
    }
    appendChatUserMessage(displayText, []);
    await streamTurn({
      endpoint: "api/paper/chat",
      payload: { arxiv_id: state.chat.paperId, message: composedMessage, model: selectedChatModel() || undefined },
      onEvent: handlePaperChatEvent,
      history: state.chat.paperMessages,
      errorLabel: "对话失败",
    });
  }

  function handlePaperChatEvent(evt, renderer) {
    if (evt.type === "stage") {
      // Paper-chat-only event: preparation progress (extraction / deep read)
      // streams as stage events before claude's first token.
      setChatStatus(evt.detail || "正在准备论文…");
      return;
    }
    handleChatEvent(evt, renderer);
  }

  async function resetPaperChat() {
    if (!state.chat.paperId) return;
    if (state.chat.streaming) abortChat();
    if (state.chat.paperMessages.length && !window.confirm("开启新对话？这篇论文的对话记录将被清空（深读缓存保留）。")) return;
    try {
      await fetch("api/paper/chat/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ arxiv_id: state.chat.paperId }),
      });
    } catch {
      // reset is best-effort; the view clears regardless
    }
    state.chat.paperMessages = [];
    state.chat.paperSessionId = null;
    nodes.chatMessages.innerHTML = "";
    setChatSessionMeta("");
    setChatStatus(null);
  }

  function workflowMode() {
    return state.chat.pane === "workflow";
  }

  function setWorkflowSession(wsId) {
    state.chat.wsId = wsId || null;
    try {
      if (wsId) localStorage.setItem("wiki.workflow.ws", wsId);
      else localStorage.removeItem("wiki.workflow.ws");
    } catch {
      // storage unavailable — workspace just won't persist across reloads
    }
  }

  function stageIndex(stage) {
    return WORKFLOW_STAGES.findIndex(([name]) => name === stage);
  }

  function renderTimeline() {
    let timeline = nodes.chatMessages.querySelector(".chat-timeline");
    if (!workflowMode()) {
      timeline?.remove();
      return;
    }
    const activeIndex = state.chat.stage === null ? -1 : stageIndex(state.chat.stage);
    if (!timeline) {
      timeline = document.createElement("div");
      timeline.className = "chat-timeline";
      nodes.chatMessages.prepend(timeline);
    }
    timeline.innerHTML = WORKFLOW_STAGES.map(([name, label], index) => {
      let statusClass = "";
      let glyph = "⬚";
      if (state.chat.awaitingInput && index === activeIndex) {
        statusClass = "is-paused";
        glyph = "⏸";
      } else if (index < activeIndex) {
        statusClass = "is-done";
        glyph = "✅";
      } else if (index === activeIndex) {
        statusClass = "is-active";
        glyph = "⏳";
      }
      return `<span class="chat-stage ${statusClass}">${glyph} ${escapeHtml(label)}</span>`;
    }).join("");
  }

  async function loadWorkflowState() {
    if (!state.chat.wsId) return;
    const wsId = state.chat.wsId;
    try {
      const response = await fetch(`api/workflow/state?ws_id=${encodeURIComponent(wsId)}`, { cache: "no-store" });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `读取失败（${response.status}）`);
      if (state.chat.wsId !== wsId) return; // workspace switched mid-flight
      state.chat.wsMessages = Array.isArray(payload.messages) ? payload.messages : [];
      state.chat.stage = payload.stage || null;
      state.chat.awaitingInput = Boolean(payload.awaiting_input);
      renderChatMessages();
      renderTimeline();
      state.chat.wsSessionId = payload.session_id || null;
      setChatSessionMeta(payload.session_id ? `会话 ${String(payload.session_id).slice(0, 8)} · 可继续追问` : "");
    } catch (error) {
      setChatSessionMeta(`工作流状态读取失败：${error.message}`);
    }
  }

  function handleWorkflowEvent(evt, renderer) {
    if (evt.type === "stage") {
      state.chat.stage = evt.stage;
      state.chat.awaitingInput = false;
      renderTimeline();
      if (evt.detail) setChatStatus(`${evt.detail}…`);
      return;
    }
    if (evt.type === "awaiting_input") {
      state.chat.awaitingInput = true;
      state.chat.stage = evt.stage || state.chat.stage;
      renderTimeline();
      appendChatSystemNote("大纲已生成。回复「继续」或提出修改意见后，将撰写三种成稿并落盘。");
      return;
    }
    if (evt.type === "topic_ready") {
      state.chat.awaitingInput = false;
      state.chat.stage = "settle";
      renderTimeline();
      const title = evt.title || evt.topic_id;
      const note = document.createElement("p");
      note.className = "chat-system-note";
      note.innerHTML = `综述已发布：<a href="#/topic/${escapeHtml(evt.topic_id)}?version=zhihu">${escapeHtml(title)}</a>`;
      nodes.chatMessages.appendChild(note);
      chatScrollToBottom(true);
      return;
    }
    if (evt.type === "topic_error") {
      state.chat.awaitingInput = false;
      appendChatError(evt.message || "综述落盘后未能定位新话题。");
      return;
    }
    handleChatEvent(evt, renderer);
  }

  function selectedChatModel() {
    return nodes.chatModel?.value || null;
  }

  async function streamWorkflow(composedMessage, displayText, quotes) {
    if (state.chat.streaming) return;
    if (!state.chat.wsId) {
      const confirmed = window.confirm("当前没有进行中的工作流，将开始一次新的综述工作流。继续吗？");
      if (!confirmed) return;
    }
    appendChatUserMessage(displayText, quotes);
    await streamTurn({
      endpoint: "api/workflow",
      payload: {
        message: composedMessage,
        model: selectedChatModel() || undefined,
        ws_id: state.chat.wsId || undefined,
      },
      onEvent: handleWorkflowEvent,
      history: state.chat.wsMessages,
      errorLabel: "工作流失败",
      onResponse: (response) => {
        const wsId = response.headers.get("X-Workflow-Id");
        if (wsId && !workflowMode()) setWorkflowSession(wsId);
      },
    });
    if (state.chat.awaitingInput) setWorkflowSession(state.chat.wsId);
  }

  async function consumeSSE(response, onEvent) {
    // Shared SSE frame reader for streamChat and streamWorkflow: splits
    // newline-delimited `data:` frames and dispatches parsed JSON events.
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let index;
      while ((index = buffer.indexOf("\n\n")) !== -1) {
        const frame = buffer.slice(0, index);
        buffer = buffer.slice(index + 2);
        for (const line of frame.split("\n")) {
          if (!line.startsWith("data:")) continue;
          try {
            onEvent(JSON.parse(line.slice(5).trim()));
          } catch {
            // malformed frame — skip
          }
        }
      }
    }
  }

  async function resetWorkflow() {
    if (!state.chat.wsId) return;
    if (state.chat.streaming) abortChat();
    if (state.chat.messages.length && !window.confirm("重置工作流？当前对话记录将被清空（已产生的运行文件保留在磁盘）。")) return;
    try {
      await fetch("api/workflow/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ws_id: state.chat.wsId }),
      });
    } catch {
      // reset is best-effort; the view clears regardless
    }
    setWorkflowSession(null);
    state.chat.stage = null;
    state.chat.awaitingInput = false;
    state.chat.pane = "topic";
    nodes.chatMessages.innerHTML = "";
    resetChatView();
    syncChatPane();
    if (state.topic) {
      setChatTitle(state.topic.title);
      await loadChatState();
    } else {
      setChatTitle("研究助手");
      setChatSession(null);
    }
  }

  // ---- homepage hero + interview card ------------------------------------

  function showInterviewCard(topic) {
    // The preset-question interview card: fixed choices for the workflow
    // parameters, compiled to a params object on confirm. Pure frontend —
    // deterministic, testable, zero-latency (unlike free-text interviewing).
    const card = nodes.interviewCard;
    card.innerHTML = `
      <h2>开始前，先确认几个问题</h2>
      <p class="interview-topic">综述主题：${escapeHtml(topic)}</p>
      <p class="interview-question">① 综述模式</p>
      <div class="interview-options" role="radiogroup" aria-label="综述模式">
        <label><input type="radio" name="iw-mode" value="rapid" checked>rapid 快速 · 8 篇底线</label>
        <label><input type="radio" name="iw-mode" value="scoping">scoping 标准 · 15 篇</label>
        <label><input type="radio" name="iw-mode" value="systematic">systematic 系统 · 30 篇</label>
      </div>
      <p class="interview-question">② 检索范围</p>
      <div class="interview-options" role="radiogroup" aria-label="检索范围">
        <label><input type="radio" name="iw-range" value="6mo">近 6 个月</label>
        <label><input type="radio" name="iw-range" value="3y" checked>近 3 年</label>
        <label><input type="radio" name="iw-range" value="10y">近 10 年</label>
        <label><input type="radio" name="iw-range" value="20y">近 20 年</label>
        <label><input type="radio" name="iw-range" value="custom">自定义</label>
      </div>
      <div id="iw-custom-range" hidden>
        <p class="interview-question">自定义范围（YYYY-MM-DD..YYYY-MM-DD）</p>
        <input type="text" id="iw-range-input" placeholder="2024-01-01..2026-09-01" style="width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:13.5px;">
      </div>
      <p class="interview-question">③ 目标风格</p>
      <div class="interview-options" role="radiogroup" aria-label="目标风格">
        <label><input type="radio" name="iw-style" value="scientific-memo" checked>仅科研备忘录</label>
        <label><input type="radio" name="iw-style" value="expert-explainer">仅知乎解释版</label>
        <label><input type="radio" name="iw-style" value="all">三风格全套（科研 memo / 知乎 / 小红书）</label>
      </div>
      <p class="interview-question">④ 检索策略</p>
      <div class="interview-options" role="radiogroup" aria-label="检索策略">
        <label><input type="radio" name="iw-strategy" value="smart" checked>智能（推荐）· 分类法底座 + agent 动态扩展，指定种子时引文网络扩张</label>
        <label><input type="radio" name="iw-strategy" value="fast">快速 · 纯固定流程（最快，检索约 1 分钟）</label>
        <label><input type="radio" name="iw-strategy" value="seeds">种子扩张 · 以种子论文为锚的引文网络扩张（需填种子）</label>
      </div>
      <p class="interview-question">⑤ 种子论文（可选，引文网络扩张用）</p>
      <input type="text" id="iw-seeds" placeholder="arXiv ID，逗号或空格分隔，如 2402.14207, 1704.02084" style="width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:13.5px;">
      <p class="interview-question">⑥ 关注重点（可跳过）</p>
      <textarea id="iw-focus" placeholder="例如：重点关注室外场景下的效率与鲁棒性…"></textarea>
      <p class="interview-question">⑦ 执行模型</p>
      <div class="interview-options" role="radiogroup" aria-label="执行模型">
        <label><input type="radio" name="iw-model" value="glm-5.3-flash" checked>glm-5.3-flash</label>
        <label><input type="radio" name="iw-model" value="deepseek-v4-flash-vision-exp">deepseek-v4-flash-vision-exp</label>
        <label><input type="radio" name="iw-model" value="opus">opus</label>
      </div>
      <div class="interview-actions">
        <button type="button" class="interview-cancel" id="iw-cancel">返回修改主题</button>
        <button type="submit" class="chat-send" id="iw-confirm">确认，开始综述 →</button>
      </div>`;
    nodes.homeChatHero.hidden = true;
    card.hidden = false;
    card.querySelector("#iw-cancel").addEventListener("click", () => {
      card.hidden = true;
      nodes.homeChatHero.hidden = false;
      nodes.homeChatInput.focus();
    });
    card.querySelector('input[value="custom"]')?.addEventListener("change", (event) => {
      const wrap = card.querySelector("#iw-custom-range");
      wrap.hidden = !event.target.checked;
      if (event.target.checked) card.querySelector("#iw-range-input")?.focus();
    });
    card.addEventListener("submit", (event) => {
      event.preventDefault();
      confirmInterview(topic);
    }, { once: true });
    card.querySelector("#iw-confirm")?.focus();
  }

  function confirmInterview(topic) {
    const card = nodes.interviewCard;
    const mode = card.querySelector('input[name="iw-mode"]:checked')?.value || "rapid";
    let rangePreset = card.querySelector('input[name="iw-range"]:checked')?.value || "3y";
    let rangeCustom = "";
    if (rangePreset === "custom") {
      rangeCustom = card.querySelector("#iw-range-input")?.value.trim() || "";
      if (!rangeCustom) {
        showToast("请填写自定义时间范围（YYYY-MM-DD..YYYY-MM-DD）。");
        return;
      }
    }
    const params = {
      topic,
      review_mode: mode,
      time_range: rangePreset === "custom" ? { range: rangeCustom } : rangePreset,
      target_style: card.querySelector('input[name="iw-style"]:checked')?.value || "scientific-memo",
      search_strategy: card.querySelector('input[name="iw-strategy"]:checked')?.value || "smart",
      seed_arxiv_ids: card.querySelector("#iw-seeds")?.value.trim() || "",
      focus: card.querySelector("#iw-focus")?.value.trim() || "",
    };
    const model = card.querySelector('input[name="iw-model"]:checked')?.value || "glm-5.3-flash";
    if (nodes.chatModel) nodes.chatModel.value = model; // keep the panel picker in sync
    card.hidden = true;
    nodes.homeChatHero.hidden = false;
    startWorkflow(params, model);
  }

  async function startWorkflow(params, model) {
    // Enter workflow mode and kick off the first segment. The workspace id
    // arrives on the SSE response header; the timeline renders from events.
    setWorkflowSession(null);
    state.chat.stage = "init";
    state.chat.awaitingInput = false;
    state.chat.pane = "workflow";
    resetChatView();
    syncChatPane();
    renderTimeline();
    setChatTitle("综述工作流");
    setChatSession(null);
    nodes.chatInput.disabled = false;
    nodes.chatInput.placeholder = "对大纲提修改意见，或回复「继续」…";
    setChatOpen(true); // docked split-screen; user can ⤢ to fullscreen
    await streamTurn({
      endpoint: "api/workflow",
      payload: { message: params.topic, params, model: model || selectedChatModel() || undefined },
      onEvent: handleWorkflowEvent,
      history: state.chat.wsMessages,
      errorLabel: "工作流启动失败",
      onResponse: (response) => {
        const wsId = response.headers.get("X-Workflow-Id");
        if (wsId) setWorkflowSession(wsId);
      },
    });
  }

  function bindHomeHero() {
    if (!nodes.homeChatHero) return;
    nodes.homeChatForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const topic = nodes.homeChatInput.value.trim();
      if (topic.length < 2) {
        showToast("请先描述你想综述的主题（至少 2 个字符）。");
        return;
      }
      nodes.homeChatInput.value = "";
      showInterviewCard(topic);
    });
  }

  async function restoreWorkflowSession() {
    // Best-effort: if a workflow conversation is parked (checkpoint pause),
    // re-own it after a reload so the user can continue in the panel.
    if (!state.chat.workflowAvailable) return;
    let wsId = null;
    try {
      wsId = localStorage.getItem("wiki.workflow.ws");
    } catch {
      return;
    }
    if (!wsId) return;
    try {
      const response = await fetch(`api/workflow/state?ws_id=${encodeURIComponent(wsId)}`, { cache: "no-store" });
      const payload = await response.json();
      if (!response.ok || !payload.ws_id) return;
      setWorkflowSession(wsId);
      state.chat.stage = payload.stage || null;
      state.chat.awaitingInput = Boolean(payload.awaiting_input);
      state.chat.wsMessages = Array.isArray(payload.messages) ? payload.messages : [];
      state.chat.pane = "workflow";
      setChatTitle("综述工作流");
      nodes.chatInput.disabled = false;
      nodes.chatInput.placeholder = "对大纲提修改意见，或回复「继续」…";
      renderTimeline();
    } catch {
      // Server unaware of this workspace (restarted with a wiped store) —
      // drop the stale local id.
      setWorkflowSession(null);
    }
  }

  function handleChatEvent(evt, renderer) {
    if (evt.type === "session") {
      setChatSession(evt.session_id);
      return;
    }
    if (evt.type === "status") {
      if (evt.stage === "tool") {
        const detail = evt.detail ? `：${evt.detail}` : "";
        setChatStatus(`正在调用 ${evt.tool}${detail}…`);
      } else {
        setChatStatus("正在思考…");
      }
      return;
    }
    if (evt.type === "delta") {
      // Incremental markdown render (rAF-coalesced inside the renderer) so
      // line breaks, headings and lists appear while streaming.
      renderer.append(evt.text || "");
      return;
    }
    if (evt.type === "session_reset") {
      setChatSession(null);
      appendChatSystemNote("原会话已失效，已开启新对话。");
      return;
    }
    if (evt.type === "done") {
      if (evt.session_id) setChatSession(evt.session_id);
      setChatStatus(null);
      return;
    }
    if (evt.type === "error") {
      setChatStatus(null);
      appendChatError(evt.message || "对话失败。");
    }
  }

  // The user bubble shows what they typed; the wire payload may additionally
  // carry @-quote context blocks that are displayed as chips instead.
  function appendChatUserMessage(displayText, quotes) {
    const item = appendChatMessage("user", displayText);
    if (quotes?.length) {
      const strip = document.createElement("div");
      strip.className = "chat-quote-strip";
      strip.innerHTML = quotes.map((quote) => `
        <span class="chat-quote-chip" title="${escapeHtml(quote.text)}">
          <span class="chat-quote-source">${escapeHtml(quote.source)}：</span>“${escapeHtml(quote.text.slice(0, 60))}${quote.text.length > 60 ? "…" : ""}”
        </span>`).join("");
      item.prepend(strip);
    }
    return item;
  }

  // Shared streaming-turn scaffold: user bubble → assistant bubble → fetch →
  // SSE → finalize → history push → error label. Every chat pane (topic /
  // paper / workflow) calls this with its own endpoint, payload, event
  // handler, and history array; only the deltas differ per pane.
  async function streamTurn({ endpoint, payload, onEvent, history, errorLabel, onResponse }) {
    if (state.chat.streaming) return;
    const msgEl = appendChatMessage("assistant", "");
    const renderer = makeStreamingRenderer(msgEl);
    const controller = new AbortController();
    state.chat.controller = controller;
    setChatStreaming(true);
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      if (!response.ok || !response.body) {
        const errPayload = await response.json().catch(() => ({}));
        throw new Error(errPayload.error || `${errorLabel}失败（${response.status}）`);
      }
      if (onResponse) onResponse(response);
      await consumeSSE(response, (evt) => onEvent(evt, renderer));
      renderFinalAssistant(msgEl, renderer.text());
      history.push({ role: "assistant", text: renderer.text() });
    } catch (error) {
      renderFinalAssistant(msgEl, renderer.text());
      if (renderer.text()) history.push({ role: "assistant", text: renderer.text() });
      if (error.name !== "AbortError") {
        appendChatError(`${errorLabel}：${error.message}`);
      }
    } finally {
      state.chat.controller = null;
      setChatStreaming(false);
      setChatStatus(null);
    }
  }

  async function streamChat(composedMessage, displayText, quotes) {
    if (!state.topic) {
      showToast("先选择一个话题，再开始对话。");
      return;
    }
    appendChatUserMessage(displayText, quotes);
    await streamTurn({
      endpoint: "api/chat",
      payload: { topic_id: state.topic.id, message: composedMessage, model: selectedChatModel() || undefined },
      onEvent: handleChatEvent,
      history: state.chat.messages,
      errorLabel: "对话失败",
    });
  }

  function abortChat() {
    if (state.chat.controller) state.chat.controller.abort();
    const stopPath = workflowMode() ? "api/workflow/stop" : "api/chat/stop";
    fetch(stopPath, { method: "POST" }).catch(() => {});
  }

  async function resetChatSession() {
    if (workflowMode()) return resetWorkflow();
    if (paperMode()) return resetPaperChat();
    if (!state.topic) return;
    if (state.chat.messages.length && !window.confirm("开启新对话？当前话题的对话记录将被清空。")) return;
    if (state.chat.streaming) abortChat();
    try {
      await fetch("api/chat/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic_id: state.topic.id }),
      });
    } catch {
      // reset is best-effort; the view clears regardless
    }
    resetChatView();
    setChatTitle(state.topic.title);
    await loadChatState();
  }

  function submitChatMessage() {
    const value = nodes.chatInput.value.trim();
    if (!value || state.chat.streaming) return;
    nodes.chatInput.value = "";
    const quotes = consumeQuotes();
    const composed = composeMessageWithContext(value);
    if (workflowMode()) streamWorkflow(composed, value, quotes);
    else if (paperMode()) streamPaperChat(composed, value);
    else streamChat(composed, value, quotes);
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
    nodes.readerBack.addEventListener("click", closeReaderToTopic);
    nodes.readerQuickReadTab.addEventListener("click", () => {
      const paperId = parsePaperRoute();
      if (!paperId) return;
      const showQuickRead = nodes.readerQuickReadBody.hidden;
      switchReaderTab(showQuickRead);
      // Lazy: fetch the card (or placeholder) only when the tab is opened.
      if (showQuickRead) loadQuickReadState(paperId);
    });
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
    nodes.chatOpenButton.addEventListener("click", () => setChatOpen(true));
    nodes.chatShowTopic.addEventListener("click", () => switchChatPane("topic"));
    nodes.chatShowPaper.addEventListener("click", () => switchChatPane("paper"));
    nodes.chatShowWorkflow.addEventListener("click", () => switchChatPane("workflow"));
    nodes.paperIdForm.addEventListener("submit", (event) => {
      event.preventDefault();
      loadPaperById(nodes.paperIdInput.value);
    });
    nodes.chatClose.addEventListener("click", () => setChatOpen(false));
    nodes.chatExpand.addEventListener("click", toggleChatFocus);
    nodes.chatReset.addEventListener("click", resetChatSession);
    nodes.chatStop.addEventListener("click", abortChat);
    nodes.chatForm.addEventListener("submit", (event) => {
      event.preventDefault();
      submitChatMessage();
    });
    nodes.chatInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        submitChatMessage();
      }
    });
    bindChatResizer();
    bindHomeHero();
    bindSelectionQuote();
    document.addEventListener("keydown", (event) => {
      const tag = document.activeElement?.tagName;
      if (event.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") {
        event.preventDefault();
        openSearch();
      }
      if (event.key === "Escape") {
        if (state.chat.open && state.chat.focused && nodes.chatPanel.contains(document.activeElement)) {
          setChatFocused(false);
        } else if (state.chat.open && nodes.chatPanel.contains(document.activeElement)) setChatOpen(false);
        if (readerViewActive()) closeReaderToTopic();
        closeEvidence();
        closeSidebar();
      }
    });
  }

  async function init(bust = false) {
    probeChatAvailability();
    try {
      await loadManifest(bust);
      setRefreshLabel(isLocalRefreshAvailable() ? "刷新成果" : "检查更新");
      route();
    } catch (error) {
      // A missing manifest (404) is the first-run empty-KB shape, not a
      // failure: show the empty-library state with next-step guidance.
      if (error instanceof MissingSnapshotError) {
        showEmptyLibrary(error.message);
      } else {
        showError(`成果索引读取失败：${error.message}`);
      }
    }
    await restoreWorkflowSession();
  }

  syncSidebarForViewport();
  bindEvents();
  init();
})();
