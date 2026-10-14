(() => {
  const translations = window.siteTranslations || {};
  const select = document.querySelector("[data-language]");
  let language = "en";
  const originalTitle = document.title;
  const nodes = [];
  const attributes = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (
      node.textContent.trim() &&
      !node.parentElement.closest("script, style, pre, code, select")
    ) {
      nodes.push({ node, original: node.textContent });
    }
  }
  document
    .querySelectorAll("[placeholder], [aria-label], img[alt]")
    .forEach((element) => {
      for (const name of ["placeholder", "aria-label", "alt"]) {
        if (element.hasAttribute(name))
          attributes.push({
            element,
            name,
            original: element.getAttribute(name),
          });
      }
    });
  function translate(text) {
    if (language === "en") return text;
    const key = text.trim();
    let value = translations[key];
    if (!value && key.startsWith("Preview "))
      value = "预览：" + (translations[key.slice(8)] || key.slice(8));
    if (!value && key.startsWith("Short creator preview of "))
      value =
        "原作者短预览：" +
        (translations[key.slice("Short creator preview of ".length)] ||
          key.slice("Short creator preview of ".length));
    if (!value && key.startsWith("Original post by @"))
      value = key.replace("Original post by @", "原帖作者 @");
    if (!value) return text;
    return (
      text.slice(0, text.indexOf(key)) +
      value +
      text.slice(text.indexOf(key) + key.length)
    );
  }
  window.siteI18n = { t: translate };
  function apply(value) {
    language = value === "zh-CN" ? "zh-CN" : "en";
    document.documentElement.lang = language;
    select.value = language;
    nodes.forEach(({ node, original }) => {
      node.textContent = translate(original);
    });
    attributes.forEach(({ element, name, original }) => {
      element.setAttribute(name, translate(original));
    });
    const pageTitle = originalTitle.replace(" | Leadde Open Lab", "");
    const caseTitle = pageTitle.replace(" — Gemini 4 prompt", "");
    document.title =
      language === "en"
        ? originalTitle
        : (translations[caseTitle] ||
            translations[pageTitle] ||
            "Gemini 4 视频与动画提示词") +
          (pageTitle.endsWith(" — Gemini 4 prompt") ? " — Gemini 4 提示词" : "") +
          " | Leadde Open Lab";
    document.dispatchEvent(new Event("languagechange"));
  }
  let saved = "en";
  try {
    saved = localStorage.getItem("leadde-language") || "en";
  } catch {}
  apply(saved);
  select.addEventListener("change", () => {
    apply(select.value);
    try {
      localStorage.setItem("leadde-language", language);
    } catch {}
  });
})();
