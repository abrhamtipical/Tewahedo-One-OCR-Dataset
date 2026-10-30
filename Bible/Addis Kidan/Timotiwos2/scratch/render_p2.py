import pymupdf
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos2.pdf"
out_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos2\scratch"

doc = pymupdf.open(pdf_path)
page = doc[1] # Page 2 (index 1)
rect = page.rect

zoom = 5.0
mat = pymupdf.Matrix(zoom, zoom)

# Section 1: Top (verses 15 to Ch 2 heading)
clip_top = pymupdf.Rect(30, 40, 310, 300)
pix = page.get_pixmap(matrix=mat, clip=clip_top)
pix.save(os.path.join(out_dir, "p02_crop1_top.png"))

# Section 2: Middle (Ch 2 verses 1 to 10)
clip_mid = pymupdf.Rect(30, 280, 310, 540)
pix = page.get_pixmap(matrix=mat, clip=clip_mid)
pix.save(os.path.join(out_dir, "p02_crop2_mid.png"))

# Section 3: Bottom (Ch 2 verses 10 to bottom)
clip_bot = pymupdf.Rect(30, 520, 310, 770)
pix = page.get_pixmap(matrix=mat, clip=clip_bot)
pix.save(os.path.join(out_dir, "p02_crop3_bot.png"))

print("Saved p02 crops: top, mid, bot")
