# Assets

## TRUCKY Animated Logo

- Asset name: `trucky-logo.gif`
- Creator/source: User-provided GIF from the project owner
- Source file: `/Users/aryanbaki/Downloads/screenshots_test/original-efefc43fed4168d8eb3319ad5dcf2f57.gif`
- License/usage: Provided by the project owner for use in this buildathon app
- Attribution required: No separate attribution requested
- Date added: 2026-06-18
- Files in repo:
  - `frontend/src/assets/brand/trucky-logo.gif`
- Modifications:
  - Used only as the compact animated logo mark in the app brand lockup.
  - Not used as a page background or hero banner.

## Kenney Car Kit — Truck

- Asset name: `truck.glb` and `truck-preview.png`
- Creator: Kenney
- Source website: https://kenney.nl/
- Source page: https://kenney.nl/assets/car-kit
- Download URL used: https://kenney.nl/media/pages/assets/car-kit/1a312ec241-1775131960/kenney_car-kit.zip
- License: Creative Commons Zero, CC0
- Attribution required: No
- Date downloaded: 2026-06-18
- Files in repo:
  - `frontend/src/assets/truck/truck.glb`
  - `frontend/src/assets/truck/truck-preview.png`
  - `frontend/src/assets/truck/License.txt`
- Modifications:
  - No model geometry edits.
  - The landing page applies CSS filter/glow styling so the preview fits the AI Trucky forest-green theme.
  - The GLB is bundled locally for future 3D rendering; the landing page uses the lightweight local PNG preview for reliable rendering without adding a heavy 3D runtime dependency.

The dashboard preview and surrounding UI visuals are local React markup and CSS.
