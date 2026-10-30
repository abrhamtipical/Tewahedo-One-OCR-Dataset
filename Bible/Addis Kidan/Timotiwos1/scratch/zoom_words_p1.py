import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch"

doc = fitz.open(pdf_path)
p1 = doc[0]
mat = fitz.Matrix(16.0, 16.0) # 16x ultra-zoom

# Heading & Section 1: y around 195 to 255
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 195, 300, 255)).save(os.path.join(scratch_dir, "u_heading_sec1.png"))

# v4 line 1: y around 385 to 430
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 385, 300, 430)).save(os.path.join(scratch_dir, "u_v4_l1.png"))

# v6: y around 490 to 535
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 490, 300, 535)).save(os.path.join(scratch_dir, "u_v6.png"))

# v10 line 1: y around 645 to 685
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 645, 300, 685)).save(os.path.join(scratch_dir, "u_v10.png"))

# v11 line 1: y around 680 to 720
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 680, 300, 720)).save(os.path.join(scratch_dir, "u_v11.png"))

print("Captured 16x ultra-zoom crops for Page 1.")
