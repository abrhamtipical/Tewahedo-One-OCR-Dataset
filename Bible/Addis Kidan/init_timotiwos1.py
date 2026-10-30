import fitz # PyMuPDF
import os

pdf_path = r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf"
base_dir = r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1"
scratch_dir = os.path.join(base_dir, "scratch")
audited_dir = os.path.join(base_dir, "Audited_Pages")
docx_dir = os.path.join(base_dir, "Pages_Docx")

os.makedirs(scratch_dir, exist_ok=True)
os.makedirs(audited_dir, exist_ok=True)
os.makedirs(docx_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages in timotiwos1.pdf: {len(doc)}")
for i, page in enumerate(doc):
    print(f"Page {i+1}: rect={page.rect}")
