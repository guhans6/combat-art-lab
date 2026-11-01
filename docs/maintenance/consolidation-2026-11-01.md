# Local consolidation — 1 November 2026

User request: consolidate current/other branches, retain important assets, remove
safe duplicates, set old character aside, prepare for a new design with workflow
unchanged. No publication requested. This file is the scope/acceptance record.

Baseline: all branches initially9e35c5c, substantive work uncommitted in parent and
teaching worktrees. Recovery snapshot (both trees, excluding runtime caches):
`.scratch/consolidation-2026-11-01/before-consolidation.tar.gz` (395818103bytes).
Parent preservation commit0930aba; teaching commit6f745de. Consolidation branch
`work/new-character-ready` merges teaching plus the parent’s current work.
Only docs/handoff conflicted; both histories were retained below a new current entry.

Retained: canonical original images, editable masters, reconstruction sources,
workflow/ADRs, research, source/evidence hashes, Godot fixtures, lessons, generic
converter and tote preset/batch examples. Existing runtime configuration retained.
Installed runtime/node dependencies and caches are ignored, not removed/reinstalled.

Cleanup:65files/6352440bytes removed from active tree:45exact binary copies of
canonical material03 exports/sources and20superseded browser QA outputs. Lesson
HTML consumers point directly to the canonical originals. See JSON inventory with
per-file canonical locations/hashes for the45exact asset copies and deletion
rationale for the20superseded browser outputs. All unique historical native studies remain
as evidence; no blind native/source/Godot path deletion, hardlinks or symlinked
writable assets. Git content storage also deduplicates identical retained blobs.
Original pre-cleanup copies are recoverable from teaching commit and recovery tar.

Acceptance: both branches’ meaningful work consolidated, important catalog/new-asset
entry present, workflow unchanged, cleanup references resolve, current6pose native
and converter inputs preserved, focused tool tests and a new conversion run pass.
Historical native/Godot runtime proofs are retained; no new gameplay validation
is inferred. Old branches/worktree are recovery references, not parallel workflows.
No push, PR, remote merge, new asset, new paid service or installation.

Historical files contain pre-existing whitespace and recorded absolute host paths;
these were preserved rather than rewriting evidence during the snapshot. New
maintenance files and handoff are checked separately. Next owner: user supplies
new references; agent applies the existing intake/conversion/native workflow.
