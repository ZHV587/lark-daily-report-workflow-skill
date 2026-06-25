# Skill Auto-Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the published daily-report skill check GitHub Releases on startup, auto-update itself when a newer release exists, and continue silently when already current or when update checks fail.

**Architecture:** Add a tiny version manifest at the repo root, a `scripts/self_update.py` helper that compares the local version with the latest GitHub Release, downloads and applies the release archive when needed, and preserves local ignored config files. Wire a one-line preflight call into `SKILL.md` so the update check runs before normal skill work. Keep the update path best-effort: on any network or filesystem failure, skip the update and continue.

**Tech Stack:** Python stdlib, GitHub Releases API, zip extraction, existing Markdown skill files.

---

### Task 1: Define the release contract

**Files:**
- Create: `version.json`
- Create: `tests/test_version_manifest.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import json


def test_version_manifest_exists_and_has_version():
    data = json.loads(Path("version.json").read_text(encoding="utf-8"))
    assert data["version"] == "0.1.0"
    assert data["release_tag"] == "v0.1.0"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_version_manifest -v`
Expected: FAIL because `version.json` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```json
{
  "version": "0.1.0",
  "release_tag": "v0.1.0"
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_version_manifest -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add version.json tests/test_version_manifest.py
git commit -m "test: add release version manifest"
```

### Task 2: Build the updater core

**Files:**
- Create: `scripts/self_update.py`
- Create: `tests/test_self_update.py`

- [ ] **Step 1: Write the failing tests**

```python
from scripts.self_update import should_update, parse_version


def test_parse_version_handles_v_prefix():
    assert parse_version("v1.2.3") == (1, 2, 3)


def test_should_update_when_remote_is_newer():
    assert should_update("v1.2.3", "v1.2.4") is True


def test_should_not_update_when_versions_match():
    assert should_update("v1.2.3", "v1.2.3") is False


def test_should_not_raise_on_network_failure(monkeypatch):
    from scripts import self_update

    def boom():
        raise OSError("offline")

    monkeypatch.setattr(self_update, "fetch_latest_release", boom)
    assert self_update.run_update_check() is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_self_update -v`
Expected: FAIL because `scripts/self_update.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

import json
from pathlib import Path


def parse_version(value: str) -> tuple[int, int, int]:
    value = value.lstrip("v")
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def should_update(local: str, remote: str) -> bool:
    return parse_version(remote) > parse_version(local)


def fetch_latest_release() -> dict:
    raise OSError("network not implemented yet")


def run_update_check() -> bool:
    try:
        release = fetch_latest_release()
    except OSError:
        return False
    local = json.loads(Path("version.json").read_text(encoding="utf-8"))["version"]
    remote = release["tag_name"]
    return should_update(local, remote)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_self_update -v`
Expected: PASS for the comparison tests and the offline fallback test.

- [ ] **Step 5: Commit**

```bash
git add scripts/self_update.py tests/test_self_update.py
git commit -m "feat: add updater core"
```

### Task 3: Apply GitHub Release archives safely

**Files:**
- Modify: `scripts/self_update.py`
- Modify: `tests/test_self_update.py`

- [ ] **Step 1: Add a failing test for archive application**

```python
from pathlib import Path

from scripts.self_update import apply_release_archive


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

    apply_release_archive(source, target)

    assert (target / "SKILL.md").read_text(encoding="utf-8") == "updated"
    assert (target / "references" / "team-config.md").read_text(encoding="utf-8") == "updated"
    assert (target / "references" / "team-config.local.md").read_text(encoding="utf-8") == "keep"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_self_update -v`
Expected: FAIL because `apply_release_archive` is not implemented yet.

- [ ] **Step 3: Implement archive extraction and copy logic**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_self_update -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/self_update.py tests/test_self_update.py
git commit -m "feat: preserve local config during update"
```

### Task 4: Wire the preflight into the skill and document it

**Files:**
- Modify: `SKILL.md`
- Modify: `references/first-run-checklist.md`
- Modify: `references/team-migration.md`
- Create: `references/update-policy.md`

- [ ] **Step 1: Add the failing documentation expectation**

```markdown
## 更新检查

在执行任何日报、任务查询或写入动作前，先静默运行 `python scripts/self_update.py`。
检查成功就继续；检查失败也继续，不打断工作流。
```

- [ ] **Step 2: Update `SKILL.md` to call the updater first**

```markdown
在执行任何飞书任务或日报工作流前，先静默运行 `python scripts/self_update.py`。
如果检查到新版本，自动更新本地技能包后继续；如果检查失败或已经是最新版，直接继续，不要打断用户流程。
```

- [ ] **Step 3: Update the first-run checklist**

```markdown
1. 先静默运行 `python scripts/self_update.py`，确保当前技能包是最新版本；失败也继续。
2. 确认 `lark-cli` 可用，并完成当前同事的 `lark-cli` 登录。
```

- [ ] **Step 4: Add the update policy reference**

```markdown
# 更新策略

技能启动时先检查 GitHub Releases 最新版本。
如果远端版本更新，自动下载并应用整个 release archive。
如果网络失败、下载失败或写入失败，静默跳过，继续当前任务。
本地 `references/team-config.local.md` 始终保留，不参与覆盖。
```

- [ ] **Step 5: Run the full validation**

Run:
```bash
python -m unittest tests.test_version_manifest tests.test_self_update -v
python scripts/self_update.py --dry-run
python -m compileall scripts
```
Expected: all pass, dry-run reports no blocking failures.

- [ ] **Step 6: Commit**

```bash
git add SKILL.md references/first-run-checklist.md references/team-migration.md references/update-policy.md
git commit -m "feat: add silent GitHub release auto-update"
```

