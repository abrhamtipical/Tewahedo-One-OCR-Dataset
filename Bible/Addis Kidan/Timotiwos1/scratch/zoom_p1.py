import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch"

doc = fitz.open(pdf_path)
p1 = doc[0]
mat = fitz.Matrix(10.0, 10.0)

# Banner, Heading, Section 1, v1-2 (y: 190 to 410)
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 190, 305, 410)).save(os.path.join(scratch_dir, "z_p1_top.png"))

# v3, v4, v5, v6 (y: 400 to 570)
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 400, 305, 570)).save(os.path.join(scratch_dir, "z_p1_mid.png"))

# v7, v8, v9 (y: 560 to 710)
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 560, 305, 710)).save(os.path.join(scratch_dir, "z_p1_mid2.png"))

# v10, v11, v12, v13 (y: 700 to 790)
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 700, 305, 790)).save(os.path.join(scratch_dir, "z_p1_bot.png"))

print("Captured Page 1 zoom crops.")
