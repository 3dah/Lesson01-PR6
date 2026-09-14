# Exports — The Mystery of Fire

Offline deliverables generated from the HTML master experience.
**The interactive HTML app is unchanged and remains the source of truth.**

## Files

| Deliverable | Path |
|-------------|------|
| Premium PDF (16 pages) | `exports/pdf/The-Mystery-of-Fire.pdf` |
| Premium editable PPTX (18 slides) | `exports/powerpoint/The-Mystery-of-Fire.pptx` |
| Shared diagrams | `exports/assets/` |
| Visual QA previews | `exports/previews/` |

## Rebuild

```bash
python scripts/export_all.py
```

Or step-by-step:

```bash
python scripts/generate_diagrams.py
python scripts/build_pdf.py
python scripts/build_pptx.py
```

## Design system (matches HTML)

- Background void `#070B14`
- Air / oxygen cyan · Fire amber · Fresh teal · Warm outflow
- Typography: Sora (UI) + Georgia/Sora SemiBold headlines
- Narrative arc mirrors the 13 HTML chapters

## PowerPoint notes

Every major slide includes speaker notes with:
teacher explanation · scientific point · student question · expected answer · teaching tip
