import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
p3 = doc[2] # Page 3

scale = 10 # 10x scale for crystal clarity
bitmap = p3.render(scale=scale)
img = bitmap.to_pil()

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# Let's crop specific regions:
# 1. v11-v13: y from 90 to 260 pt
crop1 = img.crop((int(25 * scale), int(90 * scale), int(295 * scale), int(260 * scale)))
crop1.save(os.path.join(scratch_dir, "p03_v11_v13_z10.png"))

# 2. v14-v16: y from 240 to 390 pt
crop2 = img.crop((int(25 * scale), int(240 * scale), int(295 * scale), int(390 * scale)))
crop2.save(os.path.join(scratch_dir, "p03_v14_v16_z10.png"))

# 3. v17-v19: y from 370 to 510 pt
crop3 = img.crop((int(25 * scale), int(370 * scale), int(295 * scale), int(510 * scale)))
crop3.save(os.path.join(scratch_dir, "p03_v17_v19_z10.png"))

# 4. v20-v22 & Chapter 3 & Section 4 heading: y from 490 to 630 pt
crop4 = img.crop((int(25 * scale), int(490 * scale), int(295 * scale), int(630 * scale)))
crop4.save(os.path.join(scratch_dir, "p03_v20_ch3_z10.png"))

# 5. Chapter 3: v1-v5: y from 610 to 765 pt
crop5 = img.crop((int(25 * scale), int(610 * scale), int(295 * scale), int(765 * scale)))
crop5.save(os.path.join(scratch_dir, "p03_ch3_v1_v5_z10.png"))

print("All 5 high-res 10x crops of Page 3 saved!")
