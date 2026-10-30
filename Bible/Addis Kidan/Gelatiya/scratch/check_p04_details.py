import fitz

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\gelatiya.pdf"
doc = fitz.open(pdf_path)
p4 = doc[3]

mat30 = fitz.Matrix(30, 30)

# 1. v3 line 1: abdan and zemenfes/bemenfes
pix1 = p4.get_pixmap(matrix=mat30, clip=fitz.Rect(50, 140, 290, 165))
pix1.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_p04_v3_line1.png")

# 2. v8 line 3: asefewo
pix2 = p4.get_pixmap(matrix=mat30, clip=fitz.Rect(50, 385, 120, 410))
pix2.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_p04_v8_asefewo.png")

# 3. sec4 heading: tsinu'e
pix3 = p4.get_pixmap(matrix=mat30, clip=fitz.Rect(180, 680, 240, 715))
pix3.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_p04_sec4_word.png")

# 4. v15 line 2: zetsinu'e
pix4 = p4.get_pixmap(matrix=mat30, clip=fitz.Rect(50, 725, 140, 755))
pix4.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_p04_v15_word.png")

# 5. v16 line 2: wele'azre'etike
pix5 = p4.get_pixmap(matrix=mat30, clip=fitz.Rect(145, 750, 255, 785))
pix5.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_p04_v16_azre.png")

# Amharic column for page 4
pix_amh = p4.get_pixmap(matrix=fitz.Matrix(5, 5), clip=fitz.Rect(300, 120, 575, 750))
pix_amh.save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\check_p04_amh.png")

print("Page 4 check crops generated")
