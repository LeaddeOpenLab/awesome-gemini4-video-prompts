# Opus field extraction and homepage audit — 2026-09-30

The existing 32 homepage picks were reviewed against retained original posts, prompts and author supplements before applying the same field rules to the historical library. No new model call or repository reproduction was performed for this repair. Author prompts, translations, original posts and existing media-review results remain unchanged.

## Responsibility by pipeline stage

- **Input:** `src/extract/gemini-client.ts::extractSourcePrompt` and `reviewCase` serialize the complete supplied post, including `sourceMaterials`. These case paths do not invoke the generic 12,000-character length guard. The stored product, Apple, UI and Auren prompts contain their inputs/stack sections; their omissions are not explained by missing text. Collection is nevertheless bounded: `src/extract/author-materials.ts` searches one thread page (20 replies) and three links, and records limit/access errors. The old linked-text reader silently sliced at 50,000 characters; this truncation was removed, and existing supplements are now preserved on enrichment. There is no evidence that this particular limit caused the twelve reported errors. The machine-readable audit records source lengths, prompt location and collection errors for every record.
- **Model request/output:** source-index extraction previously requested only `title`, `summary`, `prompt`, `englishPrompt`, explicitly excluding broader verification. It never requested inputs, tools or purpose. The constructor then set `inputs: []`, `tools: []`, `inputsDocumented: false`, and a default task. Successful raw Gemini response envelopes were not persisted, so historical raw outputs cannot honestly be asserted to contain or omit extra fields. The retained parsed result and exact request schema establish this import defect without another paid call. New requests include structured input origins, tool statuses and task purpose; successful response envelopes and full textual input are retained locally under `.artifacts/model-evidence/` (media bytes and credentials are excluded).
- **Parsing/validation:** Zod validates the requested schema and rejects bad types rather than silently defaulting them; undeclared object keys are stripped. Thus even unsolicited tools/inputs in the old four-field response would not survive. The regular review schema retained inputs/tools but had no way to distinguish supplied assets, production materials, prohibited tools or author-confirmed use. These distinctions are additive fields in the existing arrays now.
- **Existing review extraction:** UI loop `2103273003555402193` retained the complete `<inputs>` block, but its saved review listed only fetched music and Geist, omitting 8–12 UI states and palette. Its Playwright/FFmpeg/NumPy tools were already correct. The repair retains the prompt-requested music separately from the author's later statement that the agent found audio online. Raw pre-parse output is unavailable, so this is attributed to the persisted review/extraction stage, not proved to be a model-only defect.
- **Import/cache:** `src/pipeline/source-backfill.ts` overwrote task with the discovery index category after extraction. This override was removed. `src/local-admin/integrations.ts` reused an old analysis when main text and media matched, without checking author supplements; cache comparison now includes supplements. Grounded field completion runs when reading and writing library records, including reused analyses, so existing empty imports and the correction set cannot silently reappear through the old cache path. Local canonical records and matching queue analyses are migrated; queue eligibility and media results are preserved.
- **Page generation:** `src/local-admin/curated-layout.ts::requirements` scanned prompt keywords and appended Three.js from “No Three.js/Babylon.js”. Strawberry cake's stored tools were WebGPU/WGSL already: the wrong Three.js was introduced by the homepage. `useCase` mapped “weather|seasons” to weather data visualization and product/brand words to promos, regardless of task goal. Homepage topics had a separate selection override while tool pages compared the task enum literally, leaving Manim at zero. Rendering now uses shared normalized evidence, a goal-based purpose, and one active-tool category predicate for both counts and cards. Unknown renderers stay unknown; image generation is not categorized as video rendering.

## What “Consistency check skipped” means

Source-index import does not inspect media or compare the author's video against the prompt. It sets `result.consistent=false`, `checkMethod=text`, `prompt.status=fragment`, and publishes only as a reference using the import exception in `publishableEvidence`. This is not a repository reproduction check and never proves a working reproduction. Skipping media consistency did not require skipping inputs/tools: the two operations were bundled by the old import implementation. This repair completes text metadata while preserving the skipped media check, publication tier and prompt disclosure. Author model-use statements, disclosure, media review and repository reproduction are displayed separately.

## Rules and homepage changes

`src/extract/case-fields.ts` performs conservative, idempotent completion from retained original-language quotes. `opus-field-corrections.json` holds separately attributed editorial corrections for all 32 reviewed picks; a correction applies only while its quoted prompt evidence remains present. Required, prohibited, author-confirmed and inferred tool records remain distinguishable. Only required/author-confirmed tools enter active-tool cards and categories. Input origins are user/generated/searched/downloaded/unknown. Explicit `<inputs>` sections retain their full evidence, with concise descriptions where reviewed. Non-explicit asset availability is not converted into confirmed access.

The homepage retains its existing sections and card structure. It now has **30 distinct picks**: Vincent's Cats, 15-second showreel and looping UI are the three large cards; Orbe remains a normal product-promo pick. The rain/Unity fragment stays in the full library but leaves the homepage. The duplicate showreel stays as another creator result, linked bidirectionally with the primary prompt, and no longer consumes a second featured slot. No weak cases were added to hit a quota. The latest-addition date/count is unchanged because corrections are not new records.

## Remaining evidence gaps

- No repository reproduction was performed. Existing media consistency claims are reused, not presented as new checks.
- Source-index media consistency remains unreviewed. Renderer, prior context, missing base scenes and unspecified assets remain unknown where the author does not establish them.
- Collection warnings include thread page limits, link limits and inaccessible linked documents; retaining a complete extracted prompt does not prove that every author reply was collected.
- The music-video reference short link resolves to the author's referenced GitHub source repository, and the song short link to a YouTube page. Both returned HTTP 200 on 2026-09-30. This establishes page access, not media playback, download rights or a successful reproduction.
- Police-game Unity is a PRD requirement; an actual Unity implementation is not independently verified. Spotify's renderer remains unspecified. Magnific's dependent services are prompt requirements, not tested credentials or successful generations.

## Validation

Regression tests cover negated tool lists, “no project exists” versus React use, explicit inputs, generated artwork, task goals, duplicate-result relationships, immutable prompts, and idempotence across the original 32 cases. Publication checks compare every original prompt/translation against the remote baseline, validate all internal generated links against the repository tree, assert 30 unique homepage picks and no duplicate hero placement, require the Manim case in its tool page, and reconcile category totals with the full library. Exact counts and before/after field evidence are in the adjacent JSON audit.


## Review of the original 32 homepage picks

| Case | Purpose | User inputs / production assets | Active tools |
|---|---|---|---|
| [2103802923465768972](../../prompts/2103802923465768972.md) | 3D exploration game / hidden cats | Not stated | Claude Code |
| [2103846311149936736](../../prompts/2103846311149936736.md) | Product promotional video | [user] Product URL and product details | FFmpeg, JavaScript, Playwright |
| [2103449416325890146](../../prompts/2103449416325890146.md) | 15-second motion design showreel | No supplied assets specified; agent chooses production details | Remotion |
| [2103129343253778767](../../prompts/2103129343253778767.md) | Infinite zoom collage animation | Requires external generation services | GPT 2.5, Kling 2.5, Lyria 3, Magnific MCP, Seedream 5 Pro |
| [2102554209166000267](../../prompts/2102554209166000267.md) | Product motion promotional film | Product name + one-line promise; 3–5 UI scenes; accent color; 10–20 owned vertical clips; music | FFmpeg, NumPy, Playwright |
| [2102476258948927543](../../prompts/2102476258948927543.md) | Procedural pixel-art animation | No external assets required by the prompt | Canvas 2D, Vanilla JavaScript |
| [2103801834930606193](../../prompts/2103801834930606193.md) | Music-product motion graphics | No supplied assets required; artwork generated during production | Not stated |
| [2103835273813496100](../../prompts/2103835273813496100.md) | Brand launch film | Brand name; 9–12 high-res photos; ~120 BPM music; moving plant-shadow stock video | FFmpeg, Playwright |
| [2103124033365762215](../../prompts/2103124033365762215.md) | Atmospheric animation / seasonal loop | Not stated | Not stated |
| [2103746736980378066](../../prompts/2103746736980378066.md) | Concept advertisement / Apple 1984 homage | Not stated | Not stated |
| [2103845264649761062](../../prompts/2103845264649761062.md) | Product introduction video | [user] Product URL, screenshots, logo and assets; [user] Music for beat-synchronized motion | Not stated |
| [2103128559174971663](../../prompts/2103128559174971663.md) | Derivative concept lesson | Not stated | edge-tts, Manim |
| [2103688362960019567](../../prompts/2103688362960019567.md) | Recursion explainer | Not stated | Not stated |
| [2103697580421181894](../../prompts/2103697580421181894.md) | Motion graphics / music videos | [user] Reference MV; [user] Song | Not stated |
| [2103678647777230877](../../prompts/2103678647777230877.md) | Weather data visualization / Japan summer | [searched] Online weather data and historical comparisons | JavaScript |
| [2103629247751618782](../../prompts/2103629247751618782.md) | Science explainer / photon journey | [generated] Script, characters, narration, original music and sound design | JavaScript |
| [2102853258582880547](../../prompts/2102853258582880547.md) | Cocktail recipe explainer | [user] Reference cocktail recipe illustration image attached to the prompt | JavaScript |
| [2104542961081983435](../../prompts/2104542961081983435.md) | Educational motion graphics / AI agents | [generated] Paper cutout image assets via GPT Image 2.5 on Fal AI; [searched] Recent research on self-evolving agents | GPT Image 2.5 on Fal AI |
| [2103804606794879327](../../prompts/2103804606794879327.md) | 3D multiplayer space game | Not stated | Not stated |
| [2103194052850241739](../../prompts/2103194052850241739.md) | Explorable cinematic 3D world | Not stated | Not stated |
| [2102466523164274839](../../prompts/2102466523164274839.md) | Historical 3D reconstruction | [searched] Historical maps, film, period photographs and topography; build a cited source file | Blender |
| [2103119648271290566](../../prompts/2103119648271290566.md) | Detailed character animation | Not stated | Not stated |
| [2104458970865996117](../../prompts/2104458970865996117.md) | Unity weather-effects experiment | [user] Base Unity scene with simple 3D primitives and terrain before weather effects were added. | Not stated |
| [2104541344945627171](../../prompts/2104541344945627171.md) | 15-second motion design showreel | Not stated | Not stated |
| [2104471436039803295](../../prompts/2104471436039803295.md) | 3D motion graphics / website hero | Not stated | Three.js |
| [2103273003555402193](../../prompts/2103273003555402193.md) | UI motion / interaction demonstration | 8–12 UI states; palette; ~120 BPM music | FFmpeg, NumPy, Playwright |
| [2103820321673675031](../../prompts/2103820321673675031.md) | Scroll-driven website hero | [user] Background video; [user] Two feature-card images | Framer Motion, GSAP ScrollTrigger, React |
| [2103789415323562325](../../prompts/2103789415323562325.md) | Mobile arcade game prototype | [user] Existing Unity CLI project | Unity |
| [2103763192971461057](../../prompts/2103763192971461057.md) | Pixel-art card game prototype | Not stated | Not stated |
| [2104520072014508316](../../prompts/2104520072014508316.md) | Interactive floor-plan design tool | [user] Floor plan image with millimeter dimension annotations | Three.js |
| [2104514806443303238](../../prompts/2104514806443303238.md) | Interactive soft-body physics demo | No external assets required by the prompt | WebGPU, WGSL |
| [2104189915693269112](../../prompts/2104189915693269112.md) | Calming rain interaction | Not stated | Not stated |

Counts: `{"total":360,"homepageAudited":32,"homepageAfter":30,"imported":244,"changed":254,"historyChanged":222,"categories":{"motion-graphics":244,"explainers":46,"3d-scenes":24,"games-interactive":46}}`
