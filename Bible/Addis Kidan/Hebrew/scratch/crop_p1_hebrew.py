import fitz
import PIL.Image as Image
import io

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\hebrew.pdf")
print("Total pages in hebrew.pdf:", len(doc))

page = doc[0]
mat = fitz.Matrix(3.0, 3.0)
pix = page.get_pixmap(matrix=mat)
img = Image.open(io.BytesIO(pix.tobytes("png")))
w, h = img.size
print(f"Page 1 size: {w}x{h}")

# Left column
c_top = img.crop((int(w * 0.05), int(h * 0.12), int(w * 0.50), int(h * 0.55)))
c_top.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Hebrew\scratch\p01_col_top.png")

c_bot = img.crop((int(w * 0.05), int(h * 0.50), int(w * 0.50), int(h * 0.95)))
c_bot.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Hebrew\scratch\p01_col_bot.png")

print("Rendered Page 1 crops for Hebrews!")
