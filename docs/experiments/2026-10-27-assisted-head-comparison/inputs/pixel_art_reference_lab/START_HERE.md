# Pixel Art Reference Lab
## Multi-reference, style-faithful asset production • 27 October 2026

**The goal is the same character, aesthetic, expression and atmosphere—not an exact copy of every pixel.** Use additional generated poses, close-ups, simplified studies and animation references whenever useful. The agent draws, converts, cleans up, structures and verifies the asset; the user directs and selects the result.

This is a self-contained research and experiment kit, **not a replacement repository or finished game-asset pack**. The live workspace is `/Users/guhan/Guhan/Projects/combat-art-lab`. No file in that workspace was modified while preparing this kit.

### Read in this order
1. [HANDOFF.md](HANDOFF.md): the task for the next agent, including the user's clarified intent.
2. [workflow/PIPELINE.md](workflow/PIPELINE.md): reference acquisition, tracing/conversion/hybrid routes and review gates.
3. [workflow/FIRST_EXPERIMENT.md](workflow/FIRST_EXPERIMENT.md): the first bounded comparison to run.
4. [workspace/INTEGRATION.md](workspace/INTEGRATION.md): targeted changes to the existing workspace; do not overwrite it with this kit.

Read [prompts/README.md](prompts/README.md) when additional images are needed, [workflow/ANIMATION.md](workflow/ANIMATION.md) for motion, and [research/FINDINGS.md](research/FINDINGS.md) for evidence and tradeoffs. [research/SOURCES.md](research/SOURCES.md) contains dated primary-source links.

### What is included
Original uploads and previous visual tests; current research synthesis; generation/edit prompts; a reference registry and style-contract template; an experiment plan; a companion instruction file for the existing director; and small offline image-processing tools with tests.

### What has and has not been demonstrated
The earlier reductions are actual source-derived images, not new drawings. This kit's utility checks are recorded in [validation/RESULTS.md](validation/RESULTS.md). No new character art, generated pose, traced sprite, Aseprite master, finished animation or Godot playback was produced for this delivery. Hybrid drawing and multi-reference motion remain experiments to execute.

### Run the offline helpers
Use an existing Python 3.10+ environment with Pillow if available. `requirements.txt` records the version tested here; installing into another environment is a separate local choice.

```sh
python scripts/verify_manifest.py .
python -m unittest discover -s tests -v
python scripts/reference_lab.py inspect references/approved_concept_upload.png
python scripts/reference_lab.py seeds references/approved_concept_upload.png \
  --crop 380 100 800 415 --sizes 56x42 84x63 112x84 --colors 32 \
  --method BOX --out /tmp/pixel-art-seed-study-new
```

The crop/sizes above reproduce the earlier *diagnostic head study*, not an approved production specification. Output directories must be new. Read [scripts/README.md](scripts/README.md) before processing transparent images or animation frames.

### Integration rule
Extract to a separate directory. Give the next agent this folder and the live workspace path. It should merge the relevant ideas into existing documents/skills after inspecting their current state, preserve all previous artwork and failures, and run a small test rather than build a new framework.
