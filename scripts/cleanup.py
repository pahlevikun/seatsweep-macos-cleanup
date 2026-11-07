#!/usr/bin/env python3
"""Delete confirmed buckets from a scan.py report. Dry-run unless --confirm.

Safety:
  - Categories prefixed EXCLUDE: are never deleted unless --include-category.
  - Default is dry run.
  - brew-formula uses `brew uninstall --formula` (never brew as root).
  - go module cache prefers `go clean -modcache`.
  - CoreSimulator is not deleted here; SKILL.md covers unmount + admin rm.

Usage:
    python3 cleanup.py /tmp/account-cleanup.json
    python3 cleanup.py /tmp/account-cleanup.json --exclude-category "Extra applications"
    python3 cleanup.py /tmp/account-cleanup.json --include-category "Browser local data" --confirm
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys


def human(n):
    n = float(n)
    for unit in ["B", "K", "M", "G", "T"]:
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}{unit}"
        n /= 1024
    return f"{n:.1f}P"


def chmod_writable(path):
    subprocess.run(["chmod", "-R", "u+w", path], capture_output=True)


def delete_one(entry):
    kind = entry.get("kind") or "rmtree"
    path = entry["path"]
    if kind == "brew-formula":
        r = subprocess.run(
            ["brew", "uninstall", "--formula", entry["basename"]],
            capture_output=True,
            text=True,
        )
        return r.returncode == 0, (r.stderr or r.stdout).strip()
    if kind == "brew-cask":
        r = subprocess.run(
            ["brew", "uninstall", "--cask", entry["basename"]],
            capture_output=True,
            text=True,
        )
        return r.returncode == 0, (r.stderr or r.stdout).strip()
    if entry["basename"] == "go" or path.endswith("/go/pkg") or path.endswith("/pkg/mod"):
        if shutil.which("go"):
            r = subprocess.run(["go", "clean", "-modcache"], capture_output=True, text=True)
            if r.returncode == 0:
                return True, ""
        chmod_writable(path)
    if kind == "app-bundle":
        try:
            shutil.rmtree(path)
            return True, ""
        except PermissionError as e:
            return False, f"{e} (root-owned apps need admin, not this script)"
    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
        else:
            return True, "already gone"
        return True, ""
    except Exception as e:
        return False, str(e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report_json")
    ap.add_argument("--exclude-category", action="append", default=[])
    ap.add_argument("--exclude-basename", action="append", default=[])
    ap.add_argument("--include-category", action="append", default=[])
    ap.add_argument(
        "--only-category",
        action="append",
        default=[],
        help="If set, delete only these categories (still respects EXCLUDE: unless also included)",
    )
    ap.add_argument("--confirm", action="store_true")
    ap.add_argument("--paths-file", help="Write the full target path list here")
    args = ap.parse_args()

    with open(args.report_json) as f:
        data = json.load(f)

    exclude_cats = set(args.exclude_category)
    include_cats = set(args.include_category)
    exclude_names = set(args.exclude_basename)
    only_cats = set(args.only_category)

    to_delete, kept = [], []
    for e in data["entries"]:
        is_excluded = e["category"].startswith("EXCLUDE:") and e["category"] not in include_cats
        if is_excluded or e["category"] in exclude_cats or e["basename"] in exclude_names:
            kept.append(e)
            continue
        if only_cats and e["category"] not in only_cats:
            kept.append(e)
            continue
        to_delete.append(e)

    total = sum(e["size_bytes"] for e in to_delete)
    label = "WOULD DELETE" if not args.confirm else "DELETING"
    print(f"{label}: {len(to_delete)} entries, {human(total)}")
    print(f"Excluded/kept: {len(kept)} entries, {human(sum(e['size_bytes'] for e in kept))}")

    if args.paths_file:
        with open(args.paths_file, "w") as f:
            for e in to_delete:
                f.write(f"{e['size_str']}\t{e['category']}\t{e['path']}\n")
        print(f"path list: {args.paths_file}")

    if not args.confirm:
        print("\nDry run. Rerun with --confirm to delete. First 30 targets:")
        for e in to_delete[:30]:
            print(f"  {e['size_str']:>8}  [{e['category']}]  {e['path']}")
        if len(to_delete) > 30:
            print(f"  ... and {len(to_delete) - 30} more")
        return

    deleted, reclaimed, skipped, failed = 0, 0, 0, []
    for e in to_delete:
        if e.get("kind") not in {"brew-formula", "brew-cask"} and not os.path.exists(e["path"]):
            skipped += 1
            continue
        ok, err = delete_one(e)
        if ok:
            deleted += 1
            reclaimed += e["size_bytes"]
        else:
            failed.append((e["path"], err))

    if any(e.get("kind") == "brew-formula" for e in to_delete):
        subprocess.run(["brew", "autoremove"], capture_output=True)

    print(f"\nDeleted: {deleted}")
    print(f"Reclaimed: {human(reclaimed)}")
    print(f"Skipped (already gone): {skipped}")
    print(f"Failed: {len(failed)}")
    for p, err in failed[:20]:
        print(f"  FAILED: {p} -- {err}")


if __name__ == "__main__":
    main()
