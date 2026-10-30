import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p4 = doc[3]
mat = fitz.Matrix(10.0, 10.0) # 10x high-DPI

# v14, 15, 16 (y: 110 to 260)
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 110, 300, 260)).save(os.path.join(scratch_dir, "zoom_p4_v14_to_v16.png"))

# v17, 18 (y: 250 to 360)
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 250, 300, 360)).save(os.path.join(scratch_dir, "zoom_p4_v17_to_v18.png"))

# colophon (y: 380 to 480)
p4.get_pixmap(matrix=mat, clip=fitz.Rect(35, 380, 300, 480)).save(os.path.join(scratch_dir, "zoom_p4_colophon.png"))

print("Page 4 zoom crops generated.")
