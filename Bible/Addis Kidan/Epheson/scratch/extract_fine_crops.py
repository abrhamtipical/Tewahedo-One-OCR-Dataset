from PIL import Image
import os

scratch_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Epheson\scratch"

# From crop1 (v11-v13, 2700x1700)
c1 = Image.open(os.path.join(scratch_dir, "p03_v11_v13_z10.png"))
# line 1 first word: around y 150-350, x 200-600
c1.crop((200, 160, 600, 360)).save(os.path.join(scratch_dir, "fine_line1_word1.png"))
# v12 line 1 "ወኢተአምርዎ"
c1.crop((200, 340, 700, 520)).save(os.path.join(scratch_dir, "fine_v12_word1.png"))
# v12 line 2 "ወነግዳን/ወነጋድያን"
c1.crop((1200, 480, 1750, 660)).save(os.path.join(scratch_dir, "fine_v12_wenegdan.png"))
# v12 line 3 "ወኢተአምርዎ"
c1.crop((1300, 640, 1850, 800)).save(os.path.join(scratch_dir, "fine_v12_weiteamrewo2.png"))

# From crop2 (v14-v16)
c2 = Image.open(os.path.join(scratch_dir, "p03_v14_v16_z10.png"))
# v15 "ሰላመ ።"
c2.crop((200, 500, 600, 700)).save(os.path.join(scratch_dir, "fine_v15_selame.png"))
# v16 "በአሐዱ"
c2.crop((1200, 600, 1700, 780)).save(os.path.join(scratch_dir, "fine_v16_beahadu.png"))

# From crop3 (v17-v19)
c3 = Image.open(os.path.join(scratch_dir, "p03_v17_v19_z10.png"))
# v18 "አቡሁ"
c3.crop((200, 300, 550, 480)).save(os.path.join(scratch_dir, "fine_v18_abuhu.png"))
# v19 "ወፈላሴ" punctuation
c3.crop((1300, 420, 1750, 600)).save(os.path.join(scratch_dir, "fine_v19_punct.png"))

# From crop4 (v20-v22 & headings)
c4 = Image.open(os.path.join(scratch_dir, "p03_v20_ch3_z10.png"))
# v21 "ዘቦቱ የኀድር"
c4.crop((200, 120, 800, 300)).save(os.path.join(scratch_dir, "fine_v21_yehadir.png"))
# v22 "ተሐነፅክሙ"
c4.crop((750, 300, 1300, 480)).save(os.path.join(scratch_dir, "fine_v22_tehanetskmu.png"))
# Chapter 3 heading
c4.crop((700, 550, 1600, 750)).save(os.path.join(scratch_dir, "fine_ch3_heading.png"))
# Section 4 heading
c4.crop((100, 700, 2600, 950)).save(os.path.join(scratch_dir, "fine_sec4_heading.png"))

# From crop5 (ch3 v1-v5)
c5 = Image.open(os.path.join(scratch_dir, "p03_ch3_v1_v5_z10.png"))
# v2 "ሶበሰ" mark
c5.crop((200, 160, 850, 360)).save(os.path.join(scratch_dir, "fine_v2_sobes.png"))
# v4 "በምክረ ለክርስቶስ"
c5.crop((200, 600, 950, 800)).save(os.path.join(scratch_dir, "fine_v4_bemkre.png"))

print("All targeted fine crops successfully created!")
