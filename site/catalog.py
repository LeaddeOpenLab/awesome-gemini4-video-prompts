"""Adapt the public video catalog to the Leadde collection layout."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = json.loads((ROOT / 'data/videos.json').read_text())
CATEGORY_NAMES = {
    'motion': ('Motion graphics & explainers', '动画与科普'),
    '3d': ('3D scenes & physics', '3D 场景与物理'),
    'interactive': ('Games & interactive experiences', '游戏与交互'),
    'comparison': ('Model comparisons', '模型对比'),
    'workflow': ('Build walkthroughs & workflow demos', '制作过程与工作流演示'),
}
CATEGORIES = {
    key: dict(name=en, title='Gemini 4 '+en.lower(),
              intro='Creator-shared '+en.lower()+', with video previews, original posts and public prompts when available.',
              when='Explore the videos and original posts to find a direction for your own project.',
              before='Check the prompt status and creator’s notes. Some entries share a public prompt or template; others document the result only.',
              short=en+'. Watch the result and explore the creator’s process.')
    for key, (en, _) in CATEGORY_NAMES.items()
}
SELECTION = []
for video in VIDEOS:
    status = ('Shared prompt template' if video['promptStatus'] == 'verbatim_template' else 'Public shared prompt') if video['prompt'] else 'Prompt not published'
    SELECTION.append(dict(video, slug=video['id'], author=video['author']['handle'],
        source=video['sourceUrl'], status=status,
        description=f"{video['duration']:.0f}s · {video['width']} × {video['height']} · {status}",
        tool='Gemini 4 Argon', model='Gemini 4 Argon · model comparison' if video['category']=='comparison' else 'Gemini 4 Argon (creator-reported)',
        inputs='Refer to the original post for the tools, assets and workflow used by the creator.',
        steps=['Watch the video and read the creator’s original post.',
               'Copy the public prompt when available; fill in any template placeholders.',
               'Check the creator’s tools and inputs, then preview and refine your result.'],
        note=video.get('note') or 'Model attribution follows the creator’s published account. This collection has not independently reproduced the result.',
        published=video['publishedAt'][:10], modified=video['publishedAt'][:10]))

FEATURED = json.loads((ROOT / 'data/featured.json').read_text())
for item in SELECTION:
    feature = next((f for f in FEATURED if f['id'] == item['id']), None)
    if feature:
        item.update({k: feature[k] for k in ['title', 'tool', 'description', 'inputs']})
