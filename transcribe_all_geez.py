"""
Comprehensive Ge'ez Gospel of Matthew Transcription Pipeline
============================================================
Processes all 69 pages of matthewos.pdf:
- Crops left column (Ge'ez only) with exact pixel precision
- Excludes headers, footers, Amharic column, and column borders
- Runs Tesseract 5.4.0 with high-precision 'amh_best' model at 300 DPI
- Performs intelligent cleanup of OCR margin artifacts
- Generates:
    1. Geez_Matthew_Gospel_Complete.docx (Full Master Word Document)
    2. Geez_Matthew_Gospel_Complete.txt  (Full Master Text File)
    3. Pages_Docx/Geez_Matthew_Page_XXX.docx (Individual Page Word Files)
"""

import os
import sys
import time
import re
import subprocess
import pymupdf
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

PDF_PATH = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\matthewos.pdf"
TESSERACT_EXE = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tesseract.exe"
TESSDATA_DIR = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tessdata"

OUTPUT_DIR = r"C:\Users\Abraham.sisay\Documents\Kidase"
PAGES_DOCX_DIR = os.path.join(OUTPUT_DIR, "Pages_Docx")
SCRATCH_DIR = r"C:\Users\Abraham.sisay\.gemini\antigravity-ide\brain\e26cdabe-af62-4d68-8170-94db7d0ea027\scratch\ocr_all"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PAGES_DOCX_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

sys.stdout.reconfigure(encoding='utf-8')


def clean_ocr_line(line):
    """Clean common OCR edge artifacts while preserving authentic Ge'ez characters."""
    line = line.strip()
    if not line:
        return ""
    
    # Strip common column boundary lines captured at the edge
    line = re.sub(r'[\|\]\[]{1,3}$', '', line).strip()
    line = re.sub(r'^[\|\]\[]{1,3}', '', line).strip()
    
    # If the line only contains noise or single punctuation, drop it
    if len(line) <= 2 and not any('\u1200' <= c <= '\u137F' for c in line):
        return ""
    
    return line


def post_process_page_text(raw_text):
    """Process lines of a page, keeping meaningful text and verse layout."""
    lines = raw_text.splitlines()
    cleaned = []
    for l in lines:
        c = clean_ocr_line(l)
        if c:
            cleaned.append(c)
    return cleaned


def add_page_to_doc(doc, page_num, lines, is_first=False):
    """Add a transcribed page to python-docx Document with professional styling."""
    if not is_first:
        doc.add_page_break()
    
    # Page Header marker
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_h = p_header.add_run(f"ገጽ {page_num}  |  Page {page_num}")
    run_h.font.size = Pt(9)
    run_h.font.color.rgb = RGBColor(128, 128, 128)
    run_h.font.name = "Nyala"
    
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        
        # Check if line is Chapter heading (e.g. ምዕራፍ ...)
        if "ምዕራፍ" in line:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line)
            run.font.bold = True
            run.font.size = Pt(14)
            run.font.name = "Nyala"
            run.font.color.rgb = RGBColor(140, 20, 20) # Traditional church burgundy/red
        # Check if line is Part heading (e.g. ክፍል ...)
        elif "ክፍል" in line:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line)
            run.font.bold = True
            run.font.size = Pt(12)
            run.font.name = "Nyala"
            run.font.color.rgb = RGBColor(180, 40, 40)
        # Check if line is title on Page 1
        elif "ወንጌል ቅዱስ" in line or "ብሥራተ ማቴዎስ" in line:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line)
            run.font.bold = True
            run.font.size = Pt(13)
            run.font.name = "Nyala"
            run.font.color.rgb = RGBColor(140, 20, 20)
        else:
            # Regular Bible verse text
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(line)
            run.font.size = Pt(11)
            run.font.name = "Nyala"


def main():
    print(f"Opening PDF: {PDF_PATH}")
    pdf_doc = pymupdf.open(PDF_PATH)
    total_pages = len(pdf_doc)
    print(f"Total pages to transcribe: {total_pages}")
    
    master_doc = docx.Document()
    
    # Configure document margins (1 inch)
    sections = master_doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
    
    # Document Title Page / Header
    title_p = master_doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(10)
    trun = title_p.add_run("ወንጌል ቅዱስ ዘማቴዎስ\n(ግዕዝ)")
    trun.font.bold = True
    trun.font.size = Pt(22)
    trun.font.color.rgb = RGBColor(140, 20, 20)
    trun.font.name = "Nyala"
    
    sub_p = master_doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(25)
    srun = sub_p.add_run("The Holy Gospel of Matthew — Classical Ge'ez Text\nHigh-Precision Complete Transcription (69 Pages)")
    srun.font.size = Pt(11)
    srun.font.color.rgb = RGBColor(80, 80, 80)
    
    all_pages_text = []
    start_time = time.time()
    
    for page_idx in range(total_pages):
        page_num = page_idx + 1
        p_t0 = time.time()
        page = pdf_doc[page_idx]
        
        # Crop coordinates:
        # Page 1: exclude top church title & logo banner (start at y=145)
        # Pages 2-69: start at y=104 (right below running header)
        # Stop at y=750 (before website footer at y=755)
        # x: 38 to 283 (Ge'ez column only, excluding right column & divider)
        y0 = 145 if page_idx == 0 else 104
        clip = pymupdf.Rect(38, y0, 283, 750)
        
        # High resolution 300 DPI rendering
        mat = pymupdf.Matrix(300 / 72, 300 / 72)
        pix = page.get_pixmap(matrix=mat, clip=clip)
        
        img_path = os.path.join(SCRATCH_DIR, f"page_{page_num:03d}.png")
        out_base = os.path.join(SCRATCH_DIR, f"ocr_{page_num:03d}")
        pix.save(img_path)
        
        # Run Tesseract 5.4.0 with amh_best model
        cmd = [
            TESSERACT_EXE,
            img_path,
            out_base,
            "-l", "amh_best",
            "--tessdata-dir", TESSDATA_DIR,
            "--psm", "6"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"Error on page {page_num}: {res.stderr.decode('utf-8', errors='ignore')}")
            continue
        
        txt_path = out_base + ".txt"
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        cleaned_lines = post_process_page_text(raw_text)
        
        # Add to master text
        page_block = f"--- ገጽ {page_num} ---\n" + "\n".join(cleaned_lines)
        all_pages_text.append(page_block)
        
        # Add to master Word document
        add_page_to_doc(master_doc, page_num, cleaned_lines, is_first=(page_idx == 0))
        
        # Create individual page Word document
        indiv_doc = docx.Document()
        for s in indiv_doc.sections:
            s.top_margin = Inches(0.8)
            s.bottom_margin = Inches(0.8)
            s.left_margin = Inches(0.9)
            s.right_margin = Inches(0.9)
        add_page_to_doc(indiv_doc, page_num, cleaned_lines, is_first=True)
        indiv_docx_path = os.path.join(PAGES_DOCX_DIR, f"Geez_Matthew_Page_{page_num:03d}.docx")
        indiv_doc.save(indiv_docx_path)
        
        elapsed = time.time() - start_time
        page_time = time.time() - p_t0
        print(f"[{page_num:02d}/{total_pages}] Transcribed {len(cleaned_lines)} lines ({page_time:.1f}s) | Total: {elapsed:.1f}s")
    
    pdf_doc.close()
    
    # Save Master Word Document
    master_docx_path = os.path.join(OUTPUT_DIR, "Geez_Matthew_Gospel_Complete.docx")
    master_doc.save(master_docx_path)
    print(f"\n Master Word Document saved: {master_docx_path}")
    
    # Save Master Plain Text
    master_txt_path = os.path.join(OUTPUT_DIR, "Geez_Matthew_Gospel_Complete.txt")
    with open(master_txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_pages_text))
    print(f" Master Plain Text saved: {master_txt_path}")
    
    total_elapsed = time.time() - start_time
    print(f"\n All {total_pages} pages successfully transcribed in {total_elapsed:.1f} seconds ({total_elapsed/60:.1f} minutes)!")


if __name__ == "__main__":
    main()
