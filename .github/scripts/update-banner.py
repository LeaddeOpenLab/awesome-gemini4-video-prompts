"""Render the Gemini 4 collection banner using the current catalog."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[2] / "collection"
videos = json.loads((root / 'data/videos.json').read_text())
shared = sum(bool(v['prompt']) for v in videos)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="560" viewBox="0 0 1440 560" role="img" aria-labelledby="title desc">
<title id="title">1000 prompts · Awesome Gemini 4 Video Prompts</title>
<desc id="desc">Leadde Open Lab. Explore Gemini 4 Argon videos, motion graphics, 3D worlds and interactive experiences. Current catalog: {len(videos)} creations, {shared} public prompts and templates, 5 collections.</desc>
<defs><linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#EDE5FF"/><stop offset="1" stop-color="#E4F4F0"/></linearGradient><linearGradient id="violet"><stop stop-color="#6E4DFC"/><stop offset="1" stop-color="#A27BFF"/></linearGradient></defs>
<rect x="1" y="1" width="1438" height="558" rx="26" fill="#FAF9FF" stroke="#E6E1F3"/>
<g font-family="Arial, Helvetica, sans-serif">
<text x="58" y="65" fill="#241C35" font-size="25" font-weight="700">Leadde <tspan font-weight="400" fill="#756C84">/ Open Lab</tspan></text>
<rect x="1154" y="32" width="228" height="44" rx="22" fill="#EEE8FF"/><circle cx="1178" cy="54" r="5" fill="#6E4DFC"/><text x="1195" y="61" fill="#6E4DFC" font-size="16" font-weight="700">GEMINI 4 · ARGON</text>
<text x="58" y="121" fill="#655D72" font-size="17" letter-spacing="2">THE GEMINI 4 VIDEO PROMPT COLLECTION</text>
<text x="45" y="307" fill="#6E4DFC" font-size="198" font-weight="800" letter-spacing="-10">1000</text>
<text x="60" y="352" fill="#241C35" font-size="28" font-weight="700" letter-spacing="7">PROMPTS TO EXPLORE</text>
<text x="60" y="399" fill="#655D72" font-size="21">See the result. Start with the prompt.</text>
<rect x="750" y="112" width="632" height="295" rx="20" fill="url(#panel)"/>
<g transform="translate(788 142)"><rect width="208" height="232" rx="14" fill="#FFF" stroke="#DDD5ED"/><circle cx="22" cy="23" r="4" fill="#A78BFA"/><circle cx="37" cy="23" r="4" fill="#D8CDF4"/><circle cx="52" cy="23" r="4" fill="#D8CDF4"/><path d="M24 135C45 135 46 80 65 80S88 166 108 166S130 72 148 72S169 125 184 125" fill="none" stroke="url(#violet)" stroke-width="7" stroke-linecap="round"/><text x="22" y="208" font-size="15" fill="#4E4265" font-weight="700">MOTION / EXPLAINERS</text></g>
<g transform="translate(1016 142)"><rect width="328" height="108" rx="14" fill="#FFF" stroke="#DDD5ED"/><path d="m28 41 26-15 26 15v30L54 86 28 71z M28 41l26 15 26-15M54 56v30" fill="#EEE8FF" stroke="#7B59D8" stroke-width="2"/><text x="104" y="53" font-size="19" fill="#241C35" font-weight="700">WORLDS IN CODE</text><text x="104" y="78" font-size="15" fill="#756C84">3D scenes · Physics</text></g>
<g transform="translate(1016 266)"><rect width="328" height="108" rx="14" fill="#241C35"/><path d="M48 34v40M28 54h40" stroke="#C9B7FF" stroke-width="8" stroke-linecap="round"/><circle cx="86" cy="46" r="5" fill="#A5E5CA"/><circle cx="100" cy="63" r="5" fill="#A5E5CA"/><text x="125" y="52" font-size="17" fill="#FFF" font-weight="700">PLAY / INTERACT</text><text x="125" y="77" font-size="14" fill="#C6BCD6">Games · Workflows</text></g>
<path d="M58 441H1382" stroke="#E6E1F3"/>
<text x="60" y="484" fill="#241C35" font-size="23" font-weight="700">{len(videos)} creations <tspan fill="#BBB0CB"> / </tspan> {shared} shared prompts <tspan fill="#BBB0CB"> / </tspan> 5 collections</text>
<text x="60" y="521" fill="#756C84" font-size="17">Creator videos · Original posts · Public prompts &amp; templates</text>
<rect x="1044" y="466" width="338" height="62" rx="12" fill="#6E4DFC"/><text x="1074" y="505" fill="#FFF" font-size="21" font-weight="700">Explore the collection</text><path d="m1331 484 10 10-10 10m-15-10h25" fill="none" stroke="#FFF" stroke-width="2" stroke-linecap="round"/>
</g></svg>'''
(root / 'data/banner.svg').write_text(svg+'\n')
print(f'Banner: 1000 headline / {len(videos)} creations / {shared} public prompts')
