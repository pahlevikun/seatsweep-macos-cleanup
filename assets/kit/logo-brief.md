# Logo brief: seatsweep

## 0. Routing

- **Mode:** one_shot
- **Kit tier:** lite
- **Library category:** oss_repo_mark
- **Clichés to avoid:** broom clipart, trash-can glyph, mug (Murk), cloud-as-the-whole-logo, Chrome multicolor circle logo, octocat or gnu-style mascot, scanline stripes, red/green diff rows
- **Grill mode:** skip (one_shot, copy and metaphor locked)
- **Intent:** The four README assets should tell a macOS user that this account can feel newly created while the person, iCloud, and the keep-list tools stay. The mark is a dustpan seen from the side, stopped short of a small key and a small cloud. One gold lip is the only metal accent. Column 3 is a terminal that lists sample category totals, flags EXCLUDE keep, and waits for a category pick. Kit tier is lite, so the ship set is the four SVGs plus platform PNGs and social SVG+PNG. Library marks were study-only.
- **Context sources:**
  - Google Chrome brand color vocabulary (study only; **not** official Google branding): Blue `#4285F4`, Red `#EA4335`, Yellow `#FBBC04`, Green `#34A853`
  - Material / Google gray text tokens: `#202124`, `#5F6368`, surfaces `#F8F9FA`, `#F1F3F4`, `#E8F0FE` (cloud tint only)
  - Prior generation cited `levistack/docs/assets/logo.svg` for layout; palette superseded by Chrome-inspired bright theme (2026-11-07)
  - logo-kit-svg `references/token-table.md` (roles)
  - logo-kit-svg `references/svg-blueprints.md` (904×256 grid)
  - logo-kit-svg `references/banner-column-3.md` (column 3 mode)
  - logo-kit-svg `references/animation-choreography.md`
  - logo-kit-svg `references/brand-kit-tiers.md`
  - logo-kit-svg `references/xml-and-qa-gate.md`
  - `SKILL.md`, `references/keep-policy.md` (keep list, scan first)
  - Library search: `search_library.py --category oss_repo_mark --summary` (github, go, gitlab, gnu, mozilla, and others)
  - Example search: `search_examples.py --has-animation true --summary` (applydiff, logo-kit-svg)
- **Unknown after lookup:** none for color. Social-card muted default inside `social_cards.py` is `#a99b83`, which is not in the cited logo. Shipped social SVGs replace that with `#98a2b6`.
- **Preview artifacts:** none (lite, one_shot)
- **Platform pack:** favicon + iOS + Android (`assets/kit/platform/`)
- **Gallery publish:** skip
- **Social cards:** `assets/kit/social/` via `social_cards.py` (SVG + PNG)
- **Banner column 3 mode:** `feature-summary` (terminal narrative: category totals, EXCLUDE keep, waiting for a category pick). Not `diff-hunks`.
- **Library reference slugs (study only):** `github`, `go`, `gitlab` for symbol weight. `cloudflare` and `cloud9` noted only as cloud clichés to avoid. No library geometry in the four deliverables.

## 1. Brand and copy

- **Wordmark:** `seat` in `#202124` + `sweep` in `#4285F4` (9 chars). Cursor strip: four 7px bands (blue, red, yellow, green).
- **Wordmark cursor x:** formula `184 + ceil(9 × 20.2) = 366`. Drawn at `x="382"` so a wider fallback face still has about 8px of air. On IBM Plex that is about 16px, still under the 18px QA limit.
- **Tagline:** This Mac account, minus the leftovers. Scan first. iCloud stays.
  Split across three 13px mono lines so each line stays left of `x=456` with a 24px gutter:
  - `This Mac account,` (17)
  - `minus the leftovers.` (20)
  - `Scan first. iCloud stays.` (25)
- **Pill 1:** `scan first` (10 chars). Width `10 × 7.2 + 32 = 104`. Dot at x=13, text at x=24.
- **Pill 2:** `iCloud stays` (12 chars). Width `12 × 7.2 + 32 = 118.4`, drawn `119`. x=`104 + 8 = 112`.
- **Combined pills:** `104 + 8 + 119 = 231`. Origin x=186, right edge 417. Gutter to column 3 (`x=456`) is 39px.
- **Motto:** A dustpan with a keep list.

## 2. Column 3 card copy

Mode is not `diff-hunks`. No red or green rows. No `-` or `+` lines. Sizes below are round brand samples, not a scan of a real home directory.

- **Topbar chip:** `scan $HOME` (10 chars). Formula `ceil(10 × 6.8) + 28 = 96`. Drawn width `118` so the dollar sign keeps padding. Text starts at x=82.
- **Topbar section tag:** `dry run`
- **Context lines:** `Browser data` 1.2G, `OS caches` 640M, `Homebrew unused` 96M
- **Keep row:** `EXCLUDE keep` / `iCloud` (gold stroke `#b2853a`, not a diff hunk)
- **Waiting line:** `waiting for a category pick`
- **Pipeline:** `scan &#8594; list &#8594; wait` then pill `your category`

## 3. Color tokens

Source: Chrome-inspired palette (not official Google branding). Roles follow `logo-kit-svg/references/token-table.md`.

| Role | Hex | Where |
|---|---|---|
| `--bg` | `#F8F9FA` | banner, icon tile, social cards |
| `--surface` | `#FFFFFF` | terminal card, panels |
| `--surface2` | `#F1F3F4` | terminal top bar |
| `--line` | `#DADCE0` | outer stroke, rules |
| `--line2` | `#E8EAED` | card stroke |
| `--fg` | `#202124` | wordmark `seat`, list headings |
| `--muted` | `#5F6368` | tagline, waiting line, key outline |
| `--dim` | `#80868B` | motto |
| `--accent` | `#4285F4` | wordmark `sweep`, chip text, EXCLUDE label |
| chrome-yellow | `#FBBC04` | dustpan lip |
| chrome-red / green | `#EA4335` / `#34A853` | window dots, pill strokes |
| cloud fill | `#E8F0FE` | iCloud cloud only |
| pan stroke | `#3C4043` | dustpan body |
| pill fill | `#F1F3F4` | column 2 pills |

`--del` and `--add` are omitted. Column 3 is `feature-summary`.

Flat `#F8F9FA` only. No scanlines. No Chrome circle mark.

## 4. Type

IBM Plex Sans for the wordmark and motto. IBM Plex Mono for the tagline, pills, and terminal. Same stacks as `logo.svg` lines 61 and 63, with the system fallbacks from `svg-blueprints.md`.

## 5. Mark

Side-view dustpan: short grip, back wall, floor, yellow chrome lip. The lip stops short of a small key (Keychain stays) and a light-blue cloud (iCloud stays). Stroke-dash draw on the animated files. No mug. No broom. Not the Chrome logo.

## 6. Animation

Icon loop `4.6s`. Banner loop `6s`. Cursor blink `1.1s`. Draw order: pan, gold lip, key, cloud. Hold the finished state through 64–88%. Rows and the keep bar fade from 0.35 opacity in CSS only. No `opacity="0"` attributes. `prefers-reduced-motion: reduce` zeroes dash offset and clears transforms.
