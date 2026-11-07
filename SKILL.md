---
name: seatsweep-macos-cleanup
description: Cleans a macOS user account toward a freshly-created feel without factory-resetting or deleting the user. Scans known leftover buckets (browser data, extra apps, OS caches, leftover CLIs, Homebrew unused, simulator runtimes), lists sizes, then deletes only the categories the user picks. Use when the user wants a fresh macOS account, laptop cleanup, wipe-this-user-but-keep-the-account, or an account that feels newly created while keeping iCloud, OS setup, folder layout, terminal, and agentic tools.
---

<objective>
I make this macOS account feel new. I do not erase the Mac, I do not delete the user, and I do not sign out of iCloud. I scan first, I list sizes by category, and I wait. You pick what goes. Same contract as `dev-cache-cleanup`: a rollup is not a delete list.
</objective>

<essential_principles>
- **List, then wait.** Scan and report before any `rm`, `brew uninstall`, or admin dialog. Dry-run the full path list when there are more than a handful of paths.
- **Keep list is a gate, not a vibe.** Read [keep-policy.md](references/keep-policy.md) and confirm it at the start. If they change it, follow the new list.
- **Never:** factory reset, delete another macOS user, wipe Documents/Desktop/Pictures, delete `CommandLineTools`, delete `.cargo/bin` or `.cargo/env`, run `brew` as root, run `brew cleanup --prune=all` as the unused-cleaner.
- **iCloud is not cache.** Accounts, Keychains, Mobile Documents, CloudDocs, FileProvider stay. Read [safety-notes.md](references/safety-notes.md) before the first run on a machine.
- **Admin paths are opt-in.** CoreSimulator and root-owned apps are `EXCLUDE:admin`. I say they need a password dialog. I do not hang on `sudo` with no TTY.
- If a delete breaks a kept CLI, I say so immediately, I fix it if I can, and I add the trap to `references/safety-notes.md`.
</essential_principles>

<intake>
What do you want to do?

1. Scan and list (default: I always start here unless you already picked categories this session)
2. Delete categories I already named
3. Homebrew unused leaves only (still scan/list first)
</intake>

<routing>
| Choice | Start at |
|--------|----------|
| 1, "scan", "list", "fresh account", "cleanup laptop" | `<process>` step 1 |
| 2, named categories from this chat | `<process>` step 5, only after a scan JSON exists |
| 3, "homebrew unused" | `<process>` step 1, then only-category Homebrew |
</routing>

<quick_start>
Read [keep-policy.md](references/keep-policy.md) and [safety-notes.md](references/safety-notes.md). Confirm the keep list in one short message. Then:

```
python3 scripts/scan.py --home "$HOME" --output /tmp/account-cleanup.json
python3 scripts/report.py /tmp/account-cleanup.json --output /tmp/account-cleanup-report.html
python3 scripts/cleanup.py /tmp/account-cleanup.json --paths-file /tmp/account-cleanup-paths.txt
```

Show the category totals. Do not pass `--confirm` until they pick categories by name.
</quick_start>

<process>
**Step 1. Confirm keep policy.**
State the defaults from [keep-policy.md](references/keep-policy.md) in a short list (iCloud, both users, OS, folder layout, terminal, Cursor/Claude/Codex/Trae, Python/Elixir/Go/Rust). Ask only if something is unclear. If they already locked this in this session, do not re-ask.

**Step 2. Scan.**
From this skill directory:

```
python3 scripts/scan.py --home "$HOME" --output /tmp/account-cleanup.json
```

Add `--project-root ~/Documents` only if they also want engineering caches under Documents (node_modules, `_build`, and the rest). Skip migrate-zip staging folders. Do not recurse all of `$HOME`.

**Step 3. Cross-check on the first run, or if they say something is missing.**
`du -sh ~/Library/Application\ Support ~/Library/Caches ~/Library/Containers /Library/Developer 2>/dev/null`. Large uncategorized paths: either add a pattern to `scripts/scan.py` or flag them in the write-up. Permission denied on Chrome: say Full Disk Access is blocking the scan, do not pretend the bucket is empty.

**Step 4. Report. Stop.**
```
python3 scripts/report.py /tmp/account-cleanup.json --output /tmp/account-cleanup-report.html
```
Open or attach the HTML if you can. In chat, give category totals (size + count). Call out `EXCLUDE:keep` and `EXCLUDE:admin` as not in the reclaimable number. Homebrew unused is a list of leaf formulae, not every Cellar dep.

Ask which categories to delete. Recommend skipping Extra applications until they glance at the names. Recommend skipping unverified project `build/`/`dist` unless they asked for project caches.

**Step 5. Dry-run the picked set.**
```
python3 scripts/cleanup.py /tmp/account-cleanup.json \
  --only-category "Browser local data" \
  --paths-file /tmp/account-cleanup-paths.txt
```
Repeat `--only-category` per picked category. Send the paths file when the list is long. Wait for an explicit yes.

**Step 6. Delete.**
Same command plus `--confirm`. Then `brew autoremove` is already triggered inside cleanup for brew-formula deletes.

CoreSimulator if they picked it: do not use cleanup.py. Check `mount | grep -i simulator`. Admin script: force-unmount `Volumes/*` and Cryptex bundles, eject those disks, `rm -rf /Library/Developer/CoreSimulator`. Keep CommandLineTools. SIP can leave a few MB of stubs. Password via `osascript` `do shell script "..." with administrator privileges`, never `brew` as root.

**Step 7. Verify and report.**
Check iCloud folders still exist, then `python3 --version`, `go version`, `elixir --version`, `rustc --version`, `git --version`. Report deleted count, reclaimable vs `df` (APFS can lag), and any `EXCLUDE:admin` leftovers (root-owned .app, SIP stubs).
</process>

<watch_for>
- CoreSimulator: unmount APFS volumes or `rm` fails with Operation not permitted for 8+ minutes and frees nothing.
- `~/go/pkg/mod`: mode 444. Use `go clean -modcache` or `chmod -R u+w` first.
- asdf `bin/erl` may set `ROOTDIR` to `/opt/homebrew/Cellar/erlang@22`. Read it before uninstalling brew Erlang.
- `brew cleanup --prune=all` can drop a leaf they still want. Named uninstall + `brew autoremove` only.
- `sudo` here has no TTY. Use the admin dialog. One script, one password.
- `defaults read MobileMeAccounts` printing `{}` is not a sign-out. Check `Accounts4.sqlite` and `Mobile Documents`.
</watch_for>

<reference_guides>
- [keep-policy.md](references/keep-policy.md)
- [safety-notes.md](references/safety-notes.md)
- Scripts: `scripts/scan.py`, `scripts/report.py`, `scripts/cleanup.py`
</reference_guides>

<success_criteria>
- I scanned and listed before any delete.
- Only user-picked categories were removed.
- iCloud, Keychain, the other macOS user, Command Line Tools, and the keep-list tools still work.
- Chat ends with counts and disk numbers, plus any admin leftovers named plainly.
</success_criteria>
