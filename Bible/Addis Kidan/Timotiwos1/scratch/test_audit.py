import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\Audited_Pages"
for i in range(1, 9):
    p = os.path.join(base_dir, f"page_{i:03d}.txt")
    with open(p, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    first_few = lines[0] if lines else "EMPTY"
    last_few = lines[-1] if lines else "EMPTY"
    print(f"Page {i}: {len(lines)} non-empty lines | Starts: '{first_few}' | Ends: '{last_few}'")
