import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p4 = doc[3]
mat = fitz.Matrix(16.0, 16.0) # 16x ultra-zoom

# v14 line 1: y around 110-130
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 110, 290, 135)).save(os.path.join(scratch_dir, "ultra_v14_l1.png"))

# Colophon lines 1, 2, 3: y around 335-395
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 335, 290, 400)).save(os.path.join(scratch_dir, "ultra_colophon.png"))

print("Captured 16x ultra-zoom crops.")
