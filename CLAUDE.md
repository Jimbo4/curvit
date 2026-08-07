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

- Section order in every generated CV is fixed: Summary, Experience, Education, Publications, Personal projects, Skills, Languages.
- Right after the Languages section, always add the availability lines (see the "Availability" section of the master).
- Experiences are listed in reverse chronological order: the most recent is always first.
- Experience titles are always in the form "Role - Company".
- Ongoing positions: `period: MM/YYYY – present` and `duration: ongoing`. Ended positions: fixed period and rounded duration (e.g. "2 years").
- Training/instructor activities are NOT a separate section: they live as bullets inside the experience where they happened.
- There is no Inbox section: Jacopo requests changes directly via chat.
- Each experience has: metadata and "Available bullets:" (tagged).
- Skills and tools are NOT repeated inside experiences, education or projects: they all live in the single "Main Tools / Skills (full pool)" section of the master, grouped by tag.

## Generation rules (layout and style)

- Voice: in the generated CV use an impersonal style (no "I ..."), even though the master pool is written in first person. Rewrite the bullets accordingly.
- Client names: always frame them as examples, with wording like "clients such as ..." or "including ...", never as an exhaustive list.
- Separators: use `|` as the inline separator, never `•`.
- Never use the em dash. Use commas, brackets, colons or semicolons depending on the context; a line break or formatting can also replace it.
- Summary: never a wall of text. If it gets long, split it into short paragraphs so it stays pleasant to read for a human.
- Colours: before generating a CV, always ask Jacopo for three colours:
  1. base colour, for body text;
  2. primary colour, for section titles, experience titles, personal project names, publication names, and graphic elements such as rules and separators;
  3. secondary colour, for subtitles and the names of the companies he worked for.
- Respect the Gestalt law of proximity: a heading must sit closer to the block it introduces than to the preceding one, and related items must be grouped with tighter spacing than unrelated ones.

## Output rules

- By default, create every generated file (CVs, drafts, exports) inside the project's `./output` folder. That folder is git-ignored.
- Never overwrite an existing output file: always create a new version with a timestamp in the filename, format `YYYYMMDD_HHmm` (e.g. `cv_jacopo_marcolini_20260807_1830.pdf`).

## Tags

- Claude chooses the tags autonomously, based on what fits best. Current pool: design, dev, pm, leadership, b2b, training, ai-training, presales, research, soft. New tags can be added when needed.

## When editing the master

- Enrich raw notes into polished tagged bullets; ask Jacopo only when key information is missing (dates, numbers, scope).
- Add any new tool or skill to "Main Tools / Skills (full pool)" only, in the right tag group.
- Update this file if a new rule or important information is found.
