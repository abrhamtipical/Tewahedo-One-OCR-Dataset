import os
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import pymupdf
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Ensure proper UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Default configurations
TESSERACT_EXE = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tesseract.exe"
TESSDATA_DIR = r"C:\Users\Abraham.sisay\AppData\Local\Tesseract5\tessdata"
DEFAULT_LANG = "amh_best"   # Options: amh_best, amh, eng
MAX_WORKERS = 8             # Number of concurrent CPU worker threads


def get_target_pdf():
    """Determine which PDF to process based on command line arguments or current folder."""
    if len(sys.argv) > 1:
        target = Path(sys.argv[1]).resolve()
        if target.exists() and target.suffix.lower() == ".pdf":
            return target
        else:
            print(f"Error: Provided file '{sys.argv[1]}' does not exist or is not a PDF.")
            sys.exit(1)
            
    # Default: look in current script directory
    script_dir = Path(__file__).parent.resolve()
    pdfs = list(script_dir.glob("*.pdf"))
    if pdfs:
        # If 02haimanoteabewu.pdf exists, prioritize it, else use first found PDF
        haimanote = [p for p in pdfs if "02haimanote" in p.name.lower()]
        return haimanote[0] if haimanote else pdfs[0]
        
    print("No PDF file specified and none found in script directory.")
    print("Usage: python fast_ocr.py <path_to_pdf>")
    sys.exit(1)


def process_page(page_idx, pdf_path, scratch_dir, pages_dir, lang):
    """Worker function: extracts image and runs Tesseract OCR."""
    page_num = page_idx + 1
    t0 = time.time()
    
    try:
        doc = pymupdf.open(str(pdf_path))
        page = doc[page_idx]
        images = page.get_images()
        
        img_path = os.path.join(scratch_dir, f"page_{page_num:03d}.png")
        if not images:
            # Fallback to rendering pixmap at 200 DPI
            pix = page.get_pixmap(dpi=200)
            pix.save(img_path)
        else:
            # Extract raw embedded image
            xref = images[0][0]
            base_img = doc.extract_image(xref)
            with open(img_path, "wb") as f:
                f.write(base_img["image"])
        doc.close()
        
        out_base = os.path.join(scratch_dir, f"ocr_{page_num:03d}")
        cmd = [
            TESSERACT_EXE,
            img_path,
            out_base,
            "-l", lang,
            "--tessdata-dir", TESSDATA_DIR
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        txt_path = out_base + ".txt"
        
        text = ""
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
        
        # Save individual page text file
        page_txt_file = os.path.join(pages_dir, f"page_{page_num:03d}.txt")
        with open(page_txt_file, "w", encoding="utf-8") as pf:
            pf.write(text)
            
        # Clean up temporary page image
        try:
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass
            
        elapsed = time.time() - t0
        return page_idx, text, elapsed, None
    except Exception as e:
        return page_idx, "", 0, str(e)


def main():
    pdf_path = get_target_pdf()
    output_dir = pdf_path.parent
    base_name = pdf_path.stem
    
    pages_txt_dir = os.path.join(output_dir, f"{base_name}_pages_text")
    scratch_dir = os.path.join(output_dir, f"_temp_{base_name}_scratch")
    
    os.makedirs(pages_txt_dir, exist_ok=True)
    os.makedirs(scratch_dir, exist_ok=True)
    
    lang = DEFAULT_LANG
    if len(sys.argv) > 2:
        lang = sys.argv[2]
        
    print(f"==================================================")
    print(f"      Fast Multi-Threaded Tesseract OCR Pipeline   ")
    print(f"==================================================")
    print(f"Target PDF : {pdf_path}")
    print(f"Output Dir : {output_dir}")
    print(f"Language   : {lang}")
    print(f"Workers    : {MAX_WORKERS} parallel threads")
    
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)
    doc.close()
    
    print(f"Total Pages: {total_pages}\n")
    start_time = time.time()
    
    results = [None] * total_pages
    completed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_page, idx, pdf_path, scratch_dir, pages_txt_dir, lang): idx 
            for idx in range(total_pages)
        }
        
        for future in as_completed(futures):
            page_idx, text, elapsed, err = future.result()
            completed_count += 1
            page_num = page_idx + 1
            if err:
                print(f"[{completed_count:03d}/{total_pages:03d}] Page {page_num:03d} FAILED: {err}")
            else:
                char_count = len(text.strip())
                print(f"[{completed_count:03d}/{total_pages:03d}] Page {page_num:03d} done in {elapsed:.1f}s ({char_count} chars)")
            results[page_idx] = text
            
    total_time = time.time() - start_time
    print(f"\nAll {total_pages} pages completed in {total_time:.1f} seconds! (Avg: {total_time/total_pages:.2f}s/page)")
    
    # 1. Complete Text (.txt)
    complete_txt_path = os.path.join(output_dir, f"{base_name}_complete.txt")
    with open(complete_txt_path, "w", encoding="utf-8") as f:
        for idx, text in enumerate(results):
            f.write(f"\n{'='*50}\n")
            f.write(f"ገጽ {idx+1}  |  Page {idx+1}\n")
            f.write(f"{'='*50}\n\n")
            f.write((text or "").strip() + "\n")
    print(f"-> Text file:     {complete_txt_path}")
    
    # 2. Complete Markdown (.md)
    complete_md_path = os.path.join(output_dir, f"{base_name}_complete.md")
    with open(complete_md_path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name}\n\n")
        f.write(f"*OCR Transcription generated from `{pdf_path.name}` ({total_pages} pages)*\n\n---\n\n")
        for idx, text in enumerate(results):
            f.write(f"## ገጽ {idx+1} (Page {idx+1})\n\n")
            f.write((text or "").strip() + "\n\n---\n\n")
    print(f"-> Markdown file: {complete_md_path}")
    
    # 3. Formatted Word Document (.docx)
    complete_docx_path = os.path.join(output_dir, f"{base_name}_complete.docx")
    word_doc = docx.Document()
    
    for section in word_doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    title_p = word_doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(16)
    title_p.paragraph_format.space_after = Pt(8)
    run_t = title_p.add_run(base_name)
    run_t.font.name = "Nyala"
    run_t.font.size = Pt(20)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(140, 20, 20)
    
    sub_p = word_doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(20)
    run_sub = sub_p.add_run(f"High-Precision Transcription ({total_pages} Pages)")
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
        
        for line in (text or "").splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            p = word_doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            
            run = p.add_run(line_str)
            run.font.name = "Nyala"
            if any(k in line_str for k in ["ምዕራፍ", "አርእስት", "ሃይማኖተ ፤ አበው", "ክፍል"]):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.bold = True
                run.font.size = Pt(13)
                run.font.color.rgb = RGBColor(140, 20, 20)
            else:
                run.font.size = Pt(11)
                
    word_doc.save(complete_docx_path)
    print(f"-> Word document: {complete_docx_path}")
    
    # Remove scratch folder
    try:
        import shutil
        shutil.rmtree(scratch_dir, ignore_errors=True)
    except Exception:
        pass
        
    print(f"\nIndividual page text files saved in: {pages_txt_dir}")
    print("Done!")

if __name__ == "__main__":
    main()
