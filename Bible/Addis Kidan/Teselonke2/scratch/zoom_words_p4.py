import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p4 = doc[3]
mat = fitz.Matrix(12.0, 12.0)

# v14
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 125, 295, 175)).save(os.path.join(scratch_dir, "w_p4_v14.png"))

# v17
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 260, 295, 335)).save(os.path.join(scratch_dir, "w_p4_v17.png"))

# Colophon
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 400, 295, 475)).save(os.path.join(scratch_dir, "w_p4_colophon.png"))

print("Captured Page 4 targeted HD crops.")
