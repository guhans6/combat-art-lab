#!/usr/bin/env python3
"""Read-only environment inventory. Never installs packages or connects to an MCP."""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def version(executable: str | None) -> dict:
    if not executable:
        return {'found': False}
    try:
        result = subprocess.run([executable, '--version'], capture_output=True,
                                text=True, timeout=15, check=False)
        return {'found': True, 'executable': executable, 'returncode': result.returncode,
                'version_output': (result.stdout + result.stderr).strip()[:500]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'found': True, 'executable': executable, 'version_error': str(exc)}


def aseprite_inventory(executable: str | None, probe_version: bool = False) -> dict:
    """Report discovery without starting Aseprite unless explicitly requested."""
    if not executable:
        return {'found': False, 'version_probe': 'not_run'}
    path = Path(executable)
    result = {
        'found': True,
        'executable': executable,
        'size_bytes': path.stat().st_size,
        'version_probe': 'not_run',
        'version_probe_reason': (
            'Direct Aseprite launch was not requested. This inventory does not '
            'establish headless MCP readiness; run the configured MCP preflight '
            'under the editor-lease procedure for that boundary.'
        ),
    }
    if probe_version:
        result.update(version(executable))
        result['version_probe'] = 'completed'
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--aseprite', help='Explicit path to your trusted Aseprite executable')
    p.add_argument('--probe-aseprite-version', action='store_true', help=(
        'Deliberately execute Aseprite --version. Use only where direct editor '
        'launch is permitted; this is not an MCP health check.'))
    args = p.parse_args()
    candidates = [args.aseprite, os.environ.get('ASEPRITE_PATH'), shutil.which('aseprite'),
                  '/Applications/Aseprite.app/Contents/MacOS/aseprite',
                  str(Path.home() / 'Library/Application Support/Steam/steamapps/common/Aseprite/Aseprite.app/Contents/MacOS/aseprite')]
    aseprite = next((v for v in candidates if v and Path(v).is_file() and os.access(v, os.X_OK)), None)
    try:
        pillow = importlib.metadata.version('Pillow')
    except importlib.metadata.PackageNotFoundError:
        pillow = None
    print(json.dumps({
        'schema': 1, 'platform': platform.platform(),
        'python': sys.version.split()[0], 'python_executable': sys.executable,
        'pillow': pillow,
        'aseprite': aseprite_inventory(aseprite, args.probe_aseprite_version),
        'node': version(shutil.which('node')), 'uv': version(shutil.which('uv')),
        'client_executables': {k: shutil.which(k) for k in ('claude', 'gemini', 'codex', 'opencode')},
        'mcp_connection': 'not_tested', 'image_delivery_to_model': 'not_tested',
        'native_edit_smoke': 'not_tested',
        'note': 'Presence/version inventory is not a working-toolchain test. Review setup.md.'
    }, indent=2))


if __name__ == '__main__':
    main()
