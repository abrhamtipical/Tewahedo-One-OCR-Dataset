import fitz
import sys
import os

pdf_path = r'C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\korontos1.pdf'
scratch_dir = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Korontos1\scratch'

doc = fitz.open(pdf_path)

def render_page_slices(page_num):
    # page_num is 1-indexed
    p_idx = page_num - 1
    page = doc[p_idx]
    
    # Left column roughly x: 40 to 285, y: 110 to 765
    mat = fitz.Matrix(5.0, 5.0)
    
    # Slice 1: top
    r1 = fitz.Rect(40, 110, 285, 335)
    # Slice 2: mid
    r2 = fitz.Rect(40, 325, 285, 550)
    # Slice 3: bot
    r3 = fitz.Rect(40, 540, 285, 765)
    
    pix1 = page.get_pixmap(matrix=mat, clip=r1)
    pix2 = page.get_pixmap(matrix=mat, clip=r2)
    pix3 = page.get_pixmap(matrix=mat, clip=r3)
    
    prefix = f"p{page_num:02d}"
    pix1.save(os.path.join(scratch_dir, f"{prefix}_hd1.png"))
    pix2.save(os.path.join(scratch_dir, f"{prefix}_hd2.png"))
    pix3.save(os.path.join(scratch_dir, f"{prefix}_hd3.png"))
    print(f"Rendered {prefix} slices")

def render_custom_zoom(page_num, y_start, y_end, name):
    p_idx = page_num - 1
    page = doc[p_idx]
    mat = fitz.Matrix(6.0, 6.0)
    r = fitz.Rect(45, y_start, 280, y_end)
    pix = page.get_pixmap(matrix=mat, clip=r)
    out_path = os.path.join(scratch_dir, name)
    pix.save(out_path)
    print(f"Saved {name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "slice":
            pg = int(sys.argv[2])
            render_page_slices(pg)
        elif cmd == "zoom":
            pg = int(sys.argv[2])
            y1 = float(sys.argv[3])
            y2 = float(sys.argv[4])
            nm = sys.argv[5]
            render_custom_zoom(pg, y1, y2, nm)
