# Research: original character design before sprite construction

Reviewed: 1 November 2026. This is a practical reference library for the new-character discovery phase, not an approved style or a benchmark of the project's image generator. Use the [character-design-director skill](../../tools/character-design-director/SKILL.md) to turn the human's answers into controlled experiments.

## Design axes to separate

**Silhouette and personality:** Begin with gameplay purpose, emotional contrast, recognizable outline, body language and one or two defining shapes. A distinctive accessory is not automatically the whole identity.

**Proportion:** Compare compact/cartoon, medium stylized, lean action-oriented and more anatomical shapes. Keep the same total displayed height and camera within a single comparison, while varying head/body, leg, shoulder and mass ratios intentionally. Proportion families are choices, not levels of artistic quality.

**Rendering:** Pixel cluster size/density, colored versus dark contours, shading amount, palette/contrast, material treatment and illustration versus rig/cutout are independent of head/body proportions. Do not assume a tool or historical tote project fixes them.

**Motion:** Combat pose silhouettes, anticipation, connected shoulder/hip/arm/prop structure, contact and recovery. A gorgeous idle can still be unsuitable for the required attack.

**Production:** A chosen image must remain readable at intended game size, and be feasible as an editable/native asset. Concept comparison canvas size is not the final Aseprite drawing grid.

## A beginner-friendly six-stage method adapted for an AI-directed project

1. **Brief:** Human decides role, emotional intent, distinctive cues and constraints; agent interviews and researches. No random character generation.
2. **References:** Agent gathers visual references from actual games and creators, labels what each contributes, keeps provenance/usage restrictions, and asks the human to choose relevant properties.
3. **Silhouette/proportions:** Agent makes a small set of meaningfully different, named variations at matched comparison size. Human identifies useful/rejected shapes.
4. **Construction:** Agent tests structural anatomy/overlaps, front/side constraints and a viable pose. Do not hide anatomy failures with detailed clothing.
5. **Clothing/color/rendering:** Keep selected silhouette stable while separately exploring outfit details, palettes and edge/shading language. Every iteration states its changed variable.
6. **Animation feasibility:** Lock a canonical identity/reference before generating coherent key poses. Inspect consistency and then hand off to native reconstruction and actual gameplay-sized motion review.

## Common failure modes

- Polishing a single random first output instead of generating deliberate silhouette options.
- Confusing a stylish background or palette with a readable character design.
- Combining silhouette, face, outfit, palette and camera changes in one comparison, then attributing improvement to one feature.
- Reusing a prior character's pixel height, proportions, costume or color policy as a default for a new character.
- Comparing different source crops and visible heights as if they were a controlled style experiment.
- Accepting an image-generation prompt as evidence that the returned frame retained identity, exact size, transparency or anatomy.
- Generating every animation frame before approving the character and essential key poses.
- Treating a pleasing flattened image as proof of meaningful native editability or Godot readiness.
- Asking the beginner to find obscure reference facts or manually repaint the agent's errors.
- Confusing what the human approved for *exploration* with what they approved for production.

## Primary visual references and what to learn

| Reference | Specific useful lesson | Source |
| --- | --- | --- |
| **Arietta of Spirits**, Third Spirit Games developer diary | Several revisions of the same protagonist; recognizable hair silhouette; simplify palette/detail to make animation economical | https://thirdspiritgames.itch.io/ariettaofspirits/devlog/108255/character-design-deep-dive-how-i-came-up-with-the-art-style-for-arietta-of-spirits |
| **River City Girls 2**, WayForward director's character breakdown | Outfit/expression and attack moves conceived together, with concept art and animation of Marian | https://blog.playstation.com/2022/10/24/river-city-girls-2-new-marian-gameplay-and-character-design-details-revealed/ |
| **SLYNYRD Pixelblog 7: Developing Style** | Style arises through testing color, resolution, pixel clusters, subject and perspective, not declaring a signature style immediately | https://www.slynyrd.com/blog/2018/7/14/pixelblog-7-developing-style |
| **SLYNYRD Pixelblog 53: Punches and Kicks** | Proportions, arcade-action anatomy, and readable attack poses should be designed for gameplay | https://www.slynyrd.com/blog/2024/11/25/pixelblog-53-punches-and-kicks |

Use the actual art/images in these pages to explain principles, not as files to copy into the game. Discuss other games supplied by the user (e.g., Dan the Man, Scott Pilgrim, River City Girls or Katana ZERO) as *reference candidates* and record exactly which properties are approved. Avoid claiming an inspiration has been approved merely because it appears in this research.

## Evidence and limits

The links above document published creator practice, not controlled experiments with this repository's image generation or Aseprite tools. This repo has historical tests of source-assisted pixel reconstruction and animation; those tests do not validate new character styles. The next new-character experiment should record exact reference images, generation settings, actual outputs, user feedback and independent size/identity observations before recommending a production recipe.
