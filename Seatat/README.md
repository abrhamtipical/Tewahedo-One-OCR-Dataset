# Seatat (መጽሐፈ ሰዓታት) — Ge'ez and Amharic OCR

Source: the printed *Mets'hafe Se'atat* in Ge'ez and Amharic (79-page scan, `Metsehafeseatat.pdf`).
The Amharic translation is by Aleqa Mekonnen Solomon of Debre Libanos, printed by Tensae Zegubae Press.
The text was typed and edited from the print by Abraham Sisay, then proofread against the scan.

## Layout

| Folder | Contents |
|---|---|
| `ocr/raw/` | First OCR pass, pages 1–79, as seven parts (`part01.txt` … `part07.txt`). |
| `ocr/raw2/` | Second pass with the Ge'ez and Amharic columns split line by line (printed line *i* of Ge'ez pairs with line *i* of Amharic). Pages 49, 65 and 66 are missing. |
| `ocr/clean/` | `pages.json` (`[{page, geez[], amharic[]}]`) and `removed.txt` (everything the cleaner stripped, for review). |
| `ocr/fill/` | `old_vs_ocr.json`: where the OCR lacked a word or line that the app's earlier text had. |
| `ocr/merged/` | OCR merged with the earlier app text, before the later proofreading fixes. `REPORT.md` and `gaps_inside_matched_entries.tsv` list every fill. |
| `ocr/gemini_check_prompt*.md` | Prompts used for the Gemini cross-check. Its claims were verified against the print before being applied. |
| `scripts/` | The Python scripts used (see below). |
| `app_json_plain/` | The final section files `book_of_hours_01 … 37.json` as used in the app (plain text, after the proofreading fixes). |
| `app_json_encrypted/` | The same sections as shipped in the app (encrypted container, not readable). |

## Scripts

Run in this order from the root of the app project, since they use paths such as `research/seatat_ocr/…`, `unencrypted_data/liturgy/…` and `assets/liturgy/…`.

1. `clean_seatat_ocr.py` — cleans `raw/part*.txt` into `clean/pages.json` and `removed.txt`.
2. `compare_seatat_ocr.py` — diffs the first and second OCR pass.
3. `compare_seatat_old_vs_ocr.py` — reports what the OCR lacks compared with the earlier app text.
4. `merge_seatat_ocr_with_old.py` — merges the OCR with the earlier text into `merged/`.
5. `align_seatat_to_aba_tume.py` and `build_seatat_additions.py` — spelling alignment to a second edition, and sections 25–32.

## Conventions

- Words are separated by `፡`, as in the print.
- OCR misreads of the separator (`'`, `:`, `·`, `=`) were turned into `፡` and logged.
- Amharic appears only where the book has it (pp. 4–34 and 65–74).
- Section files have a `/* … */` header, then a JSON list of `{sortOder, text, title, turn, metadata}`. `sortOder` is a misspelling kept on purpose.
