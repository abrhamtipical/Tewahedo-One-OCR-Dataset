import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch"

doc = fitz.open(pdf_path)
p1 = doc[0]
mat = fitz.Matrix(20.0, 20.0) # 20x hyper-zoom

# Heading: y around 160-205
p1.get_pixmap(matrix=mat, clip=fitz.Rect(110, 160, 240, 205)).save(os.path.join(scratch_dir, "h_heading.png"))

# v10 line 1: y around 605-645
p1.get_pixmap(matrix=mat, clip=fitz.Rect(30, 605, 300, 645)).save(os.path.join(scratch_dir, "h_v10_l1.png"))

# v11 line 1 word 'በዘይትቃወሞ...': x around 140-230, y around 645-675
p1.get_pixmap(matrix=mat, clip=fitz.Rect(130, 645, 230, 675)).save(os.path.join(scratch_dir, "h_v11_word.png"))

print("Captured 20x hyper-zoom crops.")
