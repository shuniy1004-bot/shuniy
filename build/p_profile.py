import os
from shell import page, SHARED_TAIL

HERE = os.path.dirname(os.path.abspath(__file__))


def _read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()


def build():
    return page(slug="profile", title="프로필", desc="프로필", root="../",
                body=_read('_profile_body.txt'),
                css=_read('_profile_css.txt'),
                script=SHARED_TAIL + _read('_profile_script.txt'),
                footer_mark="STAR ATLAS · LOG 01")
