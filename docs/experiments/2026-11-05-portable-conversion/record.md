# Publish the reusable conversion workflow

Date: 5 November 2026. Request: preserve and push image-to-sprite conversion and
Aseprite automation for use in Dot/another execution environment, without sweeping
unrelated character experiments into the publication.

## Baseline and scope

Remote `guhans6/combat-art-lab`, branch `work/new-character-ready`, baseline
`a7162c9849e1151310a2dec7548800068570a022`, verified after fetch. The repository
currently reports public; its default `main` remains the earlier foundation.
The core converter, six-pose automation, native recipes and director skill were
already published. No corresponding conversion issue was found in the open issue
list; no issue or PR was created.

Prepared in a separate clone at `/private/tmp/combat-art-portable-20261105` to
preserve the original checkout's dirty handoff, concept galleries and lessons.
No existing branch was renamed or switched. Added only the lantern preset and
its original source/conversion/native-copy evidence, the weapon-fighter conversion
experiment, pinned dependencies and new-machine documentation. The practice-board
redraws, concept skill/gallery work, game previews and Godot lessons remain local.

The launcher now selects a checkout-local venv instead of an absolute user cache.
Pillow is pinned to 13.0.0. The Aseprite MCP manifest/lock preserves the previously
tested 0.8.2 dependency graph and archive integrity while resolving the package
from npm instead of an ignored local tarball. New-machine instructions explicitly
require replacing host-specific MCP paths, isolating optional Godot enablement,
and testing the actual receiving host. No claim about Dot's OS or MCP support.

## Observed checks

Publishing target: macOS 26.6.2 arm64. A fresh clone-local Python 3.11.13 venv
installed Pillow 13.0.0 from requirements. An additional clean Python 3.14.7 venv
with the same Pillow version ran the replay and director checks.

- Reach: direct converter replay matches the stored RGBA output. The executable
  `run-reach.command` selects the clone-local venv and produces the same pixels.
- Lantern: `verify.py` passes every-pixel original-source mapping, 144px height,
  binary alpha, stored native/export equality and byte-identical conversion replay.
  Converter/source/native hashes remain the recorded historical values.
- Weapon fighter: replay in a scratch copy reproduces foreground-mask, pixel JSON
  and palette JSON bytes. Reconstructed pixels equal the saved PNG, stored reopen
  export and independently decoded native cel; original hash is unchanged.
- Director: all 42 existing unit tests pass.
- Dependency restoration: `npm ci --prefix tools/aseprite-mcp --ignore-scripts
  --no-audit --no-fund --cache .art-tools/npm-cache` succeeds (97 packages).
  All 97 dependency entries retain their versions and integrity hashes. Node
  26.9.0 runs the newly installed CLI help, confirming 0.8.2 and the headless flags.
- Shell syntax, staged whitespace, all staged relative Markdown links, JSON parsing
  and credential-pattern checks pass. Copied source/script/evidence bytes match
  the original checkout. Independent standards and request reviews each report
  zero findings; the standards review also reports no baseline code smells.

These checks do not launch Aseprite or Godot. Comparing historical reopen exports
does not establish a fresh editor reopen. No new art, animation, visual approval,
engine playback, global installation or paid service is claimed.

## Next owner

User opens branch `work/new-character-ready` in Dot/the receiving environment;
the receiving agent follows [new-machine setup](../../new-machine.md), inventories
the actual host, installs the needed local runtimes and performs the dedicated
MCP scratch save/reopen/revision test before claiming native automation works there.
Publication is complete only once the remote branch's commit matches the local
publishing commit; that exact revision is reported in the chat after the push.
