import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)

# Let's render Page 4 (index 3)
p4 = doc[3]
rect4 = p4.rect
crop_box4 = fitz.Rect(30, 40, rect4.width * 0.52, rect4.height - 35)
mat = fitz.Matrix(4.0, 4.0)

h4 = crop_box4.height
box4_top = fitz.Rect(crop_box4.x0, crop_box4.y0, crop_box4.x1, crop_box4.y0 + h4 * 0.5)
box4_bot = fitz.Rect(crop_box4.x0, crop_box4.y0 + h4 * 0.45, crop_box4.x1, crop_box4.y1)

p4.get_pixmap(matrix=mat, clip=box4_top).save(os.path.join(scratch_dir, "p04_crop1_top.png"))
p4.get_pixmap(matrix=mat, clip=box4_bot).save(os.path.join(scratch_dir, "p04_crop2_bot.png"))

print("Rendered Page 4 crops.")
