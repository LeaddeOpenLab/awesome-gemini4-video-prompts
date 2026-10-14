const t = (text) => window.siteI18n?.t(text) || text;
// Queue events even before a configured analytics provider has loaded.
window.dataLayer = window.dataLayer || [];
window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
const analyticsId = document.querySelector('meta[name="ga-measurement-id"]')?.content;
if (analyticsId) {
  window.gtag("js", new Date());
  window.gtag("config", analyticsId);
  const script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(analyticsId);
  document.head.append(script);
}
function track(name, params = {}) {
  window.gtag("event", name, { page_path: location.pathname, ...params });
}
document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href]");
  if (!link) return;
  const url = new URL(link.href);
  if (url.hostname === "github.com" || url.hostname === "leadde.ai") {
    track(url.hostname === "github.com" ? "github_click" : "leadde_click", {
      link_url: url.href,
      placement: link.dataset.placement || (link.closest("header") ? "header" : link.closest("footer") ? "footer" : "content"),
    });
  }
});
const search = document.querySelector("input[data-search]");
const cards = [...document.querySelectorAll("[data-card]")];
const filters = [...document.querySelectorAll("[data-filter]")];
let category = "all";
function filterCards() {
  const query = search?.value.trim().toLowerCase() || "";
  let visible = 0;
  for (const card of cards) {
    const show =
      (category === "all" || card.dataset.category === category) &&
      (card.dataset.search + " " + card.textContent.toLowerCase()).includes(
        query,
      );
    card.hidden = !show;
    if (show) visible++;
  }
  const count = document.querySelector("[data-count]");
  if (count)
    count.textContent = t(
      `${visible} ${visible === 1 ? "example" : "examples"}`,
    );
  const empty = document.querySelector("[data-empty]");
  if (empty) empty.hidden = visible !== 0;
  document.dispatchEvent(new Event("collectionfiltered"));
}
search?.addEventListener("input", filterCards);
document.addEventListener("languagechange", filterCards);
filters.forEach((button) =>
  button.addEventListener("click", () => {
    category = button.dataset.filter;
    filters.forEach((item) =>
      item.setAttribute("aria-pressed", String(item === button)),
    );
    filterCards();
  }),
);
document.querySelectorAll("[data-copy]").forEach((button) =>
  button.addEventListener("click", async () => {
    const code = document.getElementById(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(code.textContent);
      track("prompt_copy", { prompt_id: button.dataset.promptId, placement: button.closest("dialog") ? "preview" : "detail" });
      button.textContent = t("Copied ✓");
      const hint = document.querySelector(`[data-star-hint="${button.dataset.copy}"]`);
      if (hint) hint.hidden = false;
      setTimeout(() => {
        button.textContent = t("Copy prompt");
      }, 2000);
    } catch {
      code.hidden = false;
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = t("Text selected — copy manually");
    }
  }),
);
const dialog = document.querySelector("[data-preview-dialog]");
if (dialog) {
  const video = dialog.querySelector("video");
  document.querySelectorAll("[data-preview]").forEach((button) =>
    button.addEventListener("click", () => {
      dialog.dataset.title = button.dataset.title;
      dialog.querySelector("h2").textContent = t(button.dataset.title);
      const prompt = dialog.querySelector("#preview-prompt");
      prompt.textContent = window.sitePrompts[button.dataset.promptId];
      prompt.hidden = true;
      dialog.querySelector("[data-star-hint]").hidden = true;
      const copy = dialog.querySelector("[data-copy]");
      copy.dataset.promptId = button.dataset.promptId;
      copy.textContent = t("Copy prompt");
      video.dataset.promptId = button.dataset.promptId;
      dialog.querySelector("[data-preview-link]").href = button.dataset.link;
      video.poster = button.dataset.poster;
      video.src = button.dataset.preview;
      dialog.showModal();
      document.querySelectorAll("[data-hero-video], [data-card-video]").forEach((preview) => preview.pause());
      video.play().catch(() => {});
    }),
  );
  dialog
    .querySelector("[data-close]")
    .addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (
        event.clientX < r.left ||
        event.clientX > r.right ||
        event.clientY < r.top ||
        event.clientY > r.bottom
      )
        dialog.close();
    }
  });
  dialog.addEventListener("close", () => {
    video.pause();
    video.removeAttribute("src");
    video.load();
    document.dispatchEvent(new Event("previewclosed"));
  });
}

// Count one actual playback per video source and page view, not every loop.
const played = new Set();
document.querySelectorAll("video").forEach((video) => {
  video.addEventListener("playing", () => {
    const placement = video.matches("[data-hero-video]") ? "hero" : video.dataset.cardVideo || (video.closest("dialog") ? "preview" : "detail");
    const key = placement + video.dataset.promptId;
    if (played.has(key)) return;
    played.add(key);
    track("preview_play", { prompt_id: video.dataset.promptId, placement, autoplay: placement === "hero" || placement === "spotlight" });
  });
});
const heroVideo = document.querySelector("[data-hero-video]");
if (heroVideo) {
  const toggle = document.querySelector("[data-hero-toggle]");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let visible = false;
  let paused = reduced.matches;
  function updateLabel() {
    toggle.textContent = t(heroVideo.paused ? "Resume preview" : "Pause preview");
  }
  function syncHero() {
    if (visible && !paused && !document.hidden && !dialog?.open) {
      if (!heroVideo.getAttribute("src")) heroVideo.src = heroVideo.dataset.src;
      heroVideo.play().catch(() => { toggle.hidden = false; updateLabel(); });
    } else heroVideo.pause();
  }
  new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; syncHero(); }, { threshold: 0.15 }).observe(heroVideo);
  heroVideo.addEventListener("playing", () => { heroVideo.classList.add("is-playing"); toggle.hidden = false; updateLabel(); });
  heroVideo.addEventListener("pause", updateLabel);
  toggle.hidden = false;
  updateLabel();
  toggle.addEventListener("click", () => { paused = !heroVideo.paused; syncHero(); updateLabel(); });
  reduced.addEventListener("change", () => { paused = reduced.matches; syncHero(); });
  document.addEventListener("visibilitychange", syncHero);
  document.addEventListener("previewclosed", syncHero);
  document.addEventListener("languagechange", updateLabel);
}
document.addEventListener("languagechange", () => {
  if (dialog?.open) dialog.querySelector("h2").textContent = t(dialog.dataset.title);
});

// Load card previews only when they are about to play.
const hoverPointer = matchMedia("(hover: hover) and (pointer: fine)");
const reducedCards = matchMedia("(prefers-reduced-motion: reduce)");
document.querySelectorAll("[data-card-video]").forEach((video) => {
  const card = video.closest(".card");
  const media = video.closest(".card-media");
  const spotlight = video.dataset.cardVideo === "spotlight";
  const toggle = media.querySelector("[data-card-toggle]");
  let visible = false;
  let hovering = false;
  let paused = reducedCards.matches;
  function label() {
    if (toggle) toggle.textContent = t(video.paused ? "Resume preview" : "Pause preview");
  }
  function sync() {
    const active = spotlight ? !paused : hovering && hoverPointer.matches && !reducedCards.matches;
    if (visible && active && !card.hidden && !document.hidden && !dialog?.open) {
      if (!video.getAttribute("src")) video.src = video.dataset.src;
      video.play().catch(() => {});
    } else {
      video.pause();
      if (!spotlight) video.classList.remove("is-playing");
    }
  }
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    sync();
  }, { threshold: 0.15 }).observe(media);
  card.addEventListener("pointerenter", (event) => {
    if (event.pointerType === "touch") return;
    hovering = true;
    sync();
  });
  card.addEventListener("pointerleave", () => { hovering = false; sync(); });
  video.addEventListener("playing", () => {
    video.classList.add("is-playing");
    label();
  });
  video.addEventListener("pause", label);
  if (toggle) {
    toggle.hidden = false;
    label();
    toggle.addEventListener("click", () => { paused = !video.paused; sync(); label(); });
  }
  reducedCards.addEventListener("change", () => { paused = reducedCards.matches; sync(); });
  hoverPointer.addEventListener("change", sync);
  document.addEventListener("visibilitychange", sync);
  document.addEventListener("previewclosed", sync);
  document.addEventListener("collectionfiltered", sync);
  document.addEventListener("languagechange", label);
});
