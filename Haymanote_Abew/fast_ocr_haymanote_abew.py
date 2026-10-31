import os
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import pymupdf
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Reconfigure stdout for UTF-8 in Windows console
sys.stdout.reconfigure(encoding='utf-8')

PDF_PATH = r"C:\Users\Abraham.sisay\Documents\Haymanote Abew\Haymanote Abew OCR\02haimanoteabewu.pdf"
OUTPUT_DIR = r"C:\Users\Abraham.sisay\Documents\Haymanote Abew\Haymanote Abew OCR"
PAGES_TXT_DIR = os.path.join(OUTPUT_DIR, "pages_text")
SCRATCH_DIR = r"C:\Users\Abraham.sisay\.gemini\antigravity-ide\brain\1d76463d-dbad-4ca2-a97f-10d34c7336d4\scratch\ocr_haymanote"

TESSERACT_EXE = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tesseract.exe"
TESSDATA_DIR = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tessdata"
MAX_WORKERS = 8

os.makedirs(PAGES_TXT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)


def process_page(page_idx):
    """Worker function: extracts image and runs Tesseract OCR."""
    page_num = page_idx + 1
    t0 = time.time()
    
    try:
        doc = pymupdf.open(PDF_PATH)
        page = doc[page_idx]
        images = page.get_images()
        if not images:
            pix = page.get_pixmap(dpi=200)
            img_path = os.path.join(SCRATCH_DIR, f"page_{page_num:03d}.png")
            pix.save(img_path)
        else:
            xref = images[0][0]
            base_img = doc.extract_image(xref)
            img_path = os.path.join(SCRATCH_DIR, f"page_{page_num:03d}.png")
            with open(img_path, "wb") as f:
                f.write(base_img["image"])
        doc.close()
        
        out_base = os.path.join(SCRATCH_DIR, f"ocr_{page_num:03d}")
        cmd = [
            TESSERACT_EXE,
            img_path,
            out_base,
            "-l", "amh_best",
            "--tessdata-dir", TESSDATA_DIR
        ]
        
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        txt_path = out_base + ".txt"
        
        text = ""
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
        
        # Save individual page text file
        page_txt_file = os.path.join(PAGES_TXT_DIR, f"page_{page_num:03d}.txt")
        with open(page_txt_file, "w", encoding="utf-8") as pf:
            pf.write(text)
        
        elapsed = time.time() - t0
        return page_idx, text, elapsed, None
    except Exception as e:
        return page_idx, "", 0, str(e)


def main():
    print(f"=== Fast Multi-Threaded OCR Pipeline ===")
    print(f"Input PDF: {PDF_PATH}")
    print(f"Tesseract: {TESSERACT_EXE}")
    print(f"Language: amh_best")
    print(f"Parallel Workers: {MAX_WORKERS}")
    
    doc = pymupdf.open(PDF_PATH)
    total_pages = len(doc)
    doc.close()
    
    print(f"Total pages to process: {total_pages}")
    start_time = time.time()
    
    results = [None] * total_pages
    completed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_page, idx): idx for idx in range(total_pages)}
        
        for future in as_completed(futures):
            page_idx, text, elapsed, err = future.result()
            completed_count += 1
            page_num = page_idx + 1
            if err:
                print(f"[{completed_count:02d}/{total_pages}] Page {page_num:03d} FAILED: {err}")
            else:
                char_count = len(text.strip())
                print(f"[{completed_count:02d}/{total_pages}] Page {page_num:03d} done in {elapsed:.1f}s ({char_count} chars)")
            results[page_idx] = text
    
    total_ocr_time = time.time() - start_time
    print(f"\nAll {total_pages} pages OCR completed in {total_ocr_time:.1f} seconds! (Avg: {total_ocr_time/total_pages:.2f}s/page)")
    
    # 1. Generate Combined Text File
    complete_txt_path = os.path.join(OUTPUT_DIR, "02haimanoteabewu_complete.txt")
    with open(complete_txt_path, "w", encoding="utf-8") as f:
        for idx, text in enumerate(results):
            f.write(f"\n{'='*50}\n")
            f.write(f"ገጽ {idx+1}  |  Page {idx+1}\n")
            f.write(f"{'='*50}\n\n")
            f.write(text.strip() + "\n")
    print(f"Saved complete text: {complete_txt_path}")
    
    # 2. Generate Combined Markdown File
    complete_md_path = os.path.join(OUTPUT_DIR, "02haimanoteabewu_complete.md")
    with open(complete_md_path, "w", encoding="utf-8") as f:
        f.write("# ሃይማኖተ አበው (ክፍል ፪)\n\n")
        f.write(f"*OCR Transcription generated from `02haimanoteabewu.pdf` ({total_pages} pages)*\n\n---\n\n")
        for idx, text in enumerate(results):
            f.write(f"## ገጽ {idx+1} (Page {idx+1})\n\n")
            f.write(text.strip() + "\n\n---\n\n")
    print(f"Saved complete Markdown: {complete_md_path}")
    
    # 3. Generate Formatted Word Document (.docx)
    complete_docx_path = os.path.join(OUTPUT_DIR, "02haimanoteabewu_complete.docx")
    word_doc = docx.Document()
    
    # Set standard margins (0.8 inch)
    for section in word_doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    title_p = word_doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(16)
    title_p.paragraph_format.space_after = Pt(8)
    run_t = title_p.add_run("ሃይማኖተ አበው — ክፍል ፪")
    run_t.font.name = "Nyala"
    run_t.font.size = Pt(22)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(140, 20, 20)
    
    sub_p = word_doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(20)
    run_sub = sub_p.add_run(f"Complete High-Precision Transcription ({total_pages} Pages)")
    run_sub.font.name = "Nyala"
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(100, 100, 100)
    
    for idx, text in enumerate(results):
        if idx > 0:
            word_doc.add_page_break()
            
        p_hdr = word_doc.add_paragraph()
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run(f"ገጽ {idx+1}  |  Page {idx+1}")
        r_hdr.font.name = "Nyala"
        r_hdr.font.size = Pt(9)
        r_hdr.font.color.rgb = RGBColor(128, 128, 128)
        
        for line in text.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            p = word_doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            
            run = p.add_run(line_str)
            run.font.name = "Nyala"
            if "ምዕራፍ" in line_str or "አርእስት" in line_str or "ሃይማኖተ ፤ አበው" in line_str:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.bold = True
                run.font.size = Pt(13)
                run.font.color.rgb = RGBColor(140, 20, 20)
            else:
                run.font.size = Pt(11)
                
    word_doc.save(complete_docx_path)
    print(f"Saved complete Word document: {complete_docx_path}")
    print("=== Pipeline Complete! ===")

if __name__ == "__main__":
    main()
