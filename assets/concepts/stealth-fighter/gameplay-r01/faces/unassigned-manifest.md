# Face studies: raw, prompt assignment uncertain

Two separate built-in image-generation calls ran concurrently on 1 November 2026. A reporting-code error occurred after both completed and discarded the return mapping; the two portrait files were recovered from the same generated-output directory. We cannot establish which image corresponds to which prompt, so neither is labeled soft or firm. They are retained as raw studies only, pending review.

Input 1 for both: `assets/concepts/stealth-fighter/atmosphere-r01/A/simplified-01.png`, SHA-256 `e1dcf18e72ce22b8b6c6031d0f00da91259dcbf4c2bfbb0e0c12c8d1c56b6e1e`; role: identity and style reference. Both calls requested `transparent_background: true`. Requested dimensions were unspecified.

Exact shared prompt:

> Use case: stylized-concept. Asset type: controlled character face comparison, not production sprite. Input image 1: identity and pixel-style reference; preserve this character's design. Create a single head-and-neck portrait at eye level, near-side right-facing angle, centered, same consistent scale and framing, with the same light and muted indigo collar as reference. Adult man early-to-mid 20s, brown skin, light stubble, long dark hair in the same half-tied arrangement and broad hair masses. Natural adult proportions, pixel art with broad quiet pixel planes, sparse facial marks, no fine strands or pores. Calm observant neutral expression. Real transparent background. Preserve hair, age, skin, lighting, collar, framing and identity; vary only the specified facial bone and brow cues. No scars, jewelry, hair redesign, costume redesign, photo realism, anime, soft painting or text. Do not make lighting darker to simulate facial structure.

One call appended: ` This alternative: softer angular cheek and jaw, relaxed narrow brow.` The other appended: ` This alternative: slightly firmer square jaw and stronger straight brow, calm intent neutral expression.`

- `unassigned-01.png`: 1168 × 1346 RGBA, SHA-256 `1210ebcc27cfb5cfd78efe77bbf9bcf8939f69d77b2459d25a3f7c88aae2d0c9`; recovered source `/Users/guhan/.codex/generated_images/01a197f2-d237-7442-a944-e7ae4f82b674/exec-a28a4e4a-2341-446e-8b26-84bd97a1c220.png`.
- `unassigned-02.png`: 1024 × 1536 RGBA, SHA-256 `5b07337d420c7d652f75999e22e846aacee7f9d4bc8b592da0df6a1f01f66e54`; recovered source `/Users/guhan/.codex/generated_images/01a197f2-d237-7442-a944-e7ae4f82b674/exec-41642e50-6356-4571-b979-73776d2374ba.png`.

Visual review: both retain the half-tied dark hair, brown skin, indigo collar and rightward gaze, but have considerably finer stubble/hair detail and more portrait-like anatomy than the reference. The hair masses are fuller and the framing and angles differ, preventing a controlled bone/brow comparison. Both appear adult, but exact age is subjective. 02 has a substantial painted orange glow despite the transparency request; alpha exists in both. Neither establishes a production sprite, gameplay readability or user approval.
