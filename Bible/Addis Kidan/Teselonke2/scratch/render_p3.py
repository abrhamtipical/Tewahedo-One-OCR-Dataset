import fitz # PyMuPDF
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"
os.makedirs(scratch_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

page_idx = 2 # Page 3
page = doc[page_idx]
rect = page.rect
print(f"Page {page_idx+1} rect: {rect}")

# Typically page width is around 595-612, height around 792-842.
# Left column is from x: 30 to width*0.5, y: 35 to height-35.
# Let's render the left half:
crop_box = fitz.Rect(30, 40, rect.width * 0.52, rect.height - 35)

# 4x zoom matrix
mat = fitz.Matrix(4.0, 4.0)

# Also split into 3 vertical crops for easy visual inspection:
h = crop_box.height
box_top = fitz.Rect(crop_box.x0, crop_box.y0, crop_box.x1, crop_box.y0 + h * 0.36)
box_mid = fitz.Rect(crop_box.x0, crop_box.y0 + h * 0.32, crop_box.x1, crop_box.y0 + h * 0.69)
box_bot = fitz.Rect(crop_box.x0, crop_box.y0 + h * 0.65, crop_box.x1, crop_box.y1)

pix_top = page.get_pixmap(matrix=mat, clip=box_top)
pix_top.save(os.path.join(scratch_dir, "p03_crop1_top.png"))

pix_mid = page.get_pixmap(matrix=mat, clip=box_mid)
pix_mid.save(os.path.join(scratch_dir, "p03_crop2_mid.png"))

pix_bot = page.get_pixmap(matrix=mat, clip=box_bot)
pix_bot.save(os.path.join(scratch_dir, "p03_crop3_bot.png"))

print("Rendered p03 crops successfully.")
