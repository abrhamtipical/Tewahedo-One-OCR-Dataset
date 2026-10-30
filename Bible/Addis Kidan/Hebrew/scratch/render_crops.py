import pymupdf
import sys
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\hebrew.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Hebrew\scratch"

def crop_page(page_idx, parts=2):
    doc = pymupdf.open(pdf_path)
    page = doc[page_idx]
    
    # Left column bounds approximately: x0=35, y0=60, x1=325, y1=750
    # Depending on page height
    h = page.rect.height
    w = page.rect.width
    
    if parts == 1:
        rect = pymupdf.Rect(35, 60, 325, 750)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), clip=rect)
        out = os.path.join(scratch_dir, f"crop_{page_idx+1}_full.png")
        pix.save(out)
        print(f"Saved {out}")
    elif parts == 2:
        # Top half
        rect1 = pymupdf.Rect(35, 60, 325, 410)
        pix1 = page.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), clip=rect1)
        out1 = os.path.join(scratch_dir, f"crop_{page_idx+1}_top.png")
        pix1.save(out1)
        
        # Bottom half
        rect2 = pymupdf.Rect(35, 400, 325, 750)
        pix2 = page.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), clip=rect2)
        out2 = os.path.join(scratch_dir, f"crop_{page_idx+1}_bottom.png")
        pix2.save(out2)
        print(f"Saved {out1} and {out2}")

if __name__ == "__main__":
    page_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    crop_page(page_idx, parts=2)
