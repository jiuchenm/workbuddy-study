"""Bounded checks for the public report; no application code is executed."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re

root = Path(__file__).resolve().parents[1]
site = root / 'site'
text = (site / 'index.html').read_text(encoding='utf-8')
records = json.loads((site / 'mechanism-evidence.json').read_text(encoding='utf-8'))

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.scripts = [], [], []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'a' and 'href' in values:
            self.hrefs.append(values['href'])
        if tag == 'script' and 'src' in values:
            self.scripts.append(values['src'])

doc = Document()
doc.feed(text)
assert len(doc.ids) == len(set(doc.ids)), 'Duplicate element IDs'
assert all(h[1:] in doc.ids for h in doc.hrefs if h.startswith('#')), 'Broken section link'
assert not doc.scripts, 'Unexpected external script'
assert len(records) == 67
assert all(r['id'] in doc.ids for r in records)
assert all('local_path' not in r for r in records)
assert 'WorkBuddy 工程剖析' in text
assert 'file://' not in text.lower()
assert not re.search(r'[A-Za-z]:[\\/](?:Users|Program Files)', text, re.I), 'Machine path in HTML'
assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}', text)
assert '__SOURCES__' not in text and '__CASES__' not in text
for href in doc.hrefs:
    if href.startswith('./'):
        assert (site / href[2:]).is_file(), href
expected = {'index.html', 'mechanism-evidence.json', '.nojekyll'}
assert {p.name for p in site.iterdir()} == expected, 'Unexpected publication asset'
print(f'Public report verified: {len(records)} evidence records; section links resolve; no local paths or external scripts.')
