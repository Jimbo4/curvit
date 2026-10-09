#!/usr/bin/env python3
"""Generate a CV (.docx + .pdf) from a JSON content spec.

Usage:
    python3 tools/build_cv.py output/<base_name>.json [--overwrite] [--keep-temp]

The spec holds content only (see CLAUDE.md, section "Generation script").
Layout constants live in LAYOUT below; build_docx.js reads them from here.
Outputs are written next to the spec, with the same base name.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image

TOOLS = Path(__file__).resolve().parent

LAYOUT = {
    'font': 'Poppins', 'language': 'en-GB',
    'bodyPt': 9, 'itemPt': 10, 'sectionPt': 12, 'titlePt': 12, 'namePt': 26,
    'pageW': 11906, 'pageH': 16838,                    # A4 in twips
    'marginLR': 794, 'marginTop': 720, 'marginBottom': 680,
    'sectionBefore': 320, 'sectionAfter': 140,         # proximity: a heading sits closer to its block
    'entryBefore': 200, 'blockGap': 140,
    'bulletIndent': 260, 'bulletHanging': 200,
    'iconPx': 11,
}
LINK_GAPS = (5, 4, 3)                                  # spaces between links, widest that fits wins
CONTENT_W = (LAYOUT['pageW'] - 2 * LAYOUT['marginLR']) / 20   # points
BULLET_W = CONTENT_W - LAYOUT['bulletIndent'] / 20
ICON_W = LAYOUT['iconPx'] * 0.75
BODY = LAYOUT['bodyPt']


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


def find_font(style):
    path = sh(['fc-match', '-f', '%{file}', f"{LAYOUT['font']}:style={style}"]).strip()
    if LAYOUT['font'].lower() not in Path(path).name.lower():
        sys.exit(f"{LAYOUT['font']} {style} is not installed (fc-match returned {path})")
    return path


class Metrics:
    """Text widths from the real font files, to predict line breaks."""

    def __init__(self, regular, bold):
        self.fonts = {}
        for key, path in (('r', regular), ('b', bold)):
            t = TTFont(path)
            self.fonts[key] = (t.getBestCmap(), t['hmtx'].metrics, t['head'].unitsPerEm)

    def width(self, text, bold=False, size=BODY):
        cmap, hmtx, upm = self.fonts['b' if bold else 'r']
        return sum(hmtx[cmap.get(ord(c), cmap[ord('?')])][0] for c in text) / upm * size

    def wrap(self, segs, width):
        """segs: [(text, bold, size)]. Greedy wrap, breaking at spaces and after hyphens."""
        lines, cur, buf = [], 0.0, ''
        for text, bold, size in segs:
            for tok in re.findall(r'[^\s-]+-?|\s+', text):
                w = self.width(tok, bold, size)
                if not tok.isspace() and cur + w > width and buf.strip():
                    lines.append(buf.rstrip())
                    buf, cur = tok, w
                else:
                    buf, cur = buf + tok, cur + w
        lines.append(buf.rstrip())
        return lines


def segs(x, bold=False, size=BODY):
    if isinstance(x, str):
        return [(x, bold, size)]
    return [(s['text'], bold or s.get('style') in ('primary', 'secondary', 'bold'), size) for s in x]


def plain(x):
    return x if isinstance(x, str) else ''.join(s['text'] for s in x)


def link_lines(links, m):
    """Pack the links on as few lines as possible, then give each line the widest gap that fits."""
    sp = m.width(' ')
    item = lambda l: ICON_W + sp + m.width(l['text'])
    lines, cur = [], []
    for l in links:
        trial = cur + [l]
        if cur and sum(map(item, trial)) + (len(trial) - 1) * min(LINK_GAPS) * sp > CONTENT_W:
            lines.append(cur)
            cur = [l]
        else:
            cur = trial
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        base = sum(map(item, ln))
        gap = next((g for g in LINK_GAPS if base + (len(ln) - 1) * g * sp <= CONTENT_W), min(LINK_GAPS))
        out.append({'gap': gap, 'items': ln})
    return out


def wrapped_blocks(spec):
    """Every paragraph that can wrap, as (where, segs, width)."""
    for sec in spec['sections']:
        kind, title = sec['type'], sec['title']
        if kind == 'paragraphs':
            for it in sec['items']:
                yield f"{title} / {it['label']}", [(it['label'] + ': ', True, BODY)] + segs(it['text']), CONTENT_W
        elif kind == 'entries':
            for e in sec['items']:
                where = f"{title} / {e['title'][:40]}"
                if not e.get('meta'):
                    head = e['title'] + (f" - {e['org']}" if e.get('org') else '')
                    yield where + ' (title)', [(head, True, e.get('titleSize', LAYOUT['itemPt']))], CONTENT_W
                for l in e.get('lines', []):
                    yield where, segs(l), CONTENT_W
                for b in e.get('bullets', []):
                    yield where, segs(b), BULLET_W
            for o in sec.get('list', []):
                yield f'{title} / list', [(o['title'], True, BODY), (f" ({o['year']})", False, BODY)], BULLET_W
        elif kind == 'lines':
            for it in sec['items']:
                yield title, segs(it['text']), CONTENT_W


def predicted_orphans(spec, m):
    out = []
    for where, sg, width in wrapped_blocks(spec):
        lines = m.wrap(sg, width)
        if len(lines) > 1 and len(lines[-1].split()) <= 2:
            out.append(f'{where}: last line "{lines[-1]}"')
    return out


def make_icons(names, color, tmp):
    rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    out = {}
    for n in names:
        svg = (TOOLS / 'icons' / f'{n}.svg').read_text(encoding='utf-8').replace('<svg ', f'<svg fill="#{color}" ', 1)
        (tmp / f'{n}.svg').write_text(svg, encoding='utf-8')
        mask = Image.open(TOOLS / 'icons' / f'{n}.png').convert('RGBA')
        solid = Image.new('RGBA', mask.size, rgb + (255,))
        solid.putalpha(mask.getchannel('A'))
        solid.save(tmp / f'{n}.png')
        out[n] = {'svg': str(tmp / f'{n}.svg'), 'png': str(tmp / f'{n}.png')}
    return out


def embed_bold(src, dst):
    """docx-js embeds one font file per family: move the bold file into the base family's embedBold slot."""
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'word/fontTable.xml':
                xml = data.decode('utf-8')
                tmp = re.search(r'<w:font w:name="EmbedBoldTmp">.*?</w:font>', xml).group(0)
                rel = re.search(r'<w:embedRegular (r:id="[^"]+" w:fontKey="[^"]+")/>', tmp).group(1)
                xml = xml.replace(tmp, '')
                pattern = r'(<w:font w:name="' + LAYOUT['font'] + r'">.*?<w:embedRegular [^>]*/>)'
                xml, n = re.subn(pattern, lambda mt: mt.group(1) + '<w:embedBold ' + rel + '/>', xml, count=1)
                assert n == 1, 'base font entry not found in fontTable.xml'
                data = xml.encode('utf-8')
            zout.writestr(info.filename, data)


def docx_paragraphs(path):
    xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
    return [''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)) for p in xml.split('</w:p>')]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('spec')
    ap.add_argument('--overwrite', action='store_true', help='replace existing .docx/.pdf with the same base name')
    ap.add_argument('--keep-temp', action='store_true', help='keep the temporary build folder')
    args = ap.parse_args()

    spec_path = Path(args.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    docx_out, pdf_out = spec_path.with_suffix('.docx'), spec_path.with_suffix('.pdf')
    if not args.overwrite and (docx_out.exists() or pdf_out.exists()):
        sys.exit(f'{docx_out.name} or {pdf_out.name} already exists: use --overwrite or a YYYYMMDD_HHmm_ name')
    if not (TOOLS / 'node_modules' / 'docx').is_dir():
        print('Installing node dependencies in tools/ ...')
        subprocess.run(['npm', 'install', '--no-audit', '--no-fund'], cwd=TOOLS, check=True)

    fonts = {'regular': find_font('Regular'), 'bold': find_font('Bold')}
    m = Metrics(fonts['regular'], fonts['bold'])
    colors = {k: v.lstrip('#').upper() for k, v in spec['colors'].items()}
    head = spec['header']
    tmp = Path(tempfile.mkdtemp(prefix='curvit_'))
    try:
        icon_names = {'link'} | {c['icon'] for c in head.get('contacts', [])}
        layout = {
            'layout': LAYOUT, 'colors': colors, 'fonts': fonts,
            'icons': make_icons(sorted(icon_names), colors['primary'], tmp),
            'header': {**head, 'linkLines': link_lines(head.get('links', []), m)},
            'sections': spec['sections'],
        }
        (tmp / 'layout.json').write_text(json.dumps(layout, ensure_ascii=False), encoding='utf-8')
        raw, final = tmp / 'raw.docx', tmp / docx_out.name
        subprocess.run(['node', str(TOOLS / 'build_docx.js'), str(tmp / 'layout.json'), str(raw)], check=True)
        embed_bold(raw, final)
        profile = (tmp / 'lo_profile').as_uri()
        subprocess.run(['soffice', f'-env:UserInstallation={profile}', '--headless', '--convert-to', 'pdf',
                        '--outdir', str(tmp), str(final)], check=True, capture_output=True, timeout=300)
        pdf = tmp / pdf_out.name

        # ---------- checks ----------
        link_texts = [l['text'] for l in head.get('links', [])]
        paras = docx_paragraphs(final)
        pdf_fonts = [l.split()[0] for l in sh(['pdffonts', str(pdf)]).splitlines()[2:] if l.strip()]
        pages = re.search(r'Pages:\s+(\d+)', sh(['pdfinfo', str(pdf)])).group(1)
        known = {head['name']} | {c['text'] for c in head.get('contacts', [])} | set(link_texts)
        known_tokens = {tok for t in known for tok in t.split()}
        pdf_short = []
        for line in sh(['pdftotext', '-layout', str(pdf), '-']).splitlines():
            s = line.strip().lstrip('\u2022').strip()
            if not s or s.isupper() or all(tok in known_tokens for tok in s.split()):
                continue  # headings, name, contacts and the links line are short on purpose
            if len(s.split()) <= 2:
                pdf_short.append(s)
        report = {
            'pages': pages,
            'pdf fonts': ', '.join(pdf_fonts),
            'non-base fonts in pdf': [f for f in pdf_fonts if LAYOUT['font'] not in f] or 'none',
            'link lines (gap)': [(len(l['items']), l['gap']) for l in layout['header']['linkLines']],
            'em dashes': [p for p in paras if '\u2014' in p] or 'none',
            'double spaces (links excluded)': [p for p in paras if '  ' in p and not any(t in p for t in link_texts)] or 'none',
            'predicted orphans': predicted_orphans(spec, m) or 'none',
            'short lines in pdf': pdf_short or 'none',
        }
        shutil.copyfile(final, docx_out)
        shutil.copyfile(pdf, pdf_out)
        print(f'written: {docx_out}\nwritten: {pdf_out}')
        for k, v in report.items():
            print(f'- {k}: {v}')
        print('- contacts as an ATS reads them:')
        for line in sh(['pdftotext', str(pdf_out), '-']).splitlines()[3:10]:
            if line.strip():
                print('    ' + line)
    finally:
        if args.keep_temp:
            print(f'temp folder kept: {tmp}')
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
