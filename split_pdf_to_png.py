"""Save every page of a scanned PDF as its own PNG: page_001.png, page_002.png, ...

Install once:
    pip install pymupdf

Examples (run from this folder):
    python split_pdf_to_png.py "Kidase/Full Kidase.pdf"
    python split_pdf_to_png.py "Kidase/Full Kidase.pdf" -o Full_Kidase_pages
    python split_pdf_to_png.py "Kidase/Full Kidase.pdf" --start 10 --end 20
    python split_pdf_to_png.py "Kidase/Full Kidase.pdf" --no-pad   # page_1.png, page_2.png, ...

The scans in Full Kidase.pdf are 200 dpi, so the default of 200 keeps them at full sharpness.
The page number in the file name is always the page number in the PDF.
"""
import argparse
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    sys.exit("PyMuPDF is not installed. Run:  pip install pymupdf")

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Save every page of a PDF as its own PNG.")
    ap.add_argument("pdf", help="path to the PDF file")
    ap.add_argument("-o", "--out", help="output folder (default: <pdf name>_pages, next to the PDF)")
    ap.add_argument("--dpi", type=int, default=200, help="image sharpness (default 200)")
    ap.add_argument("--start", type=int, default=1, help="first page to save (default 1)")
    ap.add_argument("--end", type=int, help="last page to save (default: last page)")
    ap.add_argument("--no-pad", action="store_true", help="name files page_1.png instead of page_001.png")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.is_file():
        sys.exit(f"PDF not found: {pdf_path}")
    out_dir = Path(args.out) if args.out else pdf_path.with_name(pdf_path.stem.replace(" ", "_") + "_pages")

    with pymupdf.open(str(pdf_path)) as doc:
        total = doc.page_count
        end = min(args.end or total, total)
        if args.start < 1 or args.start > end:
            sys.exit(f"Bad page range: the PDF has {total} pages, asked for {args.start}-{args.end or total}.")

        width = 1 if args.no_pad else max(3, len(str(total)))
        out_dir.mkdir(parents=True, exist_ok=True)
        for n in range(args.start, end + 1):
            pix = doc[n - 1].get_pixmap(dpi=args.dpi)
            pix.save(str(out_dir / f"page_{n:0{width}d}.png"))
            print(f"\rpage {n}/{end}", end="", flush=True)

    print(f"\nDone: {end - args.start + 1} PNG files in {out_dir}")


if __name__ == "__main__":
    main()
