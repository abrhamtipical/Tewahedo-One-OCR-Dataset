"""Compare the app's old Se'atat Ge'ez text (git HEAD, sections 1-24) with the
user's OCR (research/seatat_ocr/clean/pages.json) and report what the OCR lacks.

Words are normalised (homophone letters folded, punctuation dropped) so only
real differences show. Output: research/seatat_ocr/fill/old_vs_ocr.json + .md
"""
import difflib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'research/seatat_ocr/fill'
ETH = re.compile(r'[\u1200-\u1359]')

# fold homophone letter families onto one row (same vowel order)
FAMILIES = {'ሐ': 'ሀ', 'ኀ': 'ሀ', 'ኸ': 'ሀ', 'ሠ': 'ሰ', 'ዐ': 'አ', 'ፀ': 'ጸ'}


def fold(ch):
    cp = ord(ch)
    base = ch
    for src, dst in FAMILIES.items():
        s = ord(src)
        if s <= cp < s + 8:
            base = chr(ord(dst) + (cp - s))
    return base


def norm_word(w):
    w = ''.join(fold(c) for c in w if ETH.match(c) and c not in '፡።፣፤፥፦፧')
    return w.replace('ኵ', 'ኩ').replace('ኲ', 'ኩ').replace('ኰ', 'ኮ').replace('ቍ', 'ቁ')


def old_sections():
    secs = []
    for i in range(1, 25):
        raw = subprocess.run(
            ['git', 'show', f'HEAD:unencrypted_data/liturgy/book_of_hours_{i:02d}.json'],
            cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout
        raw = re.sub(r'^/\*.*?\*/', '', raw, flags=re.S)
        d = json.loads(raw)
        secs.append((i, [x['text'] for x in d]))
    return secs


def main():
    pages = json.loads((ROOT / 'research/seatat_ocr/clean/pages.json').read_text(encoding='utf-8'))
    ocr = [(p['page'], w) for p in pages if p['page'] >= 4
           for s in p['geez'] for w in s.replace('።', ' ').split() if norm_word(w)]
    ocr_n = [norm_word(w) for _, w in ocr]
    secs = old_sections()
    old = [(i, k, w) for i, texts in secs for k, t in enumerate(texts)
           for w in t.split() if norm_word(w)]
    old_n = [norm_word(w) for _, _, w in old]
    sm = difflib.SequenceMatcher(None, old_n, ocr_n, autojunk=False)
    only_old, matched = [], 0
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == 'equal':
            matched += a1 - a0
        elif tag in ('delete', 'replace'):
            only_old.append({
                'section': old[a0][0], 'line': old[a0][1],
                'old': ' '.join(w for _, _, w in old[a0:a1]),
                'ocr': ' '.join(w for _, w in ocr[b0:b1]),
                'ocr_page': ocr[b0][0] if b0 < len(ocr) else None,
                'tag': tag, 'words': a1 - a0,
            })
    print(f'old words {len(old_n)}  ocr words {len(ocr_n)}  matched {matched} '
          f'({100*matched/len(old_n):.1f}% of old)')
    (OUT / 'old_vs_ocr.json').write_text(json.dumps(only_old, ensure_ascii=False, indent=1), encoding='utf-8')
    by = {}
    for o in only_old:
        by.setdefault(o['section'], []).append(o)
    for s in sorted(by):
        print(f'section {s:2}: {len(by[s]):4} gaps, {sum(o["words"] for o in by[s]):5} old words not matched')


main()
