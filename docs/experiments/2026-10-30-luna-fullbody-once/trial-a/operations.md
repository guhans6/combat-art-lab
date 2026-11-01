# Native operations

All art operations below were issued through the dedicated headless Aseprite MCP on the open frozen sprite `#3`; no PNG was painted by Python, no Lua/CLI/Code-MCP/UI operation was used, and no image-generation call was made. Each layer's edits were one batched `draw` transaction in the single finishing pass, followed by `look` review.

| Layer | Intent | Palette colors used | MCP result | Touched bounds |
| --- | --- | --- | --- | --- |
| `08-hair-tie-and-hair` | Add connected crown/bun/fringe cluster accents while leaving the face/mouth treatment restrained | `#482925`, `#703f30`, `#96553a` | 3 ops, 56 pixels changed | x37–70, y6–33 |
| `02a-jacket-left` | Add hood/lapel, sleeve and lower-hem plane clusters | `#2d2c22`, `#4b4732`, `#6a613c` | 3 ops, 46 pixels changed | x34–54, y36–73 |
| `02b-jacket-right` | Add hood/sleeve fold clusters | `#2d2c22`, `#4b4732`, `#6a613c` | 3 ops, 36 pixels changed | x73–90, y40–71 |
| `04-tote` | Clarify rounded bag edge, folds and light-facing plane | `#8e7b72`, `#d2a595`, `#fcd8b6` | 3 ops, 47 pixels changed | x78–92, y72–101 |
| `00-shoes` | Strengthen laces/upper highlights and continuous dark soles | `#322322`, `#c49e91`, `#fcd8b6` | 3 ops, 62 pixels changed | x43–99, y175–184 |
| `01-denim` | Add restrained knee/lower-leg crease clusters | `#354c77`, `#58729e` | 2 ops, 40 pixels changed | x46–92, y88–157 |
| `03-shirt` | Add a small light/shadow fold rhythm; no body/pose change | `#d6b7bb`, `#fef8ee` | 2 ops, 19 pixels changed | x54–70, y48–66 |
| `05-tote-strap` | Add narrow warm edge shading to the existing strap | `#d2a595`, `#fcd8b6` | 2 ops, 25 pixels changed | x78–82, y43–64 |

The individual operation calls were intentionally pixel batches rather than many single-pixel calls. Palette lock remained enabled for every call. No drawing call targeted `07-face-and-neck`, `06a-left-hand`, `06b-right-hand`, the hidden guide, or the mouth area. Composite comparison against the baseline reports 282 changed pixels (overlap/no-op points explain why this is below the sum of call-level counts).

After the single pass, the document was saved as `outputs/luna56-fullbody-cleanup.aseprite`, exported to `outputs/luna56-fullbody-cleanup.png`, closed, reopened independently, and exported again to `outputs/luna56-fullbody-cleanup-reopen.png`. The reopened PNG is byte-identical to the first export.

## Scope-audit failure

The post-pass baseline comparison found 43 `transparent → opaque` alpha additions and no alpha removals. The outer bounding box stayed `(32,2)-(104,185)`, but 43 individual baseline-transparent cells became opaque, so the protected silhouette/alpha contract failed. The cause is the recorded pixel batches: no hard baseline alpha/silhouette mask was applied before writing, and several intended accent coordinates were outside the existing opaque mask. See `alpha-audit.json` for every coordinate and the exact baseline/candidate RGBA values. This is a technical failure of the single attempt, not authorization for a correction pass.

