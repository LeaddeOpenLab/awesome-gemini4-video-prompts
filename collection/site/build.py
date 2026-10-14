#!/usr/bin/env python3
"""Build the curated public site from repository records. Python standard library only."""
import html
import json
import os
from pathlib import Path
import shutil
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
OUT = ROOT / '_site'
CONFIG = json.loads((SITE / 'site.json').read_text())
BASE = os.environ.get('SITE_URL', CONFIG['url']).rstrip('/') + '/'
REPO = CONFIG['repository']
GA_ID = os.environ.get('GA_MEASUREMENT_ID') or CONFIG.get('ga_measurement_id', '')
VERIFY = os.environ.get('GOOGLE_SITE_VERIFICATION') or CONFIG['google_site_verification']
from catalog import SELECTION, CATEGORIES, FEATURED, TIPS, REPOSITORY
E = lambda value: html.escape(str(value), quote=True)
BY_ID = {item['id']: item for item in SELECTION}
PLAY = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3l12 7-12 7z" fill="currentColor"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>'

def case_url(item):
    return 'prompts/' + item['slug'] + '/'

def link(prefix, path=''):
    return prefix + path or './'

def preview(item, prefix):
    return f'<button class="play" data-prompt-id="{item["id"]}" aria-label="Preview {E(item["title"])}" data-preview="{E(item["videoUrl"])}" data-poster="{E(item["posterUrl"])}" data-title="{E(item["title"])}" data-link="{prefix}{case_url(item)}">{PLAY}<span>Play preview</span></button>'

def pro_tip(item):
    tip = TIPS[item['id']]
    label = 'Prompt technique' if tip['basis'] == 'public_prompt' else 'Suggested approach · prompt not public'
    return '<aside class="pro-tip" lang="en" translate="no"><strong>💡 Pro Tip</strong><span class="pro-tip-label">'+E(label)+'</span><p>'+E(tip['en'])+'</p></aside>'

def card(item, prefix, filterable=False):
    cat = CATEGORIES[item['category']]['name']
    search = ' '.join([item['title'], item['description'], item['tool'], cat, item['author']]).lower()
    data = f' data-card data-category="{item["category"]}" data-search="{E(search)}"' if filterable else ''
    feature = item.get('showcase', '') if filterable else ''
    style = ' card-' + feature if feature else ''
    motion = 'spotlight' if feature == 'spotlight' else 'hover'
    pause = '<button class="hero-pause" data-card-toggle hidden>Pause preview</button>' if feature == 'spotlight' else ''
    badge = '<div class="editor-pick">Editor’s pick</div>' if feature else ''
    return f'''<article class="card{style}"{data}>
<div class="card-media"><a href="{prefix}{case_url(item)}" tabindex="-1" aria-hidden="true"><img src="{E(item['posterUrl'])}" alt="" width="800" height="500" loading="lazy"></a><video class="card-video" data-card-video="{motion}" data-prompt-id="{item['id']}" data-src="{E(item['videoUrl'])}" muted playsinline loop preload="none" aria-hidden="true"></video>{pause}{preview(item,prefix)}</div>
<div class="card-info">{badge}<div class="card-top"><span>{E(cat)}</span><span class="tool">{E(item['tool'])}</span></div>
<h3><a href="{prefix}{case_url(item)}">{E(item['title'])}</a></h3><p>{E(item['description'])}</p>{pro_tip(item)}
<div class="card-bottom"><a href="{E(item['source'])}">@{E(item['author'])} ↗</a><a href="{prefix}{case_url(item)}">View creation →</a></div></div></article>'''

def star_hint(target):
    return f'<div class="star-hint" data-star-hint="{target}" role="status" hidden><span>Found this useful?</span> <a href="{REPO}" data-placement="copy-success">☆ Star this repo for your next project ↗</a></div>'

def document(title, description, body, path='', image_id=None, noindex=False):
    prefix = '../' * len([p for p in path.split('/') if p])
    prefix = prefix or './'
    canonical = BASE + path
    image_url = BY_ID[image_id]['posterUrl'] if image_id else BY_ID[FEATURED[0]['id']]['posterUrl']
    schema = {'@context':'https://schema.org','@type':'WebPage' if path.startswith('prompts/') else 'CollectionPage','name':title,'description':description,'url':canonical,'publisher':{'@type':'Organization','name':'Leadde Open Lab','url':'https://github.com/LeaddeOpenLab'}}
    verification = f'<meta name="google-site-verification" content="{E(VERIFY)}">' if VERIFY else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="ga-measurement-id" content="{E(GA_ID)}">
<title>{E(title)} | Leadde Open Lab</title><meta name="description" content="{E(description)}">
<link rel="canonical" href="{E(canonical)}">{verification}{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:type" content="website"><meta property="og:site_name" content="Leadde Open Lab"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{E(canonical)}"><meta property="og:image" content="{E(image_url)}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/translations.js" defer></script><script src="{prefix}assets/i18n.js" defer></script><script src="{prefix}assets/prompts.js" defer></script><script src="{prefix}assets/site.js" defer></script>
<script type="application/ld+json">{json.dumps(schema).replace('<', chr(92)+'u003c')}</script></head><body>
<a class="skip" href="#main">Skip to content</a><header class="header"><div class="wrap"><a class="brand" href="{prefix}" aria-label="Leadde Open Lab home"><img src="{prefix}assets/leadde-logo.png" width="106" height="27" alt="Leadde"><span>Open Lab</span></a><nav class="nav" aria-label="Main navigation"><a class="nav-secondary" href="{prefix}#collection">Collection</a><a class="nav-secondary" href="{prefix}#how-to-use">How to use</a><a class="github" href="{REPO}">GitHub ↗</a><select class="language-select" data-language aria-label="Language"><option value="en">English</option><option value="zh-CN">简中</option></select></nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="footer-top"><span>An open collection by <a href="https://leadde.ai">Leadde</a>.</span><div class="footer-links"><a href="{REPO}">GitHub ↗</a><a href="{REPO}/issues/new">Suggest a correction</a><a href="https://leadde.ai">Leadde.ai ↗</a></div></div><p class="footer-note">Prompts and previews are credited to their original creators. These examples have not been independently reproduced by this collection. Third-party materials remain their creators’ property. <a href="{REPO}/blob/main/collection/data/docs/RIGHTS.md">Attribution &amp; use →</a></p></div></footer>
<dialog class="dialog" data-preview-dialog aria-labelledby="preview-title"><div class="dialog-bar"><h2 id="preview-title">Creator preview</h2><button class="dialog-close" data-close aria-label="Close preview">×</button></div><video controls muted playsinline loop preload="none" aria-label="Short visual preview of the creator’s work"></video><div class="dialog-foot"><span>Creator video · audio available</span><div class="dialog-actions"><button class="copy" data-copy="preview-prompt" aria-live="polite">Copy prompt</button><a class="text-link" data-preview-link href="{prefix}">Post &amp; details →</a></div></div>{star_hint('preview-prompt')}<pre id="preview-prompt" class="preview-prompt" hidden></pre></dialog>
</body></html>'''

def prompt_section(item):
    if item['prompt']:
        content = f'<button class="copy" data-copy="prompt-text" data-prompt-id="{item["id"]}" aria-live="polite">Copy prompt</button></div>{star_hint("prompt-text")}<pre id="prompt-text">{E(item["prompt"])}</pre><p><a href="{E(item["promptSourceUrl"])}">Prompt source ↗</a></p>'
        if item.get('promptAuthor'): content += '<p>Prompt author: '+E(item['promptAuthor'])+'</p>'
    else:
        content = '</div><p>The creator did not publish an exact prompt in the reviewed sources. The original post is a description, not a reconstructed prompt.</p>'
    content = '<section class="prompt-block" id="prompt"><div class="prompt-header"><h2>'+E(item['status'])+'</h2>'+content+f'<div class="prompt-foot"><a href="{REPO}/blob/main/collection/prompts/{item["id"]}.md">View source record ↗</a></div></section>'
    content += pro_tip(item)
    content += '<section class="customize"><h2>Original post</h2><p style="white-space:pre-wrap">'+E(item['originalPost'])+'</p>'
    for post in item.get('additionalPosts', []):
        content += '<h3><a href="'+E(post['url'])+'">Additional creator post ↗</a></h3><p style="white-space:pre-wrap">'+E(post['text'])+'</p>'
    links = list(item.get('relatedSources', []))
    if item.get('modelEvidenceUrl'): links.append(dict(label='Model attribution context',url=item['modelEvidenceUrl']))
    for source in links: content += '<p><a href="'+E(source['url'])+'">'+E(source['label'])+' ↗</a></p>'
    return content+'</section>'

def write(path, content):
    dest = OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)

OUT.mkdir(exist_ok=True)
# Only replace build-owned directories; source records are never modified.
for folder in ['assets', 'prompts', 'collections']:
    if (OUT / folder).exists(): shutil.rmtree(OUT / folder)
shutil.copytree(SITE / 'assets', OUT / 'assets')
if (SITE / 'public').is_dir():
    shutil.copytree(SITE / 'public', OUT, dirs_exist_ok=True)

locale = json.loads((SITE / 'zh-CN.json').read_text())
translations = dict(locale['ui'])
translations.update({tip['en']: tip['zh'] for tip in TIPS.values()})
translations.update({'Prompt technique': '提示词解析', 'Suggested approach · prompt not public': '复用建议 · 未公开 Prompt'})
for key, translated in locale['categories'].items():
    for field, value in translated.items():
        translations[CATEGORIES[key][field]] = value
for item in SELECTION:
    translated = locale.get('cases', {}).get(item['id'])
    if not translated: continue
    for field in ['title', 'description', 'inputs', 'note']:
        translations[item[field]] = translated[field]
    for original, value in zip(item['steps'], translated['steps']):
        translations[original] = value
for count in range(len(SELECTION) + 1):
    translations[f'{count} {"example" if count == 1 else "examples"}'] = f'{count} 个案例'
write('assets/translations.js', 'window.siteTranslations = ' + json.dumps(translations, ensure_ascii=False).replace('<', '\\u003c') + ';\n')

write('assets/prompts.js', 'window.sitePrompts = ' + json.dumps({x['id']: x['prompt'] for x in SELECTION}, ensure_ascii=False).replace('<', chr(92)+'u003c') + ';\n')

featured = [BY_ID[x['id']] for x in FEATURED]
hero = featured[0]
ordered = featured + [x for x in SELECTION if x not in featured]
ordered[0]['showcase'] = 'spotlight'
for item in ordered[1:3]: item['showcase'] = 'featured'
for item in featured[3:]: item['showcase'] = 'pick'
filters = '<button class="filter" data-filter="all" aria-pressed="true">All work</button>' + ''.join(f'<button class="filter" data-filter="{key}" aria-pressed="false">{value["name"]}</button>' for key,value in CATEGORIES.items())
topics = ''.join(f'<article class="topic"><div class="topic-number">0{i+1} / COLLECTION</div><h3>{v["name"]}</h3><p>{v["short"]}</p><a class="text-link" href="./collections/{key}/">Explore collection <span>↗</span></a></article>' for i,(key,v) in enumerate(CATEGORIES.items()))
body = f'''<div class="wrap"><section class="hero"><div class="hero-copy"><div class="eyebrow">Gemini 4, in motion</div><h1>Explore Gemini 4<br><span>video prompts.</span></h1><p>Watch the work. Take the prompt. Make it yours.</p><div class="actions"><a class="button" href="#collection">Explore the collection <span>↗</span></a><a class="text-link" href="{REPO}">☆ Star on GitHub <span>↗</span></a></div><p class="hero-note">Motion graphics, explainers &amp; 3D worlds.<br>Selected by Leadde Open Lab.</p></div><div class="hero-art"><div class="hero-picture"><a href="./{case_url(hero)}"><img src="{E(hero['posterUrl'])}" alt="{E(hero['title'])}" width="800" height="500" fetchpriority="high"></a><video class="hero-video" data-hero-video data-prompt-id="{hero['id']}" data-src="{E(hero['videoUrl'])}" muted playsinline loop preload="none" aria-hidden="true"></video><button class="hero-pause" data-hero-toggle hidden>Pause preview</button><span class="corner-label">FEATURED CREATION</span>{preview(hero,'./')}</div><div class="hero-caption"><div><strong>{E(hero['title'])}</strong><p>By @{hero['author']} · {E(hero['tool'])}</p></div><a href="./{case_url(hero)}" class="text-link" aria-label="View featured creation">View creation →</a></div></div></section>
<div class="index-strip"><span>Gemini 4 video &amp; animation prompts</span><span>{len(SELECTION)} creations · {len(CATEGORIES)} collections</span><span>Original creators, always credited</span></div>
<section class="collection" id="collection"><nav class="collection-nav" aria-label="Browse prompts"><a href="#collection" aria-current="page">Selected examples</a><a href="{REPO}#browse-the-full-library">Full prompt library ↗</a></nav><div class="section-heading"><div><div class="kicker">Selected work</div><h2>Standout work. Ideas worth exploring.</h2><p>Start with our editor’s picks, then explore more creative directions.</p></div><label class="search">{SEARCH}<span class="sr-only">Search selected examples</span><input data-search type="search" placeholder="Search prompts, tools, creators…"></label></div><div class="filters"><div class="filter-options" role="group" aria-label="Filter by collection">{filters}</div><span class="result-count" data-count aria-live="polite">{len(SELECTION)} examples</span></div><div class="grid showcase-grid">{''.join(card(x,'./',True) for x in ordered)}</div><p class="no-results" data-empty hidden>No matching examples. Try a different search or choose All work.</p><div class="collection-bottom"><p>Explore every creation in our open collection.</p><a class="text-link" href="{REPO}#browse-the-full-library">Browse the full library on GitHub ↗</a></div></section></div>
<section class="topics"><div class="wrap"><div class="kicker">A closer look</div><h2>Find your next creative direction.</h2><div class="topic-grid">{topics}</div></div></section>
<div class="wrap"><section class="how" id="how-to-use"><div class="how-intro"><div class="kicker">From prompt to project</div><h2>Make something<br>of your own.</h2><p>These are creative starting points. Your tools, inputs and follow-up instructions shape the final result.</p></div><div class="steps"><div><div class="step-number">01</div><h3>Choose a direction</h3><p>Open an example. Watch the video and read the original post.</p></div><div><div class="step-number">02</div><h3>Make it specific</h3><p>Use a public prompt when available. Add your subject, audience and visual direction.</p></div><div><div class="step-number">03</div><h3>Preview, then refine</h3><p>Run the result, review the details and iterate before the final export.</p></div></div></section><section class="closing"><div><h2>Keep a few good ideas close.</h2><p>Star the GitHub collection to find it again when your next project comes along.</p></div><a class="button light" href="{REPO}">☆ Star on GitHub <span>↗</span></a></section></div>'''
write('index.html', document(REPOSITORY['title'], REPOSITORY['description'], body))
pages = [('', None)]
for key, cat in CATEGORIES.items():
    path = 'collections/' + key + '/'
    items = [x for x in SELECTION if x['category'] == key]
    body = f'''<div class="wrap"><div class="page-head"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../../">Collection</a><span>/</span><span>{cat['name']}</span></nav><div class="eyebrow">{len(items)} selected examples</div><h1>{cat['title']}</h1><p>{cat['intro']}</p></div><div class="category-intro"><div><h2>When to use these prompts</h2><p>{cat['when']}</p></div><div><h2>Before you begin</h2><p>{cat['before']}</p></div></div><section class="collection"><div class="grid">{''.join(card(x,'../../') for x in items)}</div></section><div class="closing"><p>Looking for another direction?</p><a class="text-link" href="../../#collection">See all selected work →</a></div></div>'''
    write(path+'index.html',document(cat['title'],cat['intro'],body,path))
    pages.append((path,max(x['modified'] for x in items)))
for item in SELECTION:
    path=case_url(item); cat=CATEGORIES[item['category']]
    related=[x for x in SELECTION if x['category']==item['category'] and x['id']!=item['id']][:3]
    body=f'''<div class="wrap"><div class="page-head"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../../">Collection</a><span>/</span><a href="../../collections/{item['category']}/">{cat['name']}</a><span>/</span><span>Prompt</span></nav><div class="eyebrow">{E(item['tool'])}</div><h1>{E(item['title'])}</h1><p>{E(item['description'])}</p></div>
<div class="detail"><div class="detail-main"><video class="detail-video" data-prompt-id="{item['id']}" controls muted playsinline loop preload="none" poster="{E(item['posterUrl'])}" src="{E(item['videoUrl'])}" aria-label="Creator video of {E(item['title'])}"></video><div class="media-caption"><span>Creator video · audio available</span><a href="{E(item['source'])}">Original post by @{E(item['author'])} ↗</a></div>{prompt_section(item)}</div>
<aside class="detail-sidebar" aria-label="Setup and source notes"><section class="side-section"><h2>What you’ll need</h2><p>{E(item['inputs'])}</p></section><section class="side-section"><h2>How to try it</h2><p style="font-size:11px;margin-bottom:15px">Suggested workflow from Leadde Open Lab.</p><ol>{''.join('<li>'+E(s)+'</li>' for s in item['steps'])}</ol></section><section class="side-section"><h2>About this example</h2><div class="meta-row"><span>Creator</span><span>@{E(item.get('creatorCredit') or item['author'])}</span></div><div class="meta-row"><span>Source model</span><span>{E(item['model'])}</span></div><div class="meta-row"><span>Published</span><span>{item['published']}</span></div><div class="meta-row"><span>Our reproduction</span><span>Not tested</span></div><div class="note"><strong>A note before you start</strong><p>{E(item['note'])}</p></div></section></aside></div><section class="related"><div class="kicker">Keep exploring</div><h2>More {cat['name'].lower()}.</h2><div class="grid">{''.join(card(x,'../../') for x in related)}</div></section></div>'''
    write(path+'index.html',document(item['title']+' — Gemini 4 prompt',item['description']+' Read the original post and prompt status.',body,path,item['id']))
    pages.append((path,item['modified']))
# The build date is not a content-modification date. Omit lastmod rather than invent one.
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{E(BASE+p)}</loc></url>\n' for p,_ in pages)+'</urlset>\n')
write('.nojekyll','')
not_found='<div class="wrap"><section class="page-head"><div class="eyebrow">404</div><h1>This page has moved<br>out of frame.</h1><p>Return to the collection to find a prompt for your next project.</p><div class="actions"><a class="button" href="'+E(BASE)+'">Back to the collection →</a></div></section></div>'
# Absolute asset URLs let GitHub Pages render the 404 at any missing path depth.
error=document('Page not found','Return to the Leadde Open Lab prompt collection.',not_found,noindex=True)
write('404.html',error.replace('href="./','href="'+E(BASE)).replace('src="./','src="'+E(BASE)))
print(f'Built {len(pages)} indexable pages in {OUT}')
print(f'Site URL: {BASE}')
print('Google verification: '+('HTML tag configured' if VERIFY else 'HTML verification file included' if list((SITE / 'public').glob('google*.html')) else 'not configured'))
