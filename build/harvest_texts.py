"""Rebuild texts.json from the data-t attributes in the built pages.
Run order: pages -> this -> admin. The admin text tab is generated from it."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
PAGES = [
    ('index.html', '메인'),
    ('profile/index.html', '프로필'),
    ('notice/index.html', '공지'),
    ('schedule/index.html', '일정'),
    ('song/index.html', '노래책'),
    ('dress/index.html', '옷장'),
    ('work/index.html', '업보'),
    ('diary/index.html', '일기'),
    ('game/index.html', '미니게임'),
]
TAG = re.compile(r'<(\w+)([^>]*\bdata-t="([^"]+)"[^>]*)>(.*?)</\1>', re.S)


def harvest():
    out = {}
    for rel, label in PAGES:
        with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
            html = f.read()
        for m in TAG.finditer(html):
            key, inner = m.group(3), m.group(4)
            if key in out:
                continue
            text = re.sub(r'<[^>]+>', '', inner).strip()
            out[key] = {'page': label, 'text': text}
    with open(os.path.join(HERE, 'texts.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    return out


if __name__ == '__main__':
    print(len(harvest()), 'keys')
