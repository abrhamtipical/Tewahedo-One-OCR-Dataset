import fitz
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf"
scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch"
os.makedirs(scratch_dir, exist_ok=True)

doc = fitz.open(pdf_path)
p1 = doc[0]
rect = p1.rect

# Ge'ez column is on left side (~30 to rect.width*0.52, y: 35 to rect.height-35)
crop_box = fitz.Rect(30, 35, rect.width * 0.52, rect.height - 35)
mat = fitz.Matrix(4.0, 4.0)

h = crop_box.height
box_top = fitz.Rect(crop_box.x0, crop_box.y0, crop_box.x1, crop_box.y0 + h * 0.36)
box_mid = fitz.Rect(crop_box.x0, crop_box.y0 + h * 0.32, crop_box.x1, crop_box.y0 + h * 0.69)
box_bot = fitz.Rect(crop_box.x0, crop_box.y0 + h * 0.65, crop_box.x1, crop_box.y1)

p1.get_pixmap(matrix=mat, clip=box_top).save(os.path.join(scratch_dir, "p01_crop1_top.png"))
p1.get_pixmap(matrix=mat, clip=box_mid).save(os.path.join(scratch_dir, "p01_crop2_mid.png"))
p1.get_pixmap(matrix=mat, clip=box_bot).save(os.path.join(scratch_dir, "p01_crop3_bot.png"))

print("Rendered Timotiwos1 Page 1 crops successfully.")
