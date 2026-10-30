import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\teselonke2.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Teselonke2\scratch"

doc = fitz.open(pdf_path)
p3 = doc[2]
mat = fitz.Matrix(8.0, 8.0) # 8x high-DPI

# Let's define precise rects for each area of interest
# Page height is ~795, width ~618. Left column is ~35 to 290.

# 1. Top: v16-17, Chapter 3 heading, Section 3 heading, v1-2 (y: 110 to 330)
c1 = fitz.Rect(35, 110, 300, 330)
p3.get_pixmap(matrix=mat, clip=c1).save(os.path.join(scratch_dir, "zoom_p3_v16_to_v2.png"))

# 2. Mid 1: v3, v4, v5, Section 4 heading (y: 320 to 520)
c2 = fitz.Rect(35, 320, 300, 520)
p3.get_pixmap(matrix=mat, clip=c2).save(os.path.join(scratch_dir, "zoom_p3_v3_to_sec4.png"))

# 3. Mid 2: v6, v7, v8, v9 (y: 510 to 680)
c3 = fitz.Rect(35, 510, 300, 680)
p3.get_pixmap(matrix=mat, clip=c3).save(os.path.join(scratch_dir, "zoom_p3_v6_to_v9.png"))

# 4. Bottom: v10, v11, v12, v13 (y: 660 to 780)
c4 = fitz.Rect(35, 660, 300, 780)
p3.get_pixmap(matrix=mat, clip=c4).save(os.path.join(scratch_dir, "zoom_p3_v10_to_v13.png"))

print("High-res zoom crops generated successfully.")
