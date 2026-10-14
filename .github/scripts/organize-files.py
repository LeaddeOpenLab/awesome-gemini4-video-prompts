"""Keep imports and generated documents out of the repository root."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import os, posixpath, re, subprocess

ROOT = Path(__file__).resolve().parents[2]

def destination(name):
    for prefix in ('data/', 'prompts/', 'site/'):
        if name.startswith(prefix): return 'collection/' + name
    for prefix in ('categories/', 'covers/'):
        if name.startswith(prefix): return 'collection/data/' + name
    if '/' not in name and name.startswith('README') and name != 'README.md':
        return 'collection/data/docs/translations/' + name
    return {
        'CONTRIBUTING.md': '.github/CONTRIBUTING.md',
        'RIGHTS.md': 'collection/data/docs/COLLECTION-RIGHTS.md',
        'MEDIA-RIGHTS.md': 'collection/data/docs/MEDIA-RIGHTS.md',
        'REVIEW-QUEUE.md': 'collection/data/docs/REVIEW-QUEUE.md',
        'repository.json': 'collection/data/source-repository.json',
    }.get(name, name)

def main():
    files = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
    link = re.compile(r'(\]\(|(?:href|src)=")(<)?([^\s"<>\)]+)(>)?')
    for name in files:
        path = ROOT / name
        if not path.is_file(): continue
        if path.suffix == '.md':
            def rewrite(match):
                url = urlsplit(match.group(3))
                if url.scheme or url.netloc or not url.path: return match.group(0)
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
                relative = posixpath.relpath(destination(target), posixpath.dirname(destination(name)) or '.')
                suffix = ('?' + url.query if url.query else '') + ('#' + url.fragment if url.fragment else '')
                return match.group(1) + (match.group(2) or '') + relative + suffix + (match.group(4) or '')
            text = path.read_text()
            updated = link.sub(rewrite, text)
            if updated != text: path.write_text(updated)
        elif path.suffix == '.json':
            text = path.read_text()
            updated = re.sub(r'("coverPath":\s*")(?:data/)?covers/', r'\1collection/data/covers/', text)
            if updated != text: path.write_text(updated)
    moved = 0
    # Fresh legacy imports replace their previously archived counterparts.
    files.sort(key=lambda name: name.startswith(('covers/', 'categories/', 'README_', 'README.')))
    for name in files:
        target = destination(name)
        if target == name or not (ROOT / name).is_file(): continue
        (ROOT / target).parent.mkdir(parents=True, exist_ok=True)
        os.replace(ROOT / name, ROOT / target)
        moved += 1
    print(f'Organized {moved} files under collection/ and .github/.')

if __name__ == '__main__': main()
