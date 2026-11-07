# Keep policy (defaults from a real laptop-cleanup run)

Confirm this with the user at the start of every run. Do not treat it as
locked in until they say so.

## Always keep (never delete, never sign out)

- Both macOS users. Do not `dscl` delete, do not `rm -rf /Users/<other>`.
- OS install, System Settings, FileVault, and Command Line Tools at
  `/Library/Developer/CommandLineTools`.
- iCloud data and Apple ID: `~/Library/Mobile Documents`, CloudDocs,
  FileProvider, `~/Library/Accounts`, `~/Library/Keychains`, Contacts,
  Calendars, Reminders, Notes, Mail, Messages, Safari (iCloud tabs/bookmarks).
- Folder layout and user files: Documents, Desktop, Pictures, Movies, Music.
- Terminal: `~/.zshrc`, oh-my-zsh, `~/.ssh`, `~/.gitconfig`, gnupg, Atuin.
- Agentic tools: Cursor, Claude, Codex, Trae, `~/.agents`.
- Languages the user named: Python, Elixir (+ Erlang via asdf), Go (goenv),
  Rust (rustup). Keep `.asdf` installs, `.goenv`, `.rustup`, `.cargo/bin` +
  `.cargo/env`. `.cargo/registry` is cache, not the toolchain.

## Default keep Homebrew leaves

`asdf` `atuin` `curl` `fzf` `gh` `git` `goenv` `gpgme` `jq` `pipx` `pkgconf`
`python@3.14` `yq` `zsh` `zsh-autosuggestions`

Casks: `claude-code` `codex` `copilot-cli`

## Default keep apps

Safari, Cursor, Claude, ChatGPT, Keynote, Numbers, Pages, iMovie, TestFlight,
Obsidian (vaults often live on iCloud).

## This is not

- A factory reset (`Erase All Content and Settings`).
- A wipe of another account on the same Mac.
- `dev-cache-cleanup` (project `node_modules` / `_build` only). This skill
  can scan project caches as an optional extra category. For a projects-only
  pass, use `dev-cache-cleanup`.
