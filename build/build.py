import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p_main, p_profile, p_notice, p_admin, p_overlay, p_schedule, p_song, p_dress, p_work, p_diary, p_game

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TARGETS = [
    ('index.html',          p_main),
    ('profile/index.html',  p_profile),
    ('notice/index.html',   p_notice),
    ('schedule/index.html', p_schedule),
    ('song/index.html',     p_song),
    ('dress/index.html',    p_dress),
    ('work/index.html',     p_work),
    ('diary/index.html',    p_diary),
    ('game/index.html',     p_game),
    ('admin/index.html',    p_admin),
    ('overlay/index.html',  p_overlay),
]
for rel, mod in TARGETS:
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    html = mod.build()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{rel:22} {len(html):>7,} bytes')
