import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\Audited_Pages"

all_text = ""
for i in range(1, 9):
    p = os.path.join(base_dir, f"page_{i:03d}.txt")
    with open(p, 'r', encoding='utf-8') as f:
        all_text += f"\n--- PAGE {i} ---\n" + f.read()

chapters = re.findall(r"ምዕራፍ\s+([፩-፮]+)", all_text)
sections = re.findall(r"ክፍል\s+([፩-፮]+)", all_text)

print(f"Chapters found: {chapters}")
print(f"Sections found: {sections}")

# Split by chapters and find verses
chap_blocks = re.split(r"ምዕራፍ\s+[፩-፮]+", all_text)
print(f"Total blocks split by chapter: {len(chap_blocks)}")

for idx, block in enumerate(chap_blocks[1:], 1):
    verses = re.findall(r"^([፩-፴]+)\s+", block, re.MULTILINE)
    print(f"Chapter {idx} verses ({len(verses)}): {verses}")
