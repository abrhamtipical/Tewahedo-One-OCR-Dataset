import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)
p3 = doc[2] # Page 3

scale = 25 # 25x scale for microscopic inspection
bitmap = p3.render(scale=scale)
img = bitmap.to_pil()

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# Targets:
# 1. First word of line 1: y around 100-120 pt, x 25-60 pt
img.crop((int(30 * scale), int(105 * scale), int(60 * scale), int(122 * scale))).save(
    os.path.join(scratch_dir, "t01_line1_word1.png")
)

# 2. v12 line 2 "ወነግዳን/ወነጋድያን": y 140-160 pt, x 140-220 pt
img.crop((int(135 * scale), int(143 * scale), int(195 * scale), int(160 * scale))).save(
    os.path.join(scratch_dir, "t02_v12_wenegdan.png")
)

# 3. v12 line 1 "ወኢተአምርዎ"
img.crop((int(35 * scale), int(123 * scale), int(95 * scale), int(142 * scale))).save(
    os.path.join(scratch_dir, "t03_v12_weiteamrewo.png")
)

# 4. v15 "ሰላመ ።"
img.crop((int(35 * scale), int(330 * scale), int(80 * scale), int(355 * scale))).save(
    os.path.join(scratch_dir, "t04_v15_selame.png")
)

# 5. v16 "በአሐዱ"
img.crop((int(150 * scale), int(370 * scale), int(200 * scale), int(395 * scale))).save(
    os.path.join(scratch_dir, "t05_v16_beahadu.png")
)

# 6. v18 "አቡሁ"
img.crop((int(35 * scale), int(445 * scale), int(65 * scale), int(470 * scale))).save(
    os.path.join(scratch_dir, "t06_v18_abuhu.png")
)

# 7. v19 "ወፈላሴ" punctuation
img.crop((int(170 * scale), int(465 * scale), int(215 * scale), int(490 * scale))).save(
    os.path.join(scratch_dir, "t07_v19_punctuation.png")
)

# 8. v20 "ተሐነጽክሙ" vs v22 "ተሐነጽክሙ"
img.crop((int(45 * scale), int(530 * scale), int(95 * scale), int(555 * scale))).save(
    os.path.join(scratch_dir, "t08_v20_tehanetskmu.png")
)
img.crop((int(105 * scale), int(600 * scale), int(155 * scale), int(625 * scale))).save(
    os.path.join(scratch_dir, "t08_v22_tehanetskmu.png")
)

# 9. Chapter 3 heading
img.crop((int(100 * scale), int(630 * scale), int(170 * scale), int(655 * scale))).save(
    os.path.join(scratch_dir, "t09_ch3_heading.png")
)

# 10. v2 "ሶበሰ ሰማዕክሙ"
img.crop((int(35 * scale), int(695 * scale), int(95 * scale), int(720 * scale))).save(
    os.path.join(scratch_dir, "t10_v2_sobes_semaekmu.png")
)

# 11. v4 "በምክረ ለክርስቶስ"
img.crop((int(35 * scale), int(775 * scale), int(115 * scale), int(800 * scale))).save(
    os.path.join(scratch_dir, "t11_v4_bemkre.png")
)

print("Target crops saved at 25x scale!")
