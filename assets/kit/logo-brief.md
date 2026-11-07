# Logo brief: seatsweep

## 0. Routing

- **Mode:** one_shot
- **Kit tier:** lite
- **Library category:** oss_repo_mark
- **Clichés to avoid:** broom clipart, trash-can glyph, mug (Murk), cloud-as-the-whole-logo, octocat or gnu-style mascot, scanline stripes, red/green diff rows
- **Grill mode:** skip (one_shot, copy and metaphor locked)
- **Intent:** The four README assets should tell a macOS user that this account can feel newly created while the person, iCloud, and the keep-list tools stay. The mark is a dustpan seen from the side, stopped short of a small key and a small cloud. One gold lip is the only metal accent. Column 3 is a terminal that lists sample category totals, flags EXCLUDE keep, and waits for a category pick. Kit tier is lite, so the ship set is the four SVGs plus platform PNGs and social SVG+PNG. Library marks were study-only.
- **Context sources:**
  - `levistack/docs/assets/logo.svg` (palette and type; local theme file, not shipped here)
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

- **Wordmark:** `seat` in `--fg` + `sweep` in `--accent` (9 chars)
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

Source file: `levistack/docs/assets/logo.svg` (the theme file named in the brief, not a path on this machine).

Roles follow `references/token-table.md`. Hex values are copied from that SVG. Token-table does not assign different hex values, so there is no conflict to override.

| Role | Hex | Where it appears in logo.svg |
|---|---|---|
| `--bg` | `#17152e` | outer rect fill, line 8 |
| `--surface` | `#3a3358` | terminal card fill, line 74 |
| `--surface2` | `#4a4f7a` | top bar fill, line 75 |
| `--line` | `#3a3358` | outer stroke, line 8 |
| `--line2` | `#4a4f7a` | card stroke, line 74 |
| `--fg` | `#e8e4f4` | wordmark `levi`, line 61 |
| `--muted` | `#98a2b6` | tagline, line 63 |
| `--dim` | `#6a6fa0` | motto, line 71 |
| `--accent` | `#c99d48` | wordmark `stack`, line 61, lip ellipse line 52 |
| `--amber-bg` | `#3a3358` | pill fill, line 65 |
| `--accent-dim` | `#b2853a` | gold band stroke, line 65 |
| teal band | `#3c7f7c` | line 36 |
| purple band | `#66589a` | line 37 |
| secondary text | `#c6cddb` | pill text, line 69 |
| divider | `#566782` | terminal rules, line 78 |

`--del` and `--add` are omitted. Column 3 is not `diff-hunks` (`token-table.md`, `banner-column-3.md`).

Flat solid `#17152e` only. No scanlines, no blur filters, no fog ellipses.

## 4. Type

IBM Plex Sans for the wordmark and motto. IBM Plex Mono for the tagline, pills, and terminal. Same stacks as `logo.svg` lines 61 and 63, with the system fallbacks from `svg-blueprints.md`.

## 5. Mark

Side-view dustpan: short grip, back wall, floor, one gold lip. The lip stops short of a small key (Keychain stays) and a small cloud (iCloud stays). Stroke-dash draw on the animated files. No mug. No broom.

## 6. Animation

Icon loop `4.6s`. Banner loop `6s`. Cursor blink `1.1s`. Draw order: pan, gold lip, key, cloud. Hold the finished state through 64–88%. Rows and the keep bar fade from 0.35 opacity in CSS only. No `opacity="0"` attributes. `prefers-reduced-motion: reduce` zeroes dash offset and clears transforms.
