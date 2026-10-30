from PIL import Image

# We already have p03_sec1, p03_sec2, p03_sec3, p03_sec4
sec2 = Image.open(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec2.png")
sec3 = Image.open(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec3.png")
sec4 = Image.open(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\p03_sec4.png")

# sec2: v14 line 1
sec2.crop((0, 180, 1500, 320)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\crop_v14_l1.png")

# sec2: v15
sec2.crop((0, 500, 1500, 680)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\crop_v15.png")

# sec3: v17 & v18
sec3.crop((0, 120, 1500, 480)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\crop_v17_v18.png")

# sec3: v20
sec3.crop((0, 580, 1500, 1150)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\crop_v20.png")

# sec4: Chapter 3 heading
sec4.crop((350, 480, 1000, 600)).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Gelatiya\scratch\crop_ch3_head.png")

print("Cropped from sections successfully")
