# STUDIO OS Visual Kit — Web App

A data graphics generator. Paste a JSON spec, get a 4K PNG and animated MP4.

## Local Development

```bash
cd studio_kit
pip install -r requirements.txt
playwright install chromium
python app.py
```

Open http://localhost:5000

## Deploy to Render (free)

1. Push this repo to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Root Directory**: `studio_kit` (if repo root is the outer folder)
   - **Environment**: Docker
   - **Instance Type**: Free
5. Click Deploy

Render auto-detects the `Dockerfile` and builds it.

## Templates

- `vbar` — Vertical bar chart with baseline, shortfall outlines, dated events
- `hbar` — Horizontal comparison bars with groups, ranges, status chips, callout

## Status chips

| Chip | Meaning |
|------|---------|
| verified | Independently confirmed |
| reported | Reported by credible source |
| officialclaim | Government / official claim |
| estimate | Statistical estimate |
| analysis | Editorial analysis |
| unverified | Cited but not found in source |

## Dependencies

- Python 3, Flask, Playwright (Chromium), ffmpeg
- Fonts bundled: Source Serif 4, Inter (open licence)
