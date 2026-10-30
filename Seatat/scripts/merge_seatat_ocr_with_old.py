"""Merge the user's own Se'atat OCR (Ge'ez + Amharic) with the app's old text.

Rule from the user: the OCR is the main text; whatever the OCR lacks or leaves
incomplete is added from the old text (git HEAD, sections 1-24).

Inputs : research/seatat_ocr/raw/part*.txt   first OCR (pages 1-79)
         research/seatat_ocr/raw2/*.txt      line-aligned OCR (used where present)
         git HEAD unencrypted_data/liturgy/book_of_hours_01..24.json (old text)
Output : research/seatat_ocr/merged/book_of_hours_NN.json   (proposal, not shipped)
         research/seatat_ocr/merged/REPORT.md

Nothing here touches assets/ or unencrypted_data/.
"""
import difflib
import importlib.util
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / 'research/seatat_ocr'
OUT = OCR / 'merged'


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    src = (ROOT / 'scripts' / f'{name}.py').read_text(encoding='utf-8')
    ns = {'__file__': str(ROOT / 'scripts' / f'{name}.py'), '__name__': name}
    exec(compile(src.replace("\nmain()\n", "\n").replace("\nif __name__ == '__main__':\n    main()\n", "\n"), name, 'exec'), ns)
    return ns


C = load('clean_seatat_ocr')
O = load('compare_seatat_old_vs_ocr')
norm_word = O['norm_word']


# ---------------------------------------------------------------- book pages
def book_pages():
    """page -> {'geez': [printed lines], 'amharic': [printed lines]} (raw lines)."""
    pages = {}
    for f in sorted((OCR / 'raw').glob('part*.txt')):
        for p in C['parse'](f.read_text(encoding='utf-8')):
            pages[p['page']] = {'geez': p['geez'], 'amharic': p['amharic']}
    # the line-aligned copy wins where we have it
    for f in sorted((OCR / 'raw2').glob('*.txt')):
        text = f.read_text(encoding='utf-8')
        for m in re.finditer(r'=== Page (\d+) ===\n\[GEEZ\]\n(.*?)\n\[AMHARIC\]\n(.*?)(?=\n=== Page|\Z)', text, re.S):
            g = [x for x in m.group(2).splitlines() if x.strip() and 'None present' not in x]
            a = [x for x in m.group(3).splitlines() if x.strip() and 'None present' not in x]
            pages[int(m.group(1))] = {'geez': g, 'amharic': a}
    return pages


def sentences_of(lines, page, removed):
    """Cleaned sentences of a column, each tagged with its page."""
    out = []
    for i, line in enumerate(lines):
        t = C['clean'](line, removed, f'p{page}', first=(i == 0))
        for s in C['sentences'](t):
            out.append((page, s))
    return out


def join_fragments(sents):
    """A sentence with no closing ። continues into the next one (page breaks)."""
    out = []
    carry = None
    for page, s in sents:
        if carry:
            page0, prev = carry
            s = prev + ' ' + s
            page = page0
            carry = None
        if not s.rstrip().endswith('።') and not re.search(r'[፣፤፥፧]$', s.rstrip()):
            carry = (page, s)
            continue
        out.append((page, s))
    if carry:
        out.append(carry)
    return out


# ------------------------------------------------------------ Ge'ez/Amharic
def nwords(s):
    return max(1, len([w for w in re.split(r'[\s፡።፣፤፥፧]+', s) if w]))


def align_pairs(g, a, moves=None):
    """Length-based alignment (Gale-Church style). Returns list of (gi_list, ai_list)."""
    G = [nwords(s) for _, s in g]
    A = [nwords(s) for _, s in a]
    c = sum(A) / max(1, sum(G))
    moves = moves or [(1, 1, 0), (1, 2, 4), (2, 1, 4), (1, 0, 14), (0, 1, 14), (2, 2, 8), (1, 3, 10), (3, 1, 10), (2, 3, 12), (3, 2, 12)]
    INF = 1e18
    n, m = len(g), len(a)
    cost = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if cost[i][j] >= INF:
                continue
            for di, dj, pen in moves:
                ni, nj = i + di, j + dj
                if ni > n or nj > m:
                    continue
                gw, aw = sum(G[i:ni]), sum(A[j:nj])
                dev = (aw - c * gw) ** 2 / (c * gw + 2) if gw else aw * 2
                v = cost[i][j] + dev + pen
                if v < cost[ni][nj]:
                    cost[ni][nj] = v
                    back[ni][nj] = (i, j)
    out, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj = back[i][j]
        out.append((list(range(pi, i)), list(range(pj, j))))
        i, j = pi, pj
    return out[::-1]


LINE_MOVES = [(1, 1, 0), (1, 2, 9), (2, 1, 9), (1, 0, 9), (0, 1, 9), (1, 3, 14), (3, 1, 14)]


def clean_lines(lines, page, removed):
    out = []
    for i, line in enumerate(lines):
        t = C['clean'](line, removed, f'p{page}', first=(i == 0))
        if re.match(r'መልአኩ ፡ ቅዱስ ፡ ዑራዔልን', t.strip()):
            removed.append(f'p{page}: page-foot note about the preface dropped: {t.strip()[:60]}')
            continue
        if t.strip():
            out.append(t.strip())
    return out


def is_stopped(t):
    return t.rstrip().endswith('።') or bool(re.search(r'[፣፤፥፧]$', t.rstrip()))


# Pages whose Amharic column is mixed up with Ge'ez text (checked against the scan):
# page -> [(Ge'ez line numbers, [Amharic line numbers or literal text])]
PAGE_PAIRS = {
    68: [([0], [0]), ([1], [1]), ([2], [2]), ([3], [3]), ([4], [4, 5]), ([5], [6]), ([6], [])],
    69: [([0], [0]), ([1], [1]), ([2], ['በእመቤታችን ፡ ድንግልና', 11]), ([3], [12]), ([4], [13]), ([5], [14]),
         ([6], [15]), ([7], [16]), ([8], [17]), ([9], [18]), ([10], [19]), ([11], [20]), ([12], [21]),
         ([13], [22]), ([14], [23])],
}


def pair_by_lines(pages, plist, removed):
    """Printed line i of the Ge'ez column <-> printed line i of the Amharic
    column (the book is typeset line against line). Pages whose line counts
    differ a lot fall back to sentence alignment."""
    out = []
    for p in plist:
        g = clean_lines(pages[p]['geez'], p, removed)
        a = clean_lines(pages[p]['amharic'], p, removed)
        if p in PAGE_PAIRS:
            for gi, ai in PAGE_PAIRS[p]:
                at = ' '.join(a[i] if isinstance(i, int) else i for i in ai)
                out.append({'geez': ' '.join(g[i] for i in gi), 'amharic': at, 'page': p, 'pairing': 'checked'})
        elif min(len(g), len(a)) >= 3 and abs(len(g) - len(a)) <= 2:
            for gi, ai in align_pairs([(p, x) for x in g], [(p, x) for x in a], LINE_MOVES):
                gt = ' '.join(g[i] for i in gi)
                at = ' '.join(a[i] for i in ai)
                if gi:
                    out.append({'geez': gt, 'amharic': at, 'page': p, 'pairing': 'line %d:%d' % (len(gi), len(ai))})
                elif out and at:
                    out[-1]['amharic'] = (out[-1]['amharic'] + ' ' + at).strip()
                    out[-1]['pairing'] += '+extra-am'
        else:
            gs = join_fragments(sentences_of(pages[p]['geez'], p, removed))
            as_ = join_fragments(sentences_of(pages[p]['amharic'], p, removed))
            for gi, ai in align_pairs(gs, as_):
                at = ' '.join(as_[i][1] for i in ai)
                if gi:
                    out.append({'geez': ' '.join(gs[i][1] for i in gi), 'amharic': at, 'page': p,
                                'pairing': 'sent %d:%d' % (len(gi), len(ai))})
                elif out and at:
                    out[-1]['amharic'] = (out[-1]['amharic'] + ' ' + at).strip()
                    out[-1]['pairing'] += '+extra-am'
    # a line that runs over the page break continues in the next page's first line
    merged = []
    for e in out:
        if merged and not is_stopped(merged[-1]['geez']) and e['page'] == merged[-1]['page'] + 1                 and not merged[-1].get('_closed'):
            m = merged[-1]
            m['geez'] += ' ' + e['geez']
            m['amharic'] = (m['amharic'] + ' ' + e['amharic']).strip()
            m['pairing'] += '+joined'
            m['_closed'] = True
            continue
        merged.append(e)
    for e in merged:
        e.pop('_closed', None)
    # a printed line of several sentences: split it when both columns agree
    final = []
    for e in merged:
        gs, as_ = C['sentences'](e['geez']), C['sentences'](e['amharic'])
        if len(gs) > 1 and len(gs) == len(as_):
            c = nwords(e['amharic']) / nwords(e['geez'])
            if all(0.4 * c <= nwords(y) / nwords(x) <= 2.5 * c for x, y in zip(gs, as_)):
                final += [dict(e, geez=x, amharic=y, pairing=e['pairing'] + '/split') for x, y in zip(gs, as_)]
                continue
        final.append(e)
    return final



def build_groups(pages, removed):
    """Ordered list of {'geez','amharic','page','pairing'} for pages 4-79."""
    groups = []
    seg_a, seg_b = (4, 34), (65, 74)
    nums = sorted(p for p in pages if p >= 4)
    cur = None
    # decide which pages carry an Amharic column
    for p in nums:
        has_am = bool(pages[p]['amharic'])
        key = 'am' if has_am else 'ge'
        if cur is None or cur['kind'] != key:
            cur = {'kind': key, 'pages': []}
            groups.append(cur)
        cur['pages'].append(p)
    result = []
    for seg in groups:
        if seg['kind'] == 'ge':
            g = []
            for p in seg['pages']:
                g += sentences_of(pages[p]['geez'], p, removed)
            result += [{'geez': s, 'amharic': '', 'page': p, 'pairing': 'geez-only'} for p, s in join_fragments(g)]
            continue
        result += pair_by_lines(pages, seg['pages'], removed)
    return result


# ----------------------------------------------------------------- merging
STOPS = {'።', '፣', '፤', '፥', '፧'}
NEW_SECTIONS = {
    33: ('መግቢያ (መቅድም)', 'Introduction (Preface)'),
    34: ('ምልጣን ወተሣሃለነ እግዚኦ', 'Meltan and "Have Mercy on Us, O Lord"'),
    35: ('ጳውሎስ ወጴጥሮስ ወግብረ ሐዋርያት', 'Paul, Peter and the Acts of the Apostles'),
    36: ('በ፲ቱወ፪ቱ ሰዓተ ሌሊት', 'The Twelfth Hour of the Night'),
    37: ('ሰላም ለክሙ ወመስቀል', 'Peace to You: Giyorgis, Tekle Haymanot and the Cross'),
}
SOURCE_LINES = (
    " * Language:   Ge'ez, with the Amharic translation where the book has it\n"
    " * Source:     Mets'hafe Se'atat in Ge'ez and Amharic (night and dawn);\n"
    " *             Amharic translation by Aleqa Mekonnen Solomon of Debre Libanos,\n"
    " *             Tensae Zegubae Press. Text typed and edited from the printed\n"
    " *             book by Abraham Sisay. Passages the book lacks are supplied\n"
    " *             from the Se'atat text this app already had (EOTC traditional\n"
    " *             liturgy), marked in the entry metadata.\n")


def tokens_join(toks):
    """Words separated by the Ethiopic word space, stop marks attached with a plain space."""
    out = []
    for t in toks:
        if t in STOPS:
            if out and out[-1] == '፡':
                out.pop()
            out.append(t)
        elif t == '፡':
            if out and out[-1] not in STOPS and out[-1] != '፡':
                out.append(t)
        else:
            if out and out[-1] not in STOPS and out[-1] != '፡':
                out.append('፡')
            out.append(t)
    while out and out[-1] == '፡':
        out.pop()
    return ' '.join(out)


def sep(text):
    for ch in STOPS:
        text = text.replace(ch, f' {ch} ')
    return tokens_join(text.split())


def header_for(title_line):
    return ('/*\n' + title_line + '\n' + SOURCE_LINES +
            " * Ownership:  This text belongs to the Ethiopian Orthodox Tewahedo Church.\n"
            " *             It is the Church's public heritage and is not the property of\n"
            " *             any individual, publisher or application.\n"
            " * Status:     Public content, shared for the faithful.\n"
            " * Note:       This notice is metadata only and is never shown in the app.\n */\n")


def intro_entries(pages, removed):
    """The introduction: title page and preface (pages 1-3)."""
    def col(p, key):
        out = []
        for i, line in enumerate(pages[p][key]):
            t = C['clean'](line, removed, f'p{p}', first=(i == 0))
            if t:
                out.append(t)
        return ' '.join(out)
    items = [{'text': col(1, 'geez'), 'amh': col(1, 'amharic'), 'title': 'መጽሐፈ ሰዓታት', 'turn': ''}]
    prose = (col(2, 'amharic') + ' ' + col(3, 'amharic')).strip()
    sents = [x for x in re.split(r'(?<=።)\s*', prose) if x]
    chunks, cur = [], ''
    for sn in sents:
        if cur and len(cur) + len(sn) > 650:
            chunks.append(cur.strip())
            cur = ''
        cur += sn + ' '
    if cur.strip():
        chunks.append(cur.strip())
    items.append({'text': col(2, 'geez'), 'amh': chunks[0] if chunks else '', 'title': 'መቅድም', 'turn': ''})
    for ch in chunks[1:]:
        items.append({'text': ch, 'amh': '', 'title': 'መቅድም', 'turn': ''})
    return items


def old_meta_index(old_meta):
    return {(s, k) for s, (_, body) in old_meta.items() for k in range(len(body))}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    removed = []
    pages = book_pages()
    groups = build_groups(pages, removed)

    old_meta = {}
    for i in range(1, 25):
        raw = O['subprocess'].run(
            ['git', 'show', f'HEAD:unencrypted_data/liturgy/book_of_hours_{i:02d}.json'],
            cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout
        header = re.match(r'/\*.*?\*/', raw, re.S).group(0)
        body = json.loads(re.sub(r'^/\*.*?\*/', '', raw, flags=re.S))
        old_meta[i] = (header, body)

    # book blocks from the meltan onward have no counterpart in the old text
    first_meltan = next(gi for gi, g in enumerate(groups) if g['page'] >= 67 and g['geez'].startswith('ምልጣን'))
    block_of = {}
    for gi in range(first_meltan, len(groups)):
        pg = groups[gi]['page']
        block_of[gi] = 34 if pg <= 70 else 35 if pg <= 74 else 36 if pg <= 76 else 37

    bw = []  # (group index, token index, word)
    for gi, g in enumerate(groups):
        for ti, tok in enumerate(g['geez'].split()):
            if norm_word(tok):
                bw.append((gi, ti, tok))
    ow = []  # (section, entry index, word)
    for s, (_, body) in old_meta.items():
        for k, e in enumerate(body):
            for w in e['text'].split():
                if norm_word(w):
                    ow.append((s, k, w))
    bn = [norm_word(w) for _, _, w in bw]
    on = [norm_word(w) for _, _, w in ow]
    sm = difflib.SequenceMatcher(None, on, bn, autojunk=False)
    ops = sm.get_opcodes()

    hit_old = [False] * len(ow)
    group_hits = defaultdict(Counter)
    for a, b, n in sm.get_matching_blocks():
        for j in range(n):
            hit_old[a + j] = True
            group_hits[bw[b + j][0]][(ow[a + j][0], ow[a + j][1])] += 1
    entry_tot, entry_hit = Counter(), Counter()
    for h, (s, k, _) in zip(hit_old, ow):
        entry_tot[(s, k)] += 1
        entry_hit[(s, k)] += h
    absent = {e for e in entry_tot if entry_hit[e] / entry_tot[e] < 0.30 or e[0] >= 22}
    for s, (_, body) in old_meta.items():
        for k in range(len(body)):
            if (s, k) not in entry_tot:
                absent.add((s, k))

    sec_of, last = [], (1, 0)
    for gi, g in enumerate(groups):
        if gi in block_of:
            sec_of.append((block_of[gi], 0))
            continue
        hits = Counter({e: c for e, c in group_hits[gi].items() if e[0] < 22 and e not in absent})
        if hits:
            last = hits.most_common(1)[0][0]
        sec_of.append(last)

    insert_after = defaultdict(list)
    seen = set()
    gap_tokens = defaultdict(list)  # (group, token) -> [(s, k, words)]
    for tag, a0, a1, b0, b1 in ops:
        if tag not in ('delete', 'replace'):
            continue
        anchor = bw[b0 - 1][0] if b0 > 0 else 0
        by_entry = defaultdict(list)
        for x in range(a0, a1):
            by_entry[(ow[x][0], ow[x][1])].append(ow[x][2])
        for e, words in by_entry.items():
            if e in absent:
                if e not in seen:
                    seen.add(e)
                    insert_after[anchor].append(e)
            elif tag == 'delete' and b0 > 0:
                gi, ti, _ = bw[b0 - 1]
                if gi not in block_of:
                    gap_tokens[(gi, ti)].append((e[0], e[1], words))
    for e in absent:
        if e not in seen:
            insert_after[len(groups) - 1].append(e)

    sections = defaultdict(list)

    def old_item(e):
        s, k = e
        src = old_meta[s][1][k]
        extra = {x: v for x, v in src.items() if x not in ('text', 'title', 'turn', 'amh', 'sortOder', 'metadata')}
        return {'text': sep(src['text']), 'amh': src.get('amh', ''), 'title': src.get('title'),
                'turn': src.get('turn', ''), '_k': k, '_src': 'old', '_meta': src.get('metadata'), **extra}

    for gi, g in enumerate(groups):
        s, k = sec_of[gi]
        toks = g['geez'].split()
        inserts = defaultdict(list)
        for (g2, ti), lst in gap_tokens.items():
            if g2 == gi:
                inserts[ti] += lst
        filled = []
        for ti in sorted(inserts, reverse=True):
            new = []
            for (_s, _k, words) in inserts[ti]:
                new += ' '.join(words).replace('።', ' ።').split()
                filled.append(' '.join(words))
            toks[ti + 1:ti + 1] = ['፡'] + tokens_join(new).split()
        text = tokens_join(toks)
        title, turn = None, ''
        if gi not in block_of and group_hits[gi] and (s, k) in old_meta_index(old_meta):
            e = old_meta[s][1][k]
            title, turn = e.get('title'), e.get('turn', '')
        plain = [t for t in text.split() if t not in ('፡',) and t not in STOPS]
        item = {'text': text, 'amh': g['amharic'], 'title': title or ' '.join(plain[:4]),
                'turn': turn, '_k': k + gi / 1000, '_src': 'book', '_page': g['page'], '_pairing': g['pairing'],
                '_meta': {'schemaVersion': 1, 'source': "Mets'hafe Se'atat (own transcription)",
                          'language': 'gez-am' if g['amharic'] else 'gez'}}
        if filled:
            item['_meta']['filledFromOldText'] = filled
        sections[s].append(item)
        for e in insert_after.get(gi, []):
            sections[e[0]].append(old_item(e))

    for s in list(sections):
        if all(x['_src'] == 'old' for x in sections[s]):
            sections[s].sort(key=lambda x: x['_k'])
    for s in range(1, 25):
        if not sections.get(s):
            sections[s] = [old_item((s, k)) for k in range(len(old_meta[s][1]))]

    sections[33] = [dict(x, _k=n, _src='book',
                         _meta={'schemaVersion': 1, 'source': "Mets'hafe Se'atat (own transcription)",
                                'language': 'gez-am' if x['amh'] else 'am'})
                    for n, x in enumerate(intro_entries(pages, removed))]

    rep = ['# Merge report: own transcription + old text\n',
           '| File | title | book lines | old-text lines | with Amharic | old passages added into book lines |',
           '|---|---|---|---|---|---|']
    sections.pop(33, None)  # the printed preface (መቅድም) is not shipped
    for s in sorted(sections):
        items = sections[s]
        out = []
        for n, it in enumerate(items):
            meta = it.get('_meta') or {'schemaVersion': 1, 'source': 'EOTC traditional liturgy', 'language': 'gez-am'}
            row = {'sortOder': n, 'text': it['text']}
            if it['amh']:
                row['amh'] = it['amh']
            row['title'] = it['title']
            row['turn'] = it['turn']
            for k2, v in it.items():
                if not k2.startswith('_') and k2 not in ('text', 'amh', 'title', 'turn'):
                    row[k2] = v
            row['metadata'] = meta
            out.append(row)
        if s <= 24:
            title_line = re.search(r' \* Title:.*', old_meta[s][0]).group(0)
            t = re.search(r'Title:\s*(.*?)\s*—\s*Book', old_meta[s][0]).group(1)
        else:
            t, en = NEW_SECTIONS[s]
            t = f'ሰዓታት — {t}'
            title_line = f' * Title:      {t} — Book of Hours (Seatat) — {en}'
        body = header_for(title_line) + json.dumps(out, ensure_ascii=False, indent=2) + '\n'
        (OUT / f'book_of_hours_{s:02d}.json').write_text(body, encoding='utf-8')
        nb = sum(1 for x in items if x['_src'] == 'book')
        filled = sum(len(x['_meta'].get('filledFromOldText', [])) for x in items if x.get('_meta'))
        rep.append(f'| {s} | {t} | {nb} | {len(items) - nb} | {sum(1 for x in items if x["amh"])} | {filled} |')
    pc = Counter(g['pairing'] for g in groups if g['pairing'] != 'geez-only')
    rep.append("\nPairing of Ge'ez with Amharic (groups): " + ", ".join(f"{k}: {v}" for k, v in pc.most_common()))
    (OUT / 'REPORT.md').write_text('\n'.join(rep) + '\n', encoding='utf-8')
    print('\n'.join(rep))


if __name__ == '__main__':
    main()
