# Safety notes (from a real macOS account-cleanup session)

## iCloud is not cache

`~/Library/Accounts`, Keychains, Mobile Documents, CloudDocs, FileProvider,
and Apple group containers (Notes, Calendar, Contacts, Reminders) are the
signed-in Apple ID. Deleting them looks like a sign-out. Keep them even
when the user says "wipe this account's data." `defaults read MobileMeAccounts`
can print `{}` under TCC; that is not proof iCloud is empty. Check
`Accounts4.sqlite` and `Mobile Documents/com~apple~CloudDocs` instead.

iCloud-named caches to keep: CloudKit, accountsd, itunescloudd, icloudwebd,
iCloudNotificationAgent, FileProvider daemon cache, Safari.

## Do not factory-reset, do not delete the user

The goal is "this account feels new." The user record, home folder, and the
other macOS user stay. Do not run `erase-install`, Recovery erase, or
`dscl . -delete /Users/...`.

## List first, then they pick

Same contract as `dev-cache-cleanup`. Scan, show sizes by category, dry-run
the full path list, wait. A category rollup can hide a path they still want
(Obsidian, a browser they meant to keep, a Homebrew leaf they still use).

## CoreSimulator is a mounted disk, not a folder

`/Library/Developer/CoreSimulator` can be tens of GB. `rm -rf` as admin
fails with Operation not permitted while APFS volumes are mounted under
`Volumes/` and `Cryptex/`. Force-unmount those volumes, eject the disks,
then rm. SIP may leave ~5MB of device-type stubs. Keep
`/Library/Developer/CommandLineTools`. Needs admin. Do not `brew` as root
to get there.

Check `mount | grep -i simulator` before deleting.

## Go module cache is read-only

Files under `~/go/pkg/mod` are mode 444. Raw `rm -rf` prints thousands of
Permission denied lines and leaves the tree. Prefer `go clean -modcache`.
If GOPATH is custom, `chmod -R u+w` then rm.

## asdf Erlang can wrap Homebrew Erlang

An asdf `erlang/22.x` install may ship `bin/erl` with
`ROOTDIR=/opt/homebrew/Cellar/erlang@22/...`. Uninstalling brew `erlang@22`
as "unused" then breaks `elixir`. Before removing brew Erlang, read the
asdf `erl` script. If it points at Cellar, either keep the formula or
retarget ROOTDIR to the asdf prefix (`~/.asdf/installs/erlang/<ver>`),
where `erts-*/bin/erlexec` actually lives.

## `brew cleanup --prune=all` can autoremove wanted formulae

It uninstalled Homebrew `go` once because nothing else depended on it,
while the user still wanted Go via goenv (which was fine) but the surprise
was bad. Do not use `--prune=all` as a blunt unused-cleaner. Uninstall
named unused leaves, then `brew autoremove`.

## brew as root is refused

`osascript` `do shell script "brew ..." with administrator privileges` fails:
Homebrew will not run as root. For casks whose uninstall.tool calls sudo
(Vagrant), run the uninstall.tool itself with admin, or rm the payload
paths. For formulae, run `brew uninstall` as the user.

## osascript admin GUI is the password path

`sudo` in this agent has no TTY. `do shell script "..." with administrator
privileges` shows a macOS password dialog. Chain unmount + rm in one
script so the user types the password once. Capture stderr to a log under
`/Users/Shared` so a non-zero exit still leaves evidence.

## `.cargo` is not all cache

`.cargo/bin` and `.cargo/env` are load-bearing (PATH on every shell).
Only `.cargo/registry` and `.cargo/git` are cache. Same lesson as
`dev-cache-cleanup`.

## SIP stubs and root-owned apps

Some `/Library` and `/Applications` trees are root + SIP. Visual Studio
Code.app stayed after a user-data wipe because it is owned by root. Report
it as EXCLUDE:admin. Do not hang on a sudo prompt.

## TCC / Full Disk Access

Chrome under Application Support can be unreadable without Full Disk Access
for the terminal/agent. If `ls` says Operation not permitted, say so. Do
not claim the data is gone.

## Documents and Desktop are iCloud + folder layout

Do not delete `~/Documents`, `~/Desktop`, `~/Pictures` to "make it fresh."
Optional project-cache scan under Documents is fine (`node_modules`,
`_build`). Skip laptop-migrate zip staging folders if they still exist.

## Other users on the Mac

Scan `$HOME` of the current user only. Do not walk `/Users/<other>`.
