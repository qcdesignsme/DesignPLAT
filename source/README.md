# Source for qcdesignsme.github.io/DesignPLAT

Version of the Think of Us application page (qcdesignsme/think-of-us) for the UX/Service Designer role on Maryland's Permitting & Licensing Acceleration Team (PLAT). Colors follow the Maryland Web Design System theme (designsystem.maryland.gov, Foundation / Colors); layout comes from the Figma file "Qian Chen for Think of Us".

Working files used to build this application page. The live site is the `index.html`, `img/` and `prototype/` at the repo root; nothing in `source/` is needed to view it.

To make a version for another role: copy this repo's contents into a new repo, then edit `source/page/build.py` (content) and `source/page/template.html` (layout) and rebuild.

## Page: `source/page/`

| File | What it is |
| --- | --- |
| `template.html` | The whole page: CSS tokens, hero, sections, matcher and animation scripts. Templates in the matcher: `flow0781` (VA findings) and `plain` (permit status update, before/after plain language). Placeholders: `{{STAGE}}`, `{{LOGOS}}`, `{{NEEDS}}`, `{{VA_DECK}}`, `{{VA_DECK_ATTR}}`. |
| `build.py` | Holds the six requirement-matcher panels (`needs` list: names, pills, posting quotes, evidence rows, buttons, images, embeds) and fills the template. |
| `stage.html` | Markup for the hero animation stage: four logos with names, the ground line, and the character (side view and front-facing waving view). |

Build (Python 3, no dependencies), from the repo root:

```
python3 source/page/build.py
```

This writes `index.html` at the repo root (images load from `img/`) and `source/page/qian-chen-maryland-plat.html`, a single self-contained file with images inlined (git-ignored, for emailing or uploading).

Content that is not in `build.py` (hero card, work cards, role map, quotes, letter, footer) is plain text in `template.html`.

## Hero animation: `source/animation/`

The hero is an original pen-and-ink drawing of three Baltimore rowhouses, drawn as an SVG.

- `rowhouses.py`: generates `source/page/stage.html` (the SVG). Strokes with class `ink` are drawn many at a time in about 3 seconds. `sk` is the faint dashed sketch the animation starts from. `glass` (windows) and `marble` (stoops) fill in at the end. Then a lawn flamingo pops up, a crab scuttles in and an oriole lands on the cornice. Run `python3 source/animation/rowhouses.py` and then rebuild the page.
- The timeline lives in the "hero animation" script at the end of `template.html`. It plays once and has Play/Replay and Pause buttons. With reduced motion it shows the finished drawing.
- `logos.json`, `logos/`, `loader-*.src.html` and the capture scripts are from the earlier logo-and-character animation. They are no longer used on the page but are kept for reuse.

## Figma file

Design source for this version: "Qian Chen for Maryland PLAT" (https://www.figma.com/design/kLLEtX2Rnyq3rIrj5cYAvK). Its variables are in three collections:
- **Maryland brand:** every Maryland Web Design System theme color, as primitives.
- **Color:** the same semantic names as the Think of Us file, each pointing to a Maryland brand color.
- **Spacing:** spacing, radius and size values.

`source/animation/rowhouses-static.svg` is the last frame of the hero animation as a flat SVG you can drop into Figma.

## Reading the Figma file: `source/figma-tools/`

Node scripts that read a `.fig` file without Figma (unzip it first; it contains `canvas.fig` and `images/`). Install with `npm install` (kiwi-schema, pako, fzstd).

- `parse.js <dir>`: decodes `<dir>/canvas.fig` to `<dir>.json`.
- `tree.js <dir> <depth>`: prints the node tree with ids.
- `render.js <dir> <nodeId>...`: rough HTML render plus a text dump of a frame.
- `map.js`: lists which node uses which image.

The page's design source is the Figma file "Qian Chen for Think of Us".
