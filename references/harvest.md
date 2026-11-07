Skill name:        seatsweep-macos-cleanup
Goal:              This macOS account feels newly created, without wiping the OS, the other user, iCloud, or the kept tools.
Trigger words:     fresh account, cleanup laptop, wipe this user, account like new, macos account cleanup
Not for:           factory reset, deleting a macOS user, project-only cache (use dev-cache-cleanup)

Inputs needed:     keep-policy confirmation; after the scan, which categories to delete
Steps that worked:
  1. Lock the keep list (iCloud, OS, both users, terminal, Cursor/Claude/Codex/Trae, Python/Elixir/Go/Rust) -> user confirms
  2. Scan known buckets with sizes -> categorized list
  3. User picks categories (browsers, extra apps, OS caches, leftover CLIs, Homebrew unused, simulator)
  4. Dry-run full path list -> user confirms
  5. Delete only those buckets; admin unmount for CoreSimulator if picked
  6. Verify keep tools still run; report disk delta
Exact commands:    python3 scripts/scan.py --home ~ [--project-root ~/Documents] --output /tmp/account-cleanup.json; python3 scripts/report.py ...; python3 scripts/cleanup.py ... [--only-category ...] [--confirm]
Corrections:       iCloud and Apple ID stay; do not factory reset; list CLI/Homebrew first; Documents/Desktop stay; do not brew as root; do not prune-all Homebrew
Traps hit:         CoreSimulator mounted APFS; Go pkg mode 444; asdf Erlang wrapping brew erlang@22; brew cleanup autoremoving go; sudo no TTY
Output shape:      categorized size list (HTML report + category bullets), then wait, then delete counts
Done when:         picked buckets gone, keep tools still work, iCloud folders still present, disk numbers reported

Dropped:           browser merge-restore (migration, not cleanup); a keychain export; a desktop app inventory file
Save to:           ~/.claude/skills/seatsweep-macos-cleanup and the editor user skill store
