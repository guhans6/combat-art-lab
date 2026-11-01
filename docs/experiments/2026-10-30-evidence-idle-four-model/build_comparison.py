"""Faithful comparison packaging only, from delivered transparent PNGs/timings."""
from pathlib import Path
import hashlib
import html
import json
from PIL import Image

OUT = Path(__file__).resolve().parent
NAMES = {'luna56-max': 'Luna 5.6 Max', 'luna6-max': 'Luna 6 Max',
         'terra56': 'Terra 5.6', 'sol61': 'Sol 6.1'}


def main():
    proof = json.loads((OUT / 'parent-technical-checks.json').read_text())
    target = OUT / 'comparison'
    target.mkdir(exist_ok=True)
    cards, metadata = [], {}
    for name, label in NAMES.items():
        report = proof['artists'][name]
        if report['status'] not in {'technical_delivery_pass', 'alpha_review_required'}:
            cards.append(f'<article><h2>{html.escape(label)}</h2><p>{html.escape(report["status"])}</p></article>')
            continue
        folder = OUT / name
        delivery = json.loads((folder / 'delivery.json').read_text())
        indices = report['gif_native_frame_indices_0based']
        frames = [Image.open(folder / delivery['frames'][i]).convert('RGBA') for i in indices]
        durations = [delivery['durations_ms'][i] for i in indices]
        rgb = []
        for im in frames:
            matte = Image.new('RGBA', im.size, '#34363a')
            matte.alpha_composite(im)
            rgb.append(matte.convert('RGB'))
        colors = sorted(set(c for im in rgb for c in im.get_flattened_data()))
        assert len(colors) <= 256, 'Cannot create faithful indexed GIF without quantization'
        mapping = {c: i for i, c in enumerate(colors)}
        palette = [channel for color in colors for channel in color] + [0] * (768 - 3 * len(colors))
        indexed = []
        for im in rgb:
            p = Image.new('P', im.size)
            p.putpalette(palette)
            p.putdata([mapping[c] for c in im.get_flattened_data()])
            indexed.append(p)
        dest = target / f'{name}-common-1x.gif'
        indexed[0].save(dest, save_all=True, append_images=indexed[1:], duration=durations,
                        loop=0, optimize=False, disposal=2)
        # Use the same timeline verifier as the parent native/export audit.
        from check_deliveries import gif_check
        exact = gif_check(dest, frames, durations, 1)
        zoom = [p.resize((384, 576), Image.Resampling.NEAREST) for p in indexed]
        dest3 = target / f'{name}-common-3x.gif'
        zoom[0].save(dest3, save_all=True, append_images=zoom[1:], duration=durations,
                      loop=0, optimize=False, disposal=2)
        exact3 = gif_check(dest3, frames, durations, 3)
        metadata[name] = {'path': str(dest.relative_to(OUT)), 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
                          'zoom_path': str(dest3.relative_to(OUT)), 'zoom_sha256': hashlib.sha256(dest3.read_bytes()).hexdigest(),
                          'native_frame_indices_0based': indices, 'durations_ms': durations,
                          'faithful_timeline_check': exact, 'faithful_3x_timeline_check': exact3}
        native = html.escape('../' + report['native'], quote=True)
        record = html.escape('../' + report['record'], quote=True)
        status = ('Native/export checks passed; visual selection pending.' if report['status'] == 'technical_delivery_pass'
                  else 'Initial version: seam repair pending.')
        cards.append(f'''<article><h2>{html.escape(label)}</h2>
<p>{len(frames)} displayed poses / {sum(durations)} ms; independent original timing</p>
<p>{html.escape(status)}</p>
<img src="{dest.name}" width="256" height="384" alt="{html.escape(label)} idle at 2x display">
<p><a href="{dest.name}">Native 1x GIF</a> · <a href="{native}">Native source</a> · <a href="{record}">Artist record</a></p></article>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Four independent idle studies</title><style>
body{font:16px system-ui;background:#202225;color:#f1f1ef;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}article{background:#34363a;border-radius:12px;padding:16px}h1{font-size:24px}h2{font-size:20px}img{image-rendering:pixelated;display:block;margin:auto}a{color:#a9d3ff}p{line-height:1.45}
</style><h1>Four independent idle studies</h1><p>Same character, starting source and video evidence; fresh artist contexts. Common matte and 2x display. Each GIF loops with its own authored timing. No synchronized timing, ranking, user approval or Godot validation is implied.</p><main>'''
    (target / 'index.html').write_text(page + '\n'.join(cards) + '</main></html>\n')
    (target / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps({name: row['path'] for name, row in metadata.items()}, indent=2))


if __name__ == '__main__':
    main()
