"""Builds the Se'atat sections the app lacked from the Aba Tume Lisan docx.

    python scripts/build_seatat_additions.py "<path to .docx>"

Writes unencrypted_data/liturgy/book_of_hours_25..31.json (plain, with the
notice header every file there carries) and research/seatat_aba_tume_review.md
(words the app has never used, for a proofreader). Encrypt the plain files
into assets/liturgy/ afterwards (see the end of this file's output).

The Ge'ez is copied as typed: tags and stray spacing are removed, nothing is
respelled. Spelling and typo decisions belong to a reader of the printed book.
"""
import glob
import html
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = ("Mets'hafe Se'atat, edition of Aba Tume Lisan "
          "(Debre Abay tradition); typed copy supplied by the Church fathers")

# (file number, Ge'ez title, English title, docx paragraph indexes, rubric?)
SECTIONS = [
    (25, 'መልክዐ ቍርባን', 'Melke\'a Qurban', [260], False),
    (26, 'ሠራዊት ዘ፲ወ፬ ቅዳሴያት', 'Serawit of the 14 Anaphoras', range(261, 269), False),
    (27, 'ሰቆቃወ ድንግል', 'Lamentation of the Virgin', [270], False),
    (28, 'ፍትሐት ዘወልድ', 'Absolution of the Son', [271], False),
    (29, 'በእንተ ብፁዕ ወቅዱስ', 'For the Holy Patriarch', [272], False),
    (30, 'ሥርዓተ ቡራኬ ወዕማሬ ወዑደት', 'Order of Blessing, Bowing and Procession',
     [273, 274, 275, 276, 277, 278, 279, 280, 281, 282], True),
    (31, 'ዘሙታን', 'For the Departed', [256], False),
    (32, 'መቅድመ ተአምር', 'Preface to the Miracle', range(221, 229), False),
]

ROLE = re.compile(r'(?<![ሀ-ፚ])(ይ\.ካ|ይ\.ዲ|ይ\.ሕ)\.?(?=\s)')
HEAD = re.compile(r'^((?:ዘ|ሠራዊት ዘ)[^።፦]{1,40}?)\s*[።፦]\s*')
MAX = 650


def paragraphs(docx):
    root = ET.fromstring(zipfile.ZipFile(docx).read('word/document.xml'))
    out = []
    for p in root.iter(NS + 'p'):
        t = ''.join(
            (e.text or '') if e.tag == NS + 't' else ' '
            for e in p.iter() if e.tag in (NS + 't', NS + 'tab'))
        t = html.unescape(re.sub(r'<[^>]*>', ' ', t))
        out.append(re.sub(r'\s+', ' ', t).strip())
    return out


def words(s):
    return re.findall(r'[ሀ-ፚ]+', s)


def pieces(text):
    """Splits long text at sentence ends into chunks of at most MAX chars."""
    if len(text) <= MAX:
        return [text]
    out, cur = [], ''
    for s in re.split(r'(?<=።)\s*', text):
        if cur and len(cur) + len(s) > MAX:
            out.append(cur.strip())
            cur = ''
        cur += s + ' '
    if cur.strip():
        out.append(cur.strip())
    return out


def entries(paras, rubric):
    out = []
    for para in paras:
        if not para:
            continue
        marks = list(ROLE.finditer(para))
        chunks = []
        if not marks:
            chunks.append(('', para))
        else:
            if marks[0].start() > 0 and para[:marks[0].start()].strip():
                chunks.append(('', para[:marks[0].start()].strip()))
            for i, m in enumerate(marks):
                end = marks[i + 1].start() if i + 1 < len(marks) else len(para)
                chunks.append((m.group(1) + '.', para[m.end():end].strip()))
        for turn, text in chunks:
            title = None
            h = HEAD.match(text)
            if h and not rubric:
                title, text = h.group(1).strip(), text[h.end():]
            for k, piece in enumerate(pieces(text)):
                if not piece:
                    continue
                out.append({
                    'text': piece,
                    'title': title if (title and k == 0) else ' '.join(words(piece)[:4]),
                    'turn': ('ሥርዓት' if rubric else turn) if k == 0 else '',
                })
    return out


def header(num, title, en):
    return (
        '/*\n'
        f' * Title:      ሰዓታት — {title} — Book of Hours (Seatat) — {en}\n'
        ' * Language:   Ge\'ez' + (' with Amharic rubrics' if num == 30 else '') + '\n'
        f' * Source:     {SOURCE}.\n'
        ' * Status:     Added from a typed copy; spelling not yet proofread\n'
        ' *             against the printed book.\n'
        ' * Note:       This notice is metadata only and is never shown in the app.\n'
        ' */\n')


def known_words():
    seen = set()
    for f in glob.glob(os.path.join(ROOT, 'unencrypted_data/liturgy/book_of_hours_[0-2][0-9].json')):
        if int(f[-7:-5]) > 24:
            continue
        seen.update(words(open(f, encoding='utf8').read()))
    return seen


def main():
    docx = sys.argv[1]
    paras = paragraphs(docx)
    known = known_words()
    review = ["# Se'atat additions: words the app has not used before\n",
              'Proofread against the printed book. Not shipped.\n']
    for num, title, en, idx, rubric in SECTIONS:
        data = []
        for e in entries([paras[i] for i in idx], rubric):
            data.append({
                'sortOder': len(data),
                'text': e['text'],
                'title': e['title'],
                'turn': e['turn'],
                'metadata': {
                    'schemaVersion': 1,
                    'source': "Mets'hafe Se'atat (Aba Tume Lisan edition)",
                    'language': 'gez-am' if rubric else 'gez',
                },
            })
        path = os.path.join(ROOT, f'unencrypted_data/liturgy/book_of_hours_{num}.json')
        with open(path, 'w', encoding='utf8', newline='\n') as f:
            f.write(header(num, title, en))
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
        unk = sorted({w for e in data for w in words(e['text'])} - known)
        review.append(f'\n## {num} {title} ({len(data)} entries, {len(unk)} unseen words)\n')
        review.append(' '.join(unk) + '\n')
        print(num, title, len(data), 'entries', len(unk), 'unseen words')
    os.makedirs(os.path.join(ROOT, 'research'), exist_ok=True)
    with open(os.path.join(ROOT, 'research/seatat_aba_tume_review.md'), 'w',
              encoding='utf8', newline='\n') as f:
        f.write('\n'.join(review))


if __name__ == '__main__':
    main()
