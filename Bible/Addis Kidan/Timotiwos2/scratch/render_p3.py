import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"

doc = pymupdf.open(pdf_path)
page = doc[2] # Page 3 (index 2)
rect = page.rect

zoom = 5.0
mat = pymupdf.Matrix(zoom, zoom)

# Section 1: Top (Ch 2 verses 15 to 21)
clip_top = pymupdf.Rect(30, 40, 310, 300)
pix = page.get_pixmap(matrix=mat, clip=clip_top)
pix.save(os.path.join(out_dir, "p03_crop1_top.png"))

# Section 2: Middle (Ch 2 verses 21 to Ch 3 heading)
clip_mid = pymupdf.Rect(30, 280, 310, 540)
pix = page.get_pixmap(matrix=mat, clip=clip_mid)
pix.save(os.path.join(out_dir, "p03_crop2_mid.png"))

# Section 3: Bottom (Ch 3 verses 1 to bottom)
clip_bot = pymupdf.Rect(30, 520, 310, 770)
pix = page.get_pixmap(matrix=mat, clip=clip_bot)
pix.save(os.path.join(out_dir, "p03_crop3_bot.png"))

print("Saved p03 crops: top, mid, bot")
