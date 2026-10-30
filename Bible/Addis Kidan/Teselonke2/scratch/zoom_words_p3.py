import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p3 = doc[2]
mat = fitz.Matrix(12.0, 12.0) # 12x zoom

# v3: y around 325-365
c_v3 = fitz.Rect(35, 320, 290, 365)
p3.get_pixmap(matrix=mat, clip=c_v3).save(os.path.join(scratch_dir, "w_p3_v3.png"))

# v4 line 2: y around 385-410
c_v4 = fitz.Rect(35, 385, 290, 415)
p3.get_pixmap(matrix=mat, clip=c_v4).save(os.path.join(scratch_dir, "w_p3_v4.png"))

# v6: y around 515-580
c_v6 = fitz.Rect(35, 515, 290, 580)
p3.get_pixmap(matrix=mat, clip=c_v6).save(os.path.join(scratch_dir, "w_p3_v6.png"))

# v7: y around 580-625
c_v7 = fitz.Rect(35, 580, 290, 625)
p3.get_pixmap(matrix=mat, clip=c_v7).save(os.path.join(scratch_dir, "w_p3_v7.png"))

# v12: y around 700-755
c_v12 = fitz.Rect(35, 700, 290, 755)
p3.get_pixmap(matrix=mat, clip=c_v12).save(os.path.join(scratch_dir, "w_p3_v12.png"))

print("Word zoom crops generated.")
