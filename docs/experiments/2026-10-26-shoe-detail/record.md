# v04: small shoe-detail pass

- Date: 26 October 2026
- Request: make the shoes a little more detailed. This explicitly expands the prior head-only scope to this shoe edit; it does not authorize unrelated body/head changes.
- Base: preserved standing v03. Outcome: separate [v04 native file](../../../assets/source/standing-v04/standing.aseprite) and [transparent export](../../../assets/export/standing-v04/standing.png).
- Method: existing Aseprite batch Lua edits only existing opaque pixels of `04-sneakers`. Add restrained lace/eyelet contrast, toe and quarter-panel seams, and sole-edge accents using the existing shoe colors.
- Preserved: 128x192 canvas, original alpha silhouette, feet/ground anchor, stance, and all 11 other layer images. No new colors, tools, computer interaction or paid services.
- Evidence: [before/after shoes](../../../assets/previews/standing-v04/shoes-before-after.png), [full-body preview](../../../assets/previews/standing-v04/standing-4x.png), [exact checks and hashes](checks.json), [drawing source](../../../assets/source/standing-v04/detail-shoes.lua).
- Observed checks: 89 changed pixels, all within existing shoes; decoded reopened export identical; all 11 non-shoe layers identical after native save/reopen; unchanged composite alpha and zero palette additions. Visual comparison inspected enlarged.
- State: local and uncommitted. User visual acceptance is pending. No animation, Godot playback or publication performed.

Next: user reviews this modest detail increase. Agent continues only the next requested correction, preserving previous versions and finalized design.
