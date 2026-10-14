# Leadde Open Lab · GitHub Pages

这是 `awesome-gemini4-video-prompts` 的轻量内容站。沿用 Leadde 的紫色、Logo、白底和深灰文字，以作品和使用信息为主。首页、三个专题、九个案例共 13 个可索引页面；另有 404 页面。

## 本地预览

在仓库根目录运行：

```sh
python3 collection/site/build.py
python3 collection/site/check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory _site
```

浏览器打开 `http://127.0.0.1:4173/`。构建仅需 Python 标准库，不需要 npm、数据库或 API Key。

## 发布到 GitHub Pages

1. 将本次新增的 `site/`、`.github/workflows/pages.yml`、`.gitignore` 提交到 **LeaddeOpenLab/awesome-gemini4-video-prompts** 的 main 分支。本地目录名 `opus-prompt-site` 不代表另一个远程仓库。
2. 仓库 → Settings → Pages → Build and deployment → Source，选择 **GitHub Actions**。
3. Actions → Deploy prompt collection to GitHub Pages → Run workflow。
4. 部署成功后，以工作流返回的网址为准。默认地址应为：
   `https://leaddeopenlab.github.io/awesome-gemini4-video-prompts/`
5. 可以在仓库 About 的 Website 字段和 README 中加入该地址。README 目前由其他流程维护，发布前未自动改动，避免上线前出现无效入口。

工作流只发布 `_site/`，不会把原始数据、维护记录或整个仓库发布成网站。推送 `site/` 或 `data/library/` 后会重新构建。用 GitHub 默认 GITHUB_TOKEN 推送的自动化更新通常不会触发下一个 push 工作流；如你们的数据更新使用该机制，更新后手动运行 Pages 工作流，或由更新流程显式触发部署。

发布状态以 GitHub Actions 中最近一次 Pages 部署结果为准。

## Google Search Console

1. 网站发布后，在 Search Console 添加 **网址前缀** 资源，输入完整的 Pages 网站地址（包含仓库路径和末尾 `/`）。
2. 选择 HTML 标记验证，复制 `content` 属性中的验证值。
3. 二选一：
   - 在 GitHub Settings → Secrets and variables → Actions → Variables 中添加 `GOOGLE_SITE_VERIFICATION`，然后手动运行 Pages 工作流；或
   - 填入 `site/site.json` 的 `google_site_verification`，提交后自动部署。
4. 部署后回到 Google 点击验证，保留验证值。
5. 提交 `sitemap.xml`，检查首页和案例页，然后请求索引。

没有填入验证码时不会输出伪造的验证标签。验证和提交不保证收录或排名。网站数据不会包含既有 GitHub 仓库搜索历史。

GitHub 项目站位于子路径，子路径下的 robots.txt 无法控制域名根目录的抓取规则，因此不生成一个无效的项目级 robots.txt；通过 Search Console 提交 sitemap 即可。

## 内容维护

- `site/selection.json`：九个精选案例、页面路径、编辑后的标题、简短介绍和使用建议。
- `data/library/<id>.json`：原作者、原文提示词、来源和模型说明。构建时直接读取，不另建一份提示词数据库。
- `site/build.py`：生成完整静态 HTML、独立 metadata、canonical、Open Graph、WebPage/CollectionPage 结构化数据与 sitemap。
- `site/assets/site.css`、`site.js`：响应式样式、筛选、搜索、复制提示词和预览弹窗。
- `site/assets/posters/`、`previews/`：从仓库现有 GIF 与本地已有的原作者视频中抽取的封面和静音 MP4 短预览，不代表新复现成果。资产总量约 2.6 MB，视频按需加载。

新增案例时增加 selection 记录并准备同 ID 的 jpg 封面与 mp4 预览。构建会读取最新提示词内容。媒体更换时需同步更新预览资产。

现有九个案例均明确标注未由本站独立复现。使用建议与原作者提示词分开展示；英文翻译、工具不明确、工作区上下文缺失等信息保留在案例页。没有编造成功率、制作时长、用户数或 Star 数。

站点地址变更时更新 `site/site.json` 的 `url`，再构建。默认使用 GitHub Pages 项目路径，不需要自有域名。

## 已做的验证

`python3 collection/site/check.py` 检查生成页面、元数据、站内链接、锚点、静态资产和 sitemap。

本地另进行了隔离无头浏览器检查：桌面/手机布局、筛选、搜索空状态、预览播放与关闭、复制原文、无 JavaScript 正文可读。截图位于 `site/qa/`，不随站点部署。

## 语言切换

导航栏提供 English / 简中，首次访问默认英文，手动选择后会在当前浏览器中记住语言。`site/zh-CN.json` 保存简中文案，构建时与现有英文内容生成翻译表。首页、专题、案例和操作提示均可切换，作者提示词保留现有英文文本，复制内容不变。静态 HTML 和默认 SEO 元数据仍为英文，不新增语言网址。

## 已添加 HTML 文件验证

Google 提供的 `google9ddda4d9c22709a6.html` 保存在 `site/public/`，每次构建会原样复制到网站根目录。Search Console 中使用 HTML 文件验证即可，不必再填写 meta 验证值。验证成功后保留此文件。

## 展示与行为统计

卡片常驻播放入口，预览弹窗可直接复制原始提示词；复制权限不可用时显示并选中文本，供手动复制。首屏精选静音循环预览，离开可视区域、切换后台或打开弹窗时暂停，也可手动暂停；系统设置减少动态效果时默认不自动播放。

在 `site/site.json` 中填写 `ga_measurement_id`，或在 GitHub Actions Variables 中设置 `GA_MEASUREMENT_ID`，重新构建部署后启用 GA4。未配置时只在当前页面的 `window.dataLayer` 中排队事件，不向统计服务器发送数据，也不会汇总访客数据。

事件：`preview_play`（实际开始播放，每页面同一案例同一位置只计一次）、`prompt_copy`（剪贴板写入成功）、`github_click`、`leadde_click`。事件包含位置 `placement`，播放和复制包含 `prompt_id`，首屏播放标注 `autoplay`。不发送提示词正文或搜索输入。可以在 GA4 DebugView / 实时报告验证接收；需要按案例和位置分析时，将对应参数注册为自定义维度。

作品区第一张主推卡进入可视区域后静音循环播放，可手动暂停；其他卡片在支持鼠标悬停的设备上悬停播放、移出暂停并恢复封面。移出可视区域、切换后台、筛选隐藏或打开弹窗时暂停。视频按需加载；触屏仍使用点击预览，减少动态效果设置下默认不自动播放。播放统计位置新增 `spotlight` 和 `hover`。
