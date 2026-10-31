import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import argparse
import pymupdf
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

PDF_PATH = r'C:\Users\Abraham.sisay\Documents\Sinkisar\zewerha tikemet.pdf'
DOCX_PATH = r'C:\Users\Abraham.sisay\Documents\Sinkisar\Sinkisar_Tikimt.docx'
VERIFIED_DOCX_PATH = r'C:\Users\Abraham.sisay\Documents\Sinkisar\Sinkisar_Tikimt_Verified.docx'
BASE_DIR = r'C:\Users\Abraham.sisay\Documents\Sinkisar'
IMAGES_DIR = os.path.join(BASE_DIR, 'page_images')
PAGES_DATA_DIR = os.path.join(BASE_DIR, 'pages_data')
VERIFIED_DATA_DIR = os.path.join(BASE_DIR, 'verified_data')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(PAGES_DATA_DIR, exist_ok=True)
os.makedirs(VERIFIED_DATA_DIR, exist_ok=True)

def render_page(page_num, dpi=150):
    pdf_idx = page_num - 1
    doc = pymupdf.open(PDF_PATH)
    if pdf_idx < 0 or pdf_idx >= len(doc):
        print(f"Error: Page {page_num} out of range (1-{len(doc)})")
        return None
    page = doc[pdf_idx]
    pix = page.get_pixmap(dpi=dpi)
    out_path = os.path.join(IMAGES_DIR, f"page_{page_num:03d}.png")
    pix.save(out_path)
    print(f"Rendered Page {page_num} (PDF index {pdf_idx}) -> {out_path}")
    return out_path

def render_all(dpi=150):
    doc = pymupdf.open(PDF_PATH)
    total = len(doc)
    print(f"Rendering all {total} pages at {dpi} DPI...")
    for i in range(total):
        page_num = i + 1
        out_path = os.path.join(IMAGES_DIR, f"page_{page_num:03d}.png")
        if not os.path.exists(out_path):
            pix = doc[i].get_pixmap(dpi=dpi)
            pix.save(out_path)
            if page_num % 10 == 0 or page_num == total:
                print(f"Rendered {page_num}/{total} pages...")
    print("All pages rendered successfully.")

def extract_docx_pages():
    doc = docx.Document(DOCX_PATH)
    pages = {}
    current_page = None
    current_lang = None

    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        m = re.match(r'— ገጽ (\d+) \((ግዕዝ|አማርኛ)\).*—', txt)
        if m:
            current_page = int(m.group(1))
            current_lang = 'geez' if 'ግዕዝ' in m.group(2) else 'amharic'
            if current_page not in pages:
                pages[current_page] = {
                    'page_num': current_page,
                    'pdf_index': current_page - 1,
                    'geez': [],
                    'amharic': [],
                    'status': 'pending'
                }
        elif current_page is not None and current_lang is not None:
            pages[current_page][current_lang].append(txt)

    for p_num, p_data in pages.items():
        out_file = os.path.join(PAGES_DATA_DIR, f"page_{p_num:03d}.json")
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(p_data, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(pages)} pages into {PAGES_DATA_DIR}")

def get_page(page_num):
    data_file = os.path.join(VERIFIED_DATA_DIR, f"page_{page_num:03d}.json")
    if not os.path.exists(data_file):
        data_file = os.path.join(PAGES_DATA_DIR, f"page_{page_num:03d}.json")
    if not os.path.exists(data_file):
        print(f"Page {page_num} data not found. Run extract first.")
        return
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"=== PAGE {page_num} [{data.get('status', 'pending').upper()}] ===")
    print("\n--- ግዕዝ (Ge'ez) ---")
    for i, p in enumerate(data.get('geez', [])):
        print(f"[{i+1}] {p}")
    print("\n--- አማርኛ (Amharic) ---")
    for i, p in enumerate(data.get('amharic', [])):
        print(f"[{i+1}] {p}")

def save_verified_page(page_num, geez_lines, amharic_lines, notes=""):
    data = {
        'page_num': page_num,
        'pdf_index': page_num - 1,
        'geez': geez_lines,
        'amharic': amharic_lines,
        'status': 'verified',
        'notes': notes
    }
    out_file = os.path.join(VERIFIED_DATA_DIR, f"page_{page_num:03d}.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved verified Page {page_num} -> {out_file}")

def get_status():
    doc = pymupdf.open(PDF_PATH)
    total_pages = len(doc)
    verified_count = 0
    pending_count = 0

    for i in range(1, total_pages + 1):
        v_file = os.path.join(VERIFIED_DATA_DIR, f"page_{i:03d}.json")
        if os.path.exists(v_file):
            verified_count += 1
        else:
            pending_count += 1

    print(f"Total Pages: {total_pages}")
    print(f"Verified:    {verified_count} ({(verified_count/total_pages)*100:.1f}%)")
    print(f"Pending:     {pending_count}")

def assemble_verified_docx():
    doc = pymupdf.open(PDF_PATH)
    total_pages = len(doc)
    out_doc = docx.Document()

    title_p = out_doc.add_paragraph()
    title_run = title_p.add_run("መጽሐፈ ስንክሳር ዘወርኃ ጥቅምት")
    title_run.bold = True
    title_run.font.size = Pt(20)
    title_run.font.name = "Nyala"
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub_p = out_doc.add_paragraph()
    sub_run = sub_p.add_run("ከጥቅምት ፩ እስከ ጥቅምት ፴ (ሙሉ ወር - የተረጋገጠና የተስተካከለ ቅጂ)")
    sub_run.font.size = Pt(14)
    sub_run.font.name = "Nyala"
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    out_doc.add_page_break()

    for p_num in range(1, total_pages + 1):
        v_file = os.path.join(VERIFIED_DATA_DIR, f"page_{p_num:03d}.json")
        p_file = os.path.join(PAGES_DATA_DIR, f"page_{p_num:03d}.json")
        data = None
        is_verified = False

        if os.path.exists(v_file):
            with open(v_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            is_verified = True
        elif os.path.exists(p_file):
            with open(p_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

        if not data:
            continue

        h_geez = out_doc.add_paragraph()
        r_gh = h_geez.add_run(f"— ገጽ {p_num} (ግዕዝ) / Page {p_num} (Ge'ez) —")
        r_gh.bold = True
        r_gh.font.size = Pt(12)
        r_gh.font.color.rgb = RGBColor(128, 0, 0)
        h_geez.alignment = WD_ALIGN_PARAGRAPH.CENTER

        for para in data.get('geez', []):
            p = out_doc.add_paragraph()
            r = p.add_run(para)
            r.font.name = "Nyala"
            r.font.size = Pt(11)

        h_amh = out_doc.add_paragraph()
        r_ah = h_amh.add_run(f"— ገጽ {p_num} (አማርኛ) / Page {p_num} (Amharic) —")
        r_ah.bold = True
        r_ah.font.size = Pt(12)
        r_ah.font.color.rgb = RGBColor(0, 51, 102)
        h_amh.alignment = WD_ALIGN_PARAGRAPH.CENTER

        for para in data.get('amharic', []):
            p = out_doc.add_paragraph()
            r = p.add_run(para)
            r.font.name = "Nyala"
            r.font.size = Pt(11)

        if p_num < total_pages:
            out_doc.add_page_break()

    out_doc.save(VERIFIED_DOCX_PATH)
    print(f"Successfully assembled: {VERIFIED_DOCX_PATH}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sinkisar Page Verification Tool")
    parser.add_argument('action', choices=['render', 'render-all', 'extract', 'get', 'status', 'assemble'])
    parser.add_argument('--page', type=int, help='Page number (1-113)')
    args = parser.parse_args()

    if args.action == 'render':
        if not args.page:
            print("Specify --page <num>")
        else:
            render_page(args.page)
    elif args.action == 'render-all':
        render_all()
    elif args.action == 'extract':
        extract_docx_pages()
    elif args.action == 'get':
        if not args.page:
            print("Specify --page <num>")
        else:
            get_page(args.page)
    elif args.action == 'status':
        get_status()
    elif args.action == 'assemble':
        assemble_verified_docx()

