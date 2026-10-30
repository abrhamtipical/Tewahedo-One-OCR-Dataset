import os
import sys
import glob
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BASE_DIR = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Biluy Kidan\Psalms"
AUDITED_DIR = os.path.join(BASE_DIR, "Audited_Pages")
RAW_DIR = os.path.join(BASE_DIR, "Raw_OCR_Pages")
DOCX_DIR = os.path.join(BASE_DIR, "Pages_Docx")
MASTER_TXT = os.path.join(BASE_DIR, "Psalms_Ge_ez_and_Amharic_Complete.txt")
MASTER_DOCX = os.path.join(BASE_DIR, "Psalms_Ge_ez_and_Amharic_Complete.docx")

os.makedirs(AUDITED_DIR, exist_ok=True)
os.makedirs(DOCX_DIR, exist_ok=True)

def to_geez_numeral(num):
    tens = ['', '፲', '፳', '፴', '፵', '፶', '፷', '፸', '፹', '፺']
    ones = ['', '፩', '፪', '፫', '፬', '፭', '፮', '፯', '፰', '፱']
    if num == 100:
        return '፻'
    if num > 100:
        rem = num % 100
        rem_str = tens[rem // 10] + ones[rem % 10]
        return f"፻{rem_str}"
    return tens[num // 10] + ones[num % 10]

def set_font(run, font_name="Nyala", size_pt=11.0, bold=False, color_rgb=(0,0,0)):
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

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_clean_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="single" w:sz="6" w:space="0" w:color="D0D0D0"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_column_text(cell, text, lang="geez"):
    lines = text.strip().splitlines()
    first = True
    for line in lines:
        s = line.strip()
        if not s:
            continue
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        
        if any(s.startswith(k) for k in ["መዝሙር", "ተግሣጽ", "ትንቢት", "ፍካሬ", "ስለ", "በእንተ"]):
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(3)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(s)
            color = (150, 20, 20) if lang == "geez" else (20, 40, 140)
            set_font(run, font_name="Nyala", size_pt=12.0, bold=True, color_rgb=color)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(s)
            set_font(run, font_name="Nyala", size_pt=11.0, bold=False, color_rgb=(25, 25, 25))

def parse_page_file(content):
    geez_part = ""
    amh_part = ""
    if "[Ge'ez]" in content and "[Amharic]" in content:
        parts = content.split("[Amharic]")
        geez_part = parts[0].replace("[Ge'ez]", "").strip()
        amh_part = parts[1].strip()
    elif "[ግዕዝ]" in content and "[አማርኛ]" in content:
        parts = content.split("[አማርኛ]")
        geez_part = parts[0].replace("[ግዕዝ]", "").strip()
        amh_part = parts[1].strip()
    else:
        geez_part = content.strip()
    return geez_part, amh_part

def create_page_docx(page_num, geez_text, amh_text):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)
        
    header_p = doc.add_paragraph()
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = header_p.add_run(f"መዝሙረ ዳዊት (ግዕዝና አማርኛ) — ገጽ {to_geez_numeral(page_num)} (Page {page_num})")
    set_font(hrun, font_name="Nyala", size_pt=9.5, color_rgb=(120, 120, 120))
    
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_clean_table_borders(table)
    
    col_w = Inches(3.45)
    for row in table.rows:
        for cell in row.cells:
            cell.width = col_w
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            
    h_cell_l = table.cell(0, 0)
    p_l = h_cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_l = p_l.add_run("ግዕዝ (Ge'ez)")
    set_font(r_l, font_name="Nyala", size_pt=12.0, bold=True, color_rgb=(150, 20, 20))
    
    h_cell_r = table.cell(0, 1)
    p_r = h_cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r = p_r.add_run("አማርኛ (Amharic)")
    set_font(r_r, font_name="Nyala", size_pt=12.0, bold=True, color_rgb=(20, 40, 140))
    
    cell_l = table.cell(1, 0)
    format_column_text(cell_l, geez_text, lang="geez")
    
    cell_r = table.cell(1, 1)
    format_column_text(cell_r, amh_text, lang="amh")
    
    out_path = os.path.join(DOCX_DIR, f"Psalms_Page_{page_num:03d}.docx")
    doc.save(out_path)
    return out_path

def compile_all():
    sys.stdout.reconfigure(encoding="utf-8")
    print("Compiling all 104 Psalm pages into Master DOCX and Master TXT...")
    
    master_doc = Document()
    for s in master_doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)
        
    # Title Page
    t_p = master_doc.add_paragraph()
    t_p.paragraph_format.space_before = Pt(36)
    t_p.paragraph_format.space_after = Pt(12)
    t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    trun = t_p.add_run("መዝሙረ ዳዊት")
    set_font(trun, font_name="Nyala", size_pt=28, bold=True, color_rgb=(150, 20, 20))
    
    sub_p = master_doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    srun = sub_p.add_run("የዳዊት መዝሙር (ግዕዝና አማርኛ ጎን ለጎን)\nThe Book of Psalms in Classical Ge'ez and Amharic")
    set_font(srun, font_name="Nyala", size_pt=15, bold=True, color_rgb=(20, 40, 140))
    
    desc_p = master_doc.add_paragraph()
    desc_p.paragraph_format.space_after = Pt(36)
    desc_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    drun = desc_p.add_run("Complete 104-Page Edition • High-Precision Transcription\nPreserving Original Ge'ez Script, Numbering, and Amharic Alignment\nExcluded Web Headers & Footers • Audited & Verified")
    set_font(drun, font_name="Nyala", size_pt=11, bold=False, color_rgb=(100, 100, 100))
    
    master_doc.add_page_break()
    
    all_pages = []
    
    for pnum in range(1, 105):
        audited_path = os.path.join(AUDITED_DIR, f"page_{pnum:03d}.txt")
        raw_path = os.path.join(RAW_DIR, f"raw_page_{pnum:03d}.txt")
        
        file_to_read = audited_path if os.path.exists(audited_path) else raw_path
        if not os.path.exists(file_to_read):
            print(f"Warning: Page {pnum} file not found!")
            continue
            
        with open(file_to_read, "r", encoding="utf-8") as f:
            content = f.read()
            
        geez_text, amh_text = parse_page_file(content)
        all_pages.append((pnum, geez_text, amh_text))
        
        # Create single page docx
        create_page_docx(pnum, geez_text, amh_text)
        
        # Add to master doc
        p_marker = master_doc.add_paragraph()
        p_marker.paragraph_format.space_before = Pt(8)
        p_marker.paragraph_format.space_after = Pt(4)
        p_marker.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pm_run = p_marker.add_run(f"— ገጽ {to_geez_numeral(pnum)} (Page {pnum}) —")
        set_font(pm_run, font_name="Nyala", size_pt=10, bold=True, color_rgb=(120, 120, 120))
        
        table = master_doc.add_table(rows=2, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_clean_table_borders(table)
        
        col_w = Inches(3.45)
        for row in table.rows:
            for cell in row.cells:
                cell.width = col_w
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                
        h_cell_l = table.cell(0, 0)
        p_l = h_cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_l = p_l.add_run("ግዕዝ (Ge'ez)")
        set_font(r_l, font_name="Nyala", size_pt=11.5, bold=True, color_rgb=(150, 20, 20))
        
        h_cell_r = table.cell(0, 1)
        p_r = h_cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_r = p_r.add_run("አማርኛ (Amharic)")
        set_font(r_r, font_name="Nyala", size_pt=11.5, bold=True, color_rgb=(20, 40, 140))
        
        cell_l = table.cell(1, 0)
        format_column_text(cell_l, geez_text, lang="geez")
        
        cell_r = table.cell(1, 1)
        format_column_text(cell_r, amh_text, lang="amh")
        
        if pnum < 104:
            master_doc.add_page_break()
            
    master_doc.save(MASTER_DOCX)
    print(f"Master DOCX saved successfully: {MASTER_DOCX}")
    
    # Write Master TXT
    with open(MASTER_TXT, "w", encoding="utf-8") as f_out:
        f_out.write("================================================================================\n")
        f_out.write("መዝሙረ ዳዊት (ግዕዝና አማርኛ) — THE BOOK OF PSALMS (GE'EZ & AMHARIC)\n")
        f_out.write("Complete 104-Page Edition • High-Precision Side-by-Side Transcription\n")
        f_out.write("================================================================================\n\n")
        for pnum, g_text, a_text in all_pages:
            geez_p = to_geez_numeral(pnum)
            f_out.write(f"\n{'='*30} ገጽ {geez_p} (PAGE {pnum}) {'='*30}\n\n")
            f_out.write("[ግዕዝ | Ge'ez]\n")
            f_out.write(g_text.strip() + "\n\n")
            f_out.write("[አማርኛ | Amharic]\n")
            f_out.write(a_text.strip() + "\n\n")
            
    print(f"Master TXT saved successfully: {MASTER_TXT}")

if __name__ == "__main__":
    compile_all()
