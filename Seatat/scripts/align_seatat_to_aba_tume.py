"""Proposes the Aba Tume Lisan spelling for the existing Se'atat sections (1-24).

    python scripts/align_seatat_to_aba_tume.py "<path to .docx>" [--out DIR] [--all]

It never touches the section files: with --out it writes the proposed files and
a review list (replacements.md) into DIR; without it it only prints totals.

Each app sentence is matched to its closest docx sentence (>= 0.85 similar,
similar length) and compared word by word.
  * Default: only spelling variants (ሠ/ሰ, ሐ/ኀ/ሀ, ዐ/አ, ፀ/ጸ, ኲ/ኵ ...) take
    the docx form. Every other difference keeps the app word and is listed as
    "decide" for a reader of the printed book.
  * --all also takes different words, provided every docx word already occurs
    in the app (a word the app never used is more likely a typo of the typed
    copy than a better reading).
  * Docx abbreviations ("ቅ.", "ለዓ.") never come over. Words are never deleted.
"""
import collections
import difflib
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_seatat_additions as b  # noqa: E402

ROOT = b.ROOT
ETH = re.compile(r'[\u1200-\u135A]+')
SPLIT = re.compile(r'[^።]+።?\s*')


def fam(c):
    o = ord(c)
    if o == 0x12B2:  # ኲ is written for ኵ
        return chr(0x12B5)
    for s, t in ((0x1220, 0x1230), (0x1210, 0x1200), (0x1280, 0x1200),
                 (0x1300, 0x12A0), (0x1340, 0x1338)):
        if s <= o < s + 8:
            return chr(t + o - s)
    return c


def fold(s):
    return ' '.join(ETH.findall(''.join(fam(c) for c in s)))


def letters(tok):
    return ''.join(ETH.findall(tok))


def load(path):
    raw = open(path, encoding='utf8').read()
    m = re.match(r'\s*/\*.*?\*/\s*', raw, flags=re.S)
    return (m.group(0) if m else ''), json.loads(raw[m.end() if m else 0:])


def docx_sentences(docx):
    out = []
    for para in b.paragraphs(docx)[176:]:
        para = b.ROLE.sub(' ', para)
        for s in SPLIT.findall(para):
            s = re.sub(r'\s+', ' ', s).strip()
            if len(ETH.findall(s)) >= 3 and re.search(r'[\u1200-\u135A]', s):
                out.append(s)
    return out


def main():
    docx = sys.argv[1]
    out_dir = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    write = out_dir is not None
    take_all = '--all' in sys.argv
    if write:
        os.makedirs(out_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(ROOT, 'unencrypted_data/liturgy/book_of_hours_[0-2][0-9].json')))
    files = [f for f in files if int(f[-7:-5]) <= 24]
    data = {f: load(f) for f in files}
    vocab = collections.Counter()
    for _, rows in data.values():
        for r in rows:
            vocab.update(ETH.findall(r['text']))

    vfold = {fold(w) for w in vocab}
    dsent = docx_sentences(docx)
    dfold = [fold(s) for s in dsent]
    index = collections.defaultdict(set)
    for i, f in enumerate(dfold):
        for w in set(f.split()):
            index[w].add(i)

    def best(sent):
        f = fold(sent)
        ws = set(f.split())
        votes = collections.Counter()
        for w in ws:
            if len(index.get(w, ())) < 400:
                votes.update(index[w])
        top = [i for i, _ in votes.most_common(15)]
        pick, score = None, 0.85
        for i in top:
            if not 0.85 <= len(dfold[i]) / max(1, len(f)) <= 1.18:
                continue
            r = difflib.SequenceMatcher(None, f, dfold[i]).ratio()
            if r > score:
                pick, score = i, r
        return pick

    report = ['# Se\'atat: replacements from the Aba Tume Lisan docx\n',
              'Each line: app wording -> docx wording. "kept" = a docx word the '
              'app has never used replaced one app word, so the app word stayed.\n']
    total = changed = kept = 0
    for f, (head, rows) in data.items():
        sec = f[-7:-5]
        sec_changes = 0
        report.append(f'\n## Section {sec}\n')
        for row in rows:
            new_parts = []
            for sent in SPLIT.findall(row['text']):
                total += 1
                end = sent[len(sent.rstrip()):]
                core = sent.strip()
                term = '።' if core.endswith('።') else ''
                core = core.rstrip('።').strip()
                i = best(core) if len(ETH.findall(core)) >= 3 else None
                if i is None:
                    new_parts.append(sent)
                    continue
                dcore = dsent[i].rstrip('።').strip()
                at, dt = core.split(), dcore.split()
                ak = [letters(t) for t in at]
                dk = [letters(t) for t in dt]
                out = []
                sm = difflib.SequenceMatcher(None, ak, dk, autojunk=False)
                for op, a1, a2, d1, d2 in sm.get_opcodes():
                    if op == 'equal' or op == 'delete':
                        out += at[a1:a2]
                    elif op == 'insert':
                        ok = (take_all and 0 < a1 < len(ak) and d2 - d1 == 1
                              and vocab[dk[d1]] and '.' not in dt[d1])
                        out += dt[d1:d2] if ok else []
                    else:
                        variant = (a2 - a1 == d2 - d1 and all(
                            fold(x) == fold(y)
                            for x, y in zip(ak[a1:a2], dk[d1:d2])))
                        abbrev = any('.' in t for t in dt[d1:d2])
                        known = all(vocab[w] or fold(w) in vfold for w in dk[d1:d2])
                        if variant and not abbrev:
                            out += dt[d1:d2]
                        elif take_all and known and not abbrev:
                            out += dt[d1:d2]
                        else:
                            out += at[a1:a2]
                            if not abbrev:
                                kept += 1
                                report.append(
                                    f'- decide `{" ".join(at[a1:a2])}` / docx `{" ".join(dt[d1:d2])}`')
                new = ' '.join(out) + term + end
                if new.strip() != sent.strip():
                    changed += 1
                    sec_changes += 1
                    report.append(f'- {sent.strip()}\n  -> {new.strip()}')
                new_parts.append(new)
            row['text'] = ''.join(new_parts).strip()
        report.append(f'\n{sec_changes} sentences changed in section {sec}\n')
        if write and sec_changes:
            note = ' * Revision:   Wording aligned to the Aba Tume Lisan edition (typed copy);\n *             see research/seatat_aba_tume_replacements.md.\n'
            if 'Revision:' not in head:
                head = head.replace(' * Note:', note + ' * Note:')
            with open(os.path.join(out_dir, os.path.basename(f)), 'w',
                      encoding='utf8', newline='\n') as fh:
                fh.write(head)
                json.dump(rows, fh, ensure_ascii=False, indent=2)
                fh.write('\n')
    print(f'sentences {total}, changed {changed}, kept-app-word {kept}, write={write}')
    if write:
        with open(os.path.join(out_dir, 'replacements.md'), 'w', encoding='utf8', newline='\n') as fh:
            fh.write('\n'.join(report))


main()
