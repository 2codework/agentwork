# Creative workflows R2 independent QA

**Disposition: 7 accept, 2 fix, 0 reject.** Acceptance means documentation-supported original teaching proposal, not tested operation. All twelve listed official URLs were independently opened. No product, third-party code, browser account, credentials or Mac used. No writer/source changes.

## Required narrow fixes

1. **FFmpeg:** specify statistics output on pass 2 and remeasurement, not only pass 1; the filter defaults to no statistics. Make measured-input field mapping explicit. This is a missing instruction, not an observed FFmpeg runtime failure. [Official loudnorm options](https://ffmpeg.org/ffmpeg-filters.html#loudnorm).
2. **Sprite-sheet dedup rationale:** existing `video-silent-animation-loop` includes traditional keyframes as well as a historical model route. State that the new case adds SpriteFrames/sheet slicing/FPS resource handoff rather than only contrasting diffusion. The new workflow itself is supported. [Official sprite workflow](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html).

## Per-case review

### creative-r2-freecad-constrained-part — accept
Accept as original dimensional adaptation, not a reproduction of the tutorial geometry. Official archived tutorial supports Body, constrained sketches, Pad/Pocket and editing dimensions. Archive status does not establish software obsolescence.
Sources: [FreeCAD archived PartDesign tutorial](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Creating_a_simple_part_with_PartDesign.md)

### creative-r2-openscad-parameter-guard — accept
Accept with historical v2021.01 label. Official cheatsheet supports assert, cylinder, translate, difference and preview/render distinction; tolerance and dimensions are original design choices. Prefer explicit conjunction (outer > inner && inner > 0 && height > 0) in any eventual code, not a chained comparison.
Sources: [OpenSCAD CheatSheet](https://openscad.org/cheatsheet/)

### creative-r2-gltf-handoff — accept
Accept. Official docs support complete glTF asset copying, separate import settings, .blend external dependency and OBJ animation limitations; original size/checklist is not claimed executed.
Sources: [Godot available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html), [Godot import configuration](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html)

### creative-r2-game-collision — accept
Accept. Advanced settings document Static/Dynamic body types and restrict Trimesh to static bodies. Convex/primitive dynamic choice and future drop-test bounds are accurate.
Sources: [Godot advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html)

### creative-r2-sprite-sheet — fix
Fix dedup rationale, not workflow. Existing video-silent-animation-loop includes BOTH traditional keyframe and historical model routes; distinguish the new deliverable as editable SpriteFrames plus sheet slicing and FPS/frame-order evidence rather than implying the older case is diffusion-only.
Sources: [Godot 2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)

### creative-r2-impress-master — accept
Accept. Official help supports master views and current-slide versus all-slide application; preserve special-slide validation. Current help identifies 26.8, not proof of installed version.
Sources: [Impress master view](https://help.libreoffice.org/latest/en-US/text/simpress/01/03150000.html), [Impress changing master](https://help.libreoffice.org/latest/en-US/text/simpress/guide/masterpage.html)

### creative-r2-impress-handouts — accept
Accept. Official help supports Handouts selection, per-page count and Notes/Handouts header/footer settings. Print-to-file is expressly conditional and no PDF output is claimed.
Sources: [Impress printing presentations](https://help.libreoffice.org/latest/en-US/text/simpress/guide/printing.html)

### creative-r2-spectral-hum — accept
Accept as bounded workflow design. Official manual supports dedicated spectral effects for time/frequency ranges, distinguishes ordinary delete and narrows suitable noise. No promise of restoration or listening test.
Sources: [Audacity spectral selection](https://manual.audacityteam.org/man/spectral_selection.html)

### creative-r2-loudness-two-pass — fix
Fix operational evidence instructions. Explicitly set print_format=json (or summary) in SECOND pass and output verification pass, preserving logs, because default is none. Clearly map input_i/input_lra/input_tp/input_thresh to measured_I/measured_LRA/measured_TP/measured_thresh and target_offset to offset. Keep fallback/sample-rate and no-universal-target caveats.
Sources: [FFmpeg loudnorm filter](https://ffmpeg.org/ffmpeg-filters.html#loudnorm), [FFmpeg legal](https://ffmpeg.org/legal.html)

## Evidence and licensing boundaries

- FreeCAD documentation archive date is not a software deprecation date. Tutorial version 0.17+ and unfixed main history remain explicit; recipe geometry is original.
- OpenSCAD v2021.01 is a historical cheatsheet label. Its footer says CC-BY; that is not an automatic license for unrelated libraries or models.
- LibreOffice help page currently displays 26.8. MPL2.0 help licensing does not license all templates/fonts. Godot stable and Audacity development documentation are not installed-version evidence.
- FFmpeg LGPL/GPL configuration caveat is supported by its [official legal page](https://ffmpeg.org/legal.html); no distribution or commercial clearance was evaluated.
- All proposed operations remain unexecuted and all unknown publication dates remain null. Original assets only; no tutorial assets copied or downloaded.

## Dedup and coverage

Compared all97 baseline IDs/titles/goals and closest slide, podcast/mastering, animation-loop and archive workflows. Zero ID collisions. New cases differ in constraints/geometry, physical collision, editable sprite resource, master scope, audience separation, frequency-specific repair, or auditable loudness passes. This is a useful nine-case gap increment, not proof of comprehensive design/music/video coverage.

## Limits/blockers

No new source-access blockers. Prior Blender HTTP402 observations remain uncertain and untouched; no retry or alternate route. No actual CAD/import/physics/playback/printing/audio operation tested. Reports only were written.

## Correction closure

Root authorized the two narrow research edits after this independent review. Both have been applied to JSON and Markdown; original dispositions and exact before files remain preserved in `before/`. `corrections.json` records before/after hashes. Corrected disposition: accept all nine as documentation-supported unexecuted proposals. No canonical repository changed. See INTEGRATION_PLAN.md for pending baseline/schema work.
