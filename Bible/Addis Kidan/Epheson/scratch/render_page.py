import pypdfium2 as pdfium
from PIL import Image
import os
import sys

def render_page(page_num, scale=6):
    pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
    scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"
    doc = pdfium.PdfDocument(pdf_path)
    
    idx = page_num - 1
    page = doc[idx]
    bitmap = page.render(scale=scale)
    img = bitmap.to_pil()
    w, h = img.size
    
    prefix = f"p{page_num:02d}"
    
    # Left col: x roughly 25 to 295 pt
    left_box = (int(25 * scale), int(40 * scale), int(295 * scale), int(765 * scale))
    img.crop(left_box).save(os.path.join(scratch_dir, f"{prefix}_left_full.png"))
    
    # 4 slices
    img.crop((int(25 * scale), int(40 * scale), int(295 * scale), int(240 * scale))).save(os.path.join(scratch_dir, f"{prefix}_sec1.png"))
    img.crop((int(25 * scale), int(220 * scale), int(295 * scale), int(420 * scale))).save(os.path.join(scratch_dir, f"{prefix}_sec2.png"))
    img.crop((int(25 * scale), int(400 * scale), int(295 * scale), int(600 * scale))).save(os.path.join(scratch_dir, f"{prefix}_sec3.png"))
    img.crop((int(25 * scale), int(580 * scale), int(295 * scale), int(765 * scale))).save(os.path.join(scratch_dir, f"{prefix}_sec4.png"))
    
    print(f"Page {page_num} rendered successfully: {w}x{h}")

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    render_page(p)
