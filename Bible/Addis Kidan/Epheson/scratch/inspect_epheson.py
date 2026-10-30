import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\epheson.pdf"
doc = pdfium.PdfDocument(pdf_path)

print(f"Total pages: {len(doc)}")
for i, page in enumerate(doc):
    w, h = page.get_size()
    print(f"Page {i+1}: {w} x {h} pt")

# Now let's render Page 1 (index 0)
page1 = doc[0]
scale = 6
bitmap = page1.render(scale=scale)
img = bitmap.to_pil()
w, h = img.size
print(f"Rendered Page 1 at {scale}x: {w} x {h} px")

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# Save full page
img.save(os.path.join(scratch_dir, "p01_full.png"))

# Left column: x roughly 25 to 295 pt
left_box = (int(25 * scale), int(40 * scale), int(295 * scale), int(765 * scale))
img.crop(left_box).save(os.path.join(scratch_dir, "p01_left_full.png"))

# Right column: x roughly 295 to 580 pt
right_box = (int(295 * scale), int(40 * scale), int(580 * scale), int(765 * scale))
img.crop(right_box).save(os.path.join(scratch_dir, "p01_right_full.png"))

# Let's also slice the left column into 4 sections for close reading
img.crop((int(25 * scale), int(40 * scale), int(295 * scale), int(240 * scale))).save(os.path.join(scratch_dir, "p01_sec1.png"))
img.crop((int(25 * scale), int(220 * scale), int(295 * scale), int(420 * scale))).save(os.path.join(scratch_dir, "p01_sec2.png"))
img.crop((int(25 * scale), int(400 * scale), int(295 * scale), int(600 * scale))).save(os.path.join(scratch_dir, "p01_sec3.png"))
img.crop((int(25 * scale), int(580 * scale), int(295 * scale), int(765 * scale))).save(os.path.join(scratch_dir, "p01_sec4.png"))

print("Page 1 crops saved successfully!")
