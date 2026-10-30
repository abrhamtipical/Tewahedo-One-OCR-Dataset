import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p3 = doc[2]

mat = fitz.Matrix(30, 30)

# Chapter 3 heading punctuation
pix = p3.get_pixmap(matrix=mat, clip=fitz.Rect(170, 420, 210, 440))
# Wait, let's find the exact PDF rect of Chapter 3 heading
# In p03_sec4, Chapter 3 is around y = 490 to 540 in pixels of sec4.
# Let's find rect in PDF units
# p3 rect height is 794.88.
# p03_sec4 was clip (45, int(H*0.75)=555, 295, 740)
# Let's search for text rect or scan pixels
for b in p3.get_text("blocks"):
    if "ምዕራፍ" in b[4] or "፫" in b[4]:
        print("Block:", b)
