# Instructions - CV project (curvit)

Read this file before working on `cv_master.md` or generating any CV.
Content lives in `cv_master.md`; rules live here. Keep the two in sync: if a rule changes the shape of the content, update the master too.

## Purpose

- `cv_master.md` is a master pool of content, not a CV itself. Tailored CVs are generated from it by selecting bullets via tags. Bullets are alternatives to pick from, they can also be included in full but it isn't mandatory.

## Language and style (master file)

- The master is written in English only, always. Translate any Italian input before adding it.
- First person for experience bullets ("I manage...", past tense for ended roles, present tense for ongoing ones).
- Quantify where possible (team size, budget, users, contract value, audience size).

## Structure rules

- Section order in every generated CV is fixed: Summary, Experience, Education, Publications, Personal projects, Skills, Certifications, Languages.
- Certifications: professional or mandatory certifications. Each has date, standard/reference and tags. Always include all of them in every generated CV, whatever the target role.
- Right after the Languages section, always add the availability lines (see the "Availability" section of the master).
- Experiences are listed in reverse chronological order: the most recent is always first.
- Experience titles are always in the form "Role - Company".
- Ongoing positions: `period: MM/YYYY – present` and `duration: ongoing`. Ended positions: fixed period and rounded duration (e.g. "2 years").
- Work experiences in a generated CV have at most 5 bullets each. Pick the 5 most significant for the target role; when needed, merge two related bullets into one point, written discursively and coherently.
- Training/instructor activities are NOT a separate section: they live as bullets inside the experience where they happened.
- There is no Inbox section: Jacopo requests changes directly via chat.
- Each experience has: metadata and "Available bullets:" (tagged).
- Entries are self-contained: a bullet never mentions another entry (employer, role or project), unless it explains a change of employer such as an acquisition. The Summary never links two entries.
- Personal projects have two shapes: a one-liner (title, year or period, tags) or a full entry shaped like an experience (metadata and "Available bullets:"). A full entry uses the title "Name - Short descriptor", a period without duration and a one-line description, always shown in generated CVs.
- Matcha always lives in Personal projects, never in Experience, so employers do not read it as a full-time job.
- Skills and tools are NOT repeated inside experiences, education or projects: they all live in the single "Main Tools / Skills (full pool)" section of the master, grouped by tag.
- ATS keywords: the generated CV always includes the FULL skills pool from the master, every tool and skill in every group, never a subset. Automatic ATS screeners match on keywords, so no keyword may be dropped to save space: recover space by shortening bullets or spacing, never by cutting skills. Only the order of the groups changes, with the ones relevant to the target role first. The more keywords the better: when a new relevant tool or skill emerges, add it to the master pool.
- Exception to the full-pool rule: the [marketing] group is optional. Include it, in full, only for roles that need marketing skills.

## Generation rules (layout and style)

- The main title in the master is a fallback. In a generated CV, never copy the job posting title verbatim: pick the best-fitting title among the master's main and secondary titles and adapt it slightly to the target role (e.g. "Senior Product Designer", "Product Lead"). Then reorder the secondary titles so the ones relevant to that role come first.
- Voice: in the generated CV use an impersonal style (no "I ..."), even though the master pool is written in first person. Rewrite the bullets accordingly.
- Client names: always frame them as examples, with wording like "clients such as ..." or "including ...", never as an exhaustive list.
- Separators: use `|` as the inline separator for lists (contacts metadata, experience metadata, languages), never `•`. Between role and company (and between publication venue and DOI) use `-`, e.g. "AI Business Developer - DGS".
- Lead-in labels (in Summary paragraphs and Skills groups) are followed by a colon, e.g. "Leadership & Delivery: ...", never by `·` or other separators.
- Duration goes in parentheses right after the period, e.g. "03/2026 – present (ongoing) | Milan, Italy" or "03/2024 – 12/2025 (2 years) | Milan, Italy".
- Education metadata order: period | location | grade (grade last).
- Contacts: links first, then email, phone and location. Link order: portfolio (always first), LinkedIn, GitHub, then any future links. They share the first line, separated by 3 to 5 spaces depending on the available width (the generation script picks the count; if they do not fit, they wrap onto a second links line). Below, one per line: email, phone, location. Links and email are clickable but visually discreet: body colour, no underline.
- Contact icons: each contact is preceded by a generic Material Symbols icon in the primary colour, separated from the text by a single space: `link` for every link (portfolio, LinkedIn, GitHub and future ones), `mail`, `call`, `location_on`. Insert the icons as small inline images in the document body, never as icon-font glyphs or emoji: when an ATS extracts the text, glyphs turn into stray characters that can break email and phone parsing. The full contact text always stays visible; no tables, text boxes or page headers for contacts.
- Never use the em dash. Use commas, brackets, colons or semicolons depending on the context; a line break or formatting can also replace it.
- Never use two or more consecutive spaces (spacebar whitespace): spacing between words is always a single space, as per standard Word writing rules. Visual separation is obtained with tabs, indents or spacing properties, not repeated spaces. The only exception is the 3 to 5 spaces between links in the contacts.
- Fonts: set weights through the bold property of a base family (e.g. font "Poppins" + bold), never through a weight-named family such as "Poppins Bold", unless that exact family is embedded in the .docx. Otherwise the PDF export falls back to a substitute font (e.g. DejaVu Serif). After exporting, check the fonts embedded in the PDF.
- Embed Poppins Regular and Bold in the .docx, so Word renders it identically on machines without Poppins.
- List bullets use `•` (U+2022). Poppins has no `■` or `▪`: those glyphs fall back to another font (e.g. DejaVu Sans) in the PDF.
- Typography: one single uniform body size for all body text, no small size variations between sections. Section titles are clearly larger and heavier (bold weight) to mark the hierarchy.
- Summary: never a wall of text. If it gets long, split it into short paragraphs so it stays pleasant to read for a human.
- Summary: the Leadership & Delivery paragraph includes quantitative project figures (team size, budgets, projects per year, users).
- Summary: when a paragraph ends with a mostly empty last line, add a sentence with further relevant information to fill it.
- Incidental clauses, such as a short description of an entry, go in brackets to keep the sentence readable, e.g. "Co-founder of Matcha (a dating app developed as a personal project), leading ...".
- Colours: before generating a CV, always ask Jacopo for three colours:
  1. base colour, for body text;
  2. primary colour, for section titles, experience titles, personal project names, publication names, and graphic elements such as rules and separators;
  3. secondary colour, for subtitles and the names of the companies he worked for.
- Avoid orphans: the last line of a paragraph or bullet must contain at least 3 words; a last line with only 1 or 2 words (e.g. "teams.", "Graph", "media (2020)") is an orphan. Fix it by rephrasing the sentence; in skill lists, reorder the items within the group (never drop a keyword). Exact titles that cannot be rephrased (e.g. a paper title) are the only exception: their font size may be reduced by 0.5 pt (the smallest step a .docx supports). This is a rare exception: standard font sizes stay fixed everywhere else. The generation script reports possible orphans; fix them in the spec and regenerate.
- Respect the Gestalt law of proximity: a heading must sit closer to the block it introduces than to the preceding one, and related items must be grouped with tighter spacing than unrelated ones.

## Output rules

- By default, create every generated file (CVs, drafts, exports) inside the project's `./output` folder. That folder is git-ignored.
- Each CV has its own subfolder in `./output`, named after the CV base name followed by the target company in lowercase snake_case, when there is one (e.g. `output/20260810_cv_jacopo_marcolini_product_lead_satispay/`). The folder holds all the files of that CV: `.json` spec, `.docx`, `.pdf` and any related file such as a cover letter, all named without the company (e.g. `20260810_cv_jacopo_marcolini_product_lead.pdf`). No CV file sits loose in `./output`.
- File naming: date prefix at the start of the filename, format `YYYYMMDD_`, followed by `cv_jacopo_marcolini_` and the target position in lowercase snake_case, to tell outputs apart (e.g. `20260810_cv_jacopo_marcolini_product_lead.docx`). The target company never appears in file names: it goes only in the CV folder name.
- Never overwrite an existing output file: if a CV folder with the same name already exists for the same day, add the time (`YYYYMMDD_HHmm_`) to both the folder and the file names to disambiguate.
- Alongside every generated `.docx`, also export the matching `.pdf` with the same base name.
- The JSON spec of each generated CV stays in its CV folder next to its `.docx` and `.pdf` (same base name): it is the source to regenerate or tweak that CV, not a temporary file.
- Temporary files created as intermediate steps (previews, conversion leftovers such as `.tmp` files) must be deleted once the final output is ready. Jacopo has given permission for this cleanup.

## Generation script

- Generate every CV with `tools/build_cv.py`, to keep layout rules consistent and save tokens: Claude writes only the content spec, the script does the rest.
- Usage: `python3 tools/build_cv.py output/<base_name>_<company>/<base_name>.json [--overwrite]`: create the CV folder and write the spec there first; the outputs are written next to the spec. The script builds the `.docx` (via `tools/build_docx.js`), embeds Poppins Regular and Bold, colours the icons, exports the `.pdf` with LibreOffice and prints a report: fonts embedded in the PDF, pages, em dashes, double spaces, possible orphans, contact lines as an ATS reads them. It refuses to overwrite existing files without `--overwrite`.
- The spec is a JSON file: base name, colours, header (name, title, subtitle, links, contacts) and an ordered list of sections. Use the latest spec in `./output` (inside its CV folder) as the template for a new one. Section types: `paragraphs` (labelled paragraphs: Summary, Skills), `entries` (experience, education, publications, projects, certifications: title, org, meta, subtitle, lines, bullets, optional `titleSize` and a trailing `list` of one-liners), `lines` (Languages and availability). Rich text is a string or a list of segments `{text, style: primary|secondary|bold, url}`.
- Layout constants (fonts, sizes, spacing, margins, keep-together rules) live in the script: change them there, not in the spec, and update this file if a rule changes.
- Requirements: Node.js (run `npm install` once in `tools/`), Python 3 with fontTools and Pillow, LibreOffice (`soffice`), poppler-utils (`pdftotext`, `pdffonts`), Poppins installed (`fc-match` must find it).

## Tags

- Claude chooses the tags autonomously, based on what fits best. Current pool: design, dev, pm, leadership, b2b, training, ai-training, presales, research, soft, safety, marketing. New tags can be added when needed.

## When editing the master

- Enrich raw notes into polished tagged bullets; ask Jacopo only when key information is missing (dates, numbers, scope).
- Add any new tool or skill to "Main Tools / Skills (full pool)" only, in the right tag group.
- Update this file if a new rule or important information is found.
