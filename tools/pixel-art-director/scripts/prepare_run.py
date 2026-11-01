#!/usr/bin/env python3
"""Freeze named art inputs into a new run directory; never modify original art."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import sys
from PIL import Image
from pixel_checks import mask_from_profile, sha256


def within(repo: Path, relative: str) -> Path:
    p = (repo / relative).resolve()
    if not p.is_relative_to(repo):
        raise ValueError(f'Input escapes repository: {relative}')
    if not p.is_file():
        raise FileNotFoundError(p)
    return p


def prepare(repo: Path, output_root: Path, run_id: str, profile_path: Path,
            model: str, host: str, backend: str) -> Path:
    repo = repo.resolve()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', run_id):
        raise ValueError('run-id must be 1-80 simple filename characters.')
    profile = json.loads(profile_path.read_text())
    for reference in profile['references']:
        if not re.fullmatch(r'[a-z0-9-]+', reference['role']):
            raise ValueError('Reference role must be a safe lowercase filename label.')
    named = [('baseline.aseprite', profile['baseline_source']), ('baseline.png', profile['baseline_png'])]
    named += [(f'reference-{i:02d}-{r["role"]}.png', r['path']) for i, r in enumerate(profile['references'])]
    inputs = [(name, within(repo, path)) for name, path in named]
    with Image.open(inputs[1][1]) as image:
        if list(image.size) != profile['canvas']:
            raise ValueError('Baseline PNG is not the native canvas in the profile; do not rescale it.')
    mask = mask_from_profile(profile)
    destination = output_root.resolve() / run_id
    destination.mkdir(parents=True, exist_ok=False)
    for sub in ('input', 'work', 'passes', 'evidence'):
        (destination / sub).mkdir()
    hashes = []
    for name, source in inputs:
        target = destination / 'input' / name
        shutil.copy2(source, target)
        original_hash = sha256(source)
        if sha256(target) != original_hash:
            raise OSError(f'Copy mismatch for {source}')
        hashes.append({'source': str(source), 'copy': f'input/{name}', 'sha256': original_hash})
    shutil.copy2(destination / 'input/baseline.aseprite', destination / 'work/candidate.aseprite')
    mask.save(destination / 'input/editable-mask.png')
    hashes.append({'source': None, 'copy': 'input/editable-mask.png', 'sha256': sha256(destination / 'input/editable-mask.png')})
    (destination / 'task.json').write_text(json.dumps(profile, indent=2) + '\n')
    (destination / 'frozen-inputs.json').write_text(json.dumps(hashes, indent=2) + '\n')
    manifest = {
        'schema': 1, 'run_id': run_id, 'task_id': profile['task_id'],
        'created_utc': datetime.now(timezone.utc).isoformat(), 'state': 'prepared_not_executed',
        'model_id_requested': model, 'model_id_actual': None,
        'host_requested': host, 'host_version': None, 'backend': backend,
        'backend_version_or_commit': None, 'aseprite_version': None,
        'skill_tree_sha256': None, 'tool_catalog_sha256': None,
        'budget': profile['budget'], 'actual_tool_calls': None,
        'duration_seconds': None, 'reported_cost': None,
        'manual_interventions': [], 'automatic_subagents': [],
        'seed_if_supported': None, 'results': {'png_checks': None, 'native_checks': None, 'human_review': None}
    }
    (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    references = '\n'.join(
        f'- {reference["role"]}: input/reference-{index:02d}-{reference["role"]}.png'
        for index, reference in enumerate(profile['references'])
    )
    brief = f'''# Frozen art-task brief

Task: {profile['task_id']}

Inspect the copied baseline and each authoritative reference before diagnosing a
difference. Record observations, uncertainty, and a small visible hypothesis before
editing. The profile defines the native canvas, editable region, permitted native
ownership (when supplied), reference roles, and budget; it is the task authority.

References:
{references}

Work only on `work/candidate.aseprite` and new pass files. Preserve content outside
the editable region and any declared protected layers/frames. Retain the existing
palette and pixel construction unless this profile explicitly authorizes a change.
Do not replace this bounded native task with a redraw or imported resized reference.

At each pass, export and inspect the actual candidate with the references, best
eligible prior, and baseline at native size plus useful integer zoom and full-asset
context. Verify scope and native ownership/readback. Deliver the native source,
transparent PNG, comparison, patch log, checks, reviewer status, and unresolved
gaps. Preserve candidates. A passing validator is not visual approval.
'''
    (destination / 'BRIEF.md').write_text(brief)
    return destination


def verify(run: Path) -> dict:
    entries = json.loads((run / 'frozen-inputs.json').read_text())
    failures = []
    for entry in entries:
        copy = (run / entry['copy']).resolve()
        if not copy.is_relative_to(run.resolve()):
            raise ValueError('Frozen input path escapes run directory.')
        for label, file in [('copy', copy), ('original', Path(entry['source']) if entry['source'] else None)]:
            if file is not None and (not file.is_file() or sha256(file) != entry['sha256']):
                failures.append({'kind': label, 'path': str(file)})
    return {'passed': not failures, 'changed_or_missing_inputs': failures}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--output-root', type=Path, required=True)
    p.add_argument('--run-id', required=True)
    p.add_argument('--model', required=True)
    p.add_argument('--host', required=True)
    p.add_argument('--backend', choices=['pebbly', 'diivi', 'aseprite-cli'], required=True)
    p.add_argument('--profile', type=Path, required=True,
                   help='Task profile to freeze; choose the historical v03 profile explicitly when needed.')
    p = sub.add_parser('verify-inputs')
    p.add_argument('--run', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'verify-inputs':
            result = verify(args.run)
            print(json.dumps(result, indent=2))
            return 0 if result['passed'] else 1
        destination = prepare(args.repo, args.output_root, args.run_id, args.profile,
                              args.model, args.host, args.backend)
        print(destination)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'prepare_run: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
