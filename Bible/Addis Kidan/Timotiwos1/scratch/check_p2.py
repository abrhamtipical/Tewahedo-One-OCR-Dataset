import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch"

doc = fitz.open(pdf_path)
p2 = doc[1]
rect2 = p2.rect
crop2_top = fitz.Rect(30, 35, rect2.width * 0.52, 220)
mat = fitz.Matrix(4.0, 4.0)

p2.get_pixmap(matrix=mat, clip=crop2_top).save(os.path.join(scratch_dir, "p02_top_check.png"))
print("Rendered p02 top check.")
