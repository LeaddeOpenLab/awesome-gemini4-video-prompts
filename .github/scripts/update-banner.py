"""Refresh the README banner after new content is published."""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[2]
update_file = root / 'data/latest-update.json'
update = json.loads(update_file.read_text()) if update_file.exists() else {}
def update_date(value):
    if not value:
        return 'DATE PENDING'
    then = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if then.tzinfo is None:
        then = then.replace(tzinfo=timezone.utc)
    return then.astimezone(timezone.utc).strftime('%d %b %Y · %H:%M UTC').upper()

added = int(update.get('added', 0))
addition_date = str(update.get('date', ''))
# Published batch metadata is authoritative, including editorial withdrawals.
history = [{'date': item['date'], 'added': item['published']}
           for item in update.get('history', [])]
if not history:
    history = json.loads(os.environ.get('BANNER_UPDATES', '[]'))
if not history and os.environ.get('GITHUB_TOKEN'):
    repo = os.environ['GITHUB_REPOSITORY']
    req = urllib.request.Request(
        f'https://api.github.com/repos/{repo}/commits?path=data%2Flibrary&per_page=30',
        headers={'Authorization': 'Bearer ' + os.environ['GITHUB_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'User-Agent': 'readme-banner'})
    with urllib.request.urlopen(req) as response:
        commits = json.load(response)
    history = []
    for commit in commits:
        match = re.match(r'^Add ([1-9]\d*) prompts?(?: ·|$)', commit['commit']['message'].splitlines()[0])
        if match:
            batch_count = 0
            page = 1
            while True:
                detail_req = urllib.request.Request(
                    f'https://api.github.com/repos/{repo}/commits/{commit["sha"]}?per_page=100&page={page}',
                    headers=req.headers)
                with urllib.request.urlopen(detail_req) as response:
                    files = json.load(response).get('files', [])
                batch_count += sum(1 for file in files
                    if re.fullmatch(r'data/library/[^/]+\.json', file['filename'])
                    and file['status'] in ('added', 'modified'))
                if len(files) < 100:
                    break
                page += 1
            history.append({'date': commit['commit']['committer']['date'], 'added': batch_count})
        if len(history) == 3:
            break
if history:
    added, addition_date = history[0]['added'], history[0]['date']
else:
    history = [{'date': addition_date, 'added': added}]
timeline = ''
for i, item in enumerate(reversed(history[:3])):
    x = 66 + i * 448
    timeline += f'<circle cx="{x}" cy="439" r="5" fill="#6E4DFC"/><text x="{x}" y="477" fill="#655D72" font-size="17">{escape(update_date(item["date"]))}</text><text x="{x}" y="516" fill="#241C35" font-size="28" font-weight="700">+{int(item["added"])} prompts updated</text>'
# Maintainer-provided collection headline; separate from public inventory metadata.
headline = '2000+'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="650" viewBox="0 0 1440 650" role="img" aria-labelledby="title desc">
<title id="title">{headline} prompts · Actively updated · Leadde Open Lab</title>
<desc id="desc">2000+ prompts for video, animation, 3D and interactive work. Latest batch: {added} prompts updated on {escape(update_date(addition_date))}. Open the web collection for previews, prompts and setup notes.</desc>
<rect x="1" y="1" width="1438" height="648" rx="24" fill="#FAF9FF" stroke="#E6E1F3"/>
<g font-family="Arial, Helvetica, sans-serif">
<text x="64" y="65" fill="#241C35" font-size="25" font-weight="700">Leadde <tspan font-weight="400" fill="#756C84">/ Open Lab</tspan></text>
<rect x="1132" y="33" width="244" height="45" rx="22" fill="#EEE8FF"/>
<circle cx="1157" cy="55" r="5" fill="#6E4DFC"/>
<text x="1175" y="62" fill="#6E4DFC" font-size="17" font-weight="700">ACTIVELY UPDATED</text>
<text x="64" y="120" fill="#655D72" font-size="19" letter-spacing="1">THE GEMINI 4 VIDEO PROMPT COLLECTION · CURATED BY LEADDE</text>
<text x="54" y="301" fill="#6E4DFC" font-size="190" font-weight="800" letter-spacing="-10">{headline}</text>
<text x="66" y="352" fill="#241C35" font-size="31" font-weight="700" letter-spacing="7">PROMPTS TO EXPLORE</text>
<path d="M836 160V358" stroke="#E0D8EF"/>
<text x="900" y="192" fill="#655D72" font-size="18" font-weight="700" letter-spacing="2">LATEST CONTENT DROP</text>
<text x="894" y="291" fill="#241C35" font-size="98" font-weight="800">+{added}</text>
<text x="900" y="329" fill="#241C35" font-size="24">prompts updated</text>
<text x="900" y="365" fill="#655D72" font-size="18">{escape(update_date(addition_date))}</text>
<text x="66" y="399" fill="#655D72" font-size="19">VIDEO · MOTION GRAPHICS · EXPLAINERS · 3D · INTERACTIVE</text>
<path d="M66 439H1335" stroke="#DAD1ED" stroke-width="2"/>
{timeline}
<path d="M64 548H1376" stroke="#E6E1F3"/>
<text x="66" y="597" fill="#241C35" font-size="23" font-weight="700">See the result. Start with the prompt.</text>
<text x="66" y="626" fill="#655D72" font-size="17">Video previews · Copyable prompts · Setup notes · English / 简体中文</text>
<rect x="1006" y="569" width="370" height="61" rx="10" fill="#6E4DFC"/>
<text x="1031" y="608" fill="white" font-size="23" font-weight="700">Explore the web collection</text>
<path d="M1340 590l9 9-9 9m-13-9h22" stroke="white" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</svg>
'''
target = root / 'data/banner.svg'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(svg)
print(f'Updated {target.relative_to(root)}')

# Each content batch gets a new image URL, avoiding stale raw-image caches.
stamp = datetime.fromisoformat(addition_date.replace('Z', '+00:00')).strftime('%Y%m%d-%H%M%S') if addition_date else 'pending'
versioned = root / f'data/banner-{stamp}-collection.svg'
versioned.write_text(svg)
readme = root / 'README.md'
readme.write_text(re.sub(r'\]\(data/banner[^)]*\)', f']({versioned.relative_to(root)})', readme.read_text()))
