"""Cross-check the line-aligned second OCR (raw2) against the first OCR (raw).

Both are normalised the same way (non-Ethiopic stripped, every separator and
space removed) so only real letter differences show up.
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
R1 = ROOT / 'research/seatat_ocr/raw'
R2 = ROOT / 'research/seatat_ocr/raw2'
ETH = re.compile(r'[\u1200-\u137F]')
KEEP = re.compile(r'[\u1200-\u135F\u1369-\u137C]')  # letters + numerals, no punctuation


def norm(s):
    s = re.sub(r'\[None present on this page\]', '', s)
    s = re.sub(r'የኢትዮጵያ ኦርቶዶክስ ተዋሕዶ ቤተ ክርስቲያን ሃይማኖትና ሥርዓት', '', s)
    return ''.join(KEEP.findall(s))


def first():
    out = {}
    for f in sorted(R1.glob('part*.txt')):
        raw = f.read_text(encoding='utf-8')
        raw = re.sub(r'\((?:Note|note)[^)]*\)', '', raw)
        parts = re.split(r'Page\s+(\d+)', raw)[1:]
        for i in range(0, len(parts), 2):
            pg, body = int(parts[i]), parts[i + 1]
            col, d = None, {'g': [], 'a': []}
            for line in body.splitlines():
                if line.startswith('ግዕዝ:'): col, line = 'g', line[5:]
                elif line.startswith('አማርኛ:'): col, line = 'a', line[6:]
                if col: d[col].append(line)
            out[pg] = {k: norm(' '.join(v)) for k, v in d.items()}
    return out


def second():
    out = {}
    for f in sorted(R2.glob('*.txt')):
        for m in re.finditer(r'=== Page (\d+) ===\n\[GEEZ\]\n(.*?)\n\[AMHARIC\]\n(.*?)(?=\n=== Page|\Z)',
                             f.read_text(encoding='utf-8'), re.S):
            out[int(m.group(1))] = {'g': norm(m.group(2)), 'a': norm(m.group(3)),
                                    'gl': m.group(2).strip().splitlines(),
                                    'al': m.group(3).strip().splitlines()}
    return out


def main():
    a, b = first(), second()
    bad = 0
    for pg in sorted(b):
        for k, name in (('g', "Ge'ez"), ('a', 'Amharic')):
            x, y = a[pg][k], b[pg][k]
            if x != y:
                bad += 1
                i = next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))
                print(f'p{pg} {name}: differs at char {i}: ocr1 …{x[max(0,i-12):i+12]}…  ocr2 …{y[max(0,i-12):i+12]}…  (len {len(x)} vs {len(y)})')
        print(f'p{pg}: lines Ge\'ez {len(b[pg]["gl"])} / Amharic {len(b[pg]["al"])}')
    print('pages with a letter difference:', bad)


main()
