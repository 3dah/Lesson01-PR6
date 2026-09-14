# Experience Architecture — The Mystery of Fire

## Experience Model
Not slides. **Immersive chapters** with a continuous cinematic shell:
- Persistent dark stage (WebGL/Canvas atmosphere)
- Scene-specific overlays and interactions
- Progress ribbon (chapter dots) + mute + keyboard navigation
- Learning arc: Mystery → Question → Prediction → Experiment → Observation → Investigation → Discovery → Explanation → Challenge → Conclusion

## Chapter Sequence

| ID | Chapter | Intent | Primary Interaction |
|----|---------|--------|---------------------|
| 00 | Boot / Enter | Immersion gate | Click/tap to begin |
| 01 | The Mystery | Emotional hook; flame as hero | Observe flame; advance |
| 02 | The Invisible Air | Make air visible | Reveal particles |
| 03 | The Experiment | Assemble apparatus | Step-build equipment |
| 04 | Make a Prediction | Commit before seeing | Choose A/B/C |
| 05 | The Closed Jar | Cover & trap air | Place lid |
| 06 | The Flame Goes Out | Dramatic extinguish | Watch oxygen deplete |
| 07 | Why? | Cause explanation | Scrub oxygen timeline |
| 08 | Fresh Air | Convection / renewal | Open gaps; see flow |
| 09 | The Aha Moment | Closed vs airflow | Compare side-by-side |
| 10 | The Science | Combustion equation | Animate reaction |
| 11 | Real World | Transfer | Explore examples |
| 12 | Science Challenge | Apply | Choose which candle lasts |
| 13 | Final Discovery | Lock conclusions | Reflect & finish |

## Scene Shell Layout
```
┌─────────────────────────────────────────────┐
│ progress · title · mute                     │
│                                             │
│           VISUAL STAGE (full bleed)         │
│                                             │
│  headline / support copy (minimal)          │
│  interaction cluster                        │
│                                             │
│ ← back                          continue →  │
└─────────────────────────────────────────────┘
```

## State Machine
`AppState`: `{ chapterIndex, prediction, challengeAnswer, muted, reducedMotion, experimentMode }`

Experiment modes: `openTop` | `sealed` | `bottomOnly` | `airflow`

## Narrative Guarantees
- Prediction answers are not graded until after observation scenes.
- Challenge uses Step 4 vs Step 5 logic: both openings required.
- Safety note appears when lighter/lighting is referenced.
