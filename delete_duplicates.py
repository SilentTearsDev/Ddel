#!/usr/bin/env python3

import argparse
import hashlib
import re
import sys
from pathlib import Path


# Common copy suffixes used by Linux/file managers and Windows.
COPY_PATTERNS = (
    re.compile(r"^(.*)[_-](\d+)$"),      # file_1, file-1
    re.compile(r"^(.*) \((\d+)\)$"),     # file (1)
)


def file_hash(path, chunk_size=1024 * 1024):
    """Return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    try:
        with path.open("rb") as file:
            while chunk := file.read(chunk_size):
                sha256.update(chunk)
    except OSError:
        return None

    return sha256.hexdigest()


def copy_number(path):
    """Return the copy number from a common duplicate filename, or None."""
    stem = path.stem

    for pattern in COPY_PATTERNS:
        match = pattern.match(stem)
        if match:
            return int(match.group(2))

    return None


def find_duplicate_groups(directory):
    """
    Find groups of files with identical contents.

    A file is considered an original when its filename does not contain
    a recognized copy-number suffix. If a group contains an original,
    the original is kept and numbered copies are returned for deletion.
    """
    files_by_size = {}

    for path in directory.rglob("*"):
        if not path.is_file():
            continue

        try:
            size = path.stat().st_size
        except OSError:
            continue

        files_by_size.setdefault(size, []).append(path)

    groups = []

    for files in files_by_size.values():
        if len(files) < 2:
            continue

        hashes = {}

        for path in files:
            digest = file_hash(path)

            if digest is not None:
                hashes.setdefault(digest, []).append(path)

        for same_files in hashes.values():
            if len(same_files) < 2:
                continue

            originals = [
                path for path in same_files
                if copy_number(path) is None
            ]

            copies = [
                path for path in same_files
                if copy_number(path) is not None
            ]

            # Only delete copies when there is exactly one clear original.
            if len(originals) == 1 and copies:
                groups.append((originals[0], sorted(copies)))

    return groups


def main():
    parser = argparse.ArgumentParser(
        prog="ddel",
        description=(
            "Find and delete duplicate files while keeping the original."
        ),
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search (default: current directory)",
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List duplicate files without deleting anything",
    )

    mode.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Delete confirmed duplicate files",
    )

    args = parser.parse_args()

    directory = Path(args.directory).expanduser().resolve()

    if not directory.exists():
        print(f"Error: directory does not exist: {directory}", file=sys.stderr)
        return 1

    if not directory.is_dir():
        print(f"Error: not a directory: {directory}", file=sys.stderr)
        return 1

    groups = find_duplicate_groups(directory)

    if not groups:
        print("No duplicate files were found.")
        return 0

    duplicate_count = sum(len(copies) for _, copies in groups)

    print(f"Found {duplicate_count} duplicate file(s) in {len(groups)} group(s):\n")

    for original, copies in groups:
        print(f"Original: {original}")

        for copy in copies:
            print(f"  Duplicate: {copy}")

        print()

    if args.list:
        return 0

    answer = input("Delete these duplicate files? [y/N] ").strip().lower()

    if answer not in {"y", "yes"}:
        print("Cancelled.")
        return 0

    deleted = 0
    failed = 0

    for _, copies in groups:
        for duplicate in copies:
            try:
                duplicate.unlink()
                print(f"Deleted: {duplicate}")
                deleted += 1
            except OSError as exc:
                print(f"FAILED: {duplicate} ({exc})", file=sys.stderr)
                failed += 1

    print("\nDone.")
    print(f"Deleted: {deleted}")
    print(f"Failed:  {failed}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
