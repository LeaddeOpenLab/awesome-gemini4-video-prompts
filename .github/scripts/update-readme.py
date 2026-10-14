"""Build Leadde-style README cards and category indexes from the video catalog."""
from pathlib import Path
import json,html,sys,re
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'site'))
from catalog import CATEGORY_NAMES, FEATURED, TIPS, REPOSITORY
videos=json.loads((ROOT/'data/videos.json').read_text());by_id={v['id']:v for v in videos}
base=json.loads((ROOT/'site/site.json').read_text())['url']
metrics={p['id']:p for p in json.loads((ROOT/'data/engagement.json').read_text())['posts']}
E=lambda text:html.escape(str(text),quote=True)
def cards(items,columns=3,prefix='',featured=False,zh=False):
 lines=['<table>']
 for i in range(0,len(items),columns):
  lines.append('<tr>')
  for v in items[i:i+columns]:
   f=next((f for f in FEATURED if f['id']==v['id']),{})
   title=f.get('titleZh',v['title']) if zh else v['title']
   tip=TIPS[v['id']]
   label=('提示词解析' if zh else 'Prompt technique') if tip['basis']=='public_prompt' else ('复用建议 · 未公开 Prompt' if zh else 'Suggested approach · prompt not public')
   tip_box='<blockquote><strong>💡 Pro Tip / 核心咒语</strong><br><sub>'+label+'</sub><br>'+E(tip['zh' if zh else 'en'])+'</blockquote>'
   note=''
   if featured:
    m=metrics[v['id']]
    note=f'<br><sub>♥ {m["likes"]} · {m["replies"]} '+('评论' if zh else 'replies')+f' · {m["retweets"]} '+('转发' if zh else 'reposts')+'</sub><br><sub>'+E(f.get('reasonZh' if zh else 'reason',''))+'</sub>'
   lines.append(f'<td width="{100//columns}%" valign="top"><a href="{base}prompts/{v["id"]}/"><img src="{E(v["previewUrl"])}" alt="{E(title)}" width="100%" /></a><br><strong>{E(title)}</strong><br><sub><a href="{prefix}prompts/{v["id"]}.md">'+('查看提示词' if zh else 'View prompt')+f' · GitHub</a> · <a href="{base}prompts/{v["id"]}/">'+('观看视频' if zh else 'Watch preview')+f'</a> · <a href="{v["sourceUrl"]}">@{E(v["author"]["handle"])} ↗</a></sub>{note}{tip_box}</td>')
  lines.append('</tr>')
 lines.append('</table>');return '\n'.join(lines)
for zh in [False,True]:
 lines=['# '+REPOSITORY['title'],'',('[English](README.md) · 简体中文' if zh else 'English · [简体中文](README.zh-CN.md)'),'',f'[![1000 prompts · Gemini 4 Argon · Leadde Open Lab](data/banner.svg)]({base})','',('**由 Leadde Open Lab 整理的 Gemini 4 Argon 创作、视频预览与公开提示词。**' if zh else '**Gemini 4 Argon creations, video previews and public prompts — curated by Leadde Open Lab.**'),'',f'**[{"打开在线作品集 →" if zh else "Open the web collection →"}]({base})** · English / 简体中文','',('**☆ Star 本仓库，为下一个项目收藏灵感。**' if zh else '**☆ Star this repo to keep your next creative starting point close.**'),'',f'{len(videos)} '+('条视频案例 · ' if zh else 'video creations · ')+str(sum(bool(v['prompt']) for v in videos))+(' 条公开提示词或模板 · 5 个分类。' if zh else ' public prompts or templates · 5 collections.'),'',('其余作品明确标注未公开提示词，保留作者原帖供参考。' if zh else 'Entries without a public prompt are labelled accordingly and retain the creator’s original post.'),'',('[精选作品](#featured-creations) · [从这里开始](#start-here) · [完整分类](#browse-the-full-library)' if zh else '[Featured creations](#featured-creations) · [Start here](#start-here) · [Browse the full library](#browse-the-full-library)'),'', '<a id="featured-creations"></a>', '## '+('精选作品' if zh else 'Featured creations'),'',('从 47 条公开提示词或模板中，结合点赞、评论、转发和可复用性选取。互动数据采集于 2026-10-14，随时间变化。' if zh else 'Selected from 47 public prompts or templates for engagement and reusability. Likes, replies and reposts checked on October 14, 2026; counts change over time.'),'',cards([by_id[f['id']] for f in FEATURED],2,featured=True,zh=zh),'','<a id="start-here"></a>','## '+('从这里开始' if zh else 'Start here'),'',cards([by_id[id] for id in ['2110048102321365205','2110045963951956250','2110119580207337739']],zh=zh),'','## '+('最近发布' if zh else 'Recently added'),'',cards(sorted(videos,key=lambda v:v['publishedAt'],reverse=True)[:3],zh=zh),'','<a id="browse-the-full-library"></a>','## '+('浏览完整资料库' if zh else 'Browse the full library'),'']
 for key,(en,cn) in CATEGORY_NAMES.items():
  group=[v for v in videos if v['category']==key]
  lines.append(f'- [{cn if zh else en}](data/categories/{key}.md) ({len(group)})')
 for key,(en,cn) in CATEGORY_NAMES.items():
  group=[v for v in videos if v['category']==key]
  lines+=['','## '+(cn if zh else en)+' — '+('首页选摘' if zh else 'homepage picks'),'',cards(group[:3],zh=zh),'',f'[{"浏览全部" if zh else "Browse all"} {len(group)} →](data/categories/{key}.md)']
 lines+=['','## '+('使用方法' if zh else 'How to use'),'','1. '+('打开案例，观看视频并阅读原帖。' if zh else 'Open a creation, watch the video and read the original post.'),'2. '+('复制作者公开的提示词，按需要替换主题、参考图和模板占位符。' if zh else 'Copy a public prompt and replace the subject, reference images or template placeholders.'),'3. '+('按作者要求准备工具与素材，预览并迭代结果。' if zh else 'Prepare the tools and inputs described by the creator, then preview and refine.'),'','## '+('作者与权利' if zh else 'Creators & rights'),'','Videos, prompts and quoted posts belong to their original creators. See [media rights](MEDIA-RIGHTS.md). Every entry retains creator credits and original source links.','','[Catalog](data/videos.json) · [Selection notes](data/featured.json) · [Engagement snapshot](data/engagement.json)','']
 (ROOT/('README.zh-CN.md' if zh else 'README.md')).write_text('\n'.join(lines))
folder=ROOT/'data/categories';folder.mkdir(exist_ok=True)
for key,(en,cn) in CATEGORY_NAMES.items():
 group=[v for v in videos if v['category']==key]
 (folder/(key+'.md')).write_text(f'# {en}\n\n[← Back to the collection](../../README.md) · [{cn} · Website]({base}collections/{key}/)\n\n{len(group)} creations. Prompt availability is shown on each entry.\n\n'+cards(group,prefix='../../')+'\n')
print(f'Built two README pages and {len(CATEGORY_NAMES)} category indexes.')

# Keep each original prompt intact and refresh only the editorial callout.
for video in videos:
 tip=TIPS[video['id']]
 label='Prompt technique / 提示词解析' if tip['basis']=='public_prompt' else 'Suggested approach · prompt not public / 复用建议 · 未公开 Prompt'
 block='<!-- pro-tip -->\n> [!TIP]\n> **💡 Pro Tip / 核心咒语** · '+label+'\n>\n> '+tip['en']+'\n>\n> '+tip['zh']+'\n<!-- /pro-tip -->\n'
 path=ROOT/'prompts'/(video['id']+'.md')
 text=path.read_text()
 if '<!-- pro-tip -->' in text:
  text=re.sub(r'<!-- pro-tip -->.*?<!-- /pro-tip -->\n',lambda _:block,text,flags=re.S)
 else:
  text=text.replace('\n## Prompt\n','\n'+block+'\n## Prompt\n',1)
 path.write_text(text)
