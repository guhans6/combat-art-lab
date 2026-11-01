# Evidence review — Pixel Art Class: Simple Character Idle Animation

[Source video](https://www.youtube.com/watch?v=vs-ierVdE7I) · AdamCYounis · 17:57 · prepared 30 October 2026

This is an evidence delivery with a bounded gap review. It preserves source artifacts and separates direct image observations, transcript support, and unresolved details. It is not an assertion that every pixel edit or every moment has been semantically reviewed.

## Evidence quality

- Source media: 1920×1080, 30 fps, original English audio. Video and audio packet hashes match the downloaded streams after stream-copy muxing; see [media recovery verification](provenance/media-recovery-verification.json). AgentWatch still records URL-to-local-media equivalence as unverified.
- Transcript: 172 segments from local faster-whisper large-v3-turbo, CPU/int8. No runtime quality flags; reported duration coverage 1.0; maximum reported gap 5.86 seconds. Automatic-caption comparison is a close match (0.9616 text similarity). These are extraction signals, not measured word accuracy. See [selected transcript](provenance/selected-transcript.json) and [audit](provenance/transcript-audit.json).
- OCR: moderate. AgentWatch flags 74 prepared frames for low OCR confidence. Those flags are preserved; inspecting six delivered images does not clear the remaining flags. See [run summary](provenance/run-summary.json) and [visual review](VISUAL-REVIEW.json).

## Crucial gaps addressed

| Gap | Evidence added or preserved | Status |
| --- | --- | --- |
| Selected URL stream lacked audio | Original English audio recovered and muxed without transcoding; local transcription completed | Addressed |
| Compact budget omitted late editing detail | All 77 prepared native frame files included, with original event IDs and file checksums | Addressed for prepared stills |
| Stills cannot preserve subtle motion | Seven source-linked video/audio excerpts covering 147 seconds of core demonstrations | Addressed within these intervals |
| Early frame counts could be mistaken for the final result | 16:00 native image, 17:00 native image, and focused 17:05 follow-up show final tags/timeline; narration supplies the explicit 13-frame explanation | Addressed |
| Generic extraction did not export chapters | Creator chapter metadata retained separately and audited against delivered sample times | Addressed as supplemental metadata |

## Instructional checkpoints

Transcript citations below refer to exact IDs in the [included transcript JSONL](agentwatch-compact/transcript/transcript.jsonl). Prose paraphrases narration; static image observations remain bounded to what is visible.

| Source interval | Supported checkpoint | Evidence |
| --- | --- | --- |
| 04:57–05:18 | Start from two breathing poses and shift the body above the hips by one pixel; the early plan uses 10 frames. | transcript-052, transcript-053, transcript-054; [core excerpt](motion-evidence/01-core-poses.mp4), clip-01-core-poses |
| 06:18–07:25 | The working plan becomes 12 frames; chest highlight tones transition across several frames to soften the displacement. | transcript-064, transcript-065, transcript-072–074; [chest excerpt](motion-evidence/02-chest-subpixel.mp4), clip-02-chest-subpixel |
| 10:14–10:47 | Narration delays the hands and moves them outward. The inspected 10:45 image shows the intermediate 24-column timeline. | transcript-103–107; [native 10:45](prepared-frames/chunk-002-frame-004.jpg), chunk-002-frame-004; [arm excerpt](motion-evidence/03-arms-delay.mp4), clip-03-arms-delay |
| 12:07–12:30 | Narration describes the hair flaring and settling; the 12:30 image exposes the separate curled strand at large scale. | transcript-117, transcript-118; [native 12:30](prepared-frames/chunk-002-frame-012.jpg), chunk-002-frame-012; [hair excerpt](motion-evidence/04-hair-settle.mp4), clip-04-hair-settle |
| 14:28–14:56 | Narration prefers shifting the leg shadow while retaining the leg silhouette. The still shows the enlarged lower-body region. | transcript-134–139; [native 14:30](prepared-frames/chunk-002-frame-021.jpg), chunk-002-frame-021; [shading excerpt](motion-evidence/05-leg-shading.mp4), clip-05-leg-shading |
| 15:47–16:38 | Narration reorders the loop into a 13-frame Breathe animation and a separate one-frame Idle animation that can be held between breaths. The 16:00 still visibly has Breathe and 13 columns. | transcript-146–154; [native 16:00](prepared-frames/chunk-002-frame-028.jpg), chunk-002-frame-028; [tag excerpt](motion-evidence/06-breathe-tag.mp4), clip-06-breathe-tag |
| 16:55–17:17 | Narration calls for removing the reference from the frame and restoring the original canvas before export; later narration mentions Unity slicing. The 17:05 follow-up shows the isolated sprite and both tags. | transcript-157–159; [native 17:00](prepared-frames/chunk-002-frame-032.jpg), chunk-002-frame-032; [focused 17:05](agentwatch-cumulative/assets/frames/follow-up-74e95e8d2e3cc427804c423c640ee9d31c4f3281a7f6c985d2e2496dd4cc7720-2832d0ed62641c7abb07819eb7cb76c01aa3a0494bcbd6d0333d27d7509efefa.jpg), follow-up-74e95e8d2e3cc427804c423c640ee9d31c4f3281a7f6c985d2e2496dd4cc7720-2832d0ed62641c7abb07819eb7cb76c01aa3a0494bcbd6d0333d27d7509efefa; [cleanup excerpt](motion-evidence/07-cleanup-and-export.mp4), clip-07-cleanup-and-export |

## Chapter coverage

Sample presence is structural coverage, not proof that every edit is represented. These creator chapters come from [provider description metadata](provenance/source-description.json); they were not invented from content.

| Chapter | Interval | Requested sample instants delivered |
| --- | --- | --- |
| Introduction | 00:00–00:34 | 3 |
| Setup | 00:34–04:56 | 20 |
| Core Frames | 04:56–06:30 | 10 |
| Chest Sub-pixel Animation | 06:30–10:12 | 20 |
| Arms Secondary Motion | 10:12–12:02 | 10 |
| Hair Secondary Motion | 12:02–14:08 | 10 |
| Sub-pixel Shading | 14:08–15:19 | 6 |
| Preparing for Export | 15:19–17:17 | 11 |
| Wrap Up | 17:17–17:37 | 1 |
| Outro | 17:37–17:57 | 3 |

## Evidence still unavailable or uncertain

- The editable .aseprite project, original palette values, and exported sprite-sheet file were not acquired. Video screenshots cannot establish the exact underlying asset pixels. The next owner needs the creator-provided project/assets for an exact reconstruction.
- Exact duration/FPS settings for every Aseprite animation cel were not established. The source video recording is 30 fps; that is not the animation playback rate. The narration discusses duplicated holds and engine-specific duration handling at 06:00–06:13 (transcript-061–063), plus example one- or two-second Idle holds at 16:27–16:38 (transcript-152–154).
- The custom export script and Unity animation-system code are not shown as retrievable source in this pack. The creator description links an [export-workflow tutorial](https://www.youtube.com/watch?v=hiMBVCFMj6E) and a [sub-pixel tutorial](https://www.youtube.com/watch?v=cs1Gp61yafQ). These links are preserved references; their contents were not researched or validated here.
- JPEG frames and re-encoded excerpts preserve visible evidence, not original editable sprite pixels. Intervals outside the seven excerpts remain sparsely sampled. OCR and STT can contain errors despite the favorable runtime signals.

## Extraction history and completion

- AgentWatch prepare, validate, merge, render, and Compact export completed for `run-685706ba8c60b1e15f47126ff98be675f978cf4d084c31ad4f4e1a70a3821ede`. Compact package: `pkg-27f82cd7-dcb1-4305-a5dd-278495b4c140`. Source SHA-256: `c946289c8fc1ff74faf4fbc0206c58f2e1c9eebd37e18f595f5418e9b5e93a95`.
- The initial managed-library attempt failed with a media read timeout. The successful result is the separate source-bound run created from the recovered media; it was not installed or registered as a completed managed-library run.
- The first broad follow-up was stopped after four frames because the implementation repeats a full-video timestamp inventory for each sample. Its receipt is honestly partial. Its remaining targets were superseded for this delivery by the complete prepared frame collection and motion excerpts, not marked fulfilled. See [history](follow-up-history/round-1-receipt.json).
- The focused final-export follow-up completed: `receipt-26be61fa-4307-49e1-b9ce-b5230047249a`. Its cumulative transport includes all 53 initial Compact frames and all five newly decoded follow-up frames as local assets. The separate prepared collection retains all 77 original prepared frames.
- The immutable AgentWatch exports are unmodified. Supplemental metadata, excerpts, review prose, and prepared-frame copies sit alongside them. Pending external-author intake templates remain pending; no completed knowledge-pack intake or exhaustive semantic audit is claimed.
- Final verification details are in [VALIDATION.json](VALIDATION.json). The next owner can use the pack for grounded learning or authoring, and obtain the creator assets/script if exact implementation fidelity is needed.
