"""Offline evidence only: read existing art, write diagnostics beside this script."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw
from tools.check_native_pilot import read

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
EXP = ROOT / 'docs/experiments'
CASES = [
    ('A-left Terra', EXP / '2026-10-30-idle-breathing-comparison/terra', [0, 1, 2, 3]),
    ('A-right Sol', EXP / '2026-10-30-natural-idle-sol', [0, 1, 2, 3]),
    ('B redraw', EXP / '2026-10-30-redrawn-breathing-sol', list(range(8))),
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def compose(d, f):
    im = Image.new('RGBA', tuple(d['canvas']))
    for layer, meta in enumerate(d['layers']):
        assert meta['type'] == 0 and meta['level'] == 0
        if not meta['flags'] & 1:
            continue
        assert meta['blend'] == 0 and meta['opacity'] == 255
        cel = d['cels'].get((f, layer))
        if cel:
            assert cel['opacity'] == 255 and cel['z'] == 0
            im.alpha_composite(cel['image'])
    return im


def matte(im, color):
    result = Image.new('RGBA', im.size, (*color, 255))
    result.alpha_composite(im)
    return result.convert('RGB')


def verify_gif(p, sequences):
    gif = Image.open(p)
    assert gif.n_frames == len(sequences[0])
    durations, equal, backgrounds = [], [], []
    for f in range(gif.n_frames):
        gif.seek(f)
        actual = gif.convert('RGB')
        bg = actual.getpixel((0, 0))
        expected = Image.new('RGB', actual.size, bg)
        for panel, frames in enumerate(sequences):
            expected.paste(matte(frames[f], bg).resize((384, 576), Image.Resampling.NEAREST), (panel * 384, 0))
        equal.append(actual.tobytes() == expected.tobytes())
        durations.append(gif.info['duration'])
        backgrounds.append(bg)
    assert all(equal)
    return dict(path=str(p.relative_to(ROOT)), sha256=sha(p), size=gif.size,
                durations_ms=durations, cycle_ms=sum(durations), loop=gif.info.get('loop'),
                all_decoded_frames_equal_native=all(equal), matte_rgb=backgrounds[0])


def main():
    result, sequences = {'sequences': []}, []
    sheet = Image.new('RGB', (8 * 320, 3 * 254), '#34363a')
    draw = ImageDraw.Draw(sheet)
    # Equal matte/scale, actual unregistered body crops; labels include native time.
    # Registration must follow a named anatomical region, not this crop rectangle.
    for row, (label, directory, selected) in enumerate(CASES):
        native = directory / 'pass01.aseprite'
        d = read(native)
        frames = [compose(d, f) for f in range(len(d['frames']))]
        sequences.append(frames)
        base_colors = {c[:3] for c in frames[0].get_flattened_data() if c[3]}
        new_colors = [len({c[:3] for c in im.get_flattened_data() if c[3]} - base_colors) for im in frames]
        for f, im in enumerate(frames):
            assert im.tobytes() == Image.open(directory / f'frame-{f}.png').convert('RGBA').tobytes()
        for col, f in enumerate(selected):
            x, y = col * 320, row * 254
            draw.text((x + 5, y + 4), f'{label} F{f+1}: {d["frames"][f]["duration_ms"]}ms', fill='white')
            sheet.paste(matte(frames[f], (52, 54, 58)).crop((32, 32, 96, 78)).resize((320, 230), Image.Resampling.NEAREST), (x, y + 24))
        result['sequences'].append(dict(label=label, native=str(native.relative_to(ROOT)),
            sha256=sha(native), canvas=d['canvas'], layer_count=len(d['layers']),
            frame_count=len(frames), native_equals_all_exports=True,
            new_visible_RGB_per_frame=new_colors,
            durations_ms=[f['duration_ms'] for f in d['frames']]))
    sheet.save(OUT / 'independent-torso-contact.png')
    result['gifs'] = [
        verify_gif(EXP / '2026-10-30-natural-idle-sol/proof/terra-left-sol-right-3x.gif', sequences[:2]),
        verify_gif(EXP / '2026-10-30-redrawn-breathing-sol/proof/neutral-3x.gif', sequences[2:]),
    ]
    for gif, seq in zip(result['gifs'], [0, 2]):
        assert gif['durations_ms'] == result['sequences'][seq]['durations_ms']
    # Head is a rigid registration case, unlike deforming cloth. This is a
    # protection observation, not an assumed mapping of the shirt or jacket.
    b = sequences[2]
    result['B_raised_head_registered_exact_above_y30'] = {
        str(f+1): b[f].crop((0, 0, 128, 30)).tobytes() == b[0].crop((0, 1, 128, 31)).tobytes()
        for f in [3, 4, 5]
    }
    result['B_visible_shirt_witness_x60_to64_y57'] = {
        str(f+1): ['#%02x%02x%02x' % b[f].getpixel((x, 57))[:3] for x in range(60, 65)]
        for f in [0, 3, 4, 5]
    }
    result['all_three_rest_composites_equal'] = len({s[0].tobytes() for s in sequences}) == 1
    result['limits'] = 'Static diagnostic; no actual-speed viewing, art score, or gameplay validation. No cloth registration inferred from head movement.'
    (OUT / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
