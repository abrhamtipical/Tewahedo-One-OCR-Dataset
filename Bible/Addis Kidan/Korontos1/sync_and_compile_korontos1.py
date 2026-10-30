import os
import sys
import glob

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Korontos1"
AUDITED_DIR = os.path.join(BASE_DIR, "Audited_Pages")
DOCX_DIR = os.path.join(BASE_DIR, "Pages_Docx")
MASTER_TXT = os.path.join(BASE_DIR, "Geez_Korontos1_Audited_Complete.txt")
MASTER_DOCX = os.path.join(BASE_DIR, "Geez_Korontos1_Audited_Complete.docx")

os.makedirs(DOCX_DIR, exist_ok=True)

# Ge'ez numerals mapping for page numbers 1-29
GEEZ_NUMS = {
    1: '፩', 2: '፪', 3: '፫', 4: '፬', 5: '፭', 6: '፮', 7: '፯', 8: '፰', 9: '፱', 10: '፲',
    11: '፲፩', 12: '፲፪', 13: '፲፫', 14: '፲፬', 15: '፲፭', 16: '፲፮', 17: '፲፯', 18: '፲፰', 19: '፲፱', 20: '፳',
    21: '፳፩', 22: '፳፪', 23: '፳፫', 24: '፳፬', 25: '፳፭', 26: '፳፮', 27: '፳፯', 28: '፳፰', 29: '፳፱'
}

def set_font(run, font_name="Nyala", size_pt=12.5, bold=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.append(rFonts)

def create_page_docx(page_num, text_content):
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Header
    header_p = doc.add_paragraph()
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = header_p.add_run(f"መልእክት ቀዳማዊት ኀበ ሰብአ ቆሮንቶስ — ገጽ {GEEZ_NUMS.get(page_num, str(page_num))} (Page {page_num})")
    set_font(hrun, font_name="Nyala", size_pt=9.5, color_rgb=(120, 120, 120))

    lines = text_content.strip().split('\n')
    for line in lines:
        stripped = line.strip()
        if not stripped:
            doc.add_paragraph()
            continue

        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(2)

        if stripped.startswith("ምዕራፍ"):
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(stripped)
            set_font(run, font_name="Nyala", size_pt=14, bold=True, color_rgb=(160, 20, 20))
        elif stripped.startswith("ክፍል"):
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(stripped)
            set_font(run, font_name="Nyala", size_pt=13, bold=True, color_rgb=(20, 40, 140))
        elif stripped.startswith("ተፈጸመ") or stripped.startswith("መልእክት"):
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(stripped)
            set_font(run, font_name="Nyala", size_pt=13.5, bold=True, color_rgb=(100, 20, 60))
        else:
            if line.startswith("    ") or line.startswith("\t"):
                p.paragraph_format.left_indent = Inches(0.3)
            run = p.add_run(stripped)
            set_font(run, font_name="Nyala", size_pt=12.5, bold=False, color_rgb=(20, 20, 20))

    docx_path = os.path.join(DOCX_DIR, f"Geez_Korontos1_Page_{page_num:03d}.docx")
    doc.save(docx_path)
    return docx_path

def compile_all():
    print("Reading and verifying all 29 audited pages for 1 Corinthians (፩ ቆሮንቶስ)...")
    all_pages_text = []
    
    for i in range(1, 30):
        txt_path = os.path.join(AUDITED_DIR, f"page_{i:03d}.txt")
        if not os.path.exists(txt_path):
            raise FileNotFoundError(f"Missing audited page: {txt_path}")
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        all_pages_text.append((i, content))
        create_page_docx(i, content)
    
    print(f"All 29 individual page docx files generated successfully in {DOCX_DIR}.")

    # Write Master TXT
    print("Writing Master TXT file...")
    with open(MASTER_TXT, 'w', encoding='utf-8') as f_out:
        f_out.write("ቀዳማዊ መልእክት ኀበ ሰብአ ቆሮንቶስ (Classical Ge'ez Column - 1 Corinthians)\n")
        f_out.write("High-Precision Line-by-Line Audited & Verified Full Text (Pages 1 - 29)\n")
        f_out.write("=" * 70 + "\n\n")
        
        for pnum, text in all_pages_text:
            geez_p = GEEZ_NUMS.get(pnum, str(pnum))
            f_out.write(f"\n{'='*25} ገጽ {geez_p} (PAGE {pnum}) {'='*25}\n\n")
            f_out.write(text.strip() + "\n")
    print(f"Master TXT saved: {MASTER_TXT}")

    # Write Master DOCX
    print("Writing Master DOCX file...")
    master_doc = Document()
    for section in master_doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Title Page
    title_p = master_doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    trun = title_p.add_run("ቀዳማዊ መልእክት ኀበ ሰብአ ቆሮንቶስ")
    set_font(trun, font_name="Nyala", size_pt=26, bold=True, color_rgb=(160, 20, 20))

    sub_p = master_doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(24)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    srun = sub_p.add_run("The First Epistle of Saint Paul to the Corinthians in Classical Ge'ez\nየተሟላና የተስተካከለ የግዕዝ ጽሑፍ (ምዕራፍ ፩ - ፲ወ፮)")
    set_font(srun, font_name="Nyala", size_pt=14, bold=False, color_rgb=(70, 70, 70))

    meta_p = master_doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(36)
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    mrun = meta_p.add_run("Exhaustive Line-by-Line Manual Audit & Visual Verification\n29 Pages (Complete) • High-Accuracy Classical Ge'ez Transcription")
    set_font(mrun, font_name="Nyala", size_pt=11, bold=False, color_rgb=(100, 100, 100))

    master_doc.add_page_break()

    for pnum, text in all_pages_text:
        # Page marker
        p_marker = master_doc.add_paragraph()
        p_marker.paragraph_format.space_before = Pt(10)
        p_marker.paragraph_format.space_after = Pt(6)
        p_marker.alignment = WD_ALIGN_PARAGRAPH.CENTER
        geez_p = GEEZ_NUMS.get(pnum, str(pnum))
        pm_run = p_marker.add_run(f"— ገጽ {geez_p} (Page {pnum}) —")
        set_font(pm_run, font_name="Nyala", size_pt=10, bold=True, color_rgb=(120, 120, 120))

        lines = text.strip().split('\n')
        for line in lines:
            stripped = line.strip()
            if not stripped:
                master_doc.add_paragraph()
                continue

            p = master_doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(2)

            if stripped.startswith("ምዕራፍ"):
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(stripped)
                set_font(run, font_name="Nyala", size_pt=14, bold=True, color_rgb=(160, 20, 20))
            elif stripped.startswith("ክፍል"):
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(stripped)
                set_font(run, font_name="Nyala", size_pt=13, bold=True, color_rgb=(20, 40, 140))
            elif stripped.startswith("ተፈጸመ") or stripped.startswith("መልእክት"):
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run(stripped)
                set_font(run, font_name="Nyala", size_pt=13.5, bold=True, color_rgb=(100, 20, 60))
            else:
                if line.startswith("    ") or line.startswith("\t"):
                    p.paragraph_format.left_indent = Inches(0.3)
                run = p.add_run(stripped)
                set_font(run, font_name="Nyala", size_pt=12.5, bold=False, color_rgb=(20, 20, 20))

        if pnum < 29:
            master_doc.add_page_break()

    master_doc.save(MASTER_DOCX)
    print(f"Master DOCX saved successfully: {MASTER_DOCX}")

if __name__ == "__main__":
    compile_all()
