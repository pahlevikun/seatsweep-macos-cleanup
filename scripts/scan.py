#!/usr/bin/env python3
"""Scan this macOS user account for leftover data that can make it feel new.

Does not recurse all of $HOME. Looks up known buckets: browser data, extra
Application Support, non-Apple containers, extra home dots, user OS caches,
Homebrew unused leaves, extra /Applications, and optional project caches.

Keep-list paths are reported as EXCLUDE:keep (informational only).

Usage:
    python3 scan.py --home ~ --output /tmp/account-cleanup.json
    python3 scan.py --home ~ --project-root ~/Documents --output /tmp/account-cleanup.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess

HOME_KEEP_DOTS = {
    ".CFUserTextEncoding",
    ".DS_Store",
    ".Trash",
    ".agents",
    ".asdf",
    ".atuin",
    ".cargo",
    ".claude",
    ".claude-mem",
    ".claude.json",
    ".claude.json.backup",
    ".codex",
    ".config",
    ".cursor",
    ".gitconfig",
    ".gnupg",
    ".goenv",
    ".hex",
    ".kiex",
    ".local",
    ".oh-my-zsh",
    ".profile",
    ".rustup",
    ".ssh",
    ".teamonia",
    ".tool-versions",
    ".trae",
    ".trae-aicc",
    ".trae-cn",
    ".zprofile",
    ".zsh_history",
    ".zsh_sessions",
    ".zshenv",
    ".zshrc",
    ".zshrc.pre-oh-my-zsh",
}

KEEP_APP_SUPPORT = {
    "App Store",
    "AddressBook",
    "Animoji",
    "CallHistoryDB",
    "CallHistoryTransactions",
    "Claude",
    "ClipboardAppIcons",
    "CloudDocs",
    "Codex",
    "ControlCenter",
    "CrashReporter",
    "Cursor",
    "DifferentialPrivacy",
    "DiskImages",
    "Dock",
    "FaceTime",
    "FamilySettings",
    "FileProvider",
    "Instruments",
    "IntelligenceFlow",
    "Knowledge",
    "MobileSync",
    "Music",
    "OpenAI",
    "Spotlight",
    "SyncServices",
    "Trae",
    "appplaceholdersyncd",
    "com.openai.codex",
    "contactsd",
    "cursor-computer-use",
    "go",
    "gopls",
    "homeenergyd",
    "iCloud",
    "iMovie",
    "icdd",
    "icloudmailagent",
    "identityservicesd",
    "locationaccessstored",
    "networkserviceproxy",
    "privatecloudcomputed",
    "stickersd",
    "tipsd",
}

KEEP_APPS = {
    "ChatGPT.app",
    "Claude.app",
    "Cursor.app",
    "Keynote.app",
    "Numbers.app",
    "Obsidian.app",
    "Pages.app",
    "Safari.app",
    "TestFlight.app",
    "iMovie.app",
}

KEEP_BREW_LEAVES = {
    "asdf",
    "atuin",
    "curl",
    "fzf",
    "gh",
    "git",
    "goenv",
    "gpgme",
    "jq",
    "pipx",
    "pkgconf",
    "python@3.14",
    "yq",
    "zsh",
    "zsh-autosuggestions",
}

KEEP_CASKS = {"claude-code", "codex", "copilot-cli"}

BROWSER_AS = {
    "Google/Chrome": "Browser local data",
    "BraveSoftware": "Browser local data",
    "Arc": "Browser local data",
    "Chromium": "Browser local data",
    "Microsoft Edge": "Browser local data",
    "Vivaldi": "Browser local data",
    "company.thebrowser.Browser": "Browser local data",
}

ICLOUD_CACHE_KEEP = (
    "CloudKit",
    "accountsd",
    "itunescloudd",
    "FileProvider",
    "iCloudNotification",
    "icloudwebd",
    "Safari",
    "Family",
    "AppleMediaServices",
)

PROJECT_PATTERNS = {
    "Rust": {"target"},
    "Elixir": {"_build", "deps", ".elixir_ls"},
    "JavaScript / Node": {
        "node_modules",
        ".next",
        ".nuxt",
        ".turbo",
        ".expo",
        ".pnpm-store",
        ".output",
        ".angular",
        ".svelte-kit",
        ".parcel-cache",
        ".vite",
    },
    "Python": {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox"},
    "Android / Gradle": {".gradle", ".cxx"},
    "iOS / Swift": {"Pods", "DerivedData", "xcuserdata"},
}

KNOWN_JUNK_DOTS = {
    ".android",
    ".colima",
    ".docker",
    ".gradle",
    ".kube",
    ".m2",
    ".minikube",
    ".npm",
    ".vscode",
    ".vscode-shared",
    ".fvm",
    ".pub-cache",
    ".yarn",
    ".gemini",
    ".codeium",
    ".marscode",
    ".orbstack",
}


def human(n):
    n = float(n)
    for unit in ["B", "K", "M", "G", "T"]:
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}{unit}"
        n /= 1024
    return f"{n:.1f}P"


def du_bytes(path):
    try:
        out = subprocess.run(
            ["du", "-sk", path], capture_output=True, text=True, check=True
        ).stdout
        return int(out.split()[0]) * 1024
    except Exception:
        return 0


def entry(path, basename, category, scope, note=None, kind="rmtree"):
    size = du_bytes(path) if os.path.isdir(path) or os.path.isfile(path) else 0
    return {
        "path": path,
        "basename": basename,
        "size_bytes": size,
        "size_str": human(size),
        "category": category,
        "scope": scope,
        "note": note,
        "kind": kind,
    }


def appleish(name):
    lname = name.lower()
    return (
        name.startswith("com.apple.")
        or name.startswith("group.com.apple.")
        or "icloud" in lname
        or name.startswith(".")
    )


def scan_app_support(home, entries):
    asup = os.path.join(home, "Library", "Application Support")
    if not os.path.isdir(asup):
        return
    for name in os.listdir(asup):
        path = os.path.join(asup, name)
        if appleish(name) or name in KEEP_APP_SUPPORT:
            continue
        if name == "Google":
            chrome = os.path.join(path, "Chrome")
            if os.path.isdir(chrome):
                entries.append(
                    entry(chrome, "Chrome", "Browser local data", "user", "Chrome profile data")
                )
            continue
        cat = "Browser local data" if name in BROWSER_AS else "Extra app support"
        entries.append(entry(path, name, cat, "user"))


def scan_containers(home, entries, dirname, category):
    base = os.path.join(home, "Library", dirname)
    if not os.path.isdir(base):
        return
    for name in os.listdir(base):
        if appleish(name):
            continue
        path = os.path.join(base, name)
        if os.path.isdir(path):
            entries.append(entry(path, name, category, "user"))


def scan_home_dots(home, entries):
    for name in os.listdir(home):
        if not name.startswith(".") or name in HOME_KEEP_DOTS:
            continue
        if name.startswith(".zcompdump"):
            continue
        path = os.path.join(home, name)
        if not os.path.isdir(path) and name not in KNOWN_JUNK_DOTS:
            continue
        if os.path.isdir(path):
            cat = "Extra home dots"
            note = None
            if name in KNOWN_JUNK_DOTS:
                note = "known leftover toolchain/app dir"
            entries.append(entry(path, name, cat, "user", note))


def scan_caches(home, entries):
    caches = os.path.join(home, "Library", "Caches")
    if not os.path.isdir(caches):
        return
    for name in os.listdir(caches):
        if any(k.lower() in name.lower() for k in ICLOUD_CACHE_KEEP):
            continue
        path = os.path.join(caches, name)
        entries.append(entry(path, name, "User OS caches", "user"))


def scan_httpstorages(home, entries):
    base = os.path.join(home, "Library", "HTTPStorages")
    if not os.path.isdir(base):
        return
    for name in os.listdir(base):
        lname = name.lower()
        if "apple" in lname or "icloud" in lname or "safari" in lname:
            continue
        path = os.path.join(base, name)
        entries.append(entry(path, name, "User OS caches", "user", "HTTPStorages"))


def scan_keep_flagged(home, entries):
    flagged = [
        ("Library/Mobile Documents", "iCloud Drive documents", "EXCLUDE:keep"),
        ("Library/Accounts", "Apple ID / account store", "EXCLUDE:keep"),
        ("Library/Keychains", "Keychain", "EXCLUDE:keep"),
        ("Library/Application Support/CloudDocs", "iCloud CloudDocs", "EXCLUDE:keep"),
        ("Library/Application Support/Cursor", "Cursor app data", "EXCLUDE:keep"),
        ("Library/Application Support/Claude", "Claude app data", "EXCLUDE:keep"),
        ("Library/Application Support/Codex", "Codex app data", "EXCLUDE:keep"),
        (".cursor", "Cursor config", "EXCLUDE:keep"),
        (".claude", "Claude Code", "EXCLUDE:keep"),
        (".codex", "Codex", "EXCLUDE:keep"),
        (".asdf", "asdf language installs", "EXCLUDE:keep"),
        (".goenv", "goenv installs", "EXCLUDE:keep"),
        (".rustup", "Rust toolchains", "EXCLUDE:keep"),
        (".oh-my-zsh", "terminal", "EXCLUDE:keep"),
        (".ssh", "SSH keys", "EXCLUDE:keep"),
    ]
    for rel, note, cat in flagged:
        path = os.path.join(home, rel)
        if os.path.exists(path):
            entries.append(entry(path, os.path.basename(rel), cat, "user", note))


def scan_simulator(entries):
    path = "/Library/Developer/CoreSimulator"
    if os.path.isdir(path):
        entries.append(
            entry(
                path,
                "CoreSimulator",
                "EXCLUDE:admin",
                "system",
                "Unmount APFS simulator volumes first, then rm as admin. SIP stubs (~5M) may remain. Keep CommandLineTools.",
            )
        )


def scan_brew(entries):
    try:
        leaves = subprocess.run(
            ["brew", "leaves"], capture_output=True, text=True, check=True
        ).stdout.split()
    except Exception:
        return
    cellar = "/opt/homebrew/Cellar"
    for name in leaves:
        if name in KEEP_BREW_LEAVES:
            continue
        path = os.path.join(cellar, name)
        if not os.path.isdir(path):
            path = name
        e = entry(path, name, "Homebrew unused leaves", "global", "brew leaf not on keep list", kind="brew-formula")
        entries.append(e)
    try:
        casks = subprocess.run(
            ["brew", "list", "--cask"], capture_output=True, text=True, check=True
        ).stdout.split()
    except Exception:
        return
    for name in casks:
        if name in KEEP_CASKS:
            continue
        e = entry(
            f"/opt/homebrew/Caskroom/{name}",
            name,
            "Homebrew unused casks",
            "global",
            "brew cask not on keep list; uninstall may need admin (not brew as root)",
            kind="brew-cask",
        )
        entries.append(e)


def scan_apps(entries):
    apps = "/Applications"
    if not os.path.isdir(apps):
        return
    for name in os.listdir(apps):
        if not name.endswith(".app") and name != "Utilities":
            continue
        if name in KEEP_APPS or name == "Utilities":
            continue
        # Apple-shipped
        if name in {"Safari.app", "Mail.app", "Photos.app", "Maps.app", "Notes.app"}:
            continue
        path = os.path.join(apps, name)
        st = os.stat(path)
        cat = "EXCLUDE:admin" if st.st_uid == 0 else "Extra applications"
        note = "root-owned; needs admin to uninstall" if st.st_uid == 0 else None
        entries.append(entry(path, name, cat, "system", note, kind="app-bundle"))


def scan_project_root(root, entries):
    root = os.path.expanduser(root)

    def _migrate_staging(path):
        return any(part.startswith("laptop-migrate-") for part in path.split(os.sep))

    def categorize(basename):
        for cat, names in PROJECT_PATTERNS.items():
            if basename in names:
                return cat
        return None

    for dirpath, dirnames, _filenames in os.walk(root, topdown=True, followlinks=False):
        if _migrate_staging(dirpath):
            dirnames[:] = []
            continue
        keep = []
        for d in dirnames:
            if d == ".git":
                continue
            cat = categorize(d)
            full = os.path.join(dirpath, d)
            if cat:
                parent = os.path.dirname(full)
                if d == "deps" and not (
                    os.path.exists(os.path.join(parent, "mix.exs"))
                    or os.path.exists(os.path.join(parent, "_build"))
                ):
                    keep.append(d)
                    continue
                if d == "target" and not (
                    os.path.exists(os.path.join(parent, "Cargo.toml"))
                    or os.path.exists(os.path.join(parent, "Cargo.lock"))
                ):
                    keep.append(d)
                    continue
                entries.append(entry(full, d, f"Project: {cat}", "project"))
            else:
                keep.append(d)
        dirnames[:] = keep


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--home", default="~")
    ap.add_argument("--project-root", action="append", default=[])
    ap.add_argument("--output", default="/tmp/account-cleanup.json")
    args = ap.parse_args()

    home = os.path.expanduser(args.home)
    entries = []
    scan_keep_flagged(home, entries)
    scan_app_support(home, entries)
    scan_containers(home, entries, "Containers", "Non-Apple containers")
    scan_containers(home, entries, "Group Containers", "Non-Apple group containers")
    scan_home_dots(home, entries)
    scan_caches(home, entries)
    scan_httpstorages(home, entries)
    scan_simulator(entries)
    scan_brew(entries)
    scan_apps(entries)
    for root in args.project_root:
        scan_project_root(root, entries)

    entries.sort(key=lambda e: -e["size_bytes"])
    total = sum(e["size_bytes"] for e in entries if not e["category"].startswith("EXCLUDE:"))
    with open(args.output, "w") as f:
        json.dump({"entries": entries, "total": total, "home": home}, f, indent=2)
    print(f"{len(entries)} entries, {human(total)} reclaimable (excludes EXCLUDE:)")
    print(f"written to {args.output}")


if __name__ == "__main__":
    main()
