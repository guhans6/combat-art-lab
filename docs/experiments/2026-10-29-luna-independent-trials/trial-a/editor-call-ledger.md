# Trial A editor-call ledger

The supervisor granted the editor slot for the smoke and initial native
construction, released it, then re-granted it for passes 01 and 02. The current
supervisor-tracked observable editor-call count is **116**; four calls remain in
the fixed 120-call trial budget. Pass 02 and its proof artifacts are saved; the
reopened pass-02 document remains open and must not be closed or modified while
the slot is released.

After the grant, append one row per Aseprite/editor MCP call, including technical
failures and retries. Keep unknown provider compute/cost separate from this local
call count. Artifact exports consume one of the three pass slots even if a later
review rejects the image.

| Seq. | Scope | Result | Notes |
| ---: | --- | --- | --- |
| 1 | preflight | PASS | Headless Aseprite 1.3.18.6-dev / extension 0.8.2 |
| 2–27 | smoke | PASS with two corrected schema attempts and one save/close retry | Scratch image delivery, exact reads, save/reopen, one-pixel edit, protected-layer preservation, and out-of-selection guard; see `smoke-record.md` |
| 28–39 | production setup | PASS | Opened 128x192 alpha-clean seed, inspected structure/alpha, created semantic layers, imported and hid locked source reference |
| 40–45 | production inspection | PASS/technical retry | Native previews, head/region reads, palette snap from 3,572 off-palette colors to 254 visible colors; one oversized ASCII read retained as a technical failure |
| 46–59 | face cleanup | PASS | Compared reference/seed, authored six-pixel eye/sclera cleanup, rejected an overlarge four-pixel smile overlay, replaced it with a restrained three-pixel smile, reviewed head and full candidate |
| 60–76 | semantic structure | PASS | Duplicated/renamed clipped raster layers and cleared outside reviewed head, jacket/shirt, and jeans regions; tote/shoes selection was active at release |
| 77–85 | pass 01 export | PASS | Completed tote/shoes clipping, inspected tote/shoes/full previews, saved `passes/pass-01.aseprite`, exported `passes/pass-01.png`; released slot for defect-only review |
| 86–94 | pass 02 correction/export | PASS | Reopened pass 01, corrected eye highlights/smile, reviewed head/full previews, saved/exported pass 02 |
| 95–98 | pass 02 reopen proof | PASS | Closed/reopened pass 02, inspected native structure, exported `pass-02-reopen.png`; hash matched pass 02 |
| 99–105 | duplicate local edit | PASS | Opened separate pass-02 document, added two-pixel tote overlay accent, reviewed it, saved/exported duplicate |
| 106–115 | protected-layer comparison | PASS | Read and compared five converted raster layers on candidate/duplicate; zero differences each |
| 116 | duplicate close | PASS | Closed proof duplicate; pass-02 reopen document remains open |
