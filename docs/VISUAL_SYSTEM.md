# Visual System — The Mystery of Fire

## Direction
**Apple × National Geographic × Science Museum × Documentary**  
Cinematic darkness, one hero visual per chapter, restrained UI.

## Semantic Color Tokens
| Token | Hex | Meaning |
|-------|-----|---------|
| `--bg-void` | `#070B14` | Stage void |
| `--bg-closed` | `#0A1224` | Closed environment |
| `--air` | `#5EC8FF` | Air / atmosphere |
| `--air-deep` | `#1A6B9A` | Deep air depth |
| `--oxygen` | `#7AD7FF` | Oxygen particles |
| `--fresh` | `#9EFFF0` | Fresh air inflow |
| `--fire` | `#FF8A3D` | Flame body |
| `--fire-core` | `#FFE566` | Flame core |
| `--heat` | `#FF4D2E` | Heat glow |
| `--warm-out` | `#FFB070` | Warm air leaving |
| `--clay` | `#2F5FA8` | Experiment clay |
| `--wood` | `#8B6A45` | Wooden board |
| `--glass` | `rgba(180,210,230,0.25)` | Jar |
| `--metal` | `#C9A227` | Lid |
| `--text` | `#F2F5FA` | Primary text |
| `--text-muted` | `#9AA6B8` | Secondary text |
| `--accent-warn` | `#E24A3B` | Caution / emphasis |

## Typography
- Display: **"Fraunces"** — mystery headlines
- UI / body: **"Sora"** — clarity for Grade 6
- Avoid Inter/Roboto/Arial/system defaults as primary brand fonts

## Motion Principles
- Meaning over spectacle
- Flame: organic noise + buoyancy
- Oxygen: soft cyan drift; density encodes availability
- Airflow: bottom→in (cyan), top→out (warm amber)
- Extinguish: scale + luminosity decay, then ember smoke
- Respect `prefers-reduced-motion`

## Composition Rules
- First viewport = brand + one question + one flame (no cards)
- No dashboard grids
- Cards only for prediction/challenge choices (true interactions)
- Large visual plane; sparse copy
