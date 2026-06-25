from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


REPO_OWNER = "ZHV587"
REPO_NAME = "lark-daily-report-workflow-skill"
ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "version.json"


def parse_version(value: str) -> tuple[int, int, int]:
    value = value.lstrip("v")
    parts = [int(part) for part in value.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])  # type: ignore[return-value]


def should_update(local: str, remote: str) -> bool:
    return parse_version(remote) > parse_version(local)


def read_local_version() -> str:
    data = json.loads(VERSION_FILE.read_text(encoding="utf-8"))
    return data["version"]


def fetch_latest_release() -> dict:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "codex-skill-updater",
        },
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def download_release_zip(url: str, target: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/octet-stream",
            "User-Agent": "codex-skill-updater",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response, target.open("wb") as f:
        shutil.copyfileobj(response, f)


def apply_release_archive(source_root: Path, target_root: Path) -> None:
    for path in source_root.rglob("*"):
        relative = path.relative_to(source_root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        if relative.as_posix() == "references/team-config.local.md":
            continue
        destination = target_root / relative
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(path.read_bytes())


def run_update_check() -> bool:
    try:
        release = fetch_latest_release()
        local_version = read_local_version()
        remote_version = release["tag_name"]
        if not should_update(local_version, remote_version):
            return False

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / "release.zip"
            extract_dir = tmpdir / "extract"
            extract_dir.mkdir()
            download_release_zip(release["zipball_url"], archive)
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(extract_dir)
            extracted = next(extract_dir.iterdir())
            apply_release_archive(extracted, ROOT)
        return True
    except (OSError, urllib.error.URLError, StopIteration, KeyError, json.JSONDecodeError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        try:
            release = fetch_latest_release()
            local = read_local_version()
            remote = release["tag_name"]
            if should_update(local, remote):
                print(f"update available: {local} -> {remote}")
            else:
                print(f"already current: {local}")
            return 0
        except Exception as exc:  # best-effort
            print(f"update check skipped: {exc}")
            return 0

    updated = run_update_check()
    if updated:
        print("skill updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
