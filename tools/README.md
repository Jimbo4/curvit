# CV generator

Builds a tailored CV (`.docx` + `.pdf`) from a JSON content spec. The spec holds content only; layout rules (fonts, sizes, colour roles, spacing, icons, keep-together rules) live in the scripts and follow `../CLAUDE.md`.

## Usage

```bash
python3 tools/build_cv.py output/20261009_cv_jacopo_marcolini_generic.json            # refuses to overwrite
python3 tools/build_cv.py output/20261009_cv_jacopo_marcolini_generic.json --overwrite
```

Outputs are written next to the spec with the same base name. The script prints a report: pages, fonts embedded in the PDF, em dashes, double spaces, predicted orphans (last line with 1 or 2 words), short lines found in the PDF and the contact lines as an ATS extracts them.

## Spec format

Start from the latest spec in `output/`. Top-level keys:

- `colors`: `base`, `primary`, `secondary` (hex).
- `header`: `name`, `title`, `subtitle`, `links` (`text`, `url`; all on one line, 3 to 5 spaces apart), `contacts` (`icon`: `mail` | `call` | `location_on`, `text`, optional `url`).
- `sections`: ordered list. Types:
  - `paragraphs`: `items` of `{label, text}`, optional `gap` (twips after each item). Summary, Skills.
  - `entries`: `items` of `{title, org, meta, subtitle, lines, bullets, titleSize}`, optional `keepTogether` and a trailing `list` of `{title, year}` one-liners. Experience, Education, Publications, Personal projects, Certifications.
  - `lines`: `items` of `{text, gapBefore}`. Languages and availability.
- Rich text (`text`, `meta`, `lines`, `bullets`, `subtitle`): a string or a list of segments `{text, style: primary | secondary | bold, url}`.

## Requirements

- Node.js, then `npm install` once in `tools/` (the script runs it if `node_modules` is missing).
- Python 3 with `fonttools` and `Pillow`.
- LibreOffice (`soffice`) and poppler-utils (`pdftotext`, `pdffonts`, `pdfinfo`).
- Poppins installed, findable with `fc-match`.

## Credits

Icons in `icons/` are Material Symbols (Rounded, filled) by Google, Apache License 2.0. The `.png` files are black masks used to build the coloured fallback images.
