"""Clean the user's own Se'atat OCR (Ge'ez + Amharic columns) into JSON.

Input:  research/seatat_ocr/raw/part*.txt  (pasted OCR, "Page N" markers,
        "ግዕዝ:" / "አማርኛ:" column lines)
Output: research/seatat_ocr/clean/pages.json  [{page, geez: [..], amharic: [..]}]
        research/seatat_ocr/clean/removed.txt  everything stripped, for review

Only noise is removed (scan watermark, English and other non-Ethiopic
letters, notes, stray Latin digits, running heads); wording is not changed.
The word separator ፡ is kept (the user wants it, unlike the old space-only
text); OCR misreads of it (' : · = etc.) become ፡. Ethiopic ፣ ፤ ፥ ፧ stay.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'research' / 'seatat_ocr' / 'raw'
OUT = ROOT / 'research' / 'seatat_ocr' / 'clean'

WATERMARK = re.compile(
    r'የኢትዮጵያ\s*ኦርቶዶክስ\s*ተዋሕዶ\s*ቤተ\s*ክርስቲያን\s*ሃይማኖትና\s*ሥርዓት'
    r'|The Ethiopian Orthodox Tewahido Church Faith and Order'
    r'|www\.ethiopianorthodox\.org')
NOTE = re.compile(r'\((?:Note|note)[^)]*\)\.?|\[None present on this page\]')
# Running heads printed at the top of every page.
RUNNING_HEAD = re.compile(r'^\s*(?:መጽሐፈ[\s፡]*ሰዓታት|መቅድም)\s*።\s*')
# Any non-Ethiopic letters (English, OCR junk such as Thai or Greek).
LATIN = re.compile(r'[^\W\d_ሀ-፿]+')
# Words the OCR split in two at a line break.
SPLIT_WORDS = {'እግዚ አብሔር': 'እግዚአብሔር', 'ዑራ ኤል': 'ዑራኤል'}
MATH = re.compile(r'\$[^$]*\$')  # LaTeX the OCR invented
STOPS = '።፣፤፥፧'
STRAY_DIGITS = re.compile(r'(?<![፩-፼])\b\d+[-–]?(?![፩-፼])')
# OCR read ፡ as ' : · = etc. Inside a line these are word separators.
SEPARATORS = re.compile(r"[፡'’‘`´˙:·•▪»«\"“”,.\-–|›‹;=!?\s]*[፡'’‘`´˙:·•▪»«\"“”,.\-–|›‹;=!?][፡'’‘`´˙:·•▪»«\"“”,.\-–|›‹;=!?\s]*")
FULL_STOP = re.compile(r'\s*(?:።|፡፡|::)\s*')


def clean(text, removed, where, first=True):
    for pat in (WATERMARK, NOTE, MATH):
        for m in pat.findall(text):
            removed.append(f'{where}: {m}')
        text = pat.sub(' ', text)
    text = text.replace('AR:', ' ')
    for m in LATIN.findall(text):
        removed.append(f'{where}: {m}')
    text = LATIN.sub(' ', text)
    for m in STRAY_DIGITS.findall(text):
        removed.append(f'{where}: digit {m}')
    text = STRAY_DIGITS.sub(' ', text)
    for split, word in SPLIT_WORDS.items():
        text = text.replace(split, word)
    text = FULL_STOP.sub(' ። ', text)
    text = SEPARATORS.sub(' ፡ ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(rf'(?:\s*፡)+\s*([{STOPS}])', r' \1', text)  # no ፡ before a stop
    text = re.sub(rf'([{STOPS}])(?:\s*፡)+', r'\1', text)
    text = re.sub(rf'\s*([{STOPS}])\s*', r' \1 ', text)
    text = re.sub(r'^\s*፡\s*|\s*፡\s*$', '', text).strip()
    head = RUNNING_HEAD.match(text) if first else None
    if head:
        removed.append(f'{where}: running head {head.group(0).strip()}')
        text = text[head.end():]
    # A bare space means the scan lost the separator (፡, sometimes ።).
    word = rf'[^\s፡{STOPS}]+'
    for m in re.finditer(rf'({word}) (?={word})', text):
        removed.append(f'{where}: ፡ added (check for lost ።): {m.group(0)}…')
    text = re.sub(rf'(?<=[^\s፡{STOPS}]) (?=[^\s፡{STOPS}])', ' ፡ ', text)
    return text


def sentences(text):
    parts = [p.strip() for p in text.split('።')]
    out = [p + ' ።' for p in parts[:-1] if p]
    if parts and parts[-1]:
        out.append(parts[-1])  # runs on to the next page
    return out


def column(lines, removed, where):
    out = []
    for i, line in enumerate(lines):
        out += sentences(clean(line, removed, where, first=(i == 0)))
    return out


def parse(raw):
    pages = []
    raw = NOTE.sub(' ', raw)  # notes mention "Page N" themselves
    for chunk in re.split(r'Page\s+(\d+)', raw)[1:]:
        if chunk.isdigit():
            pages.append({'page': int(chunk), 'geez': [], 'amharic': []})
            continue
        col = None
        for line in chunk.splitlines():
            line = line.strip()
            if line.startswith('ግዕዝ:'):
                col, line = 'geez', line[len('ግዕዝ:'):]
            elif line.startswith('አማርኛ:'):
                col, line = 'amharic', line[len('አማርኛ:'):]
            if col and line.strip():
                pages[-1][col].append(line)  # one entry per printed line
    return pages


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    removed, result = [], []
    files = sorted(RAW.glob('part*.txt'))
    for f in files:
        for p in parse(f.read_text(encoding='utf-8')):
            where = f'p{p["page"]}'
            result.append({
                'page': p['page'],
                'geez': column(p['geez'], removed, where + ' gez'),
                'amharic': column(p['amharic'], removed, where + ' am'),
            })
    result.sort(key=lambda p: p['page'])
    (OUT / 'pages.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')
    (OUT / 'removed.txt').write_text('\n'.join(removed), encoding='utf-8')
    for p in result:
        print(f'page {p["page"]:3}: gez {len(p["geez"]):3}  am {len(p["amharic"]):3}')
    print(f'{len(removed)} removals logged', file=sys.stderr)


if __name__ == '__main__':
    main()
