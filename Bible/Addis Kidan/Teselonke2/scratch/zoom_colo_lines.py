import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p4 = doc[3]
mat = fitz.Matrix(16.0, 16.0)

# Colophon lines 1 and 2: y around 300 to 350
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 300, 290, 350)).save(os.path.join(scratch_dir, "ultra_colophon_l1_2.png"))

print("Captured colophon l1 and l2.")
