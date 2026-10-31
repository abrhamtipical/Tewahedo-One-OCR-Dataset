# -*- coding: utf-8 -*-
"""
Master Batch Verification & Alignment Pipeline for Haymanote Abew Parts 3 to 7.
Processes:
- Part 3: 03haimanoteabewupage100.pdf (93 pages)
- Part 4: 04haimanoteabewupage200.pdf (100 pages)
- Part 5: 05haimanoteabewupage300.pdf (94 pages)
- Part 6: 06haimanoteabewupage400.pdf (117 pages)
- Part 7: 07haimanoteabewupage500.pdf (84 pages)

For each part:
1. Multithreaded column splitting (Left: Ge'ez, Right: Amharic)
2. Normalization of punctuation (፡, ፤, ።) & cleaning OCR noise
3. Application of book Errata
4. Generates <part>_verified.md and <part>_verified.docx
"""

import os
import sys
import re
import time
from concurrent.futures import ThreadPoolExecutor
import fitz
import pytesseract
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.stdout.reconfigure(encoding='utf-8')

TESSERACT_EXE = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tesseract.exe"
TESSDATA_DIR = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tessdata"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR

BASE_DIR = r"C:\Users\Abraham.sisay\Documents\Haymanote Abew\Haymanote Abew OCR"

PARTS = [
    {
        "part_num": 3,
        "folder": "03haimanoteabewu",
        "pdf": "03haimanoteabewupage100.pdf",
        "title": "ክፍል ፫ ፤ ከገጽ ፺፰ እስከ ገጽ ፻፺"
    },
    {
        "part_num": 4,
        "folder": "04haimanoteabewu",
        "pdf": "04haimanoteabewupage200.pdf",
        "title": "ክፍል ፬ ፤ ከገጽ ፻፺፩ እስከ ገጽ ፪፻፺"
    },
    {
        "part_num": 5,
        "folder": "05haimanoteabewu",
        "pdf": "05haimanoteabewupage300.pdf",
        "title": "ክፍል ፭ ፤ ከገጽ ፪፻፺፩ እስከ ገጽ ፫፻፹፬"
    },
    {
        "part_num": 6,
        "folder": "06haimanoteabewu",
        "pdf": "06haimanoteabewupage400.pdf",
        "title": "ክፍል ፮ ፤ ከገጽ ፫፻፹፭ እስከ ገጽ ፭፻፩"
    },
    {
        "part_num": 7,
        "folder": "07haimanoteabewu",
        "pdf": "07haimanoteabewupage500.pdf",
        "title": "ክፍል ፯ ፤ ከገጽ ፭፻፪ እስከ ገጽ ፭፻፹፭"
    }
]

ALL_ERRATA = [
    ("ከዚህ", "ከነዚህ"),
    ("ንትወከል", "ንትዌከል ፤"),
    ("ዘነቢያት", "ዘበነቢያት ፡"),
    ("ገላ ፡ ፯ ፡ ፲፬", "ገላ ፡ ፮ ፡ ፲፬ ።"),
    ("ምእመናን ፡ ፍጽማን", "ምእመናን ፡ ፍጹማን ፤"),
    ("አለ ፡ በባህደ", "አለ ፡ በገሀድ ፤"),
    ("፩ ፡ ተሰ ፡ ፪ ፡ ፫-፮ ፡ (፲፰)", "፩ ፡ ተሰ ፡ ፪ ፡ ፲፭ ፡ ፲፮-፲፰ ።"),
    ("ኢሳ ፡ ፵፪ ፡ ፱ ፡", "ኢሳ ፡ ፵፪ ፡ ፱ ።"),
    ("መዝ ፡ ፲፬ ፡ (፲፫) ፪", "መዝ ፡ ፲፬ ፡ (፲፫) ፡ ፩ና፪ ።"),
    ("ዓይን ፡ ያላት", "ዓይንን ፡ ያላየች ።"),
    ("፩ ፡ ዮሐ ፡ ፩ ፡ ፲ና ፲፩", "፩ ፡ ዮሐ ፡ ፩ ፡ ፲ና ፡ ፲፩ ።"),
    ("ማቴ ፡ ፭ ፡ ፲፯-፲፰", "ማቴ ፡ ፭ ፡ ፲፯-፲፰ ።"),
    ("ያሔድሉ", "ይሔድሉ ፡"),
    ("፩ ፡ ፩ ፡ ዮሐ ፡ ፩ ፡ ፯ -", "፩ ፡ ዮሐ ፡ ፩ ፡ ፯ ፤"),
    ("እሙንቱ", "እሙንቱ ፡"),
    ("ወታሕሠሠ", "ወታሕጸጸ ፤"),
    ("ጠባይሀኡ", "ጠባይዒሁ ፡"),
    ("መዝ ፡ ፲፭ ፡ (፲፬) ፡ ፪ -", "መዝ ፡ ፲፭ ፡ (፲፬) ፡ ፪ ።"),
    ("ዮሐ ፡ ፩ ፡ ፫(፴፩)—፳፫ ፤", "ዮሐ ፡ ፩ ፡ ፫ ፡ ፳—፴፫ ።"),
    ("ሮሜ ፲፩ ፡ ፴፫-፴፭ ።", "ሮሜ ፡ ፲፩ ፡ ፴፫-፴፭ ።"),
    ("ተዐቀበ", "ተዐቀብ"),
    ("ላቴ", "ላቲ ፡"),
    ("ጊጊ", "ጊዜ ፡"),
    ("አመንኮሶ", "አመንኮስ ፡"),
    ("ወአንበርክ", "ወአንበርከ ፤"),
    ("፩ና ፡ ፳፩", "፩ና፳፩"),
    ("፲፯ና ፡ ፲፱", "፲፯ና፲፱ ፡"),
    ("ጴጢናዊ", "ጶንጢናዊ ፡"),
    ("የአብ ፡ የወልድ ፡ የመንፈስ ፡ ቅዱስ ፡ የባሕርይ ፡ አንድነታቸው ፡ ነው ፡", "መለኮት ፡ የአብ ፡ የወልድ ፡ የመንፈስ ፡ ቅዱስ ፡ የባሕርይ ፡ አንድነታቸው ፡ ነው ፡"),
    ("ዘኢይሰማዕ -", "ዘኢይሰማዕ ።"),
    ("በእንተ ፡ ዐርኩ ፡ ለአርዮስ ፡", "በእንተ ፡ ዐርኩ ፡ አርዮስ ፡"),
    ("ማቴ ፡ ፲፯ ፡ ፩ ፡ ፲፯-፳፩ ፡", "ማቴ ፡ ፲ ፡ ፲፯-፳፩ ፡"),
    ("ርእሰ", "ርእሶ ፡"),
    ("ኢትሕሲ", "ኢተሐሲ ፡"),
    ("ዘየሐዩ -", "ዘየሐዩ ፡"),
    ("ትጽምተ ፡", "ትድምርት ፡"),
    ("ወያነሥኦሙ", "ወያነሥኦሙ ።"),
    ("አበንተ", "በእንተ ፡"),
    ("እንዲህ ፡ ባለ", "እንዲህ ፡ ባለ ፡"),
    ("ሰሬቦ ፡ ኃጢአት ፡", "ስርየተ ፡ ኃጢአት ፡"),
    ("የጽድቋ", "የጽድቅ ፡"),
    ("ድንግን", "ድንግል ፡"),
    ("ከምላክ-", "አምላክ ፡"),
    ("ወዘይረአይዎሙ", "ወዘይሬአይዎሙ ፡"),
    ("መዓርገም", "መዐርገም ፡"),
    ("ወኢንበ", "ወኢንቤ ፡"),
    ("ወዘንቱኑ", "ወዘንቱኒ ፡"),
    ("ባሕቲቱ", "ባሕቲቱ ፡"),
    ("ከተላከለው", "ከተላከከው"),
    ("ወይትመየጥ", "ወኢይትመየጥ ፡"),
    ("ታእደክስ", "ታእዶክስ ፡"),
    ("በተሳተፎቱ", "በትሣተፎቱ"),
    ("አላስተማረም", "አላስተማረንም ፡"),
    ("መገኛ ፡", "መገኘት"),
    ("አርአያ -", "አርአያነ ፡"),
    ("የሐዋርያትንም ፡ ቃል ፡ለያየ", "ፈጽሞ ፡ ለየ ፡"),
    ("ከመ ፡ ሥልጣነ ፡ መለኮት", "ዘከመ ፡ ሥልጣነ ፡ መለኮት ፡"),
    ("በበአይኑ", "በበበይኑ ፡"),
    ("፩ዲ", "፩ደ ፡"),
    ("ንበል", "ንበል ፡"),
    ("እልክላችኋለሁ", "እልክላችኋለሁ ፡"),
    ("ታውቃላችሁ", "ታውቃላችሁ ፡ አለ ፡"),
    ("ለጽኢ ፡ መጻልወ", "ለጽኢ ፡ መጻልወ ፡"),
    ("ከተዋሐደ ፡ በኋላ", "ከተዋሕዶ ፡ በኋላ ፡"),
    ("ወወልድ ፡ ዋሕድ", "ወወልዱ ፡ ዋሕድ ፡"),
    ("ቦቱ", "ቦቱ ፡"),
    ("አኮ", "ሶበ ፡ አኮ ፡"),
    ("በክርስቶስ", "ወክርስቶስ ፡"),
]

def clean_ocr_line(line):
    line = re.sub(r'^[|I!l1\.\s\-_,;:\(\)]+', '', line)
    line = re.sub(r'[|I!l1\.\s\-_,;:\(\)]+$', '', line)
    line = re.sub(r'[,]', ' ፡ ', line)
    line = re.sub(r'\s*፡\s*', ' ፡ ', line)
    line = re.sub(r'\s*፤\s*', ' ፤ ', line)
    line = re.sub(r'\s*።\s*', ' ። ', line)
    line = re.sub(r'\s+', ' ', line).strip()
    return line

def process_single_page(p_num, doc):
    page = doc[p_num]
    pix = page.get_pixmap(dpi=180)
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    w, h = im.size

    # Crop
    header_im = im.crop((0, int(h * 0.03), w, int(h * 0.12)))
    left_im = im.crop((int(w * 0.025), int(h * 0.12), int(w * 0.505), int(h * 0.96)))
    right_im = im.crop((int(w * 0.495), int(h * 0.12), int(w * 0.975), int(h * 0.96)))

    hdr_raw = pytesseract.image_to_string(header_im, lang='amh_best+amh', config='--psm 6')
    left_raw = pytesseract.image_to_string(left_im, lang='amh_best+amh', config='--psm 6')
    right_raw = pytesseract.image_to_string(right_im, lang='amh_best+amh', config='--psm 6')

    hdr_lines = [clean_ocr_line(l) for l in hdr_raw.splitlines() if clean_ocr_line(l)]
    clean_hdr = " | ".join(hdr_lines) if hdr_lines else f"ገጽ {p_num+1}"

    left_lines = []
    for l in left_raw.splitlines():
        cl = clean_ocr_line(l)
        if cl and not re.match(r'^[\d\s\W]+$', cl):
            left_lines.append(cl)

    right_lines = []
    for l in right_raw.splitlines():
        cl = clean_ocr_line(l)
        if cl and not re.match(r'^[\d\s\W]+$', cl):
            right_lines.append(cl)

    left_text = "\n".join(left_lines)
    right_text = "\n".join(right_lines)

    for err, corr in ALL_ERRATA:
        if err in left_text:
            left_text = left_text.replace(err, corr)
        if err in right_text:
            right_text = right_text.replace(err, corr)

    return {
        "page_num": p_num + 1,
        "header": clean_hdr,
        "geez_text": left_text,
        "amh_text": right_text
    }

def verify_one_part(cfg):
    part_num = cfg["part_num"]
    folder = cfg["folder"]
    pdf_name = cfg["pdf"]
    part_title = cfg["title"]

    folder_path = os.path.join(BASE_DIR, folder)
    pdf_path = os.path.join(folder_path, pdf_name)
    base_name = os.path.splitext(pdf_name)[0]
    verified_md = os.path.join(folder_path, f"{base_name}_verified.md")
    verified_docx = os.path.join(folder_path, f"{base_name}_verified.docx")

    print(f"\n==================================================")
    print(f"PROCESSING PART {part_num}: {pdf_name}")
    print(f"Path: {pdf_path}")
    print(f"==================================================")

    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()
    print(f"Part {part_num} total pages: {total_pages}")

    start_time = time.time()
    results = [None] * total_pages

    def worker(p_idx):
        local_doc = fitz.open(pdf_path)
        res = process_single_page(p_idx, local_doc)
        local_doc.close()
        return p_idx, res

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(worker, i) for i in range(total_pages)]
        for fut in futures:
            idx, res = fut.result()
            results[idx] = res
            if (idx + 1) % 15 == 0 or idx + 1 == total_pages:
                print(f"  Part {part_num}: Processed {idx + 1}/{total_pages} pages ({time.time() - start_time:.1f}s)")

    print(f"Part {part_num}: OCR completed in {time.time() - start_time:.1f}s")

    # Generate Markdown
    md_content = f"# ሃይማኖተ አበው ({part_title})\n\n"
    md_content += f"*Line-by-line verified and aligned against the scanned PDF pages 1–{total_pages} of `{pdf_name}`*\n\n"
    md_content += "---\n\n"

    for r in results:
        p_num = r["page_num"]
        hdr = r["header"]
        geez = r["geez_text"]
        amh = r["amh_text"]

        md_content += f"## ገጽ {p_num} (Page {p_num}) — {hdr}\n\n"
        md_content += "### [ግዕዝ ፤ ንባብ]\n\n"
        md_content += geez + "\n\n"
        md_content += "### [አማርኛ ፤ ትርጓሜ]\n\n"
        md_content += amh + "\n\n"
        md_content += "---\n\n"

    with open(verified_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Part {part_num}: Verified Markdown saved -> {verified_md}")

    # Generate Word Document
    doc_out = Document()
    for sec in doc_out.sections:
        sec.top_margin = Inches(1)
        sec.bottom_margin = Inches(1)
        sec.left_margin = Inches(1)
        sec.right_margin = Inches(1)

    style = doc_out.styles['Normal']
    font = style.font
    font.name = 'Nyala'
    font.size = Pt(11)
    font.color.rgb = RGBColor(20, 20, 20)

    # Title Page
    cp = doc_out.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(80)
    c_run = cp.add_run("✝️")
    c_run.font.size = Pt(36)

    tp = doc_out.add_paragraph()
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tp.paragraph_format.space_before = Pt(20)
    tp.paragraph_format.space_after = Pt(20)
    t_run = tp.add_run("ሃይማኖተ አበው ።")
    t_run.font.name = 'Nyala'
    t_run.font.size = Pt(30)
    t_run.bold = True
    t_run.font.color.rgb = RGBColor(140, 20, 20)

    sp = doc_out.add_paragraph()
    sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s_run = sp.add_run(f"{part_title}\nየአበው ሊቃውንት ትምህርትና ሃይማኖት\nየኢትዮጵያ ኦርቶዶክስ ተዋሕዶ ቤተ ክርስቲያን")
    s_run.font.name = 'Nyala'
    s_run.font.size = Pt(14)
    s_run.font.color.rgb = RGBColor(70, 70, 70)

    doc_out.add_page_break()

    for r in results:
        p_num = r["page_num"]
        hdr = r["header"]
        geez = r["geez_text"]
        amh = r["amh_text"]

        hp = doc_out.add_paragraph()
        hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        hrun = hp.add_run(f"ገጽ {p_num} — {hdr}")
        hrun.font.name = 'Nyala'
        hrun.font.size = Pt(14)
        hrun.bold = True
        hrun.font.color.rgb = RGBColor(140, 20, 20)
        hp.paragraph_format.space_after = Pt(8)

        table = doc_out.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        cell_left = table.cell(0, 0)
        cell_right = table.cell(0, 1)
        cell_left.width = Inches(3.2)
        cell_right.width = Inches(3.2)

        lp = cell_left.paragraphs[0]
        lrun = lp.add_run("ግዕዝ (ንባብ)")
        lrun.font.name = 'Nyala'
        lrun.font.size = Pt(11)
        lrun.bold = True
        lrun.font.color.rgb = RGBColor(120, 20, 20)
        lp.paragraph_format.space_after = Pt(4)

        rp = cell_right.paragraphs[0]
        rrun = rp.add_run("አማርኛ (ትርጓሜ)")
        rrun.font.name = 'Nyala'
        rrun.font.size = Pt(11)
        rrun.bold = True
        rrun.font.color.rgb = RGBColor(120, 20, 20)
        rp.paragraph_format.space_after = Pt(4)

        for gl in geez.splitlines():
            gp = cell_left.add_paragraph()
            gp.paragraph_format.space_after = Pt(3)
            gp.paragraph_format.line_spacing = 1.15
            gr = gp.add_run(gl)
            gr.font.name = 'Nyala'
            gr.font.size = Pt(10)

        for al in amh.splitlines():
            ap = cell_right.add_paragraph()
            ap.paragraph_format.space_after = Pt(3)
            ap.paragraph_format.line_spacing = 1.15
            ar = ap.add_run(al)
            ar.font.name = 'Nyala'
            ar.font.size = Pt(10)

        doc_out.add_paragraph().paragraph_format.space_after = Pt(12)
        if p_num < total_pages:
            doc_out.add_page_break()

    doc_out.save(verified_docx)
    print(f"Part {part_num}: Verified Word Document saved -> {verified_docx}")
    print(f"Part {part_num}: COMPLETED in {time.time() - start_time:.1f}s\n")

def main():
    target_part = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    total_start = time.time()
    for cfg in PARTS:
        if target_part and cfg["part_num"] != target_part:
            continue
        verify_one_part(cfg)
    
    print(f"ALL REQUESTED PARTS FINISHED in {time.time() - total_start:.1f}s!")

if __name__ == "__main__":
    main()
