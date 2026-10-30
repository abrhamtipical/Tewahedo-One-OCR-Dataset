import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p3 = doc[2]
mat = fitz.Matrix(12.0, 12.0)

# v3
p3.get_pixmap(matrix=mat, clip=fitz.Rect(35, 260, 290, 330)).save(os.path.join(scratch_dir, "v3_hd.png"))
# v6 & v7
p3.get_pixmap(matrix=mat, clip=fitz.Rect(35, 430, 290, 520)).save(os.path.join(scratch_dir, "v6_7_hd.png"))
# v12
p3.get_pixmap(matrix=mat, clip=fitz.Rect(35, 595, 290, 660)).save(os.path.join(scratch_dir, "v12_hd.png"))

print("Captured targeted HD crops.")
