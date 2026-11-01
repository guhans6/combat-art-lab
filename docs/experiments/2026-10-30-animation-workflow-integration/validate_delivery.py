"""Validate maintained links/schema, preservation and a standalone portable bundle.

Run from the repository root. --package creates the new archive exactly once;
subsequent runs read it and assert its complete equality to the canonical skill.
No editor calls, artwork writes, network access or dependency installation.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import re
import subprocess
import tempfile
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / 'tools/pixel-art-director'
ARCHIVE = OUT / 'pixel-art-director-2026-10-30-animation-continuity-v1.zip'
DOCS = ['docs/workflow/art-production.md', 'docs/art/motion-guide.md',
        'docs/art/style-guide.md', 'docs/handoff.md']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix != '.pyc')


def anchors(p):
    result = set()
    for heading in re.findall(r'^#{1,6} (.+)$', p.read_text(), re.M):
        text = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        result.add(text)
    return result


def check_links(documents):
    checked = 0
    for p in documents:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
            if re.match(r'^[a-zA-Z][\w+.-]*:', target):
                continue
            path, _, fragment = unquote(target).partition('#')
            dest = (p.parent / path).resolve() if path else p
            assert dest.exists(), (p, target)
            if fragment and dest.suffix == '.md':
                assert fragment in anchors(dest), (p, target, sorted(anchors(dest)))
            checked += 1
    return checked


def schema(folder):
    # A real YAML parser, independent of unavailable Python PyYAML. This is
    # supplementary validation, not a replacement claim for quick_validate.py.
    ruby = '''require 'yaml'; require 'json'
text = File.read(ARGV[0]); match = text.match(/\\A---\\n(.*?)\\n---/m)
abort 'Missing frontmatter' unless match
puts JSON.generate(YAML.safe_load(match[1]))
'''
    raw = subprocess.run(['ruby', '-e', ruby, str(folder / 'SKILL.md')],
                         check=True, capture_output=True, text=True)
    meta = json.loads(raw.stdout)
    assert set(meta) <= {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    assert meta['name'] == 'pixel-art-director'
    assert re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', meta['name']) and len(meta['name']) <= 64
    desc = meta['description']
    assert isinstance(desc, str) and 0 < len(desc) <= 1024 and '<' not in desc and '>' not in desc
    assert not re.search(r'^\s*\[TODO:', (folder / 'SKILL.md').read_text(), re.M)
    return {'yaml_parser': 'Ruby Psych safe_load', 'name': meta['name'],
            'description_characters': len(desc)}


def main(package):
    protected = json.loads((OUT / 'protected-inputs-before.json').read_text())
    violations = [path for path, digest in protected.items()
                  if not (ROOT / path).is_file() or sha(ROOT / path) != digest]
    assert not violations, violations
    assert (ROOT / '.agents/skills/pixel-art-director').resolve() == SKILL
    source_files = files(SKILL)
    source_links = check_links([p for p in source_files if p.suffix == '.md'])
    source_schema = schema(SKILL)
    # Check every newly introduced link in maintained project files. Preexisting
    # broken historical links, if any, are outside this change's ownership.
    project_new_links = []
    patch = []
    for relative in DOCS + [str(p.relative_to(ROOT)) for p in source_files if p.suffix == '.md']:
        before = OUT / 'baseline' / relative
        after = ROOT / relative
        old = before.read_text() if before.exists() else ''
        delta = list(difflib.unified_diff(old.splitlines(True), after.read_text().splitlines(True),
                     fromfile='before/' + relative, tofile='after/' + relative))
        patch.extend(delta)
        if relative in DOCS:
            # Parse only added-line links but resolve them from the real doc path.
            for line in delta:
                if line.startswith('+') and not line.startswith('+++'):
                    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', line):
                        if re.match(r'^[a-zA-Z][\w+.-]*:', target):
                            continue
                        path, _, fragment = unquote(target).partition('#')
                        dest = (after.parent / path).resolve() if path else after
                        assert dest.exists(), (relative, target)
                        if fragment and dest.suffix == '.md':
                            assert fragment in anchors(dest), (relative, target)
                        project_new_links.append([relative, target])
    (OUT / 'maintained-changes.patch').write_text(''.join(patch))
    if package:
        with zipfile.ZipFile(ARCHIVE, 'x', compression=zipfile.ZIP_DEFLATED) as z:
            for p in source_files:
                z.write(p, 'pixel-art-director/' + str(p.relative_to(SKILL)))
    expected = {'pixel-art-director/' + str(p.relative_to(SKILL)): sha(p) for p in source_files}
    with tempfile.TemporaryDirectory(prefix='combat-art-animation-package-') as tmp:
        with zipfile.ZipFile(ARCHIVE) as z:
            assert z.testzip() is None
            assert set(z.namelist()) == set(expected)
            for name in z.namelist():
                assert not name.startswith('/') and '..' not in Path(name).parts
            z.extractall(tmp)
        extracted = Path(tmp) / 'pixel-art-director'
        assert {str(p.relative_to(Path(tmp))): sha(p) for p in files(extracted)} == expected
        extracted_links = check_links([p for p in files(extracted) if p.suffix == '.md'])
        extracted_schema = schema(extracted)
        # Different cwd and a fresh extracted folder: no repo import dependency.
        test = subprocess.run([__import__('sys').executable, '-B', '-m', 'unittest',
                              'discover', '-s', str(extracted / 'tests'), '-v'],
                              cwd=tmp, capture_output=True, text=True)
        (OUT / 'extracted-tests.txt').write_text(test.stdout + test.stderr)
        assert test.returncode == 0, test.stdout + test.stderr
        assert 'Ran 35 tests' in test.stderr
    (OUT / 'bundle-manifest.json').write_text(json.dumps(expected, indent=2) + '\n')
    result = dict(protected_files=len(protected), protected_violations=violations,
                  source_local_links=source_links, extracted_local_links=extracted_links,
                  new_project_links=project_new_links, source_schema=source_schema,
                  extracted_schema=extracted_schema, extracted_tests=35,
                  archive=ARCHIVE.name, archive_sha256=sha(ARCHIVE), bundled_files=len(expected),
                  quick_validate='Not run successfully: Python PyYAML unavailable; see verification.md',
                  local_skill_symlink_resolves_to_canonical=True)
    (OUT / 'delivery-validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', action='store_true')
    main(parser.parse_args().package)
