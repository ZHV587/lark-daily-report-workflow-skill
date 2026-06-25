import json
from pathlib import Path

import pytest

from scripts import self_update


def test_parse_version_handles_v_prefix():
    assert self_update.parse_version("v1.2.3") == (1, 2, 3)


def test_should_update_when_remote_is_newer():
    assert self_update.should_update("v1.2.3", "v1.2.4") is True


def test_should_not_update_when_versions_match():
    assert self_update.should_update("v1.2.3", "v1.2.3") is False


def test_run_update_check_returns_false_when_offline(monkeypatch, tmp_path):
    version_file = tmp_path / "version.json"
    version_file.write_text(
        json.dumps({"version": "0.1.0", "release_tag": "v0.1.0"}),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    def boom():
        raise OSError("offline")

    monkeypatch.setattr(self_update, "fetch_latest_release", boom)
    assert self_update.run_update_check() is False


def test_apply_release_archive_preserves_local_config(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "SKILL.md").write_text("updated", encoding="utf-8")
    (source / "references").mkdir()
    (source / "references" / "team-config.md").write_text("updated", encoding="utf-8")
    (source / "references" / "team-config.local.md").write_text("keep", encoding="utf-8")

    target = tmp_path / "target"
    target.mkdir()
    (target / "references").mkdir()
    (target / "references" / "team-config.local.md").write_text("keep", encoding="utf-8")

    self_update.apply_release_archive(source, target)

    assert (target / "SKILL.md").read_text(encoding="utf-8") == "updated"
    assert (target / "references" / "team-config.md").read_text(encoding="utf-8") == "updated"
    assert (target / "references" / "team-config.local.md").read_text(encoding="utf-8") == "keep"
