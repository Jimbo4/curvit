#!/usr/bin/env node
// Builds the CV .docx from the resolved layout JSON written by build_cv.py.
// Do not call it directly: run `python3 tools/build_cv.py output/<name>.json`.
// Usage: node build_docx.js <layout.json> <out.docx>
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink, AlignmentType, ImageRun,
  LevelFormat, TabStopType, BorderStyle, Tab, CharacterSet,
} = require('docx');

const [, , layoutPath, outPath] = process.argv;
const L = JSON.parse(fs.readFileSync(layoutPath, 'utf8'));
const K = L.layout; // layout constants, defined once in build_cv.py
const C = L.colors;
const FONT = K.font;
const hp = (pt) => Math.round(pt * 2); // points to half-points (.docx sizes move in 0.5 pt steps)
const BODY = hp(K.bodyPt), ITEM = hp(K.itemPt), SECTION = hp(K.sectionPt), TITLE = hp(K.titlePt), NAME = hp(K.namePt);
const RIGHT = K.pageW - 2 * K.marginLR;

// ---------- text helpers ----------
const run = (text, o = {}) => new TextRun({
  text, font: FONT, size: o.size || BODY, color: o.color || C.base, bold: !!o.bold, characterSpacing: o.spacing,
});
const link = (text, url, o = {}) => new ExternalHyperlink({ link: url, children: [run(text, o)] });
const STYLE = {
  primary: { bold: true, color: C.primary },
  secondary: { bold: true, color: C.secondary },
  bold: { bold: true },
};
// rich text: a string or a list of segments {text, style, url}
const rich = (x, base = {}) => (typeof x === 'string' ? [{ text: x }] : x).map((s) => {
  const o = { ...base, ...(STYLE[s.style] || {}) };
  return s.url ? link(s.text, s.url, o) : run(s.text, o);
});
const icon = (name) => new ImageRun({
  type: 'svg', data: fs.readFileSync(L.icons[name].svg),
  fallback: { type: 'png', data: fs.readFileSync(L.icons[name].png) },
  transformation: { width: K.iconPx, height: K.iconPx },
  altText: { name: `${name} icon`, title: '', description: '' },
});

// ---------- paragraph builders ----------
const para = (children, o = {}) => new Paragraph({
  spacing: { before: o.before || 0, after: o.after || 0 }, keepNext: !!o.keepNext, keepLines: true, children,
});
const sectionTitle = (text) => new Paragraph({
  keepNext: true, keepLines: true,
  spacing: { before: K.sectionBefore, after: K.sectionAfter },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: C.primary, space: 3 } },
  children: [run(text.toUpperCase(), { size: SECTION, bold: true, color: C.primary, spacing: 20 })],
});
// title line: "Title - Org" on the left, optional metadata right-aligned on the same line
const entryTitle = (e, first) => {
  const size = e.titleSize ? hp(e.titleSize) : ITEM;
  const left = [run(e.title, { size, bold: true, color: C.primary })];
  if (e.org) left.push(run(' - ', { size, bold: true, color: C.primary }), run(e.org, { size, bold: true, color: C.secondary }));
  const right = e.meta ? [new TextRun({ children: [new Tab()], font: FONT, size: BODY }), ...rich(e.meta)] : [];
  return new Paragraph({
    keepNext: true, keepLines: true,
    spacing: { before: first ? 0 : K.entryBefore, after: 40 },
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT }],
    children: [...left, ...right],
  });
};
const bullet = (children, keepNext) => new Paragraph({
  numbering: { reference: 'bullets', level: 0 }, spacing: { after: 30 }, keepLines: true, keepNext, children,
});
// the last two bullets of a list always stay on the same page
const bullets = (items) => items.map((t, i) => bullet(rich(t), i === items.length - 2));

// ---------- sections ----------
const paragraphsSection = (sec) => [
  sectionTitle(sec.title),
  ...sec.items.map((it, i) => new Paragraph({
    keepLines: true,
    spacing: { after: i === sec.items.length - 1 ? 0 : (sec.gap ?? 60) },
    children: [run(it.label + ': ', { bold: true, color: C.secondary }), ...rich(it.text)],
  })),
];

const entriesSection = (sec) => {
  const out = [sectionTitle(sec.title)];
  sec.items.forEach((e, idx) => {
    const lastItem = idx === sec.items.length - 1;
    const lines = e.lines || [];
    const hasBullets = (e.bullets || []).length > 0;
    const glue = sec.keepTogether && !lastItem; // keep the whole section on one page
    out.push(entryTitle(e, idx === 0));
    if (e.subtitle) out.push(para(rich(e.subtitle, STYLE.secondary), { after: 20, keepNext: lines.length > 0 || hasBullets || glue }));
    lines.forEach((l, i) => {
      const last = i === lines.length - 1;
      out.push(para(rich(l), { after: last ? (hasBullets ? 40 : 0) : 20, keepNext: !last || hasBullets || glue }));
    });
    if (hasBullets) out.push(...bullets(e.bullets));
  });
  if (sec.list && sec.list.length) { // one-liners, e.g. minor personal projects
    out.push(para([], { before: K.blockGap }));
    sec.list.forEach((o) => out.push(bullet([run(o.title, { bold: true, color: C.primary }), run(` (${o.year})`)], false)));
  }
  return out;
};

const linesSection = (sec) => [
  sectionTitle(sec.title),
  ...sec.items.map((it) => para(rich(it.text), { before: it.gapBefore ? K.blockGap : 0 })),
];

const BUILDERS = { paragraphs: paragraphsSection, entries: entriesSection, lines: linesSection };

// ---------- header ----------
const H = L.header;
const header = [
  para([run(H.name, { size: NAME, bold: true, color: C.primary })]),
  para([run(H.title, { size: TITLE, bold: true, color: C.secondary })], { before: 40, after: 40 }),
  para(rich(H.subtitle), { after: 140 }),
  // links on one line, separated by the number of spaces computed by build_cv.py (3 to 5)
  ...H.linkLines.map((ln) => para(ln.items.flatMap((it, i) => [
    ...(i ? [run(' '.repeat(ln.gap))] : []), icon('link'), run(' '), link(it.text, it.url),
  ]), { after: 20 })),
  ...H.contacts.map((c) => para([icon(c.icon), run(' '), c.url ? link(c.text, c.url) : run(c.text)], { after: 20 })),
];

// ---------- document ----------
const doc = new Document({
  creator: H.name,
  title: `CV ${H.name}`,
  fonts: [
    { name: FONT, data: fs.readFileSync(L.fonts.regular), characterSet: CharacterSet.ANSI },
    // registered under a temporary name; build_cv.py moves it to the embedBold slot of the base family
    { name: 'EmbedBoldTmp', data: fs.readFileSync(L.fonts.bold), characterSet: CharacterSet.ANSI },
  ],
  styles: {
    default: {
      document: {
        run: { font: FONT, size: BODY, color: C.base, language: { value: K.language } },
        paragraph: { spacing: { line: 240, before: 0, after: 0 } },
      },
    },
  },
  numbering: {
    config: [{
      reference: 'bullets',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: K.bulletIndent, hanging: K.bulletHanging } },
          run: { font: FONT, color: C.primary, size: BODY },
        },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: K.pageW, height: K.pageH },
        margin: { top: K.marginTop, bottom: K.marginBottom, left: K.marginLR, right: K.marginLR, header: 400, footer: 400 },
      },
    },
    children: [...header, ...L.sections.flatMap((s) => BUILDERS[s.type](s))],
  }],
});

Packer.toBuffer(doc).then((buf) => fs.writeFileSync(outPath, buf));
